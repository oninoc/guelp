resource "random_id" "secret_suffix" {
  byte_length = 4
}

resource "aws_secretsmanager_secret" "db_connection" {
  name        = "${var.project_name}-db-connection-secret-${random_id.secret_suffix.hex}"
  description = "Database connection string for ${var.project_name}"

  tags = {
    Name = "${var.project_name}-db-connection-secret-${random_id.secret_suffix.hex}"
  }
}

resource "aws_secretsmanager_secret_version" "db_connection" {
  secret_id = aws_secretsmanager_secret.db_connection.id
  secret_string = jsonencode({
    connection_string = "postgresql://${var.rds_username}:${random_password.db_password.result}@${aws_rds_cluster.postgres.endpoint}:5432/${var.rds_database_name}"
    host              = aws_rds_cluster.postgres.endpoint
    port              = aws_rds_cluster.postgres.port
    database          = var.rds_database_name
    username          = var.rds_username
    password          = random_password.db_password.result
  })
}
