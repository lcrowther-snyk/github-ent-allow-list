import subprocess
import argparse
import csv
import json
import os


def add_ip_to_allow_list(github_token, owner_id, ip, name):
    mutation = '''
    mutation ($owner_id: ID!, $allowListValue: String!, $name: String!) {
      createIpAllowListEntry(input: { ownerId: $owner_id, allowListValue: $allowListValue, name: $name, isActive: true }) {
        ipAllowListEntry {
          id
          allowListValue
          name
          isActive
        }
      }
    }
    '''


    try:
        command = [
            "gh", "api", "graphql",
            "-f", f"owner_id='{owner_id}'",
            "-f", f"allowListValue='{ip}'",
            "-f", f"name='{name}'",
            "-f", f"query='{mutation.strip()}'"
        ]

        command_str = " ".join(command)

        result = subprocess.run(
            command_str,
            capture_output=True,
            shell=True,
            text=True,
            check=True,
            env={**os.environ, "GITHUB_TOKEN": github_token}
        )
        print(f"IP address {ip} added successfully.")

    except subprocess.CalledProcessError as e:
        print(f"Failed to add IP address {ip} with error:")
        print("Return code:", e.returncode)
        print("Output:", e.stdout)
        print("Error:", e.stderr)
    except Exception as e:
        print(f"An unexpected error occurred while adding IP {ip}: {e}")


def process_ip_file(file_path, github_token, owner_id):
    try:
        with open(file_path, mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                ip = row.get("ip")
                name = row.get("note")
                if ip and name:  # Ensure both IP and name are present
                    add_ip_to_allow_list(github_token, owner_id, ip, name)
                else:
                    print(f"Skipping invalid row: {row}")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def get_owner_id_from_slug(github_token, enterprise_slug):
    query = '''
    query ($slug: String!) {
      enterprise(slug: $slug) {
        id
        name
      }
    }
    '''
    try:
        command = [
            "gh", "api", "graphql",
            "-f", f"query={query.strip()}",
            "-F", f"slug={enterprise_slug}"
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            env={**os.environ, "GITHUB_TOKEN": github_token}
        )
        response = json.loads(result.stdout)
        return response["data"]["enterprise"]["id"]
    except subprocess.CalledProcessError as e:
        print(f"Failed to retrieve owner ID for enterprise slug '{enterprise_slug}' with error:")
        print("Return code:", e.returncode)
        print("Output:", e.stdout)
        print("Error:", e.stderr)
        raise
    except Exception as e:
        print(f"An unexpected error occurred while retrieving owner ID: {e}")
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add IPs to GitHub Enterprise allow list using gh CLI.")
    parser.add_argument("--file-path", required=True, help="Path to the .csv file containing IPs and names")
    parser.add_argument("--github-token", required=True, help="GitHub Personal Access Token")
    parser.add_argument("--enterprise-slug", required=True, help="Enterprise slug for the enterprise")

    args = parser.parse_args()

    try:
        owner_id = get_owner_id_from_slug(args.github_token, args.enterprise_slug)
        process_ip_file(args.file_path, args.github_token, owner_id)
    except Exception as e:
        print(f"Failed to process IP file: {e}")