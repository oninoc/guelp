run: build up

build:
	docker compose build

up:
	docker compose up

down:
	docker compose down -v

migrate:
	@docker compose up -d --wait db
	@docker compose build migrations
	@docker compose run --rm migrations

create-migrations:
	@docker compose up -d --wait db
	@docker compose run --rm create-migrations