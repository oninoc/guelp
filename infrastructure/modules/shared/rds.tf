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
  count                   = 2
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
}

# Aurora RDS Cluster
resource "aws_rds_cluster" "postgres" {
  cluster_identifier              = "${var.project_name}-postgres-cluster"
  engine                          = "postgres"
  engine_version                  = var.rds_engine_version
  master_username                 = var.rds_username
  master_password                 = random_password.db_password.result
  database_name                   = var.rds_database_name
  db_subnet_group_name            = aws_db_subnet_group.postgres.name
  vpc_security_group_ids          = [aws_security_group.postgres.id]
  skip_final_snapshot             = true

  tags = {
    Name = "${var.project_name}-postgres-cluster"
  }
}

# Aurora RDS Instance
resource "aws_rds_cluster_instance" "postgres" {
    identifier         = "${var.project_name}-postgres-instance"
  cluster_identifier = aws_rds_cluster.postgres.id
  instance_class     = var.rds_instance_class
  engine             = aws_rds_cluster.postgres.engine

  tags = {
    Name = "${var.project_name}-postgres-instance"
  }
}
