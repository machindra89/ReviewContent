

import requests
import json
import csv

# Set the base URL for the Bitbucket API
url = "https://<bitbucket_url>/rest/api/1.0"

# Set the authentication credentials
username = "<username>"
password = "<password>"

# Set the headers to accept JSON responses
headers = {
    "Accept": "application/json"
}

# Retrieve all projects
projects_url = url + "/projects"
projects_response = requests.get(projects_url, auth=(username, password), headers=headers)
projects_data = json.loads(projects_response.content)["values"]

# Open a CSV file to write the results
with open("merge_checks.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)

    # Write the header row
    writer.writerow(["Project Key", "Project Name", "Repository Name", "Repository Slug", "Merge Checks Enabled"])

    # Loop through each project and its repositories
    for project in projects_data:
        repos_url = url + f"/projects/{project['key']}/repos"
        repos_response = requests.get(repos_url, auth=(username, password), headers=headers)
        repos_data = json.loads(repos_response.content)["values"]
        
        for repo in repos_data:
            settings_url = url + f"/projects/{project['key']}/repos/{repo['slug']}/settings/pull-requests"
            settings_response = requests.get(settings_url, auth=(username, password), headers=headers)
            settings_data = json.loads(settings_response.content)
            merge_checks_enabled = settings_data["mergeConfig"]["defaultMergeStrategy"]["id"] == "squash"
            
            # Write the repository information to the CSV file
            writer.writerow([project["key"], project["name"], repo["name"], repo["slug"], merge_checks_enabled])
            
            print(f"{project['key']}/{repo['slug']} - Merge checks enabled: {merge_checks_enabled}")
            
print("Done.")
