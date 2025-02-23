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


# Function to fetch repositories with pagination
def fetch_repos(page=1):
    url = f"https://api.github.com/user/repos?page={page}&per_page=100"
    headers = {"Authorization": f"token {TOKEN}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch repositories: {response.status_code}")
        return []


# Fetch all repositories and clone them
page = 1
while True:
    repos = fetch_repos(page)
    if not repos:
        break
    for repo in repos:
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
    page += 1

print("Backup completed.")
