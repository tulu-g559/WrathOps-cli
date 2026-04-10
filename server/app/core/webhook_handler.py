from app.services.github_service import get_commit_files


def handle_github_webhook(event, payload):
    """
    Entry point for all GitHub webhook events
    """

    if event == "push":
        return handle_push_event(payload)

    return {"message": f"Ignored event: {event}"}



def handle_push_event(payload):
    print("[HANDLER] Push event triggered")

    repo_name = payload["repository"]["full_name"]
    commits = payload.get("commits", [])

    print("[HANDLER] Repo:", repo_name)
    print("[HANDLER] Commits:", len(commits))

    all_files = set()

    for commit in commits:
        commit_id = commit["id"]

        print("[HANDLER] Fetching files for commit:", commit_id)

        files = get_commit_files(repo_name, commit_id)

        print("[HANDLER] Files from API:", files)

        all_files.update(files)

    from app.core.pipeline import process_push_event

    return process_push_event(repo_name, list(all_files))