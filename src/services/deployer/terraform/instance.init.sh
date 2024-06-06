#!/bin/bash

PROJECT_LINK=${project_link}
DIR_NAME=codebase

# Update software repositories
sudo apt update -y && apt upgrade -y

# Install Docker
sudo apt install ca-certificates curl unzip -y
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update -y

sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

# Download the code and extract the files
mkdir $DIR_NAME
sudo curl -o $DIR_NAME.zip $PROJECT_LINK
sudo unzip $DIR_NAME.zip -d $DIR_NAME
echo "Code downloaded successfully"

# Run the project
cd $DIR_NAME
sudo docker compose -f deployer-compose.yml up -d
echo "Services are up & running"
