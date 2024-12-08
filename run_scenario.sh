#!/bin/bash

# Path to your JSON files
JOBSEEKER_SCRIPT="./postman_script/add-jobseekers.json"
RECRUITER_SCRIPT="./postman_script/add-recruiters-and-create-jobs.json"
ENVIRONMENT_FILE="./postman_script/environment.json"

# Number of iterations
JOBSEEKER_ITERATIONS=50
RECRUITER_ITERATIONS=30

# Delay in milliseconds
DELAY=5

# Run the add-jobseekers script 50 times using --iteration-count
echo "Running add-jobseekers script for $JOBSEEKER_ITERATIONS iterations..."
newman run "$JOBSEEKER_SCRIPT" -e "$ENVIRONMENT_FILE" --iteration-count "$JOBSEEKER_ITERATIONS" --delay-request "$DELAY"

# Run the add-recruiters-and-create-jobs script 30 times using --iteration-count
echo "Running add-recruiters-and-create-jobs script for $RECRUITER_ITERATIONS iterations..."
newman run "$RECRUITER_SCRIPT" -e "$ENVIRONMENT_FILE" --iteration-count "$RECRUITER_ITERATIONS" --delay-request "$DELAY"

echo "All iterations completed."
