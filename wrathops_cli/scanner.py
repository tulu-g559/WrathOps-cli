import os
from shared.explanation_engine import generate_explanation
from shared.patterns import PATTERNS
from shared.scanner_core import scan_content

EXCLUDED_DIRS = {".git", "__pycache__", "node_modules", ".venv", "ml"}
EXCLUDED_EXTENSIONS = {
    ".pkl", ".pyc", ".pyo", ".so", ".dll", ".exe", ".bin",
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico",
    ".pdf", ".zip", ".tar", ".gz", ".7z", ".jar", ".whl",
}
EXCLUDED_FILES = {"secrets_dataset.json"}
MAX_SCAN_BYTES = 1024 * 1024  # avoid scanning large blobs/binaries


def should_scan_file(path):
    if os.path.basename(path) in EXCLUDED_FILES:
        return False

    _, ext = os.path.splitext(path.lower())

    if ext in EXCLUDED_EXTENSIONS:
        return False

    try:
        if os.path.getsize(path) > MAX_SCAN_BYTES:
            return False
    except OSError:
        return False

    return True

def scan_repo():
    issues_found = False

    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

        for file in files:
            path = os.path.join(root, file)
            if not should_scan_file(path):
                continue

            try:
                with open(path, "r", errors="ignore") as f:
                    content = f.read()

                findings = scan_content(content, PATTERNS, file_path=path)

                if findings:
                    issues_found = True
                    print(f"\n🚨 Secrets in {path}")
                    for fnd in findings:
                        risk = fnd.get("risk", {})
                        print(
                            "   → "
                            f"{fnd['type']} "
                            f"(risk={risk.get('risk_score', '?')}, "
                            f"class={risk.get('classification', '?')}, "
                            f"confidence={risk.get('confidence', '?')})"
                        )
                        explanation = generate_explanation(
                            secret_type=fnd.get("type"),
                            classification=risk.get("classification"),
                            risk_score=risk.get("risk_score"),
                            variable_name=fnd.get("variable_name"),
                            surrounding_code=fnd.get("surrounding_code"),
                        )
                        print(f"   ⚠️ {explanation}")

            except:
                continue

    return not issues_found