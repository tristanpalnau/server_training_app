"""
Module loader utilities.

This module is responsible for loading raw module JSON files from disk
and returning them as Python dictionaries. It performs no validation
or transformation of the data.
"""

import json
from pathlib import Path

# Base directory where module JSON files are stored.
MODULE_DIR = Path(__file__).parent.parent / "content" / "modules"

def load_module_json(module_id: str) -> dict:
    """
    Loads a module JSON file from disk and returns it as a dictionary.

    Args:
        module_id: The module identifier (without .json extension).

    Raises:
        FileNotFoundError: If the module file does not exist.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    path = MODULE_DIR / f"{module_id}.json"
    with open(path, "r") as f:
        return json.load(f)