# Shared Infrastructure Module
module "shared" {
  source = "./modules/shared"

  # Basic configuration
  project_name = var.project_name
  aws_region   = var.aws_region

  # Secrets and configuration
  rds_engine_version = var.rds_engine_version
  rds_instance_class = var.rds_instance_class
  rds_database_name  = var.rds_database_name
  rds_username = var.rds_username


  apprunner_cpu    = var.apprunner_cpu
  apprunner_memory = var.apprunner_memory

  base_ecs_migration_task_cpu = var.base_ecs_migration_task_cpu
  base_ecs_migration_task_memory = var.base_ecs_migration_task_memory
}
