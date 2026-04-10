import re

def scan_content(content: str, patterns: dict):
    findings = []

    for name, pattern in patterns.items():
        matches = re.findall(pattern, content)
        if matches:
            findings.append({
                "type": name,
                "matches": matches[:3]  # limit noise
            })

    return findings