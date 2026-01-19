import os
import json

print("CONFIGURATION FOR PRODUCTION ENVIRONMENT")
print()

if os.path.exists("/config/config.json"):
    print("Configuration file (/config/config.json) already exists.")
    response = input("Do you want to replace it? (Y/n): ")
    if response != "Y":
        exit(1)

print()
print("ELASTICSEARCH:")
es_host = input("Host (eg. https://my-elastic.es.uksouth.azure.elastic-cloud.com:443): ")
es_username = input("Username: ")
es_password = input("Password: ")

print()
print("MYSQL:")
mysql_host = input("Host (eg. my-db.mysql.database.azure.com): ")
mysql_username = input("Username: ")
mysql_password = input("Password: ")

print()
print("POSTGRES:")
postgres_host = input("Host (eg. my-postgres.postgres.database.azure.com): ")
postgres_username = input("Username: ")
postgres_password = input("Password: ")

config = {
    "elasticsearch": {
        "host": es_host,
        "username": es_username,
        "password": es_password
    },
    "mysql": {
        "host": mysql_host,
        "username": mysql_username,
        "password": mysql_password
    },
    "postgres": {
        "host": postgres_host,
        "username": postgres_username,
        "password": postgres_password
    }
}

print()
print(config)
print()
response = input("Happy with the configuration? (Y/n): ")

if response == "Y":
    with open("/config/config.json", "w") as f:
        json.dump(config, f, indent=4)
    print("Configuration saved to config.json")
