# Script to populate learner record completions

## Set up

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
    }
}
```

2. Build the Docker image from the Dockerfile:

```sh
docker build -t lr-completions .
```

3. Run the data save script:

This script will store course, organisation and last completion data from the database as a .pkl (Pickle) file to save time during the main script:

```sh
docker run -it --rm -v $PWD/src:/app -w /app lr-completions python save_data.py
```

3. Run the main script:

```sh
docker run -it --rm -v $PWD/src:/app -w /app lr-completions python main.py
```

This script will create a `plan.json` file in the `data` directory.

To keep track of the logs while the main script is running run:

```sh
tail -f src/debug.log
```