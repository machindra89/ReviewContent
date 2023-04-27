import requests
import csv
import os
import xml.etree.ElementTree as ET

# Set up the TeamCity API URL
TEAMCITY_URL = 'https://your-teamcity-url.com/httpAuth/app/rest/buildTypes'

# Set up authentication credentials for TeamCity
TEAMCITY_USERNAME = 'your-teamcity-username'
TEAMCITY_PASSWORD = 'your-teamcity-password'

# Make a GET request to the TeamCity API to retrieve the XML response
response = requests.get(TEAMCITY_URL, auth=(TEAMCITY_USERNAME, TEAMCITY_PASSWORD))
response_xml = response.content

# Parse the XML response using ElementTree
root = ET.fromstring(response_xml)

# Loop through each build configuration in the XML response and create a CSV file
for build_type in root.iter('buildType'):
    project_name = build_type.attrib['projectName']
    build_type_name = build_type.attrib['name']
    vcs_root_url = ''

    # Retrieve the VCS root URL for the build configuration
    for vcs_root in build_type.iter('vcs-root'):
        vcs_root_url = vcs_root.attrib['url']
        break

    # Create the CSV file for the build configuration
    filename = f'{project_name}_{build_type_name}.csv'
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Project Name', 'Build Configuration', 'SCM Repository URL'])
        writer.writerow([project_name, build_type_name, vcs_root_url])

    print(f'{filename} created successfully.')
