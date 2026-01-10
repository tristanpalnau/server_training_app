"""
Database initialization and connection utilities.

This module is responsible only for:
- Establishing a SQLite connection
- Creating required tables if they do not exist

It intentionally contains NO business logic.
"""

import sqlite3
from pathlib import Path

# ------------------------------------------------------------
# Database location
# ------------------------------------------------------------

DB_PATH = Path(__file__).resolve().parent / "app.db"


# ------------------------------------------------------------
# Connection helper
# ------------------------------------------------------------

def get_connection() -> sqlite3.Connection:
    """
    Create and return a SQLite connection.

    Row factory is set to sqlite3.Row to allow dict-like access.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ------------------------------------------------------------
# Initialization
# ------------------------------------------------------------

def init_db() -> None:
    """
    Initialize the database and create required tables.

    Safe to call multiple times.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id TEXT NOT NULL,
            module_id TEXT NOT NULL,
            scenario_id TEXT NOT NULL,
            current_step_index INTEGER NOT NULL,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (client_id, module_id, scenario_id)
        )
        """
    )

    conn.commit()
    conn.close()
