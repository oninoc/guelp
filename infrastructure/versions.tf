terraform {
  required_version = ">=1.13.2"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">=6.14.1"
    }
  }

  # Backend set via -backend-config backend/*.backend.hcl
  backend "s3" {}
}
