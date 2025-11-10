# App Runner VPC Connector
resource "aws_apprunner_vpc_connector" "vpc_connector" {
  vpc_connector_name = "${var.project_name}-app-runner-vpc"
  security_groups    = [aws_security_group.app_runner.id]
  subnets            = aws_subnet.postgres[*].id

  tags = {
    Name = "${var.project_name}-app-runner-vpc"
  }
}

# Security Group for App Runner
resource "aws_security_group" "app_runner" {
  name        = "${var.project_name}-app-runner-sg"
  description = "Security group for App Runner service"
  vpc_id      = aws_vpc.main.id

  # Allow general outbound internet access through NAT Gateway
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-app-runner-sg"
  }
}

# App Runner Service
resource "aws_apprunner_service" "app_runner" {
  service_name = "${var.project_name}-app-runner"

  source_configuration {
    image_repository {
      image_configuration {
        port = "80"
        runtime_environment_variables = {
          "ENVIRONMENT"                 = "prod"
          "AWS_REGION"                  = var.aws_region
          "AWS_FILE_BUCKET_NAME"        = aws_s3_bucket.bucket.id
        }
        runtime_environment_secrets = {
          "POSTGRES_URL" = "${aws_secretsmanager_secret.db_connection.arn}:connection_string::"
        }
      }
      image_identifier      = "${aws_ecr_repository.ecr_base_server.repository_url}:latest"
      image_repository_type = "ECR"
    }
    authentication_configuration {
      access_role_arn = aws_iam_role.service_role.arn
    }
    auto_deployments_enabled = true
  }

  network_configuration {
    egress_configuration {
      egress_type       = "VPC"
      vpc_connector_arn = aws_apprunner_vpc_connector.vpc_connector.arn
    }
  }

  health_check_configuration {
    protocol            = "HTTP"
    path                = "/health"
    interval            = 5
    timeout             = 2
    healthy_threshold   = 1
    unhealthy_threshold = 5
  }

  instance_configuration {
    instance_role_arn = aws_iam_role.service_role.arn
    cpu               = var.apprunner_cpu
    memory            = var.apprunner_memory
  }

  depends_on = [
    aws_db_instance.postgres
  ]

  tags = {
    Name = "${var.project_name}-app-runner"
  }
}
