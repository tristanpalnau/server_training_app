"""
Persistence layer for scenario progress.

This module is responsible only for reading and writing
resume state to the database.
"""

from typing import Optional
from app.persistence.db import get_connection


# ------------------------------------------------------------
# Read progress
# ------------------------------------------------------------

def get_progress(
    client_id: str,
    module_id: str,
    scenario_id: str,
) -> Optional[int]:
    """
    Retrieve the saved step index for a client/module/scenario.

    Returns:
        current_step_index if found, otherwise None
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT current_step_index
        FROM progress
        WHERE client_id = ?
          AND module_id = ?
          AND scenario_id = ?
        """,
        (client_id, module_id, scenario_id),
    )

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    return row["current_step_index"]


# ------------------------------------------------------------
# Save (upsert) progress
# ------------------------------------------------------------

def save_progress(
    client_id: str,
    module_id: str,
    scenario_id: str,
    current_step_index: int,
) -> None:
    """
    Insert or update progress for a client/module/scenario.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO progress (
            client_id,
            module_id,
            scenario_id,
            current_step_index,
            updated_at
        )
        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(client_id, module_id, scenario_id)
        DO UPDATE SET
            current_step_index = excluded.current_step_index,
            updated_at = CURRENT_TIMESTAMP
        """,
        (
            client_id,
            module_id,
            scenario_id,
            current_step_index,
        ),
    )

    conn.commit()
    conn.close()
