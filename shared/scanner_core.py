import re
from .ml_model import predict_secret
from .entropy import shannon_entropy

def scan_content(content, patterns):
    findings = []

    for name, pattern in patterns.items():
        matches = re.findall(pattern, content)

        for match in matches:
            candidate = match if isinstance(match, str) else match[0]

            # length filter
            candidate = match if isinstance(match, str) else match[0]

            # length filter
            if len(candidate) < 20:
                continue

            # entropy filter (slightly relaxed)
            entropy = shannon_entropy(candidate)
            if entropy < 3.0:
                continue

            # ML classification
            label = predict_secret(candidate)

            # ✅ NEW LOGIC
            if label != "NOT_SECRET":
                final_type = label   # ML wins
            else:
                final_type = name    # fallback to regex

            findings.append({
                "type": final_type,
                "match": candidate
            })

    return findings