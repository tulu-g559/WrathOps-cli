import os

HOOK_SCRIPT = """#!/bin/sh
echo "🔍 WrathOps scanning..."

"C:/Users/ayonp/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0/LocalCache/local-packages/Python313/Scripts/wrathops.exe" scan

STATUS=$?

if [ $STATUS -ne 0 ]; then
    echo "❌ Commit blocked: secrets detected."
    exit 1
fi

exit 0
"""

def install_hook():
    git_dir = ".git/hooks"
    hook_path = os.path.join(git_dir, "pre-commit")

    if not os.path.exists(git_dir):
        print("❌ Not a git repo")
        return

    with open(hook_path, "w", encoding="utf-8") as f:
        f.write(HOOK_SCRIPT)

    os.chmod(hook_path, 0o775)

    print("✅ Hook installed (pre-commit)")