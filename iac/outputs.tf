output "repository_url" {
  description = "ECR Url"
  value       = aws_ecr_repository.app_repo.repository_url
}

output "task_definition_arn" {
  description = "ARN task definition"
  value       = aws_ecs_task_definition.app_task.arn
}

output "service_name" {
  description = "ECS name service"
  value       = aws_ecs_service.app_service.name
}
