import requests
import csv

# Set up the TeamCity API URL for retrieving build information
TEAMCITY_URL = 'https://your-teamcity-url.com/httpAuth/app/rest/builds?locator=buildType:<buildType>,status:SUCCESS'

# Set up authentication credentials for TeamCity
TEAMCITY_USERNAME = 'your-teamcity-username'
TEAMCITY_PASSWORD = 'your-teamcity-password'

# Specify the build configuration ID for the desired job
build_type = 'buildType:id_of_build_configuration'

# Make a GET request to the TeamCity API to retrieve the XML response for successful builds
response = requests.get(TEAMCITY_URL.replace('<buildType>', build_type), auth=(TEAMCITY_USERNAME, TEAMCITY_PASSWORD))
response_xml = response.content

# Parse the XML response using ElementTree
root = ET.fromstring(response_xml)

# Set up a list to hold the build information for each successful build
builds = []

# Loop through each successful build in the XML response and retrieve the desired information
for build in root.iter('build'):
    build_number = build.attrib['number']
    build_status = build.attrib['status']
    build_finish_time = build.attrib['finishDate']
    build_url = build.attrib['webUrl']
    project_name = build.attrib['projectName']
    deploy_location = ''

    # Retrieve the deployment location for the successful build
    for artifact_dependency in build.iter('artifact-dependency'):
        if artifact_dependency.attrib['type'] == 'buildArtifacts':
            deploy_location = artifact_dependency.attrib['location']
            break

    # Append the build information to the list
    builds.append([project_name, build_number, build_status, build_finish_time, build_url, deploy_location])

# Create the CSV file with the build information
filename = 'successful_builds.csv'
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Project Name', 'Build Number', 'Build Status', 'Build Finish Time', 'Build URL', 'Deploy Location'])
    for build in builds:
        writer.writerow(build)

print(f'{filename} created successfully.')
