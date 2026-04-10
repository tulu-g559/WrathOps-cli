import re
from .risk_classifier import classify_secret

def _line_number_at(content, index):
    return content.count("\n", 0, index) + 1


def _extract_surrounding_code(content, start_index, window=2):
    lines = content.splitlines()
    line_no = _line_number_at(content, start_index) - 1
    start = max(0, line_no - window)
    end = min(len(lines), line_no + window + 1)
    return "\n".join(lines[start:end])


def _extract_variable_name(surrounding_code):
    assignment = re.search(r"([A-Za-z_][A-Za-z0-9_]*)\s*[:=]", surrounding_code)
    if assignment:
        return assignment.group(1)
    return "UNKNOWN_VAR"


def scan_content(content, patterns, file_path=""):
    findings = []

    for name, pattern in patterns.items():
        seen = set()
        for match in re.finditer(pattern, content):
            candidate = match.group(0)
            if candidate in seen:
                continue
            seen.add(candidate)

            surrounding_code = _extract_surrounding_code(content, match.start(), window=2)
            variable_name = _extract_variable_name(surrounding_code)
            risk = classify_secret(
                secret_value=candidate,
                variable_name=variable_name,
                file_path=file_path,
                surrounding_code=surrounding_code,
            )

            if risk["classification"] != "real_and_dangerous":
                continue

            findings.append({
                "type": name,
                "match": candidate,
                "variable_name": variable_name,
                "surrounding_code": surrounding_code,
                "risk": risk,
            })

    return findings