import requests

import datetime

def get_idle_time(agent):

    agent_id = agent['id']

    agent_name = agent['name']

    agent_href = agent['href']

    

    # Retrieve the agent details

    agent_details_url = f"{agent_href}/details"

    response = requests.get(agent_details_url)

    if response.status_code == 200:

        agent_details = response.json()

        connected = agent_details['connected']

        if connected:

            # Retrieve the agent's current build details

            agent_builds_url = f"{agent_href}/builds"

            response = requests.get(agent_builds_url)

            if response.status_code == 200:

                agent_builds = response.json()

                if len(agent_builds['build']) > 0:

                    # The agent is currently busy

                    print(f"{agent_name} is busy.")

                else:

                    # The agent is idle

                    last_activity = agent_details['lastActivityTime']

                    last_activity_time = datetime.datetime.fromtimestamp(last_activity / 1000)

                    idle_time = datetime.datetime.now() - last_activity_time

                    print(f"{agent_name} is idle for {idle_time}.")

            else:

                print(f"Failed to retrieve builds for agent {agent_name}.")

        else:

            print(f"{agent_name} is not connected.")

    else:

        print(f"Failed to retrieve details for agent {agent_name}.")

# Your TeamCity server information

base_url = "http://your-teamcity-instance"

username = "your-username"

password = "your-password"

# Retrieve all connected agents

agents_url = f"{base_url}/app/rest/agents?locator=connected:true"

response = requests.get(agents_url, auth=(username, password))

if response.status_code == 200:

    agents = response.json()['agent']

    for agent in agents:

        get_idle_time(agent)

else:

    print("Failed to retrieve agents.")

