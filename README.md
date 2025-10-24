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

3. Run the script:

```sh
docker run -it --rm -v $PWD/src:/app -w /app lr-completions python main.py
```