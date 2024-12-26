AWS_ACCOUNT_ID ?= 123456789012
AWS_REGION ?= us-east-1
ENV ?= dev

COMMIT_HASH := $(shell git rev-parse --short HEAD)

format:
	@black .
	@isort src/**/*.py --quiet --apply
	@autoflake --recursive --exclude venv,.venv --in-place --expand-star-imports --remove-all-unused-imports --remove-unused-variables --quiet src/

start:
	@docker compose up -d

rebuild:
	@docker compose up --build

deploy:
	@echo "🚀 Deploying environment $(ENV)..."
	@ENV=$(ENV) AWS_ACCOUNT_ID=$(AWS_ACCOUNT_ID) AWS_REGION=$(AWS_REGION) COMMIT_HASH=$(COMMIT_HASH) bash ./scripts/deploy.sh

destroy:
	@echo "🔥 Destroying environment $(ENV)..."
	@ENV=$(ENV) AWS_ACCOUNT_ID=$(AWS_ACCOUNT_ID) AWS_REGION=$(AWS_REGION) bash ./scripts/destroy.sh

clean:
	docker rmi backend-$(ENV) || true
	docker rmi $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/platform/backend-$(ENV) || true
