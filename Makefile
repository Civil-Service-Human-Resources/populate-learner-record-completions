docker := docker compose exec app

setup:
	docker compose up -d --build
	make config

config:
	$(docker) python setup_prod_config.py

container:
	$(docker) bash 

save-data:
	$(docker) python save_data.py

save-data-replace:
	$(docker) python save_data.py --replace

down:
	docker compose down

plan:
	$(docker) python plan.py

apply:
	$(docker) python apply.py
	
analytics.byMonth:
	$(docker) python -m analytics.byMonth

analytics.byCourse:
	$(docker) python -m analytics.byCourse