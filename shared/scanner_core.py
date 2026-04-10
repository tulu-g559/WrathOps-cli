import re
from .ml_model import predict_secret
from .entropy import shannon_entropy

def scan_content(content, patterns):
    findings = []

    for name, pattern in patterns.items():
        matches = re.findall(pattern, content)

        for match in matches:
            candidate = match if isinstance(match, str) else match[0]

            score = 0

            # 1. Length
            if len(candidate) >= 20:
                score += 1

            # 2. Entropy
            entropy = shannon_entropy(candidate)
            if entropy > 3.5:
                score += 1

            # 3. Regex match (strong signal)
            score += 1

            # 4. ML prediction
            label = predict_secret(candidate)
            if label != "NOT_SECRET":
                score += 2   # ML gets higher weight

            # 🔥 Decision
            if score >= 3:
                findings.append({
                    "type": label if label != "NOT_SECRET" else name,
                    "match": candidate,
                    "score": score
                })

    return findings