import json
import os
import sys


def dump(path: str, output: dict):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as file:
        file.write(json.dumps(output))


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # noqa
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
