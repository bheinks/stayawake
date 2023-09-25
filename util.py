import json
import sys
from pathlib import Path


def resource_path(relative_path):
    base_path = Path(getattr(sys, "_MEIPASS", Path(sys.argv[0]).resolve().parent))
    return base_path / relative_path


def read_json(path):
    try:
        with open(path) as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        data = {}

    return data


def write_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f)
