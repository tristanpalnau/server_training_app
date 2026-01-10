"""
Modules API router.

This router exposes all HTTP endpoints related to training modules,
including:
- Module catalog metadata for the Module Picker UI (Phase 1)
- Scenario payload delivery for frontend-driven flows
- Engine-based debug and step-by-step lesson endpoints

This file intentionally remains a thin routing layer. All file I/O and
lesson processing logic is delegated to loaders and engines.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.loaders.module_loader import load_module_json
# from app.engines.module_engine import load_module, get_step, process_step


router = APIRouter(prefix="/modules", tags=["modules"])


# ============================================================
# Helpers (keep tiny)
# ============================================================

def _module_filename(module_id: str) -> str:
    """Converts a module ID into its corresponding JSON filename."""
    return f"{module_id}.json"


def _http404(detail: str) -> HTTPException:
    """Creates a standardized 404 HTTP exception."""
    return HTTPException(status_code=404, detail=detail)


def _load_raw_module_or_404(module_id: str) -> dict:
    """
    Loads raw module JSON from disk or raises a 404 if not found.
    """
    try:
        return load_module_json(module_id)
    except FileNotFoundError:
        raise _http404("Module not found")


def _load_engine_module_or_404(module_id: str) -> dict:
    """
    Loads a module via the module engine or raises a 404 if not found.
    """
    filename = _module_filename(module_id)
    try:
        return load_module(filename)
    except FileNotFoundError:
        raise _http404("Module not found")


# ============================================================
# Phase 1: Module catalog for picker UI
# ============================================================
# Explicit module catalog used by the Module Picker UI (Phase 1).
# This is intentionally hardcoded to avoid filesystem scanning and
# keep behavior deterministic during early development.
#
# In later phases, this can be generated dynamically from content/.
MODULE_CATALOG: list[dict] = [
    {
        "id": "orientation",
        "title": "Orientation",
        "estimated_minutes": 5,
        "default_scenario_id": "first_5_minutes",
    }
]


@router.get("")
def list_modules():
    """
    Returns module metadata used by the Module Picker UI.

    Only includes fields required by the frontend during Phase 1.
    """
    return [
        {
            "id": m["id"],
            "title": m["title"],
            "estimated_minutes": m["estimated_minutes"],
            "default_scenario_id": m["default_scenario_id"],
        }
        for m in MODULE_CATALOG
    ]


# ============================================================
# Debug: raw module JSON on disk
# ============================================================

@router.get("/{module_id}/raw")
def get_module_raw(module_id: str):
    """
    Returns the raw module JSON exactly as it exists on disk.

    Intended for debugging and development only.
    """
    return _load_raw_module_or_404(module_id)


# # ============================================================
# # Metadata: summary for a single module (engine-loaded)
# # ============================================================

# @router.get("/{module_id}/content")
# def get_module_content(module_id: str):
#     """
#     Returns summary metadata for a module loaded via the engine.

#     Includes:
#     - module id
#     - title
#     - total number of steps
#     """
#     module = _load_engine_module_or_404(module_id)
#     steps = module.get("steps", [])

#     return {
#         "id": module.get("id", module_id),
#         "title": module.get("title", ""),
#         "total_steps": len(steps),
#     }


# # ============================================================
# # Engine: processed step endpoint
# # ============================================================

# @router.get("/{module_id}/step/{index}")
# def get_module_step(
#     module_id: str,
#     index: int,
#     primary_style: str | None = None,
#     strategist: int | None = None,
#     guide: int | None = None,
#     anchor: int | None = None,
#     spark: int | None = None,
# ):
#     """
#     Returns a single processed lesson step using the module engine.

#     This endpoint supports engine-driven lesson flows and is primarily
#     used for debugging and future interactive progression models.
#     """
#     module = _load_engine_module_or_404(module_id)

#     try:
#         raw_step = get_step(module, index)
#     except IndexError:
#         raise _http404("Step index out of range")

#     processed = process_step(
#         raw_step,
#         primary_style=primary_style,
#         strategist=strategist,
#         guide=guide,
#         anchor=anchor,
#         spark=spark,
#     )

#     return {
#         "module_id": module_id,
#         "step_index": index,
#         "step": processed,
#     }


# ============================================================
# Phase 1: Scenario endpoint (explicit + unambiguous)
# ============================================================

@router.get("/{module_id}/scenario/{scenario_id}")
def get_module_scenario(module_id: str, scenario_id: str):
    """
    Returns a single scenario from a module in a frontend-friendly format.

    This is the primary content delivery endpoint used by the Phase 1
    scenario-based training flow.
    """
    module = _load_raw_module_or_404(module_id)

    scenarios = module.get("scenarios", [])
    scenario = next((s for s in scenarios if s.get("id") == scenario_id), None)

    if not scenario:
        raise _http404("Scenario not found")

    return {
        "module_id": module.get("module_id", module_id),
        "title": module.get("title", ""),
        "scenario": scenario,
    }
