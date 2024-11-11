# Use an official Python runtime as a parent image
FROM ubuntu:24.04

ARG DEBIAN_FRONTEND=noninteractive

# Install packages
RUN apt-get update
RUN apt-get install -y build-essential git gnupg2
RUN apt-get install -y curl wget
RUN apt-get install -y python3 python3-pip python3-requests
RUN apt-get install -y zsh nano vim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY autograder.py tasks.py criterias.py docker-entrypoint.sh /app/

# Set DATA directory
ENV LIMBO=/data

# Run autograder.py when the container launches
ENTRYPOINT ["/bin/bash", "docker-entrypoint.sh"]
