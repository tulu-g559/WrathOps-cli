import math
import re


# -----------------------------
# Utility: Mask secret (safety)
# -----------------------------
def mask_secret(secret):
    if len(secret) <= 8:
        return "****"
    return secret[:4] + "****" + secret[-4:]


# -----------------------------
# Utility: Entropy calculation
# -----------------------------
def calculate_entropy(s):
    prob = [float(s.count(c)) / len(s) for c in dict.fromkeys(list(s))]
    entropy = -sum([p * math.log2(p) for p in prob])
    return entropy


# -----------------------------
# Known fake/test detection
# -----------------------------
def is_known_fake(secret):
    fake_indicators = [
        "example",
        "test",
        "dummy",
        "sample",
        "xxxx",
    ]

    # AWS specific known examples
    aws_examples = [
        "AKIAIOSFODNN7EXAMPLE",
        "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    ]

    if secret in aws_examples:
        return True

    return any(x in secret.lower() for x in fake_indicators)


# -----------------------------
# Structural validation
# -----------------------------
def is_structurally_valid(secret, secret_type):
    if not secret or len(secret) < 8:
        return False

    # Basic patterns
    patterns = {
        "AWS_ACCESS_KEY": r"AKIA[0-9A-Z]{16}",
        "AWS_SECRET_KEY": r"[A-Za-z0-9/+=]{40}",
        "OPENAI_API_KEY": r"sk-[A-Za-z0-9]{20,}",
        "GOOGLE_API_KEY": r"AIza[0-9A-Za-z\-_]{35}",
    }

    pattern = patterns.get(secret_type)
    if pattern:
        return bool(re.fullmatch(pattern, secret))

    # fallback: basic length + entropy
    return len(secret) > 16


# -----------------------------
# Main Validator
# -----------------------------
def validate_secret(secret_value, secret_type):
    try:
        entropy = calculate_entropy(secret_value)
        structural_valid = is_structurally_valid(secret_value, secret_type)

        # 🚨 1. Known fake detection (highest priority)
        if is_known_fake(secret_value):
            return {
                "is_structurally_valid": structural_valid,
                "is_potentially_active": False,
                "validation_method": "offline",
                "confidence": 0.95,
                "notes": "Matches known test/example pattern"
            }

        # 🚨 2. If not structurally valid → definitely not active
        if not structural_valid:
            return {
                "is_structurally_valid": False,
                "is_potentially_active": False,
                "validation_method": "offline",
                "confidence": 0.9,
                "notes": "Invalid format"
            }

        # ⚠️ 3. Only offline checks → NEVER assume active
        if entropy > 3.5:
            return {
                "is_structurally_valid": True,
                "is_potentially_active": "Unknown",
                "validation_method": "offline",
                "confidence": 0.7,
                "notes": "Valid format and high entropy, but not verified"
            }

        # fallback
        return {
            "is_structurally_valid": True,
            "is_potentially_active": "Unknown",
            "validation_method": "offline",
            "confidence": 0.5,
            "notes": "Insufficient signals"
        }

    except Exception as e:
        return {
            "is_structurally_valid": False,
            "is_potentially_active": "Unknown",
            "validation_method": "none",
            "confidence": 0.0,
            "notes": f"Validation error: {str(e)}"
        }