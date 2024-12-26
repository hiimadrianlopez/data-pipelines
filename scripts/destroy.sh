#!/bin/bash

set -xe

export ENV=${ENV}
export AWS_ACCOUNT_ID=${AWS_ACCOUNT_ID}
export AWS_REGION=${AWS_REGION}

bash ./scripts/ecr-container-destroy.sh $ENV $AWS_ACCOUNT_ID $AWS_REGION

cd iac
terraform init
terraform destroy -var="aws_region=$AWS_REGION" -var="environment=$ENV" -auto-approve
