import csv
import sqlite3

# Specify the path to the Bitbucket database
BITBUCKET_DB_PATH = '/path/to/bitbucket_home/shared/data/db/bitbucket.db'

# Open a connection to the Bitbucket database
conn = sqlite3.connect(BITBUCKET_DB_PATH)

# Query to retrieve project, user, project key, and permissions data
query = """
SELECT p.pkey AS project_key, p.name AS project_name, u.lower_name AS username, pu.permission
FROM project p
JOIN project_role pr ON pr.project_id = p.id
JOIN user_role_mapping urm ON urm.role_id = pr.role_id
JOIN "user" u ON u.id = urm.user_id
JOIN project_permission pu ON pu.project_id = p.id AND pu.user_id = u.id
ORDER BY project_key
"""

# Execute the query and fetch the results
cursor = conn.execute(query)
rows = cursor.fetchall()

# Close the database connection
conn.close()

# Write the results to a CSV file
with open('bitbucket_permissions.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Project Key', 'Project Name', 'Username', 'Permission'])
    writer.writerows(rows)
