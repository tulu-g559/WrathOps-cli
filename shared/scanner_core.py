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
            if len(candidate) < 20:
                continue

            # entropy filter
            if shannon_entropy(candidate) < 3.5:
                continue

            # ML classification
            label = predict_secret(candidate)

            # require agreement
            if label != "NOT_SECRET" and label == name:
                findings.append({
                    "type": label,
                    "match": candidate
                })

    return findings