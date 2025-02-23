"""
This script backs up GitHub repositories for a user. It fetches the list of
repositories using the GitHub API and either clones them if they don't exist
locally, or pulls the latest changes if they do.

Environment variables:
- GITHUB_TOKEN: GitHub personal access token for authentication.
- BACKUP_DIR: Directory where the repositories will be backed up.

Usage:
1. Set the GITHUB_TOKEN and BACKUP_DIR environment variables.
2. Run the script to back up the repositories.
"""

import os
from subprocess import call
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")
if not TOKEN:
    raise ValueError("GITHUB_TOKEN environment variable not set")

BACKUP_DIR = os.getenv("BACKUP_DIR")
if not BACKUP_DIR:
    raise ValueError("BACKUP_DIR environment variable not set")

# Create a backup directory
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)


def fetch_repos(page=1):
    """Fetch repositories from GitHub with pagination."""
    url = f"https://api.github.com/user/repos?page={page}&per_page=100"
    headers = {"Authorization": f"token {TOKEN}"}
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch repositories: {response.status_code}")
        return []


def clone_or_pull_repo(repo):
    """Clone or pull the latest changes for a repository."""
    repo_name = repo["name"]
    repo_url = repo["clone_url"]
    repo_path = os.path.join(BACKUP_DIR, repo_name)
    if os.path.exists(repo_path):
        print(
            f"Repository {repo_name} already exists. Pulling latest changes..."
        )
        call(["git", "-C", repo_path, "pull"])
    else:
        print(f"Cloning {repo_name}...")
        call(["git", "clone", repo_url, repo_path])


def main():
    """Main function to fetch and backup repositories."""
    page = 1
    while True:
        repos = fetch_repos(page)
        if not repos:
            break
        for repo in repos:
            clone_or_pull_repo(repo)
        page += 1
    print("Backup completed.")


if __name__ == "__main__":
    main()
