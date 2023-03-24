import csv
import requests

# Bitbucket Cloud API endpoint
BITBUCKET_API_URL = "https://api.bitbucket.org/2.0/"

# Bitbucket credentials
BITBUCKET_USERNAME = "<your_bitbucket_username>"
BITBUCKET_PASSWORD = "<your_bitbucket_password>"

# Retrieve the list of Bitbucket projects
projects_response = requests.get(BITBUCKET_API_URL + "teams/<your_team_name>/projects",
                                 auth=(BITBUCKET_USERNAME, BITBUCKET_PASSWORD))

# Create a CSV file to store the project and repository information
with open('bitbucket_projects_repos.csv', mode='w', newline='') as csv_file:
    fieldnames = ['Project Name', 'Repository Name']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    # Loop through the Bitbucket projects
    for project in projects_response.json()['values']:
        # Retrieve the repositories for the current project
        repos_response = requests.get(BITBUCKET_API_URL + "repositories/" + project['key'],
                                      auth=(BITBUCKET_USERNAME, BITBUCKET_PASSWORD))

        # Loop through the repositories and write the project and repository names to the CSV file
        for repo in repos_response.json()['values']:
            writer.writerow({'Project Name': project['name'], 'Repository Name': repo['name']})
