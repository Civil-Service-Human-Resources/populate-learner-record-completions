docker := docker compose exec app

## Setup
setup:
	docker compose up -d --build

## Environment

env-set-local:
	ENVIRONMENT="LOCAL" make setup

env-set-prod:
	ENVIRONMENT="PROD" make setup

env-check:
	$(docker) env | grep ENVIRONMENT

# Config

config:
	$(docker) python -m actions.setup_prod_config

# Container

container:
	$(docker) bash 

down:
	docker compose down

# Actions

save-data:
	$(docker) python -m actions.save_data

save-data-replace:
	$(docker) python -m actions.save_data --replace

plan:
	$(docker) python -m actions.plan

apply:
	$(docker) python -m actions.apply

revert:
	$(docker) python -m actions.revert

# Logs

logs:
	tail -f logs/debug.log

# Analytics
	
analytics.byMonth:
	$(docker) python -m analytics.byMonth

analytics.byCourse:
	$(docker) python -m analytics.byCourse

analytics.html:
	$(docker) python -m analytics.htmlReport