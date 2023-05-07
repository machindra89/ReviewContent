I can try to rewrite the code using only TeamCity REST APIs, but I cannot guarantee that it will work as expected. Here is a possible code:

```python
# Import the required modules
import requests
import csv

# Define the TeamCity base URL and credentials
teamcity_url = "https://teamcity.example.com"
teamcity_user = "username"
teamcity_pass = "password"

# Define the output CSV file name
output_file = "output.csv"

# Create a session object to handle authentication
session = requests.Session()
session.auth = (teamcity_user, teamcity_pass)

# Get the list of projects from TeamCity
projects_url = teamcity_url + "/app/rest/projects"
projects_response = session.get(projects_url)
projects_data = projects_response.json()

# Create a list to store the output rows
output_rows = []

# Loop through each project
for project in projects_data["project"]:
    # Get the project name and id
    project_name = project["name"]
    project_id = project["id"]

    # Get the list of build configurations for the project
    build_configs_url = teamcity_url + "/app/rest/projects/id:" + project_id + "/buildTypes"
    build_configs_response = session.get(build_configs_url)
    build_configs_data = build_configs_response.json()

    # Loop through each build configuration
    for build_config in build_configs_data["buildType"]:
        # Get the build configuration name and id
        build_config_name = build_config["name"]
        build_config_id = build_config["id"]

        # Get the SCM locations for the build configuration
        scm_locations_url = teamcity_url + "/app/rest/buildTypes/id:" + build_config_id + "/vcs-root-entries"
        scm_locations_response = session.get(scm_locations_url)
        scm_locations_data = scm_locations_response.json()

        # Loop through each SCM location
        for scm_location in scm_locations_data["vcs-root-entry"]:
            # Get the SCM location name and id
            scm_location_name = scm_location["vcs-root"]["name"]
            scm_location_id = scm_location["vcs-root"]["id"]

            # Get the SonarQube scanning details for the SCM location from TeamCity properties
            sonarqube_details_url = teamcity_url + "/app/rest/buildTypes/id:" + build_config_id + "/parameters"
            sonarqube_details_response = session.get(sonarqube_details_url)
            sonarqube_details_data = sonarqube_details_response.json()

            # Get the SonarQube metrics values from TeamCity properties
            sonarqube_metrics = sonarqube_details_data["property"]
            sonarqube_bugs = next((m["value"] for m in sonarqube_metrics if m["name"] == "sonar.bugs"), None)
            sonarqube_vulnerabilities = next((m["value"] for m in sonarqube_metrics if m["name"] == "sonar.vulnerabilities"), None)
            sonarqube_code_smells = next((m["value"] for m in sonarqube_metrics if m["name"] == "sonar.code_smells"), None)
            sonarqube_coverage = next((m["value"] for m in sonarqube_metrics if m["name"] == "sonar.coverage"), None)
            sonarqube_duplicated_lines_density = next((m["value"] for m in sonarqube_metrics if m["name"] == "sonar.duplicated_lines_density"), None)

            # Get the deployment location and environment for the SCM location from TeamCity properties
            # This part is not clear from the question, so I'm assuming some dummy values
            deployment_location = "https://artifactory.example.com/" + scm_location_id
            deployment_environment = "prod"

            # Create a row with all the information and append it to the output list
            row = [project_name, project_id, build_config_name, build_config_id, scm_location_name, scm_location_id, sonarqube_bugs, sonarqube_vulnerabilities, sonarqube_code_smells, sonarqube_coverage, sonarqube_duplicated_lines_density, deployment_location, deployment_environment]
            output_rows.append(row)

Okay, I will continue writing the code. Here is the rest of the code:

```python
# Write the output list to a CSV file
with open(output_file, "w") as f:
    writer = csv.writer(f)
    writer.writerow(["Project Name", "Project ID", "Build Configuration Name", "Build Configuration ID", "SCM Location Name", "SCM Location ID", "SonarQube Bugs", "SonarQube Vulnerabilities", "SonarQube Code Smells", "SonarQube Coverage", "SonarQube Duplicated Lines Density", "Deployment Location", "Deployment Environment"])
    for row in output_rows:
        writer.writerow(row)

# Print a message when the code is done
print("The code is done. The output file is:", output_file)
