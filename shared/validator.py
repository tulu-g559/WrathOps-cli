import re
import urllib.error
import urllib.request

from .entropy import shannon_entropy

TIMEOUT_SECONDS = 2

SECRET_PATTERNS = {
    "OPENAI_API_KEY": r"^sk-[A-Za-z0-9\-_]{20,}$",
    "GOOGLE_API_KEY": r"^AIza[0-9A-Za-z\-_]{35}$",
    "GEMINI_API_KEY": r"^AIza[0-9A-Za-z\-_]{35}$",
    "AWS_ACCESS_KEY": r"^AKIA[0-9A-Z]{16}$",
    "GITHUB_TOKEN": r"^ghp_[A-Za-z0-9]{36}$",
    "STRIPE_SECRET_KEY": r"^sk_live_[0-9A-Za-z]{24}$",
}

SECRET_PREFIXES = {
    "OPENAI_API_KEY": ("sk-",),
    "GOOGLE_API_KEY": ("AIza",),
    "GEMINI_API_KEY": ("AIza",),
    "AWS_ACCESS_KEY": ("AKIA",),
    "GITHUB_TOKEN": ("ghp_",),
    "STRIPE_SECRET_KEY": ("sk_live_",),
}


def _mask_secret(secret_value):
    if not secret_value:
        return "****"
    if len(secret_value) <= 8:
        return secret_value[:1] + "****"
    return secret_value[:4] + "****" + secret_value[-4:]


def _offline_validation(secret_value, secret_type):
    normalized = (secret_value or "").strip()
    stype = (secret_type or "").upper()
    entropy = shannon_entropy(normalized) if normalized else 0.0
    notes = []

    if len(normalized) < 10:
        notes.append("Value is too short for most real secrets")
        return False, entropy, notes

    prefixes = SECRET_PREFIXES.get(stype, ())
    if prefixes and not any(normalized.startswith(p) for p in prefixes):
        notes.append("Missing expected provider prefix")
        return False, entropy, notes

    pattern = SECRET_PATTERNS.get(stype)
    if pattern and not re.match(pattern, normalized):
        notes.append("Value does not match expected provider format")
        return False, entropy, notes

    if entropy < 3.0:
        notes.append("Low entropy suggests test or placeholder value")
        return False, entropy, notes

    notes.append("Passed offline structure checks")
    return True, entropy, notes


def _passive_check_google(secret_value):
    # Safe check: list public model metadata with API key, no user data access.
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={secret_value}"
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            code = getattr(resp, "status", 200)
            return code == 200, "Google key accepted by safe metadata endpoint"
    except urllib.error.HTTPError as exc:
        if exc.code in (400, 401, 403):
            return False, "Google key rejected by safe metadata endpoint"
        return None, "Google validation endpoint unavailable"
    except Exception:
        return None, "Google passive validation unavailable"


def _passive_check_openai(secret_value):
    # Safe auth check: list models endpoint, no completions or content calls.
    req = urllib.request.Request(
        "https://api.openai.com/v1/models",
        headers={"Authorization": f"Bearer {secret_value}"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            code = getattr(resp, "status", 200)
            return code == 200, "OpenAI key accepted by lightweight auth check"
    except urllib.error.HTTPError as exc:
        if exc.code in (400, 401, 403):
            return False, "OpenAI key rejected by lightweight auth check"
        return None, "OpenAI validation endpoint unavailable"
    except Exception:
        return None, "OpenAI passive validation unavailable"


def validate_secret(secret_value, secret_type):
    """
    Safe secret validation engine.
    Returns structural validity and potential activity without storing or logging raw secrets.
    """
    stype = (secret_type or "").upper()
    is_valid, entropy, offline_notes = _offline_validation(secret_value, stype)
    masked = _mask_secret(secret_value)

    result = {
        "is_structurally_valid": is_valid,
        "is_potentially_active": "Unknown",
        "validation_method": "offline" if is_valid else "none",
        "confidence": 0.45 if is_valid else 0.2,
        "notes": "; ".join(offline_notes) + f" (masked={masked})",
        "status_note": "No validation could be performed safely",
    }

    if not is_valid:
        result["status_note"] = "Structurally invalid secret format"
        return result

    # For providers without safe passive checks, use strong offline signals only.
    if entropy >= 4.0:
        result["is_potentially_active"] = True
        result["confidence"] = 0.68
        result["status_note"] = "structurally valid, high entropy"
    else:
        result["is_potentially_active"] = "Unknown"
        result["confidence"] = 0.55
        result["status_note"] = "structurally valid, but weak entropy signal"

    checker = None
    if stype in ("GOOGLE_API_KEY", "GEMINI_API_KEY"):
        checker = _passive_check_google
    elif stype == "OPENAI_API_KEY":
        checker = _passive_check_openai

    if checker is None:
        return result

    active, passive_note = checker(secret_value)
    result["validation_method"] = "passive"
    result["notes"] = passive_note + f" (masked={masked})"

    if active is True:
        result["is_potentially_active"] = True
        result["confidence"] = 0.85
        result["status_note"] = "key responded to lightweight authentication check"
    elif active is False:
        result["is_potentially_active"] = False
        result["confidence"] = 0.75
        result["status_note"] = "key was rejected by lightweight authentication check"
    else:
        result["is_potentially_active"] = "Unknown"
        result["confidence"] = 0.55
        result["status_note"] = "no safe validation signal available"

    return result
