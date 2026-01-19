import mysql.connector
import modules.config.ConfigService as ConfigService

mysql_config = ConfigService.get_config()["mysql"]

def get_connection():
    return mysql.connector.connect(
        host=mysql_config["host"],
        user=mysql_config["username"],
        password=mysql_config["password"],
    )