#!/usr/bin/env python3
# scripts/check-awesome-status.py
"""
traceflux Awesome List Status Checker

Checks the status of pending PRs to awesome lists.
Updates .github/awesome-submissions.json with latest status.

Usage:
    python scripts/check-awesome-status.py [--notify]

Options:
    --notify    Send notification if status changed
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

STATE_FILE = Path(__file__).parent.parent / ".github" / "awesome-submissions.json"


def run_gh(args: list[str]) -> str:
    """Run gh CLI command and return output."""
    result = subprocess.run(
        ["gh"] + args,
        capture_output=True,
        text=True,
        check=False
    )
    if result.returncode != 0:
        print(f"gh command failed: {result.stderr}", file=sys.stderr)
        return ""
    return result.stdout.strip()


def check_pr_status(repo: str, pr_number: int) -> dict | None:
    """Check PR status via gh CLI."""
    try:
        output = run_gh([
            "pr", "view", f"{repo}#{pr_number}",
            "--json", "state,title,url,createdAt,updatedAt"
        ])
        if not output:
            return None
        return json.loads(output)
    except Exception as e:
        print(f"Error checking PR {repo}#{pr_number}: {e}", file=sys.stderr)
        return None


def update_state(state: dict, submission: dict, pr_info: dict) -> bool:
    """Update submission status. Returns True if changed."""
    old_status = submission["status"]
    new_status = pr_info["state"].lower()
    
    # Map GitHub states to our states
    status_map = {
        "open": "pending",
        "closed": "rejected",  # Could be merged or closed
        "merged": "accepted"
    }
    
    # Check if actually merged
    if new_status == "closed":
        # Need to check if it was merged
        merge_check = run_gh([
            "pr", "view", f"{submission['repo']}#{submission['prNumber']}",
            "--json", "mergedAt"
        ])
        if merge_check:
            merge_info = json.loads(merge_check)
            if merge_info.get("mergedAt"):
                new_status = "accepted"
    
    mapped_status = status_map.get(new_status, old_status)
    
    if mapped_status != old_status:
        submission["status"] = mapped_status
        submission["statusHistory"].append({
            "status": mapped_status,
            "timestamp": datetime.now().isoformat(),
            "source": "gh_cli_check"
        })
        submission["prUrl"] = pr_info.get("url", submission.get("prUrl"))
        print(f"Status changed: {submission['repo']}#{submission['prNumber']} "
              f"{old_status} → {mapped_status}")
        return True
    return False


def main():
    if not STATE_FILE.exists():
        print(f"State file not found: {STATE_FILE}", file=sys.stderr)
        sys.exit(1)
    
    # Load state
    with open(STATE_FILE) as f:
        state = json.load(f)
    
    changed = False
    notifications = []
    
    # Check each pending submission
    for submission in state["submissions"]:
        if submission["status"] != "pending":
            continue
        
        pr_info = check_pr_status(
            submission["repo"],
            submission["prNumber"]
        )
        
        if pr_info:
            if update_state(state, submission, pr_info):
                changed = True
                notifications.append({
                    "repo": submission["repo"],
                    "pr": submission["prNumber"],
                    "old_status": submission["statusHistory"][-2]["status"] if len(submission["statusHistory"]) > 1 else "unknown",
                    "new_status": submission["status"]
                })
        else:
            print(f"Failed to check PR: {submission['repo']}#{submission['prNumber']}")
    
    # Update stats
    state["stats"]["accepted"] = sum(
        1 for s in state["submissions"] if s["status"] == "accepted"
    )
    state["stats"]["rejected"] = sum(
        1 for s in state["submissions"] if s["status"] == "rejected"
    )
    state["stats"]["pending"] = sum(
        1 for s in state["submissions"] if s["status"] == "pending"
    )
    state["lastUpdated"] = datetime.now().isoformat()
    
    # Save state
    if changed:
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)
        print(f"State updated: {len(notifications)} status changes")
        
        # Print notifications
        for notif in notifications:
            print(f"\n📢 Notification:")
            print(f"  Repo: {notif['repo']}")
            print(f"  PR: #{notif['pr']}")
            print(f"  Status: {notif['old_status']} → {notif['new_status']}")
    else:
        print("No status changes")
    
    # Summary
    print(f"\nSummary:")
    print(f"  Accepted: {state['stats']['accepted']}")
    print(f"  Rejected: {state['stats']['rejected']}")
    print(f"  Pending: {state['stats']['pending']}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
