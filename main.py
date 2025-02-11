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

    elif event_type == 'CreateEvent':
        ref_type = event['payload']['ref_type']
        ref = event['payload'].get('ref', '')
        description = f" named '{ref};" if ref else ""

        return (f"- [{formatted_date} "
                f"Created {ref_type}{description} in {repo_name}")

    elif event_type == 'IssuesEvent':
        action = event['payload']['action']
        issue = event['payload']['issue']
        issue_number = issue['number']
        issue_title = issue['title']
        return (f"- [{formatted_date}] {action.capitalize()} "
                f"issue #{issue_number} in {repo_name}\n"
                f"      Title: {issue_title}\n"
                f"      URL: {issue['html_url']}")

    elif event_type == 'PullRequestEvent':
        action = event['payload']['action']
        pr = event['payload']['pull_request']
        pr_number = pr['number']
        pr_title = pr['title']

        return (f"- [{formatted_date}] {action.capitalize()} pull request "
                f"#{pr_number} in {repo_name}\n"
                f"      Title: {pr_title}\n"
                f"      Changes: +{pr['additions']}, -{pr['deletions']}\n"
                f"      URL: {pr['html_url']}")

    elif event_type == 'WatchEvent':
        return f"- [{formatted_date}] Starred {repo_name}"

    elif event_type == 'ForkEvent':
        fork_name = event['payload']['forkee']['full_name']
        return (f"- [{formatted_date}] Forked {repo_name}\n"
                f"      Fork: {fork_name}")

    elif event_type == 'IssueCommentEvent':
        issue_number = event['payload']['issue']['number']
        comment = event['payload']['comment']['body']
        preview = comment[:100] + '...' if len(comment) > 100 else comment
        return (f"- [{formatted_date}] Commented on issue #{issue_number} "
                f"in {repo_name}\n"
                f"      Comment preview: {preview}")

    elif event_type == 'ReleaseEvent':
        release = event['payload']['release']
        return (f"- [{formatted_date}] Published release "
                f"{release['tag_name']} in {repo_name}\n"
                f"      Title: {release['name']}\n"
                f"      URL: {release['html_url']}")

    else:
        return f"- [{formatted_date}] {event_type} on {repo_name}"


def get_supported_event_types():
    """Returns a list of supported event types for filtering"""
    return [
        'PushEvent',
        'CreateEvent',
        'IssuesEvent',
        'PullRequestEvent',
        'WatchEvent',
        'ForkEvent',
        'IssueCommentEvent',
        'ReleaseEvent'
    ]


def main():
    parser = argparse.ArgumentParser(
        description="Fetch and display user activity")
    parser.add_argument('username', help='Github username')
    parser.add_argument('--type', choices=get_supported_event_types(),
                        help='Filter events by type')
    parser.add_argument('--list-types', action='store_true',
                        help='List supported event types')

    args = parser.parse_args()

    if args.list_types:
        print("Supported event types:")
        for event_type in get_supported_event_types():
            print(f"  - {event_type}")
        return

    print(f"Fetching recent GitHub activity for user: {args.username}")
    if args.type:
        print(f"Filtering for event type: {args.type}")
    print("-" * 60)

    events = fetch_github_activity(args.username)

    if not events:
        print("No recent activity found.")
        return

    filtered_events = [e for e in events if
                       not args.type or e['type'] == args.type]

    if not filtered_events:
        print(f"No events found matching type: {args.type}")
        return

    for event in filtered_events:
        print(format_event(event))
        print()


if __name__ == "__main__":
    main()
