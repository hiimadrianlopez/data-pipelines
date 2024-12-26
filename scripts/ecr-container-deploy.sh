#!/bin/bash

ENV=$1
AWS_ACCOUNT_ID=$2
AWS_REGION=$3
COMMIT_HASH=$4

generate_region_alias() {
    local region=$1
    local first=$(echo $region | cut -d'-' -f1)
    local second=$(echo $region | cut -d'-' -f2 | head -c 1)
    local third=$(echo $region | cut -d'-' -f3)
    echo "${first}${second}${third}"
}

REGION_ALIAS=$(generate_region_alias $AWS_REGION)

export APP_NAME="${REGION_ALIAS}-backend-app-${ENV}"

COMMIT_HASH=$(git rev-parse --short HEAD)

docker build -t $APP_NAME:$COMMIT_HASH .

docker tag $APP_NAME:$COMMIT_HASH $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$APP_NAME:$COMMIT_HASH

aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

docker tag $APP_NAME:$COMMIT_HASH $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$APP_NAME:$COMMIT_HASH
docker tag $APP_NAME:$COMMIT_HASH $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$APP_NAME:latest

docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$APP_NAME:$COMMIT_HASH
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$APP_NAME:latest
