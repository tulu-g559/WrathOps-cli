import re

def scan_content(content, patterns):
    findings = []

    for name, pattern in patterns.items():
        matches = re.findall(pattern, content)

        unique_candidates = set()
        for match in matches:
            candidate = match if isinstance(match, str) else match[0]
            unique_candidates.add(candidate)

        for candidate in unique_candidates:
            findings.append({
                "type": name,
                "match": candidate
            })

    return findings