# ----------------------------------------------------------
# Local Variables - Aliases for AWS Regions
# ----------------------------------------------------------
locals {
  region_alias = {
    "us-east-1" = "use1"
    "us-east-2" = "use2"
    "us-west-1" = "usw1"
    "us-west-2" = "usw2"
  }
}

# ----------------------------------------------------------
# ECR Repository for the application
# ----------------------------------------------------------
resource "aws_ecr_repository" "app_repo" {
  name = join("-", [local.region_alias[var.aws_region], "backend-app", var.environment])

  image_scanning_configuration {
    scan_on_push = true
  }
}

# ----------------------------------------------------------
# Data Sources for VPC and Subnets
# ----------------------------------------------------------
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {}

# ----------------------------------------------------------
# Security Group for the ALB - Allow inbound traffic on port 80
# ----------------------------------------------------------
resource "aws_security_group" "alb_sg" {
  name        = join("-", [local.region_alias[var.aws_region], "alb-sg", var.environment])
  description = "Allow HTTP traffic on port 80"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "Allow HTTP traffic"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ----------------------------------------------------------
# Security Group for ECS - Allow inbound traffic on port 8080
# ----------------------------------------------------------
resource "aws_security_group" "ecs_sg" {
  name        = join("-", [local.region_alias[var.aws_region], "ecs-sg", var.environment])
  description = "Allow TCP traffic on port 8080 from any IP"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "Allow TCP traffic on port 8080 from any IP"
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ----------------------------------------------------------
# Application Load Balancer (ALB)
# ----------------------------------------------------------
resource "aws_lb" "app_alb" {
  name               = join("-", [local.region_alias[var.aws_region], "app-alb", var.environment])
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = data.aws_subnets.default.ids
}

# ----------------------------------------------------------
# Target Group for ALB
# ----------------------------------------------------------
resource "aws_lb_target_group" "app_tg" {
  name         = join("-", [local.region_alias[var.aws_region], "app-tg", var.environment])
  port         = 8080
  protocol     = "HTTP"
  vpc_id       = data.aws_vpc.default.id
  target_type  = "ip"
}

# ----------------------------------------------------------
# ALB Listener
# ----------------------------------------------------------
resource "aws_lb_listener" "http_listener" {
  load_balancer_arn = aws_lb.app_alb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app_tg.arn
  }
}

# ----------------------------------------------------------
# ECS Cluster
# ----------------------------------------------------------
resource "aws_ecs_cluster" "app_cluster" {
  name = join("-", [local.region_alias[var.aws_region], "app-cluster", var.environment])
}

# ----------------------------------------------------------
# IAM Role for ECS Task Execution
# ----------------------------------------------------------
resource "aws_iam_role" "ecs_task_execution_role" {
  name = join("-", [local.region_alias[var.aws_region], "ecs-task-execution-role", var.environment])

  assume_role_policy = <<EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Service": "ecs-tasks.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  }
  EOF
}

resource "aws_iam_policy" "ecr_pull_policy" {
  name = join("-", [local.region_alias[var.aws_region], "ecr-pull-policy", var.environment])
  description = "Allows ECS tasks to pull images from ECR"

  policy = <<EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "ecr:GetAuthorizationToken",
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage"
        ],
        "Resource": "*"
      }
    ]
  }
  EOF
}

resource "aws_iam_policy_attachment" "ecs_task_execution_role_policy" {
  name       = join("-", [local.region_alias[var.aws_region], "ecs-task-execution-role-policy", var.environment])
  roles      = [aws_iam_role.ecs_task_execution_role.name]
  policy_arn = aws_iam_policy.ecr_pull_policy.arn
}

# ----------------------------------------------------------
# ECS Task Definition
# ----------------------------------------------------------
resource "aws_ecs_task_definition" "app_task" {
  family                   = join("-", [local.region_alias[var.aws_region], "app-task", var.environment])
  container_definitions    = <<DEFINITION
  [
    {
      "name": "app",
      "image": "${aws_ecr_repository.app_repo.repository_url}:latest",
      "memory": 512,
      "cpu": 256,
      "essential": true,
      "portMappings": [
        {
          "containerPort": 8080,
          "hostPort": 8080
        }
      ]
    }
  ]
  DEFINITION
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  memory                   = "1024"
  cpu                      = "512"
}

# ----------------------------------------------------------
# ECS Service
# ----------------------------------------------------------
resource "aws_ecs_service" "app_service" {
  name            = join("-", [local.region_alias[var.aws_region], "app-service", var.environment])
  cluster         = aws_ecs_cluster.app_cluster.id
  task_definition = aws_ecs_task_definition.app_task.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = data.aws_subnets.default.ids
    security_groups = [aws_security_group.ecs_sg.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app_tg.arn
    container_name   = "app"
    container_port   = 8080
  }
}
