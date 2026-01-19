import json
import os

environment = os.getenv("ENVIRONMENT")
environment = environment if environment in ["LOCAL", "PERF", "PROD"] else "LOCAL"

def get_config():
    config_files = {
        "LOCAL": "config-local.json",
        "PERF": "config-perf.json",
        "PROD": "config.json"
    }
    config = json.load(open(f"/config/{config_files[environment]}", "r"))
    return config