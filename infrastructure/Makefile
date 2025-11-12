init:
	terraform init -backend-config=backend/prod.backend.hcl -reconfigure

plan-ecr:
	terraform plan -var-file=environments/prod/terraform.tfvars -target=module.shared.aws_ecr_repository.ecr_base_server -target=module.shared.aws_ecr_repository.ecr_base_migrations

plan:
	terraform plan -var-file=environments/prod/terraform.tfvars

apply:
	terraform apply -var-file=environments/prod/terraform.tfvars

apply-ecr:
	terraform apply -var-file=environments/prod/terraform.tfvars -target=module.shared.aws_ecr_repository.ecr_base_server -target=module.shared.aws_ecr_repository.ecr_base_migrations

destroy:
	terraform destroy -var-file=environments/prod/terraform.tfvars

unlock:
	@echo "Usage: make unlock LOCK_ID=<lock-id>"
	@if [ -z "$(LOCK_ID)" ]; then \
		echo "Error: LOCK_ID is required. Example: make unlock LOCK_ID=3ef04e75-af2b-ede9-2874-b4ca46e9f14d"; \
		exit 1; \
	fi
	terraform force-unlock -force $(LOCK_ID)

# RDS Management
plan-rds:
	terraform plan -var-file=environments/prod/terraform.tfvars -target=module.shared.aws_db_instance.postgres

destroy-rds:
	@echo "⚠️  WARNING: This will destroy the RDS instance and all its data!"
	@read -p "Are you sure? Type 'yes' to continue: " confirm && [ "$$confirm" = "yes" ] || exit 1
	terraform destroy -var-file=environments/prod/terraform.tfvars -target=module.shared.aws_db_instance.postgres

recreate-rds: destroy-rds
	@echo "Recreating RDS instance..."
	terraform apply -var-file=environments/prod/terraform.tfvars -target=module.shared.aws_db_instance.postgres

reset-rds:
	@echo "⚠️  WARNING: This will force recreation of the RDS instance (destroy + create)!"
	@echo "⚠️  All data will be lost!"
	@read -p "Are you sure? Type 'yes' to continue: " confirm && [ "$$confirm" = "yes" ] || exit 1
	@echo "Forcing recreation of RDS instance..."
	terraform apply -var-file=environments/prod/terraform.tfvars -target=module.shared.aws_db_instance.postgres -replace=module.shared.aws_db_instance.postgres