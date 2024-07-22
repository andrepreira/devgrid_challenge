include ./app/.env
export $(shell sed 's/=.*//' ./app/.env)

OS        = linux
ARCH      = amd64
APPNAME   = devgrid-challenge-api
VERSION   = 0.1.0
DB_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
MIGRATION_MESSAGE=Initial migration

.PHONY: tests

log: 
	docker-compose -f logger.yaml build
	docker-compose -f logger.yaml up -d

build:
	docker-compose --env-file ./app/.env build 
	docker-compose --env-file ./app/.env up -d
	pipenv run alembic revision --autogenerate -m "$(MIGRATION_MESSAGE)"
	pipenv run alembic upgrade head

start:
	docker-compose --env-file ./app/.env up -d

tests:
	docker-compose run test -d --rm
	@export PIPENV_DONT_LOAD_ENV=1 ; \
	pipenv run pytest -vv --cov=app --asyncio-mode=auto tests/

setup: 
	pip install --upgrade pip
	pip install pipenv
	pipenv install --dev
	pipenv shell

fmt: 
	export PIPENV_DONT_LOAD_ENV=1 ; \
	pipenv run isort app/ tests/ ; \
	pipenv run black app/ tests/

init-db:
	pipenv run alembic init alembic
	@sed -i 's|^sqlalchemy.url.*|sqlalchemy.url = $(DB_URL)|' alembic.ini
	@echo "Alembic initialized with database URL: $(DB_URL)"

migrate:
	pipenv run alembic revision --autogenerate -m "$(MIGRATION_MESSAGE)"
	@echo "Migration script created with message: $(MIGRATION_MESSAGE)"

upgrade:
	pipenv run alembic upgrade head
	@echo "Database upgraded to latest migration"

rm-env:
	docker-compose down
	docker volume rm devgrid_challenge_postgres_data
	@rm alembic/versions/*.py