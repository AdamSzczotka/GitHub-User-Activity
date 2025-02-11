# Author: Adam Szczotka
# Title: GitHub-User-Activity-CLI

import sys
import json
import urllib.request
import urllib.error
import argparse
from datetime import datetime


def fetch_github_activity(username):
    """Fetch GitHub activity for a given username using the GitHub API."""

    url = f"https://api.github.com/users/{username}/events"
    headers = {
        'User-Agent': 'Python GitHub Activity Fetcher',
        'Accept': 'application/vnd.github.v3+json'
    }

    try:
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Error: User: {username} not found")
        else:
            print(f"Error: HTTP {e.code} - {e.reason}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error: Failed to connect to Github API - {e.reason}")
        sys.exit(1)


def get_commit_details(commit):
    """Format commit details into a readable string."""

    message = commit['message'].split('\n')[0]
    return f"\n     - {commit['author']['name']}: {message}"


def format_event(event):
    """Format a GitHub event into a redable string with detailed info"""

    event_type = event['type']
    repo_name = event['repo']['name']
    created_at = datetime.strptime(event['created_at'],
                                   '%Y-%m-%dT%H:%M:%SZ')
    formatted_date = created_at.strftime('%Y-%m-%d %H:%M:%S')

    if event_type == 'PushEvent':

        commits = event['payload'].get('commits', [])
        commit_details = ''.join(get_commit_details(commit)
                                 for commit in commits)
        branch = event['payload']['ref'].split('/')[-1]

        return (f"- [{formatted_date}] Pushed "
                f"{len(commits)} commits to {repo_name} on branch '{branch}'"
                f"{commit_details}")


def main():
    pass


if __name__ == "__main__":
    main()
