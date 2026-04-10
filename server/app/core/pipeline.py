from app.services.github_service import get_file_content
from app.services.scanner import scan_files
from app.services.fixer import fix_file_content, create_env_example
from app.services.pr_creator import create_fix_pr
from app.services.llm_service import ai_fix_code
from app.services.secret_revoker import revoke_secret

# 🔥 NEW shared scanner
from shared.patterns import PATTERNS
from shared.scanner_core import scan_content


print("[PIPELINE] STARTED")


def process_push_event(repo_name, files):
    try:
        print(f"[PIPELINE] Processing push event for {repo_name} with {len(files)} files")

        file_contents = []

        # 🔹 STEP 1: Fetch files
        for file_path in files:
            try:
                content = get_file_content(repo_name, file_path)

                if content:
                    file_contents.append({
                        "filename": file_path,
                        "content": content
                    })
            except Exception as e:
                print(f"[PIPELINE ERROR] Failed to fetch {file_path}: {str(e)}")
                continue

        # 🔹 STEP 2: Scan using EXISTING system (keep this)
        findings = scan_files(file_contents)
        print(f"[PIPELINE] Scan complete. Found {len(findings)} potential secrets")

        # 🔥 STEP 2.1: ALSO extract raw secret values (NEW)
        raw_findings = []
        for file in file_contents:
            detected = scan_content(file["content"], PATTERNS)

            for d in detected:
                raw_findings.append({
                    "file": file["filename"],
                    "type": d["type"],
                    "matches": d["matches"]
                })

        # 🔹 STEP 3: If clean
        if not findings:
            return {
                "status": "clean",
                "message": "No secrets detected"
            }

        # 🔥 STEP 4: REVOKE SECRETS (NEW 🔥)
        print("[PIPELINE] Revoking detected secrets...")

        for rf in raw_findings:
            for secret_value in rf["matches"]:
                try:
                    revoke_secret(rf["type"], secret_value)
                except Exception as e:
                    print(f"[REVOKE ERROR] {rf['type']}: {str(e)}")

        # 🔹 STEP 5: Fix files
        fixed_files = []
        all_env_vars = {}

        for file in file_contents:
            file_findings = [
                f for f in findings if f["file"] == file["filename"]
            ]

            if not file_findings:
                continue

            try:
                # 🔥 AI FIX FIRST
                ai_fixed = ai_fix_code(file["content"], file_findings)

                if ai_fixed and len(ai_fixed) > 0:
                    updated_content = ai_fixed

                    # fallback env extraction
                    _, env_vars = fix_file_content(file["content"], file_findings)

                else:
                    # 🧯 SAFE fallback
                    updated_content, env_vars = fix_file_content(
                        file["content"],
                        file_findings
                    )

                fixed_files.append({
                    "path": file["filename"],
                    "content": updated_content
                })

                all_env_vars.update(env_vars)

            except Exception as e:
                print(f"[PIPELINE ERROR] Failed to fix {file['filename']}: {str(e)}")
                continue

        # 🔹 STEP 6: Safety check
        if not fixed_files:
            print("[PIPELINE] No files were fixed")
            return {
                "status": "error",
                "message": "No files could be fixed"
            }

        # 🔹 STEP 7: Create .env.example
        env_example = create_env_example(all_env_vars)

        # 🔹 STEP 8: Create PR
        try:
            pr_url = create_fix_pr(
                repo_name,
                fixed_files,
                env_example,
                findings
            )

            print(f"[PIPELINE] PR created successfully: {pr_url}")

            return {
                "status": "pr_created",
                "pr_url": pr_url,
                "files_fixed": len(fixed_files)
            }

        except Exception as e:
            print(f"[PIPELINE ERROR] Failed to create PR: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to create PR: {str(e)}"
            }

    except Exception as e:
        print(f"[PIPELINE CRITICAL ERROR] {str(e)}")
        return {
            "status": "error",
            "message": f"Pipeline error: {str(e)}"
        }