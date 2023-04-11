import requests
import csv

# Replace <TeamCity_URL> and <TeamCity_Credentials> with your TeamCity server URL and credentials
teamcity_url = "<TeamCity_URL>/app/rest/projects"
headers = {"Authorization": "Basic <TeamCity_Credentials>"}

response = requests.get(teamcity_url, headers=headers)

projects = response.json()["project"]

with open('projects.csv', mode='w', newline='') as csv_file:
    fieldnames = ['id', 'name']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()

    for project in projects:
        writer.writerow({'id': project['id'], 'name': project['name']})


import requests
import csv

# Replace <TeamCity_URL> and <TeamCity_Credentials> with your TeamCity server URL and credentials
teamcity_url = "<TeamCity_URL>/app/rest/projects/"
headers = {"Authorization": "Basic <TeamCity_Credentials>"}

# Read in the project IDs and names from the CSV file created in the previous step
with open('projects.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    projects = [(row['id'], row['name']) for row in csv_reader]

# Create a new CSV file for the project and build configuration information
with open('project_build_configs.csv', mode='w', newline='') as csv_file:
    fieldnames = ['project_name', 'build_config_name']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()

    for project_id, project_name in projects:
        response = requests.get(teamcity_url + project_id + "/buildTypes", headers=headers)
        build_configs = response.json()["buildType"]

        for build_config in build_configs:
            writer.writerow({'project_name': project_name, 'build_config_name': build_config['name']})


import requests
import csv

# Replace <TeamCity_URL> and <TeamCity_Credentials> with your TeamCity server URL and credentials
teamcity_url = "<TeamCity_URL>/app/rest/"
headers = {"Authorization": "Basic <TeamCity_Credentials>"}

# Read in the project IDs and names from the CSV file created in the previous step
with open('projects.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    projects = [(row['id'], row['name']) for row in csv_reader]

# Create a new CSV file for the project, build configuration, and repository information
with open('project_build_config_repos.csv', mode='w', newline='') as csv_file:
    fieldnames = ['project_name', 'build_config_name', 'repository_url']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()

    for project_id, project_name in projects:
        response = requests.get(teamcity_url + "projects/id:" + project_id + "/buildTypes", headers=headers)
        build_configs = response.json()["buildType"]

        for build_config in build_configs:
            response = requests.get(teamcity_url + "vcs-roots/id:" + build_config["vcs-root-entries"]["vcs-root-entry"][0]["vcs-root"]["id"], headers=headers)
            repo_info = response.json()

            if repo_info.get('properties'):
                for prop in repo_info['properties']['property']:
                    if prop['name'] == 'url':
                        writer.writerow({'project_name': project_name, 'build_config_name': build_config['name'], 'repository_url': prop['value']})



import requests
import csv

# Replace <TeamCity_URL> and <TeamCity_Credentials> with your TeamCity server URL and credentials
teamcity_url = "<TeamCity_URL>/app/rest/"
headers = {"Authorization": "Basic <TeamCity_Credentials>"}

# Read in the project and build configuration information from the CSV file created in the previous step
with open('project_build_config_repos.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    projects_build_configs_repos = [(row['project_name'], row['build_config_name'], row['repository_url']) for row in csv_reader]

# Create a new CSV file for the build configurations with SonarQube runners
with open('sonarqube_build_configs.csv', mode='w', newline='') as csv_file:
    fieldnames = ['project_name', 'build_config_name', 'sonarqube_url']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()

    for project_name, build_config_name, repo_url in projects_build_configs_repos:
        response = requests.get(teamcity_url + "buildTypes/name:" + build_config_name + "/steps", headers=headers)
        build_steps = response.json()["step"]

        for build_step in build_steps:
            runner_type = build_step.get("type")
            if runner_type and "sonar" in runner_type.lower():
                runner_properties = build_step.get("properties")
                if runner_properties:
                    for prop in runner_properties["property"]:
                        if prop.get("name") == "sonar.host.url":
                            writer.writerow({'project_name': project_name, 'build_config_name': build_config_name, 'sonarqube_url': prop["value"]})



import requests
import csv
from datetime import datetime

# Replace <TeamCity_URL> and <TeamCity_Credentials> with your TeamCity server URL and credentials
teamcity_url = "<TeamCity_URL>/app/rest/"
headers = {"Authorization": "Basic <TeamCity_Credentials>"}

# Read in the project information from the CSV file created in the first step
with open('teamcity_projects.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    project_names = [row['project_name'] for row in csv_reader]

# Create a new CSV file for the build information
with open('build_information.csv', mode='w', newline='') as csv_file:
    fieldnames = ['project_name', 'total_builds', 'last_build_date']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()

    for project_name in project_names:
        response = requests.get(teamcity_url + "builds/?locator=project:" + project_name + "&count=1", headers=headers)
        last_build = response.json()["build"][0]

        build_date = datetime.strptime(last_build["startDate"], '%Y-%m-%dT%H:%M:%S+0000')
        last_build_date = build_date.strftime('%Y-%m-%d %H:%M:%S')

        total_builds = last_build["number"]
        writer.writerow({'project_name': project_name, 'total_builds': total_builds, 'last_build_date': last_build_date})



import requests
import csv
from datetime import datetime, timedelta

# Replace <TeamCity_URL> and <TeamCity_Credentials> with your TeamCity server URL and credentials
teamcity_url = "<TeamCity_URL>/app/rest/"
headers = {"Authorization": "Basic <TeamCity_Credentials>"}

# Read in the project information from the CSV file created in the first step
with open('teamcity_projects.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    project_names = [row['project_name'] for row in csv_reader]

# Create a new CSV file for the build information
with open('build_information.csv', mode='w', newline='') as csv_file:
    fieldnames = ['project_name', 'total_builds', 'last_build_date']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()

    for project_name in project_names:
        # Calculate the date one year ago from today's date
        one_year_ago = datetime.now() - timedelta(days=365)
        formatted_date = one_year_ago.strftime('%Y-%m-%dT%H:%M:%S+0000')

        # Send a GET request to retrieve the most recent build that occurred in the last year
        response = requests.get(teamcity_url + "builds/?locator=project:" + project_name + ",running:false,sinceBuild:" + formatted_date, headers=headers)
        last_build = response.json()["build"][0]

        # Extract the build number and date, calculate the total number of builds triggered for the project,
        # and write this information to the CSV file
        build_date = datetime.strptime(last_build["startDate"], '%Y-%m-%dT%H:%M:%S+0000')
        last_build_date = build_date.strftime('%Y-%m-%d %H:%M:%S')

        total_builds = last_build["number"]
        writer.writerow({'project_name': project_name, 'total_builds': total_builds, 'last_build_date': last_build_date})





