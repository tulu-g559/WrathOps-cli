import os
import re
from typing import Dict, List, Optional

from .entropy import shannon_entropy

_ML_PREDICT_FN = None
_ML_IMPORT_ATTEMPTED = False

FAKE_KEYWORDS = ("test", "dummy", "example", "sample", "mock", "sandbox", "fake")
REAL_KEYWORDS = ("live", "prod", "production", "secret", "token", "api_key", "apikey", "key")
INVALID_HINTS = ("expired", "revoked", "invalid", "disabled", "placeholder", "changeme")
NETWORK_HINTS = (
    "requests.",
    "httpx.",
    "urllib.",
    "fetch(",
    "axios.",
    "boto3.",
    "openai.",
    "client.",
)


def _normalize_text(value: Optional[str]) -> str:
    return (value or "").strip()


def _extract_pattern_type(secret_value: str, variable_name: str) -> str:
    value = secret_value.strip()
    var = variable_name.upper()

    if value.startswith("AKIA") or "AWS" in var:
        return "AWS"
    if value.startswith("AIza") or "GOOGLE" in var or "GEMINI" in var:
        return "GOOGLE_GEMINI"
    if value.startswith("ghp_") or "GITHUB" in var:
        return "GITHUB"
    if value.startswith("sk_live_") or "STRIPE" in var:
        return "STRIPE"
    if value.startswith("Bearer "):
        return "BEARER"
    if value.startswith("eyJ") and value.count(".") == 2:
        return "JWT"
    return "GENERIC"


def _lazy_ml_predict(secret_value: str) -> Optional[str]:
    global _ML_PREDICT_FN, _ML_IMPORT_ATTEMPTED

    if _ML_IMPORT_ATTEMPTED and _ML_PREDICT_FN is None:
        return None

    if _ML_PREDICT_FN is None and not _ML_IMPORT_ATTEMPTED:
        _ML_IMPORT_ATTEMPTED = True
        try:
            # Lazy import to avoid hard dependency at startup.
            from .ml_model import predict_secret  # type: ignore
            _ML_PREDICT_FN = predict_secret
        except Exception:
            _ML_PREDICT_FN = None

    if _ML_PREDICT_FN is None:
        return None

    try:
        return str(_ML_PREDICT_FN(secret_value))
    except Exception:
        return None


def classify_secret(
    secret_value: str,
    variable_name: str,
    file_path: str,
    surrounding_code: str,
) -> Dict[str, object]:
    """
    Classify detected secret risk into:
    - fake_or_test
    - expired_or_invalid
    - real_and_dangerous
    """
    value = _normalize_text(secret_value)
    var_name = _normalize_text(variable_name)
    path = _normalize_text(file_path).lower()
    code = _normalize_text(surrounding_code)
    code_lower = code.lower()
    var_lower = var_name.lower()

    reasons: List[str] = []
    risk_score = 50

    entropy = shannon_entropy(value) if value else 0.0
    value_len = len(value)
    pattern_type = _extract_pattern_type(value, var_name)

    # Length and entropy signals
    if value_len < 12:
        risk_score -= 35
        reasons.append("Very short secret-like value")
    elif value_len >= 20:
        risk_score += 10
        reasons.append("Long secret-like value")

    if entropy >= 4.0:
        risk_score += 20
        reasons.append("High entropy string")
    elif entropy < 3.0:
        risk_score -= 20
        reasons.append("Low entropy string")

    # Variable name signals
    if any(k in var_lower for k in FAKE_KEYWORDS):
        risk_score -= 30
        reasons.append("Variable name suggests test/fake usage")
    if any(k in var_lower for k in REAL_KEYWORDS):
        risk_score += 12
        reasons.append("Variable name suggests real credentials")

    # Pattern type signal
    if pattern_type in {"AWS", "GOOGLE_GEMINI", "GITHUB", "STRIPE"}:
        risk_score += 12
        reasons.append(f"Matches high-risk provider format ({pattern_type})")

    # File path/context signals
    if path.endswith(".env") or ".env" in os.path.basename(path):
        risk_score += 8
        reasons.append("Secret stored in environment file")
    if any(part in path for part in ("test", "tests", "fixtures", "docs", "example", "samples")):
        risk_score -= 20
        reasons.append("Found in test/docs/example context")

    # Surrounding code semantics
    if re.search(r"^\s*#", code, flags=re.MULTILINE):
        risk_score -= 10
        reasons.append("Appears inside comments")
    if any(hint in code_lower for hint in NETWORK_HINTS):
        risk_score += 15
        reasons.append("Used near network/API call")
    if any(marker in code_lower for marker in INVALID_HINTS):
        risk_score -= 25
        reasons.append("Context suggests invalid/expired credential")

    # Optional ML boost/penalty
    ml_label = _lazy_ml_predict(value)
    if ml_label:
        if ml_label.upper() in {"AWS_KEY", "GITHUB_TOKEN", "GOOGLE_API_KEY", "JWT", "STRIPE_KEY", "SECRET"}:
            risk_score += 10
            reasons.append(f"ML model indicates secret-like token ({ml_label})")
        elif ml_label.upper() in {"TEST_KEY", "NOT_SECRET", "DUMMY"}:
            risk_score -= 10
            reasons.append(f"ML model indicates low-risk token ({ml_label})")

    # Clamp and map to class
    risk_score = max(0, min(100, risk_score))

    if risk_score >= 65:
        classification = "real_and_dangerous"
    elif risk_score <= 35:
        classification = "fake_or_test"
    else:
        classification = "expired_or_invalid"

    confidence = round(max(0.05, min(0.99, 0.5 + abs(risk_score - 50) / 100)), 2)

    return {
        "classification": classification,
        "confidence": confidence,
        "risk_score": risk_score,
        "reasons": reasons or ["Insufficient context; treated as medium risk"],
    }
