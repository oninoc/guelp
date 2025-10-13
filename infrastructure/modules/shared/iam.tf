# App Runner Service Role
resource "aws_iam_role" "service_role" {
  name = "${var.project_name}-app-runner-service-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "build.apprunner.amazonaws.com"
        }
      },
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "tasks.apprunner.amazonaws.com"
        }
      },
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name = "${var.project_name}-app-runner-service-role"
  }
}

# App Runner & ECS Task Service Policy with least privilege for VPC and RDS access
resource "aws_iam_policy" "service_policy" {
  name = "${var.project_name}-app-runner-service-policy"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      # Secrets Manager Access
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret"
        ]
        Resource = [
          aws_secretsmanager_secret.db_connection.arn,
        ]
      },
      # ECR Authorization (account-level, no resource restriction)
      {
        Effect = "Allow"
        Action = [
          "ecr:GetAuthorizationToken"
        ]
        Resource = "*"
      },
      # ECR Repository Access
      {
        Effect = "Allow"
        Action = [
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:DescribeImages",
          "ecr:DescribeRepositories",
          "ecr:ListImages"
        ]
        Resource = [
          aws_ecr_repository.ecr_base_migrations.arn,
          aws_ecr_repository.ecr_base_server.arn,
        ]
      },
      # ECS Operations
      {
        Effect = "Allow"
        Action = [
          "ecs:RunTask",
          "ecs:StopTask",
          "ecs:DescribeTasks",
          "ecs:ListTasks",
          "ecs:DescribeTaskDefinition",
          "ecs:DescribeClusters",
          "ecs:ListClusters"
        ]
        Resource = [
          aws_ecs_cluster.ecs-cluster.arn,
        ]
      },
      # CloudWatch Logs
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "logs:DescribeLogStreams"
        ]
        Resource = [
          "*"
        ]
      },
    ]
  })
}

# Attach Policy to Service Role
resource "aws_iam_role_policy_attachment" "service_policy_attachment" {
  role       = aws_iam_role.service_role.name
  policy_arn = aws_iam_policy.service_policy.arn
}