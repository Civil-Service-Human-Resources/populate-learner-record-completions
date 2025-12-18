# Script to populate learner record completions

## Requirements

* Docker

## Setup

<details>
<summary>Mac / Linux</summary>
<div>
Run this command to setup your environment:

```sh
make setup
```

This will build and run the Docker containers and will also walk you through creating the configuration file (`config.json`) with the necessary credentials for ElasticSearch, MySQL and Postgres in production.

</div>
</details>

<details>
<summary>Windows</summary>
<div>
Run this command to setup your environment:

```sh
docker compose up -d --build
docker compose exec app python setup_prod_config.py
```

This will build and run the Docker containers and will also walk you through creating the configuration file (`config.json`) with the necessary credentials for ElasticSearch, MySQL and Postgres in production.

</div>
</details>

## Run

<details>
<summary>Mac / Linux</summary>
<div>
Run this command to find the incomplete records:

```sh
make save-data plan
```

*Note: If there's already a `data` directory, this will stop. If you want to replace the data, use `make save-data-replace` instead of `save-data`.*

This will store some necessary data from the databases, to make the script more efficient, find the incorrect completion records. The records will be stored in `data/plan.json`.

Once you are happy and ready, run this command to insert the new data in the event completions table:

```sh
make apply
```

</div>
</details>

<details>
<summary>Windows</summary>
<div>
Run this command to find the incomplete records:

```sh
docker compose exec app python save_data.py
docker compose exec app python plan.py
```

*Note: If there's already a `data` directory, this will stop. If you want to replace the data, use `docker compose exec app python save_data.py --replace` instead.*

This will store some necessary data from the databases, to make the script more efficient, find the incorrect completion records. The records will be stored in `data/plan.json`.

Once you are happy and ready, run this command to insert the new data in the event completions table:

```sh
docker compose exec app python apply.py
```

</div>
</details>

## Analytics

<details>
<summary>Mac / Linux</summary>
<div>

### Incomplete records by month

```sh
make analytics.byMonth
```

### Incomplete records by course

```sh
make analytics.byCourse
```
</div>
</details>

<details>
<summary>Windows</summary>
<div>

### Incomplete records by month

```sh
docker compose exec app python -m analytics.byMonth
```

### Incomplete records by course

```sh
docker compose exec app python -m analytics.byCourse
```
</div>
</details>