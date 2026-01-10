"""
API routes for persisting and restoring scenario progress.

These endpoints provide a minimal persistence surface for
frontend-controlled training flow.
"""

from fastapi import APIRouter
from pydantic import BaseModel

from app.persistence.progress_repo import get_progress, save_progress

router = APIRouter(prefix="/progress", tags=["progress"])


# ------------------------------------------------------------
# Request models
# ------------------------------------------------------------

class ProgressSaveRequest(BaseModel):
    client_id: str
    module_id: str
    scenario_id: str
    current_step_index: int


# ------------------------------------------------------------
# Routes
# ------------------------------------------------------------

@router.get("")
def load_progress(
    client_id: str,
    module_id: str,
    scenario_id: str,
):
    """
    Load saved progress for a client/module/scenario.

    Returns step index 0 if no progress exists.
    """
    step_index = get_progress(
        client_id=client_id,
        module_id=module_id,
        scenario_id=scenario_id,
    )

    return {
        "current_step_index": step_index if step_index is not None else 0
    }


@router.post("")
def persist_progress(payload: ProgressSaveRequest):
    """
    Save or update progress for a client/module/scenario.
    """
    save_progress(
        client_id=payload.client_id,
        module_id=payload.module_id,
        scenario_id=payload.scenario_id,
        current_step_index=payload.current_step_index,
    )

    return {"status": "ok"}
