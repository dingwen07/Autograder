#!/bin/bash

# Copy everything from /data to the current working directory
cp -r /data/* .

# Run python3 autograder.py with all passed arguments
python3 autograder.py "$@"
