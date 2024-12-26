variable "aws_region" {
  description = "AWS Region"
  type        = string
  default     = "us-west-2"
}

variable "environment" {
  description = "Environment"
  type        = string
  default     = "prod"
}

variable "repository_name" {
  description = "Repository name in ECR"
  type        = string
  default     = ""
}

variable "image_tag" {
  description = "Docker image tag"
  type        = string
  default     = "latest"
}

variable "commit_hash" {
  description = "Commit hash to be used for the Docker image tag"
  type        = string
  default     = "latest"
}
