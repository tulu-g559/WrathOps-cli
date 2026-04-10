import os
from shared.patterns import PATTERNS
from shared.scanner_core import scan_content

EXCLUDED_DIRS = {".git", "__pycache__", "node_modules", ".venv"}

def scan_repo():
    issues_found = False

    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

        for file in files:
            path = os.path.join(root, file)

            try:
                with open(path, "r", errors="ignore") as f:
                    content = f.read()

                findings = scan_content(content, PATTERNS)

                if findings:
                    issues_found = True
                    print(f"\n🚨 Secrets in {path}")
                    for fnd in findings:
                        print(f"   → {fnd['type']}")

            except:
                continue

    return not issues_found