# Script to populate learner record completions

## Setup and run

1. Create a `config.json` file in the `src` directory containing the database credentials:

```json
{
    "elasticsearch": {
        "host": "https://hostname:443", // Protocol and host are needed here.
        "username": "username",
        "password": "password"
    },
    "mysql": {
        "host": "hostname", // Protocol and host are NOT needed here.
        "username": "username",
        "password": "password"
    },
    "postgres": {
        "host": "hostname", // Protocol and host are NOT needed here.
        "username": "username",
        "password": "password"
    }
}
```

2. Build the Docker image from the Dockerfile:

```sh
make setup
```

Or if your OS doesn't support `make`:

```sh
docker compose up -d --build
```

If you're planning to run the scripts in production, add `ENVIRONMENT=PROD` before. For example:

```sh
ENVIRONMENT=PROD make setup
```

3. Run the data save script:

This script will store course, organisation and last completion data from the database as a .pkl (Pickle) file to save time during the main script:

```sh
make save-data
```

Or, if you can't use `make`: 

```
docker compose exec app python save_data.py
```

This will create a `data` directory with the necessary data.

**Note:** If a `data` directory already exists, this will show you an error. To override it, use these commands instead:

```sh
make save-data-replace
# Or
docker compose exec app python save_data.py --replace
```

3. Run the *plan* script:

```sh
make plan
# or
docker compose exec app python plan.py
```

This script will take a few hours and will create a `plan.json` file in the `data` directory.

To keep track of the logs while the main script is running run:

```sh
tail -f src/debug.log
```

## Run analytics

### Incomplete records by month

```sh
make analytics.byMonth
# Or
docker compose exec app python -m analytics.byMonth
```

### Incomplete records by course

```sh
make analytics.byCourse
# Or
docker compose exec app python -m analytics.byCourse
```

## Set environment config

To test the script locally, set the config file in `config.py` to `config-local.json` (default).

To run the script in production, change it to `config.json`.