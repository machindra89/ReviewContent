import requests
import json

# Set the TeamCity server URL, username, and password
teamcity_url = "http://your-teamcity-server.com"
username = "your-username"
password = "your-password"

# Authenticate with the TeamCity server
auth = requests.auth.HTTPBasicAuth(username, password)

# Get the list of agents from the TeamCity server
response = requests.get(teamcity_url + "/app/rest/agents", auth=auth)

# Parse the JSON response
agents = json.loads(response.text)["agent"]

# Loop through each agent and check its idle time
for agent in agents:
    agent_id = agent["id"]
    agent_name = agent["name"]

    # Get the agent details from the TeamCity server
    response = requests.get(teamcity_url + "/app/rest/agents/id:" + agent_id, auth=auth)
    agent_details = json.loads(response.text)

    # Check if the agent is idle for more than 30 minutes
    if agent_details["lastActivityTime"] < int(time.time()) - 1800:
        print("Agent {} ({}) is idle for more than 30 minutes. Unauthorizing...".format(agent_name, agent_id))

        # Unauthorize the agent
        response = requests.put(teamcity_url + "/app/rest/agents/id:" + agent_id + "/authorized", auth=auth, data="false")

        # Check if the unauthorization was successful
        if response.status_code == 200:
            print("Agent unauthorization successful.")
        else:
            print("Agent unauthorization failed. Status code: {}".format(response.status_code))
    else:
        print("Agent {} ({}) is not idle.".format(agent_name, agent_id))
