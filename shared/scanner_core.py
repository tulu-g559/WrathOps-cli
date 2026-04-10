import re
# from .ml_model import predict_secret
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

            # basic sanity filters
            if len(candidate) < 20:
                continue

            entropy = shannon_entropy(candidate)

            # 🔥 ONLY trust strong signals
            if entropy > 3.5:
                findings.append({
                    "type": name,
                    "match": candidate
                })

    return findings