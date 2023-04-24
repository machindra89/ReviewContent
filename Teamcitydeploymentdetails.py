import requests
import xml.etree.ElementTree as ET
import csv

# Replace the following values with your own
teamcity_base_url = "http://teamcity.example.com"
output_file = "deployment_locations.csv"

# Get a list of all projects in TeamCity
projects_url = f"{teamcity_base_url}/httpAuth/app/rest/projects"
response = requests.get(projects_url, auth=("username", "password"))
root = ET.fromstring(response.text)

# Create a CSV file for the output and write headers
with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Project Name", "Build Configuration Name", "Server Name", "Environment Name", "Deployment Location"])

    # Loop through each project and its build configurations
    for project in root.iter("project"):
        project_name = project.attrib["name"]
        build_configs_url = f"{teamcity_base_url}/httpAuth/app/rest/buildTypes?projectId={project.attrib['id']}"
        response = requests.get(build_configs_url, auth=("username", "password"))
        build_configs_root = ET.fromstring(response.text)

        # Loop through each build configuration and its artifacts
        for build_config in build_configs_root.iter("buildType"):
            build_config_name = build_config.attrib["name"]
            artifacts_url = f"{teamcity_base_url}/httpAuth/app/rest/buildTypes/{build_config.attrib['id']}/artifacts/children"
            response = requests.get(artifacts_url, auth=("username", "password"))
            artifacts_root = ET.fromstring(response.text)

            # Loop through each artifact and save its deployment location
            for artifact in artifacts_root.iter("file"):
                artifact_path = artifact.attrib["name"]
                artifact_url = artifact.attrib["href"]
                build_server_url = f"{teamcity_base_url}/httpAuth/app/rest/buildTypes/{build_config.attrib['id']}"
                response = requests.get(build_server_url, auth=("username", "password"))
                server_root = ET.fromstring(response.text)

                # Extract the server name and environment name
                server_name = server_root.find(".//vcs-root-instance/properties/property[@name='url']")
                if server_name is not None:
                    server_name = server_name.text.split("/")[-1]
                else:
                    server_name = ""

                environment_name = server_root.find(".//parameters/property[@name='env']")
                if environment_name is not None:
                    environment_name = environment_name.attrib["value"]
                else:
                    environment_name = ""

                # Extract the deployment location from the artifact URL
                deployment_location = artifact_url.replace(f"/repository/download", "")

                # Write the deployment location to the output file
                writer.writerow([project_name, build_config_name, server_name, environment_name, deployment_location])

print(f"Deployment locations saved to: {output_file}")
