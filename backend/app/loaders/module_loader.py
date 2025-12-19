# Brings in Python's built-in JSON module.
import json
# Imports the Path class -- a modern way to work with file paths.
from pathlib import Path

# Points to the our base directory for modules where their JSON files live.
MODULE_DIR = Path(__file__).parent.parent / "content" / "modules"

"""Accepts the module name as input, loads the matching JSON file, and returns
   the JSON file as a Python dictionary."""
def load_module_json(module_id: str) -> dict:
    # Builds an exact file path to whatever is called.
    path = MODULE_DIR / f"{module_id}.json"
    # Opens the file located at path in read mode. 'With' auto closes file.
    with open(path, "r") as f:
        # Reads JSON file and parses it into a Python dictionary.
        return json.load(f)