run: build up

build:
	docker compose build --no-cache

up:
	docker compose up

down:
	docker compose down -v

migrate:
	@docker compose up -d --wait db
	@docker compose build migration
	@docker compose run --rm migration

create-migrations:
	@docker compose up -d --wait db
	@docker compose run --rm create-migrations

add-migration:
	@docker compose exec backend bash -c "uv run alembic revision --autogenerate -m '${name}'"

reset-db:
	@echo "Stopping and removing existing containers and volumes..."
	@docker compose down -v
	@echo "Starting database container..."
	@docker compose up -d --wait db
	@echo "Rebuilding migration image..."
	@docker compose build migration
	@echo "Applying migrations from scratch..."
	@docker compose run --rm migration