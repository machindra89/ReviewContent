import requests
import json

# Set the TeamCity API endpoint URL
url = 'http://your-teamcity-server/httpAuth/app/rest/buildTypes'

# Set the authentication details
username = 'your-username'
password = 'your-password'

# Set the request headers
headers = {
    'Accept': 'application/json'
}

# Make the HTTP request
response = requests.get(url, headers=headers, auth=(username, password))

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = json.loads(response.text)
    # Initialize a set to store the programming languages
    languages = set()
    # Loop over each build configuration
    for build_config in data['buildType']:
        # Get the build log for the last finished build
        build_url = build_config['href'] + '/builds?count=1'
        build_response = requests.get(build_url, headers=headers, auth=(username, password))
        build_data = json.loads(build_response.text)
        build_id = build_data['build'][0]['id']
        log_url = build_config['href'] + '/builds/id:' + str(build_id) + '/log'
        log_response = requests.get(log_url, headers=headers, auth=(username, password))
        # Extract the programming language from the build log
        if log_response.status_code == 200:
            log_lines = log_response.text.split('\n')
            for line in log_lines:
                if 'Compiling' in line:
                    parts = line.split()
                    for part in parts:
                        if '.' in part:
                            extension = part.split('.')[-1]
                            if extension == 'java':
                                languages.add('Java')
                            elif extension == 'py':
                                languages.add('Python')
                            elif extension == 'rb':
                                languages.add('Ruby')
                            # Add more file extensions and programming languages as required
    # Print the list of programming languages
    print('Programming Languages:')
    for lang in languages:
        print(lang)
else:
    print('Failed to fetch build configurations')
