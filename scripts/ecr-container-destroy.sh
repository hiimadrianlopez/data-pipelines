#!/bin/bash

ENV=$1
AWS_ACCOUNT_ID=$2
AWS_REGION=$3

generate_region_alias() {
    local region=$1
    local first=$(echo $region | cut -d'-' -f1)
    local second=$(echo $region | cut -d'-' -f2 | head -c 1)
    local third=$(echo $region | cut -d'-' -f3)
    echo "${first}${second}${third}"
}

REGION_ALIAS=$(generate_region_alias $AWS_REGION)
export APP_NAME="${REGION_ALIAS}-backend-app-${ENV}"

if aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com > /dev/null 2>&1; then
    echo "Login successful."
else
    echo "Failed to login to ECR."
    exit 1
fi

IMAGES=$(aws ecr list-images --repository-name $APP_NAME --query 'imageIds[*]' --region $AWS_REGION --output json 2>/dev/null)

if [ $? -ne 0 ]; then
    echo "No repositories have been created yet."
    exit 0
fi

if [ "$IMAGES" != "[]" ]; then
    IMAGE_IDS=$(echo $IMAGES | jq -c '.[]')

    for IMAGE_ID in $IMAGE_IDS; do
        if aws ecr batch-delete-image --repository-name $APP_NAME --image-ids "$IMAGE_ID" --region $AWS_REGION > /dev/null 2>&1; then
            echo "Deleted image: $IMAGE_ID"
        else
            echo "Failed to delete image: $IMAGE_ID"
        fi
    done
else
    echo "No images to destroy."
fi
