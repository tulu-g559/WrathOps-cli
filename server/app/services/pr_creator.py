from github import Github
from app.config import Config
import time

from app.services.llm_service import generate_pr_description


def pr_already_exists(repo, base_branch):
    pulls = repo.get_pulls(state="open")

    for pr in pulls:
        if "wrathops" in pr.title.lower():
            print(f"[PR_CREATOR] Existing PR found: {pr.html_url}")
            return pr.html_url

    return None


def create_fix_pr(repo_name, fixed_files, env_example, findings):
    try:
        print(f"[PR_CREATOR] Starting PR creation for {repo_name}")
        
        if not Config.GITHUB_TOKEN:
            raise ValueError("GITHUB_TOKEN environment variable not set")
        
        g = Github(Config.GITHUB_TOKEN)
        repo = g.get_repo(repo_name)

        base_branch = repo.default_branch
        
        # Check if a WrathOps PR already exists before creating a branch
        existing_pr = pr_already_exists(repo, base_branch)
        if existing_pr:
            return existing_pr

        new_branch = f"wrathops/fix-secrets-{int(time.time())}"
        print(f"[PR_CREATOR] Creating branch: {new_branch}")

        source = repo.get_branch(base_branch)
        repo.create_git_ref(ref=f"refs/heads/{new_branch}", sha=source.commit.sha)

        files_updated = 0
        for file in fixed_files:
            try:
                contents = repo.get_contents(file["path"], ref=base_branch)

                repo.update_file(
                    path=file["path"],
                    message="fix: replace hardcoded secret with env variable",
                    content=file["content"],
                    sha=contents.sha,
                    branch=new_branch
                )
                files_updated += 1
                print(f"[PR_CREATOR] Updated: {file['path']}")

            except Exception as e:
                print(f"[PR_CREATOR] Creating new file {file['path']}: {str(e)}")
                repo.create_file(
                    path=file["path"],
                    message="add fixed file",
                    content=file["content"],
                    branch=new_branch
                )
                files_updated += 1

        try:
            repo.create_file(
                path=".env.example",
                message="add env example",
                content=env_example,
                branch=new_branch
            )
            print(f"[PR_CREATOR] Created .env.example")
        except Exception as e:
            print(f"[PR_CREATOR] .env.example already exists or error: {str(e)}")

        # 🔥 AI-generated PR description
        print(f"[PR_CREATOR] Generating PR description with AI")
        try:
            pr_body = generate_pr_description(repo_name, findings, fixed_files)
        except Exception as e:
            print(f"[PR_CREATOR] AI description failed, using fallback: {str(e)}")
            pr_body = f"🔐 **WrathOps: Security Fix**\n\nAutomatically detected and fixed {len(findings)} hardcoded secrets.\n\nFiles modified: {len(fixed_files)}\n\nPlease review the changes and merge when ready."

        print(f"[PR_CREATOR] Creating pull request")
        pr = repo.create_pull(
            title="🔐 WrathOps: Secure secrets automatically",
            body=pr_body,
            head=new_branch,
            base=base_branch
        )
        
        print(f"[PR_CREATOR] PR created successfully: {pr.html_url}")
        return pr.html_url
    
    except Exception as e:
        print(f"[PR_CREATOR CRITICAL ERROR] {str(e)}")
        raise