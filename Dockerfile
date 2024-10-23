# Use an official Python runtime as a parent image
FROM ubuntu:24.04

# Install python3
RUN apt-get update && apt-get install -y make gcc git python3 python3-pip python3-requests

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY autograder.py tasks.py criterias.py docker-entrypoint.sh /app/

# Run autograder.py when the container launches
ENTRYPOINT ["/bin/bash", "docker-entrypoint.sh"]
