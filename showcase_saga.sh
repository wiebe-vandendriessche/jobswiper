#!/bin/bash

# Path to your JSON files
SAGA_SCRIPT="./postman_script/showcase-saga.postman_collection.json"
ENVIRONMENT_FILE="./postman_script/environment.json"

# Delay in milliseconds
DELAY=5

# Run the add-jobseekers script 50 times using --iteration-count
echo "Running add-jobseekers script for $JOBSEEKER_ITERATIONS iterations..."
newman run "$SAGA_SCRIPT" -e "$ENVIRONMENT_FILE" --iteration-count 1 --delay-request "$DELAY"
