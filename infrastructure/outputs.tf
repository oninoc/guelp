output "app_runner_service_url" {
  value = module.shared.app_runner_service_url
}

output "rds_endpoint" {
  value = module.shared.rds_endpoint
}

output "s3_bucket_name" {
  value = module.shared.s3_bucket_name
}

output "s3_bucket_arn" {
  value = module.shared.s3_bucket_arn
}

output "secretsmanager_secret_arn" {
  value = module.shared.secretsmanager_secret_arn
}

output "vpc_id" {
  value = module.shared.vpc_id
}

output "vpc_cidr_block" {
  value = module.shared.vpc_cidr_block
}

output "public_subnet_ids" {
  value = module.shared.public_subnet_ids
}

output "ecs_tasks_security_group_id" {
  description = "The security group ID for ECS tasks"
  value       = module.shared.ecs_tasks_security_group_id
}