import requests
import csv

# TeamCity API endpoint
TEAMCITY_API_URL = "https://<your_teamcity_server>/app/rest/"

# TeamCity credentials
TEAMCITY_USERNAME = "<your_teamcity_username>"
TEAMCITY_PASSWORD = "<your_teamcity_password>"

# Retrieve the list of build configurations from TeamCity
response = requests.get(TEAMCITY_API_URL + "buildTypes", auth=(TEAMCITY_USERNAME, TEAMCITY_PASSWORD))
if response.ok:
    build_configs_data = response.json()["buildType"]
    # Open a CSV file to write the project, build name, and repository name
    with open("build_configs.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Project", "Build Name", "Repository Name"])
        # For each build configuration, retrieve its associated VCS root and extract the repository URL and name
        for build_config in build_configs_data:
            build_config_id = build_config["id"]
            build_config_name = build_config["name"]
            build_config_project = build_config["@projectName"]
            response = requests.get(TEAMCITY_API_URL + "buildTypes/id:" + build_config_id + "/vcs-root-entries", auth=(TEAMCITY_USERNAME, TEAMCITY_PASSWORD))
            if response.ok:
                vcs_root_data = response.json()["vcs-root-entry"]
                if vcs_root_data:
                    vcs_root_id = vcs_root_data[0]["vcs-root"]["id"]
                    response = requests.get(TEAMCITY_API_URL + "vcs-roots/id:" + vcs_root_id, auth=(TEAMCITY_USERNAME, TEAMCITY_PASSWORD))
                    if response.ok:
                        vcs_root_url = response.json()["properties"]["property"][0]["value"]
                        vcs_root_name = response.json()["name"]
                        # Write the relevant information to the CSV file
                        writer.writerow([build_config_project, build_config_name, vcs_root_name])
