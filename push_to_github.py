#!/usr/bin/env python3
"""
ARCANA — GitHub Auto-Deploy Script
Pushes divination_engine.html to jayrenrok/Arcana via GitHub API.

Requirements: pip install requests
Usage:        python push_to_github.py
"""

import base64
import os
import sys
import requests

# ── CONFIG ────────────────────────────────────────────────────────
GITHUB_OWNER = "jayrenrok"
GITHUB_REPO  = "Arcana"
GITHUB_BRANCH = "main"

# Files to push: (local filename, GitHub path in repo)
FILES_TO_PUSH = [
    ("divination_engine.html", "divination_engine.html"),
    ("index.html",             "index.html"),
    ("manifest.json",          "manifest.json"),
    ("sw.js",                  "sw.js"),
]
# ─────────────────────────────────────────────────────────────────


def get_token():
    """Get GitHub token from env var or prompt."""
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not token:
        print("\n─────────────────────────────────────────")
        print("  ARCANA — GitHub Auto-Deploy")
        print("─────────────────────────────────────────")
        print("\nYou need a GitHub Personal Access Token.")
        print("Get one at: github.com/settings/tokens")
        print("  → Click 'Generate new token (classic)'")
        print("  → Tick the 'repo' scope")
        print("  → Copy the token\n")
        token = input("Paste your GitHub token here: ").strip()
    if not token:
        print("❌ No token provided. Exiting.")
        sys.exit(1)
    return token


def get_current_sha(session, owner, repo, path, branch):
    """Get the SHA of the current file (needed to update existing files)."""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    r = session.get(url, params={"ref": branch})
    if r.status_code == 200:
        return r.json().get("sha")
    return None  # File doesn't exist yet


def push_file(session, owner, repo, branch, local_path, github_path):
    """Read local file and push to GitHub."""
    if not os.path.exists(local_path):
        print(f"  ⚠  Skipping {local_path} — file not found locally")
        return False

    with open(local_path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf-8")

    sha = get_current_sha(session, owner, repo, github_path, branch)

    payload = {
        "message": f"deploy: update {github_path} via auto-deploy script",
        "content": content,
        "branch": branch,
    }
    if sha:
        payload["sha"] = sha  # Required for updating existing files

    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{github_path}"
    r = session.put(url, json=payload)

    if r.status_code in (200, 201):
        action = "Updated" if sha else "Created"
        size_kb = len(content) * 3 // 4 // 1024
        print(f"  ✓  {action}: {github_path} ({size_kb} KB)")
        return True
    else:
        print(f"  ❌  Failed: {github_path}")
        print(f"      Status: {r.status_code}")
        try:
            err = r.json().get("message", r.text)
            print(f"      Error:  {err}")
        except Exception:
            print(f"      Response: {r.text[:200]}")
        return False


def main():
    print("\n─────────────────────────────────────────")
    print("  ARCANA — GitHub Auto-Deploy")
    print(f"  Repo: {GITHUB_OWNER}/{GITHUB_REPO}")
    print("─────────────────────────────────────────\n")

    token = get_token()

    session = requests.Session()
    session.headers.update({
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "arcana-deploy-script"
    })

    # Verify token works
    r = session.get(f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}")
    if r.status_code == 401:
        print("❌ Invalid token — check it has 'repo' scope.")
        sys.exit(1)
    elif r.status_code == 404:
        print(f"❌ Repo {GITHUB_OWNER}/{GITHUB_REPO} not found.")
        print("   Check the repo name is correct and token has access.")
        sys.exit(1)
    elif r.status_code != 200:
        print(f"❌ GitHub API error: {r.status_code}")
        sys.exit(1)

    print(f"✓  Authenticated as: {session.get('https://api.github.com/user').json().get('login', '?')}")
    print(f"✓  Repo found: {GITHUB_OWNER}/{GITHUB_REPO}\n")
    print("Pushing files...\n")

    # Push each file
    success = 0
    for local_name, github_path in FILES_TO_PUSH:
        result = push_file(session, GITHUB_OWNER, GITHUB_REPO, GITHUB_BRANCH, local_name, github_path)
        if result:
            success += 1

    print(f"\n─────────────────────────────────────────")
    print(f"  Done: {success}/{len(FILES_TO_PUSH)} files pushed")
    print(f"─────────────────────────────────────────")

    if success > 0:
        print(f"\n✦  GitHub Pages rebuilds in ~60 seconds.")
        print(f"\n   Your app URL:")
        print(f"   https://{GITHUB_OWNER}.github.io/{GITHUB_REPO}/divination_engine.html\n")
        print(f"   After it rebuilds, paste your Anthropic API key")
        print(f"   in the gold bar at the top of the app.\n")
    else:
        print("\n❌ No files were pushed. Check errors above.\n")


if __name__ == "__main__":
    main()
