#!/bin/bash

INSTANCE_TYPE=$1
PROJECT_NAME=$2
PROJECT_LINK=$3
INSTANCE_OUTPUT_FILENAME=$4

cd terraform/

# Terraform Init
terraform init

# Terraform Apply
terraform apply  -var="instance_type=$INSTANCE_TYPE" -var="project_name=$PROJECT_NAME" -var="project_link=$PROJECT_LINK" -auto-approve

# Save instance public IPv4 dns
terraform output -json > $INSTANCE_OUTPUT_FILENAME

# Remove the terraform state data, To avoid conflict
rm -r .terraform*
rm terraform*