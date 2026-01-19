import psycopg
import modules.config.ConfigService as ConfigService

pg_config = ConfigService.get_config()["postgres"]

def get_connection():
    return psycopg.connect(
        dbname="reporting",
        user=pg_config["username"],
        password=pg_config["password"],
        host=pg_config["host"]
    )