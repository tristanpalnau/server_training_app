# Imports the API router class.
from fastapi import APIRouter, HTTPException

# Imports function that can read a JSON file for a module (original loader).
from app.loaders.module_loader import load_module_json

# Imports engine functions for processed lesson flow (new).
from app.engines.module_engine import load_module, get_step, process_step


"""
Create a router object with a URL prefix so every endpoint defined here
automatically begins with /modules.
"""
router = APIRouter(
    prefix="/modules",
    tags=["modules"]
)


# ============================================================
# 1. RAW MODULE ENDPOINT  (Original functionality)
# ============================================================

@router.get("/{module_id}/raw")
def get_module_raw(module_id: str):
    """
    Returns the entire raw module JSON exactly as it exists on disk.
    This is mainly useful for debugging or inspecting the full structure.
    """
    try:
        return load_module_json(module_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Module not found")


# ============================================================
# 2. MODULE METADATA ENDPOINT
# ============================================================

@router.get("/{module_id}/content")
def get_module_content(module_id: str):
    """
    Returns general metadata a frontend might need:
    - module id
    - module title
    - number of steps

    Does NOT return full content — only summary information.
    """
    filename = f"{module_id}.json"

    try:
        module = load_module(filename)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Module not found")

    return {
        "id": module["id"],
        "title": module["title"],
        "total_steps": len(module["steps"])
    }


# ============================================================
# 3. PROCESSED STEP ENDPOINT
# ============================================================

@router.get("/{module_id}/step/{index}")
def get_module_step(
    module_id: str,
    index: int,
    primary_style: str | None = None,
    strategist: int | None = None,
    guide: int | None = None,
    anchor: int | None = None,
    spark: int | None = None,
):
    """
    Returns a SINGLE processed lesson step.
    Steps are converted to standardized structures via process_step().
    """
    filename = f"{module_id}.json"

    # Load the module file
    try:
        module = load_module(filename)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Module not found")

    # Retrieve the specific step
    try:
        raw_step = get_step(module, index)
    except IndexError:
        raise HTTPException(status_code=404, detail="Step index out of range")

    # Process the step into backend-friendly format
    processed = process_step(
        raw_step,
        primary_style=primary_style,
        strategist=strategist,
        guide=guide,
        anchor=anchor,
        spark=spark
    )

    return {
        "module_id": module_id,
        "step_index": index,
        "step": processed
    }


# ============================================================
# 4. MODULE SCENARIO ENDPOINT (Orientation / Scenario-based)
# ============================================================

@router.get("/{module_id}/{scenario_id}")
def get_module_scenario(module_id: str, scenario_id: str):
    """
    Returns a single scenario from a module in a frontend-friendly shape.

    Designed for scenario-based training flows
    (e.g. Orientation → First 5 Minutes).
    """
    try:
        module = load_module_json(module_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Module not found")

    scenarios = module.get("scenarios", [])

    scenario = next(
        (s for s in scenarios if s.get("id") == scenario_id),
        None
    )

    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    return {
        "module_id": module.get("module_id", module_id),
        "title": module.get("title", ""),
        "scenario": scenario
    }
