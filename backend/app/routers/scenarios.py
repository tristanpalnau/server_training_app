# Imports the API router class.
from fastapi import APIRouter
# Imports our function that can read a JSON file for a module.
from app.loaders.scenario_loader import load_scenario_json

"""Create a router object with a URL prefix so every endpoint inside this file
   automatically starts with /scenarios."""
router = APIRouter(prefix="/scenarios")

# Decorator defines an endpoint for GET requests.
"""The following function will run when route is hit. It calls our loader
   function that will open the correct JSON file, read it, parse it, and return
   a Python dictionary. Dictionary will be converted to JSON response by
   fastAPI."""
@router.get("/{scenario_id}")
def get_scenario(scenario_id: str):
    return load_scenario_json(scenario_id)