#!/bin/bash

PROJECT_NAME=$1
PROJECT_LINK=$2
INSTANCE_OUTPUT_FILENAME=$3

cd terraform/

# Terraform Init
terraform init

# Terraform Apply
terraform apply -var="project_name=$PROJECT_NAME" -var="project_link=$PROJECT_LINK" -auto-approve

# Save instance public IPv4 dns
terraform output -json > $INSTANCE_OUTPUT_FILENAME

# Remove the terraform state data, To avoid conflict
rm -r .terraform*
rm terraform*