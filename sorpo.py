import csv
import requests

# SonarQube API endpoint
SONARQUBE_API_URL = "https://<your_sonarqube_server>/api/"

# SonarQube credentials
SONARQUBE_TOKEN = "<your_sonarqube_token>"

# SonarQube project key
SONARQUBE_PROJECT_KEY = "<your_sonarqube_project_key>"

# Bitbucket URL
BITBUCKET_URL = ""

# Retrieve the Bitbucket URL from the SonarQube project settings
response = requests.get(SONARQUBE_API_URL + "settings/values?keys=sonar.links.scm", auth=(SONARQUBE_TOKEN, ""))
if response.ok:
    settings_data = response.json()["settings"]
    for setting in settings_data:
        if setting["key"] == "sonar.links.scm":
            BITBUCKET_URL = setting["value"]
            break

# Extract the Bitbucket project name and repository name from the Bitbucket URL
bitbucket_parts = BITBUCKET_URL.split("/")
bitbucket_project = bitbucket_parts[-2]
bitbucket_repo = bitbucket_parts[-1][:-1]

# Retrieve the last analysis date for the SonarQube project
response = requests.get(SONARQUBE_API_URL + "project_analyses/search?projectKey=" + SONARQUBE_PROJECT_KEY + "&ps=1", auth=(SONARQUBE_TOKEN, ""))
if response.ok:
    analyses_data = response.json()["analyses"]
    if analyses_data:
        last_analysis_date = analyses_data[0]["date"]
    else:
        last_analysis_date = "N/A"

# Retrieve the SonarQube project name
response = requests.get(SONARQUBE_API_URL + "projects/search?projects=" + SONARQUBE_PROJECT_KEY, auth=(SONARQUBE_TOKEN, ""))
if response.ok:
    projects_data = response.json()["components"]
    if projects_data:
        sonarqube_project_name = projects_data[0]["name"]
    else:
        sonarqube_project_name = "N/A"

# Write the relevant information to a CSV file
with open("sonarqube_info.csv", "w", newline="") as csvfile:
    fieldnames = ["Bitbucket URL", "Bitbucket Project Name", "Bitbucket Repository Name", "SonarQube Project Name", "Last Analysis Date"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({
        "Bitbucket URL": BITBUCKET_URL,
        "Bitbucket Project Name": bitbucket_project,
        "Bitbucket Repository Name": bitbucket_repo,
        "SonarQube Project Name": sonarqube_project_name,
        "Last Analysis Date": last_analysis_date
    })
