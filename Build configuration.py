import requests
import csv

# Set up the API endpoint and authentication headers
api_url = "https://<your-teamcity-url>/app/rest/buildTypes"
headers = {
    "Accept": "application/json",
    "Authorization": "Bearer <your-access-token>"
}

# Send the API request and get the response
response = requests.get(api_url, headers=headers)
response.raise_for_status()

# Parse the JSON data into a list of dictionaries
data = response.json()["buildType"]

# Write the data to a CSV file using the UTF-8 encoding
with open("build-configurations.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["id", "projectName", "name"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for item in data:
        writer.writerow({
            "id": item["id"],
            "projectName": item["projectName"],
            "name": item["name"]
        })
