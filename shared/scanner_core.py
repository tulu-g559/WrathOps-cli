import re
from .ml_model import predict_secret
from .entropy import shannon_entropy

def scan_content(content, patterns):
    findings = []

    for name, pattern in patterns.items():
        matches = re.findall(pattern, content)

        unique_candidates = set()
        for match in matches:
            candidate = match if isinstance(match, str) else match[0]
            unique_candidates.add(candidate)

        for candidate in unique_candidates:
            if len(candidate) < 20:
                continue

            entropy = shannon_entropy(candidate)
            if entropy < 3.5:
                continue

            label = predict_secret(candidate)

            score = 0
            if entropy > 3.5:
                score += 1
            if label != "NOT_SECRET":
                score += 1

            if score >= 2:
                findings.append({
                    "type": label if label != "NOT_SECRET" else name,
                    "match": candidate
                })

    return findings