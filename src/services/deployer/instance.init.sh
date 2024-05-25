#!/bin/bash

PROJECT_PATH=${arg1}
PROJECT_NAME=${arg2}

# Update software repositories
sudo apt update -y && apt upgrade -y

# Install Docker
sudo apt install ca-certificates curl -y
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update -y

sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

# Copy the codebase
sudo mkdir $PROJECT_NAME
sudo cp -r $PROJECT_PATH $PROJECT_NAME

# Run the project
cd $PROJECT_NAME
docker compose up -d
docker run --name proxy -d -p 8000:8000 \
		-v ./nginx.conf \
		--network shared-network nginx:1.25.4-alpine