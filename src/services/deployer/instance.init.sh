#!/bin/bash

CODEBASE_URL=$1
DIR_NAME=codebase

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

# Download and extract codebase files
mkdir $DIR_NAME
curl -o $DIR_NAME.zip $CODEBASE_URL
unzip $DIR_NAME.zip -d $DIR_NAME
echo "Codebase downloaded successfully"

# Run the project
cd $DIR_NAME
docker-compose -f deployer-compose.yml up -d
echo "Services are up & running"
