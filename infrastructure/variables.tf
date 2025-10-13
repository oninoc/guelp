variable "aws_region" {
  description = "AWS region to deploy into."
  type        = string
}

variable "project_name" {
  description = "Main project name for shared infrastructure"
  type        = string
}

variable "rds_engine_version" {
  description = "RDS engine version"
  type        = string
  default     = "16.5"
}

variable "rds_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.medium"
}

variable "rds_database_name" {
  description = "RDS database name"
  type        = string
}

variable "rds_username" {
  description = "RDS username"
  type        = string
}

variable "apprunner_cpu" {
  description = "App Runner CPU"
  type        = number
}

variable "apprunner_memory" {
  description = "App Runner memory"
  type        = number
}

variable "base_ecs_migration_task_cpu" {
  description = "Base ECS migration task CPU"
  type        = number
}

variable "base_ecs_migration_task_memory" {
  description = "Base ECS migration task memory"
  type        = number
}