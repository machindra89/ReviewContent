import csv
import requests
import time

# Replace the following values with your own
teamcity_base_url = "http://teamcity.example.com"
username = "username"
password = "password"

# Fetch the list of agents
agents_url = f"{teamcity_base_url}/httpAuth/app/rest/agents"
response = requests.get(agents_url, auth=(username, password))
response.raise_for_status()
agents = response.json()

# Filter the list to only include connected agents
connected_agents = [agent for agent in agents["agent"] if agent["connected"]]

# Fetch the idle time for each connected agent
agent_idle_times = []
for agent in connected_agents:
    agent_url = f"{teamcity_base_url}/httpAuth/app/rest/agents/id:{agent['id']}"
    response = requests.get(agent_url, auth=(username, password))
    response.raise_for_status()
    agent_data = response.json()
    last_activity_time = agent_data["properties"]["agent.lastActivityTime"]
    last_activity_time = int(last_activity_time) / 1000  # convert to seconds
    idle_time = time.time() - last_activity_time
    agent_idle_times.append({"agent_name": agent["name"], "idle_time": idle_time})

# Write the data to a CSV file
with open("agent_idle_times.csv", "w", newline="") as csvfile:
    fieldnames = ["agent_name", "idle_time"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for agent in agent_idle_times:
        writer.writerow(agent)
