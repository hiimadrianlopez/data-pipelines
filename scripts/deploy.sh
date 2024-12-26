#!/bin/bash

set -xe

export ENV=${ENV}
export AWS_ACCOUNT_ID=${AWS_ACCOUNT_ID}
export AWS_REGION=${AWS_REGION}
export COMMIT_HASH=${COMMIT_HASH}

cd iac
terraform init
terraform apply -var="aws_region=$AWS_REGION" -var="environment=$ENV"  -var="commit_hash=$COMMIT_HASH" -auto-approve

cd ..
bash ./scripts/ecr-container-deploy.sh $ENV $AWS_ACCOUNT_ID $AWS_REGION $COMMIT_HASH
