import csv

# Load the build types from the buildTypes.csv file
with open("buildTypes.csv", "r") as f:
    build_types_reader = csv.reader(f)
    build_types = {row[0]: row[1] for row in build_types_reader}

# Load the builds from the builds.csv file
with open("builds.csv", "r") as f:
    builds_reader = csv.reader(f)
    builds = {row[0]: row[2] for row in builds_reader}

# Load the dependencies from the dependencies.csv file
with open("dependencies.csv", "r") as f:
    dependencies_reader = csv.reader(f)
    next(dependencies_reader)  # skip the header row
    dependencies = {row[0]: row[1] for row in dependencies_reader}

# Create a dictionary to store the different build dependencies for each build
build_dependencies = {}

# Iterate over each build and find its dependencies
for build_id, build_name in builds.items():
    # Find the build type ID for the current build
    build_type_id = build_types.get(build_name)
    if not build_type_id:
        # Skip this build if we can't find its build type ID
        continue
    
    # Find the dependencies for the current build type
    build_type_dependencies = []
    for dependency_id, dependency_type in dependencies.items():
        if dependency_type == "snapshot_dependency" and build_type_id in dependency_id:
            # This is a snapshot dependency of the current build type, so add it to the list
            build_type_dependencies.append(dependency_id.split(":")[2])
    
    # Save the list of dependencies for this build
    build_dependencies[build_id] = build_type_dependencies

# Save the build dependencies to a CSV file
with open("buildDependencies.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Build ID", "Dependencies"])
    for build_id, dependencies in build_dependencies.items():
        writer.writerow([build_id, ", ".join(dependencies)])
