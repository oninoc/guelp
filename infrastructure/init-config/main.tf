###################################
# Terraform Init - Bootstrap State Backend
# This module creates the S3 bucket and DynamoDB table
# needed for Terraform state backend storage.
# Note: This module does NOT use a backend itself (local state initially)
###################################

terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # No backend block here - we're creating the backend resources!
  # After running this init, configure the main terraform backend
  # using the outputs from this module
}

