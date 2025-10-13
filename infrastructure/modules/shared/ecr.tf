resource "aws_ecr_repository" "ecr_base_server" {
  name                 = "${var.project_name}-base-server"
  image_tag_mutability = "MUTABLE"
}

resource "aws_ecr_repository" "ecr_base_migrations" {
  name                 = "${var.project_name}-base-migrations"
  image_tag_mutability = "MUTABLE"
}
