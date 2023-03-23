import csv
import requests

# TeamCity API endpoint
TEAMCITY_API_URL = "https://<your_teamcity_server>/app/rest/"

# TeamCity credentials
TEAMCITY_USERNAME = "<your_teamcity_username>"
TEAMCITY_PASSWORD = "<your_teamcity_password>"

# Bitbucket URL
BITBUCKET_URL = "https://bitbucket.org/<username>/<repo>/"

# Extract the Bitbucket project name and repository name from the Bitbucket URL
bitbucket_parts = BITBUCKET_URL.split("/")
bitbucket_project = bitbucket_parts[-2]
bitbucket_repo = bitbucket_parts[-1][:-1]

# Retrieve the VCS root ID for the Bitbucket repository
response = requests.get(TEAMCITY_API_URL + "vcs-roots?locator=property:(name:URL),value:" + BITBUCKET_URL, auth=(TEAMCITY_USERNAME, TEAMCITY_PASSWORD))
if response.ok:
    vcs_root_data = response.json()["vcs-root"]
    if vcs_root_data:
        vcs_root_id = vcs_root_data[0]["id"]
        vcs_root_name = vcs_root_data[0]["name"]
        # Retrieve the build configurations that use the VCS root
        response = requests.get(TEAMCITY_API_URL + "buildTypes?locator=vcs-root:" + vcs_root_id, auth=(TEAMCITY_USERNAME, TEAMCITY_PASSWORD))
        if response.ok:
            build_configs_data = response.json()["buildType"]
            if build_configs_data:
                # Write the relevant information for each build configuration to a CSV file
                with open("build_configs.csv", "w", newline="") as csvfile:
                    fieldnames = ["Build Name", "Project Name", "VCS Root Name", "Bitbucket Project Name", "Bitbucket Repository Name"]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for build_config in build_configs_data:
                        build_config_name = build_config["name"]
                        build_config_project = build_config["@projectName"]
                        writer.writerow({
                            "Build Name": build_config_name,
                            "Project Name": build_config_project,
                            "VCS Root Name": vcs_root_name,
                            "Bitbucket Project Name": bitbucket_project,
                            "Bitbucket Repository Name": bitbucket_repo
                        })
