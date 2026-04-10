def generate_explanation(secret_type, classification, risk_score, variable_name, surrounding_code):
    secret_type = (secret_type or "GENERIC_SECRET").upper()
    classification = (classification or "expired_or_invalid").lower()
    variable_name = (variable_name or "").lower()
    surrounding_code = (surrounding_code or "").lower()

    impact_map = {
        "GOOGLE_API_KEY": "access your Google services, causing data exposure or billing abuse",
        "GEMINI_API_KEY": "access Gemini/Google services, causing data exposure or billing abuse",
        "FIREBASE_API_KEY": "access your Firebase resources, potentially exposing user data",
        "GENERIC_SECRET": "enable unauthorized access with unknown downstream impact",
    }
    impact = impact_map.get(
        secret_type,
        "enable unauthorized access and potential service abuse",
    )

    is_prod_like = ("prod" in variable_name) or ("live" in variable_name)
    is_exploitable_context = any(
        token in surrounding_code
        for token in ("requests.", "httpx.", "fetch(", "axios.", "boto3.", "openai.")
    )

    if classification == "real_and_dangerous":
        subject = "This appears to be a production secret" if is_prod_like else "This appears to be a real secret"
        explanation = f"{subject}. If exposed, attackers could {impact}."
    elif classification == "fake_or_test":
        explanation = "This looks like a test or placeholder value and is less likely to be exploitable."
    else:
        explanation = "This may be an inactive or expired key, but it should still be reviewed and rotated if uncertain."

    if classification == "real_and_dangerous" and is_exploitable_context:
        explanation += " It is referenced near network/API usage, which increases exploitability."

    if risk_score is not None and risk_score >= 90 and classification == "real_and_dangerous":
        explanation += " The high risk score suggests urgent remediation."

    return explanation
