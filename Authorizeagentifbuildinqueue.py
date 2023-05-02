import requests
import json

# Define your TeamCity server URL and authentication credentials
server_url = "http://your-teamcity-server-url"
username = "your-username"
password = "your-password"

# Define the endpoint for authorizing an agent
authorize_endpoint = "/app/rest/agents/id:{agent_id}/authorize"

# Define the endpoint for retrieving the build queue
queue_endpoint = "/app/rest/buildQueue"

# Make a request to retrieve the build queue
response = requests.get(server_url + queue_endpoint, auth=(username, password))

# Parse the response JSON to find the first build that is assigned to an agent
queue_items = json.loads(response.content)["build"]
for item in queue_items:
    if "agent" in item and item["agent"] is not None:
        agent_id = item["agent"]["id"]
        print(f"Build {item['id']} is assigned to agent {agent_id}")
        
        # Make a request to authorize the agent
        response = requests.put(server_url + authorize_endpoint.format(agent_id=agent_id), auth=(username, password))
        print(f"Agent {agent_id} authorized successfully")
        break
