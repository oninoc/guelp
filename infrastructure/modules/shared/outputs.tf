output "ecr_base_server_repository_url" {
  description = "The URL of the base server ECR repository"
  value       = aws_ecr_repository.ecr_base_server.repository_url
}

output "ecr_base_migrations_repository_url" {
  description = "The URL of the base migrations ECR repository"
  value       = aws_ecr_repository.ecr_base_migrations.repository_url
}

output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.main.id
}

output "vpc_cidr_block" {
  description = "The CIDR block of the VPC"
  value       = aws_vpc.main.cidr_block
}

output "public_subnet_ids" {
  description = "The IDs of the public subnets"
  value       = aws_subnet.public[*].id
}

output "postgres_subnet_ids" {
  description = "The IDs of the postgres subnets (private subnets for RDS)"
  value       = aws_subnet.postgres[*].id
}

output "rds_endpoint" {
  description = "The endpoint of the RDS cluster"
  value       = aws_db_instance.postgres.address
}

output "s3_bucket_name" {
  description = "The name of the S3 bucket"
  value       = aws_s3_bucket.bucket.id
}

output "s3_bucket_arn" {
  description = "The ARN of the S3 bucket"
  value       = aws_s3_bucket.bucket.arn
}

output "secretsmanager_secret_arn" {
  description = "The ARN of the Secrets Manager secret"
  value       = aws_secretsmanager_secret.db_connection.arn
}

output "app_runner_service_url" {
  description = "The URL of the App Runner service"
  value       = aws_apprunner_service.app_runner.service_url
}

output "ecs_tasks_security_group_id" {
  description = "The security group ID for ECS tasks"
  value       = aws_security_group.ecs_tasks.id
}