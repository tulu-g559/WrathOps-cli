import re
from .ml_model import predict_secret

def scan_content(content, patterns):
    findings = []

    for name, pattern in patterns.items():
        matches = re.findall(pattern, content)

        for match in matches:
            candidate = match if isinstance(match, str) else match[0]

            # 🔥 ML classification
            label = predict_secret(candidate)

            if label != "NOT_SECRET":
                findings.append({
                    "type": label,
                    "match": candidate
                })

    return findings