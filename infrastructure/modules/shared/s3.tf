resource "aws_s3_bucket" "bucket" {
  bucket        = "${var.project_name}-bucket"
  force_destroy = false

  tags = {
    Name = "${var.project_name}-bucket"
  }
}

resource "aws_s3_bucket_cors_configuration" "bucket" {
  bucket = aws_s3_bucket.bucket.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["PUT", "POST", "GET", "DELETE"]
    allowed_origins = ["*"]
    max_age_seconds = 3000
  }
}

resource "aws_s3_bucket_public_access_block" "bucket" {
  bucket = aws_s3_bucket.bucket.id

  block_public_acls       = true
  block_public_policy     = true # Allow bucket policy to be set
  ignore_public_acls      = true
  restrict_public_buckets = true
}
