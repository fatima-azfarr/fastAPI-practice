import json
from pathlib import Path

shipments = {}

FILE_PATH = Path(__file__).parent / "shipments.json"

if FILE_PATH.exists() and FILE_PATH.stat().st_size > 0:
    with open(FILE_PATH, "r") as f:
        data = json.load(f)

        # map as a dictionary
        for value in data:
            shipments[value["id"]] = value


def save():
    with open(FILE_PATH, "w") as f:
        json.dump(list(shipments.values()), f, indent=4)