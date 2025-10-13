variable "aws_region" {
  description = "AWS region to deploy infrastructure into."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Main project name for shared infrastructure"
  type        = string
  default     = "project"
}
