import json
import os

with open(os.path.join(os.path.dirname(__file__), "config.json"), "r", encoding="utf-8") as f:
    _config = json.load(f)

DB_NAME = _config["DB_NAME"]
API_TOKEN = _config["API_TOKEN"]