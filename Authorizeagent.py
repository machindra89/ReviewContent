import requests

# TeamCity server information
TEAMCITY_URL = 'https://your-teamcity-url.com'
TEAMCITY_USERNAME = 'your-teamcity-username'
TEAMCITY_PASSWORD = 'your-teamcity-password'

# Get list of all build agents and their authorization status
agents_url = f'{TEAMCITY_URL}/httpAuth/app/rest/agents?fields=name,authorized'
agents_response = requests.get(agents_url, auth=(TEAMCITY_USERNAME, TEAMCITY_PASSWORD))
agents = agents_response.json()['agent']

# Get list of all builds and their assigned agent
builds_url = f'{TEAMCITY_URL}/httpAuth/app/rest/builds?fields=buildType(name),status,agent(name)'
builds_response = requests.get(builds_url, auth=(TEAMCITY_USERNAME, TEAMCITY_PASSWORD))
builds = builds_response.json()['build']

# Find unauthorized agents and assign them to the default agent pool
unauthorized_agents = [agent for agent in agents if not agent['authorized']]
for agent in unauthorized_agents:
    print(f'{agent["name"]} is unauthorized. Authorizing...')
    authorization_url = f'{TEAMCITY_URL}/httpAuth/app/rest/agents/id:{agent["id"]}/authorized'
    requests.put(authorization_url, data='true', auth=(TEAMCITY_USERNAME, TEAMCITY_PASSWORD))
    print(f'{agent["name"]} has been authorized.')

# Find builds that are assigned to unauthorized agents and reassign them to a random authorized agent
unauthorized_builds = [build for build in builds if build['agent'] is not None and not build['agent']['authorized']]
for build in unauthorized_builds:
    print(f'Build {build["buildType"]["name"]} ({build["status"]}) is assigned to unauthorized agent {build["agent"]["name"]}. Reassigning...')
    authorized_agents = [agent for agent in agents if agent['authorized']]
    if not authorized_agents:
        print('No authorized agents available.')
    else:
        new_agent_name = authorized_agents[0]['name']
        reassign_url = f'{TEAMCITY_URL}/httpAuth/app/rest/builds/{build["id"]}/agent?newAgentName={new_agent_name}'
        requests.put(reassign_url, auth=(TEAMCITY_USERNAME, TEAMCITY_PASSWORD))
        print(f'Build {build["buildType"]["name"]} ({build["status"]}) has been reassigned to {new_agent_name}.')
