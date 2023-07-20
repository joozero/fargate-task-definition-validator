# src/utils/json_loader.py

import json


def load_json_from_file(file_path):
    """
    Load and parse a JSON file.

    Args:
    - file_path (str): Path to the JSON file.

    Returns:
    - dict: Parsed JSON data.
    """
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
    return data
