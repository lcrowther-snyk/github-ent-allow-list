# GitHub Enterprise Allow List Script

This script is designed to add IP addresses to the allow list of a GitHub Enterprise using the `gh` CLI and GraphQL API.

## Purpose

The script automates the process of:
1. Retrieving the `owner_id` (enterprise ID) from an enterprise slug.
2. Adding IP addresses and their associated notes to the allow list of a GitHub Enterprise.

## Prerequisites

1. **GitHub CLI (`gh`)**:  
   The script requires the GitHub CLI to interact with the GitHub GraphQL API.  
   Installation instructions for the GitHub CLI can be found [here](https://github.com/cli/cli#installation).

2. **Python 3.6+**:  
   Ensure you have Python installed on your system.

3. **GitHub Personal Access Token**:  
   A GitHub token with the necessary permissions to manage the allow list.

4. **CSV File**:  
   A `.csv` file containing the IP addresses and their associated notes. The file should have the following format:
   ```csv
   ip,note
   35.123.234.12,Test IP
   34.234.1.32,Test IP
   
## Command-Line Arguments

The script accepts the following arguments:

- `--file-path`: **Required**. Path to the `.csv` file containing IP addresses and notes.  
  Example: `--file-path snykips.csv`

- `--github-token`: **Required**. Your GitHub Personal Access Token.  
  Example: `--github-token ghp_XXXXXXXXXXXXXXXXXXXX`

- `--enterprise-slug`: **Required**. The slug of your GitHub Enterprise organization.  
  Example: `--enterprise-slug my-enterprise`

## Usage

Run the script using the following command:

```bash
python main.py --file-path <path_to_csv> --github-token <github_token> --enterprise-slug <enterprise_slug>