import requests
import xml.etree.ElementTree as ET

# Set the base URL for the TeamCity server and your API token
TEAMCITY_BASE_URL = 'http://your-teamcity-server-url'
TEAMCITY_API_TOKEN = 'your-api-token'

# Helper function to send authenticated API requests
def send_request(url):
    headers = {'Authorization': f'Bearer {TEAMCITY_API_TOKEN}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        return None

# Retrieve a list of projects
projects_url = f'{TEAMCITY_BASE_URL}/app/rest/projects'
projects_xml = send_request(projects_url)
projects = ET.fromstring(projects_xml)
for project in projects.findall('project'):
    project_name = project.attrib['name']
    project_id = project.attrib['id']

    # Retrieve a list of build configurations for the project
    build_configs_url = f'{TEAMCITY_BASE_URL}/app/rest/projects/{project_id}/buildTypes'
    build_configs_xml = send_request(build_configs_url)
    build_configs = ET.fromstring(build_configs_xml)
    for build_config in build_configs.findall('buildType'):
        build_config_name = build_config.attrib['name']
        build_config_id = build_config.attrib['id']

        # Retrieve the VCS roots for the build configuration
        vcs_roots_url = f'{TEAMCITY_BASE_URL}/app/rest/buildTypes/{build_config_id}/vcs-root-entries'
        vcs_roots_xml = send_request(vcs_roots_url)
        vcs_roots = ET.fromstring(vcs_roots_xml)
        for vcs_root in vcs_roots.findall('vcs-root-entry'):
            vcs_root_id = vcs_root.find('vcs-root').attrib['id']

            # Retrieve the SCM repository information for the VCS root
            vcs_root_url = f'{TEAMCITY_BASE_URL}/app/rest/vcs-roots/id:{vcs_root_id}'
            vcs_root_xml = send_request(vcs_root_url)
            vcs_root = ET.fromstring(vcs_root_xml)
            scm_repo_url = vcs_root.find('properties/property[@name="url"]').text

            # Output the information
            print(f'Project: {project_name}')
            print(f'Build Configuration: {build_config_name}')
            print(f'VCS Root ID: {vcs_root_id}')
            print(f'SCM Repository URL: {scm_repo_url}')
