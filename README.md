# GitHub Backup Script

This repository contains a Python script to backup all your GitHub repositories to a local directory. The script uses the GitHub API to fetch the list of repositories and clones or pulls them to keep the backup up-to-date.

## Setup

1. Clone this repository to your local machine:

    ```sh
    git clone https://github.com/gabrielfortuny/backup-github-repos.git
    cd backup-github-repos
    ```

2. Create a virtual environment and activate it:

    ```sh
    python3 -m venv env
    source env/bin/activate
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

4. Create a [`.env`](.env) file in the root directory of the project and add your GitHub token and backup directory path:

    ```env
    GITHUB_TOKEN=your_github_token
    BACKUP_DIR=/path/to/backup/directory
    ```

    - `GITHUB_TOKEN`: A personal access token with read access to your repositories. You can create one [here](https://github.com/settings/personal-access-tokens).
    - `BACKUP_DIR`: The directory where you want to store the backups.

## Usage

Run the script to start the backup process:

```sh
python3 backup_github_repos.py
```

The script will fetch all your repositories and clone them to the specified backup directory. If a repository already exists, it will pull the latest changes.

## Notes

-   Ensure that your GitHub token has the necessary permissions to access your repositories.
-   The script handles pagination to fetch all repositories if you have more than 30.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
