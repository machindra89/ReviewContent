import requests
import json

BITBUCKET_URL = "https://your-bitbucket-url"
PROJECT_KEY = "your-project-key"
USERNAME = "your-username"
PASSWORD = "your-password"

def get_project_permissions():
    # Create a session and set the basic authentication credentials
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)

    # Set the base URL for the Bitbucket Server REST API
    base_url = BITBUCKET_URL + "/rest/api/1.0"

    # Build the URL to fetch project permissions
    url = f"{base_url}/projects/{PROJECT_KEY}/permissions/users"

    # Fetch the project permissions from the API
    response = session.get(url)

    # Parse the response as JSON
    permissions_json = json.loads(response.text)

    # Extract the relevant information from the JSON response
    project_permissions = []
    for user_permission in permissions_json["values"]:
        user_email = user_permission["user"]["emailAddress"]
        permission = user_permission["permission"]
        project_permissions.append({"project": PROJECT_KEY, "email": user_email, "permission": permission})

    return project_permissions

if __name__ == "__main__":
    # Call the get_project_permissions() function to fetch project permissions
    project_permissions = get_project_permissions()

    # Print the project permissions
    for pp in project_permissions:
        print(f"Project: {pp['project']}, User: {pp['email']}, Permission: {pp['permission']}")
