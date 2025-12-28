from fastapi import APIRouter, HTTPException
from pathlib import Path
import json

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent
MODULES_DIR = BASE_DIR / "content" / "modules"


@router.get("/scenarios/{scenario_id}")
def get_scenario(scenario_id: str):
    """
    Direct scenario loader (by scenario id).
    """
    scenario_file = MODULES_DIR / f"{scenario_id}.json"

    if not scenario_file.exists():
        raise HTTPException(status_code=404, detail="Scenario not found")

    with open(scenario_file, "r", encoding="utf-8") as f:
        return json.load(f)


@router.get("/modules/{module_id}/scenario")
def get_module_default_scenario(module_id: str):
    """
    Load the default scenario for a module.
    """
    module_file = MODULES_DIR / f"{module_id}.json"

    if not module_file.exists():
        raise HTTPException(status_code=404, detail="Module not found")

    with open(module_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    scenarios = data.get("scenarios", [])
    if not scenarios:
        raise HTTPException(status_code=404, detail="Scenario not found")

    return {
        "module_id": data["id"],
        "scenario": scenarios[0]
    }
