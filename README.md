# Script to populate learner record completions

## Requirements

* Docker

## Setup

Run this command to setup your environment:

```sh
docker compose up -d --build
docker compose exec app python setup_prod_config.py
```

This will build and run the Docker containers and will also walk you through creating the configuration file (`config.json`) with the necessary credentials for ElasticSearch, MySQL and Postgres in production.

This will set up the environment to be run locally. If you want to run the scripts in production set the environment like so:

```sh
ENVIRONMENT=PROD docker compose up -d --build
```

## Run

Run this command to find the incomplete records:

```sh
docker compose exec app python -m actions.save_data
docker compose exec app python -m actions.plan
```

*Note: If there's already a `data` directory, this will stop. If you want to replace the data, use `docker compose exec app python save_data.py --replace` instead.*

This will store some necessary data from the databases, to make the script more efficient, find the incorrect completion records. The records will be stored in `data/plan.json`.

Once you are happy and ready, run this command to insert the new data in the event completions table:

```sh
docker compose exec app python -m actions.apply
```

## Analytics

*These commands use the `plan.json` file to run analytics so make sure it exists before running these.*

### Incomplete records by month

```sh
docker compose exec app python -m analytics.byMonth
```

### Incomplete records by course

```sh
docker compose exec app python -m analytics.byCourse
```