#!/bin/bash

# Copy everything from /data to the current working directory
cp -r /data/* .

# If exist ./setup.sh, run it
if [ -f "./setup.sh" ]; then
    chmod +x ./setup.sh
    ./setup.sh
fi

# Run python3 autograder.py with all passed arguments
python3 autograder.py "$@"
