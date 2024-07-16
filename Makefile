OS        = linux
ARCH      = amd64
APPNAME   = devgrid-challenge-api
VERSION   = 0.1.0

.PHONY: tests

log: ## show logs
	docker-compose -f logger.yaml build
	docker-compose -f logger.yaml up -d
build: ## build app
	docker-compose --env-file ./app/.env build 
	docker-compose --env-file ./app/.env up -d
start: ## start app
	docker-compose --env-file ./app/.env up -d

tests: ## run all tests
	@export PIPENV_DONT_LOAD_ENV=1 ; \
	export API_KEY="abs" ; \
	pipenv run pytest -vv

setup: ## Configure the python environment installing and using pipenv
	pip install --upgrade pip
	pip install pipenv
	pipenv install --dev

fmt: ## format code using isort and black
	export PIPENV_DONT_LOAD_ENV=1 ; \
	pipenv run isort app/ tests/ ; \
	pipenv run black app/ tests/