# GitHub Activity CLI

A command-line interface tool to fetch and display GitHub user activity. This tool allows you to view recent GitHub activities of any user, with options to filter by event type and display detailed information about each activity.

Project inspired by [GitHub User Activity Project](https://roadmap.sh/projects/github-user-activity)

## Features

- Fetch recent GitHub activity for any public GitHub user
- Filter activities by event type
- Detailed information for different event types:
  - Push events (commits, branch information)
  - Issue events (title, URL)
  - Pull request events (title, changes, URL)
  - Repository creation events
  - Watch events (starring)
  - Fork events
  - Issue comments
  - Release events
- No authentication required for basic usage
- Clean and formatted output

## Installation

1. Clone this repository:
```bash
git clone https://github.com/AdamSzczotka/GitHub-User-Activity
cd GitHub-User-Activity
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

## Usage

Basic usage:
```bash
python github-activity.py <username>
```

View specific event types:
```bash
python github-activity.py <username> --type PushEvent
```

List supported event types:
```bash
python github-activity.py --list-types
```

### Example Output

```
Fetching recent GitHub activity for user: octocat
------------------------------------------------------------
- [2025-02-08 16:50:42] Pushed 4 commits to AdamSzczotka/Class2Calendar on branch 'main'
     - Adam Szczotka: chore: add gitignore file
     - Adam Szczotka: docs: add readme file
     - Adam Szczotka: docs: add readme file
     - Adam Szczotka: Merge branch 'main' of https://github.com/AdamSzczotka/Class2Calendar

- [2025-02-08 16:44:26] Pushed 6 commits to AdamSzczotka/Class2Calendar on branch 'main'
     - Adam Szczotka: fix: not enough values to unpack
     - Adam Szczotka: build: update
     - Adam Szczotka: docs: example of credentials
     - Adam Szczotka: style: remove trailing whitespaces and limit line length
```

### Supported Event Types

- `PushEvent`: Code pushes
- `CreateEvent`: Branch or repository creation
- `IssuesEvent`: Issue operations
- `PullRequestEvent`: Pull request operations
- `WatchEvent`: Repository starring
- `ForkEvent`: Repository forking
- `IssueCommentEvent`: Comments on issues
- `ReleaseEvent`: Release publications

## Requirements

- Python 3.6+
- Standard library modules (no external dependencies)

## Error Handling

The tool handles various error cases:
- Invalid usernames
- Network connectivity issues
- API rate limiting
- Invalid event type filters

## Contributing

Feel free to open issues or submit pull requests with improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.