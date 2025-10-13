# ECS Cluster
resource "aws_ecs_cluster" "ecs-cluster" {
  name = "${var.project_name}-ecs-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = {
    Name = "${var.project_name}-ecs-cluster"
  }
}

# Security Group for ECS Tasks
resource "aws_security_group" "ecs_tasks" {
  name        = "${var.project_name}-ecs-tasks-sg"
  description = "Security group for ECS tasks"
  vpc_id      = aws_vpc.main.id

  # Allow outbound HTTPS for VPC endpoints (Secrets Manager, ECR, CloudWatch)
  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.main.cidr_block]
    description = "HTTPS to VPC endpoints"
  }

  # Allow all outbound (covers PostgreSQL to RDS and other services)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound"
  }

  tags = {
    Name = "${var.project_name}-ecs-tasks-sg"
  }
}

# ECS Task Definition for Migration
resource "aws_ecs_task_definition" "migration" {
  family                   = "${var.project_name}-migration-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.base_ecs_migration_task_cpu
  memory                   = var.base_ecs_migration_task_memory
  execution_role_arn       = aws_iam_role.service_role.arn
  task_role_arn            = aws_iam_role.service_role.arn

  container_definitions = jsonencode([
    {
      name  = "migration"
      image = "${aws_ecr_repository.ecr_base_migrations.repository_url}:latest"

      secrets = [
        {
          name      = "POSTGRES_URL"
          valueFrom = "${aws_secretsmanager_secret.db_connection.arn}:connection_string::"
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.migration.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
    }
  ])

  tags = {
    Name = "${var.project_name}-migration-task"
  }
}

# CloudWatch Log Group for Migration
resource "aws_cloudwatch_log_group" "migration" {
  name              = "/ecs/${var.project_name}-migration"
  retention_in_days = 7

  tags = {
    Name = "${var.project_name}-migration-logs"
  }
}
