# Security Group for Aurora RDS
resource "aws_security_group" "postgres" {
  name_prefix = "${var.project_name}-postgres-sg"
  vpc_id      = aws_vpc.main.id

  # Allow PostgreSQL traffic from within the VPC
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.main.cidr_block]
    description = "PostgreSQL access from VPC"
  }

  # Allow App Runner and additional services to access Aurora database
  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app_runner.id]
    description     = "Allow App Runner and additional services to access Aurora database"
  }

  # Allow ECS tasks to access Aurora database
  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs_tasks.id]
    description     = "Allow ECS tasks to access Aurora database"
  }

  # No egress rules - database cannot make outbound connections
  # This prevents the database from accessing external services

  tags = {
    Name = "${var.project_name}-postgres-group"
  }
}

# Aurora Subnet for Aurora RDS
resource "aws_subnet" "postgres" {
  count                   = 3
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.${count.index + 1}.0/24"
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = false

  tags = {
    Name = "${var.project_name}-postgres-subnet-${count.index + 1}"
  } 
}

# DB Subnet Group for Aurora
resource "aws_db_subnet_group" "postgres" {
  name       = "${var.project_name}-postgres-subnet-group"
  subnet_ids = aws_subnet.postgres[*].id

  tags = {
    Name = "${var.project_name}-postgres-subnet-group"
  }
}

# Random password resource (kept for state compatibility, not used)
resource "random_password" "db_password" {
  length  = 10
  special = true
  upper   = true
  lower   = true
  numeric = true
  override_special = "!#$%^&*()-_=+[]{}<>?"
}

# Aurora RDS Cluster
# PostgreSQL RDS Instance
resource "aws_db_instance" "postgres" {
  identifier                 = "${var.project_name}-postgres"
  engine                     = "postgres"
  engine_version             = var.rds_engine_version
  instance_class             = var.rds_instance_class
  allocated_storage          = 20
  db_name                    = var.rds_database_name
  username                   = var.rds_username
  password                   = random_password.db_password.result
  db_subnet_group_name       = aws_db_subnet_group.postgres.name
  vpc_security_group_ids     = [aws_security_group.postgres.id]
  multi_az                   = false
  publicly_accessible        = false
  storage_encrypted          = true
  skip_final_snapshot        = true
  auto_minor_version_upgrade = true

  tags = {
    Name = "${var.project_name}-postgres"
  }
}
