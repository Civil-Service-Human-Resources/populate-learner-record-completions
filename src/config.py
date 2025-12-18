import json
import os

environment = os.getenv("ENVIRONMENT")
environment = environment if environment in ["LOCAL", "PROD"] else "LOCAL"
print(environment)

def get_config():
    config_files = {
        "LOCAL": "config-local.json",
        "PROD": "config.json"
    }
    return json.load(open(config_files[environment], "r"))