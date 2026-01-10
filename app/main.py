"""
FastAPI application entry point for the Server Training App backend.

Responsibilities:
- App initialization
- Middleware
- API router registration
- Frontend static file serving
"""

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from contextlib import asynccontextmanager
from pathlib import Path

from app.routers import modules, scenarios, quiz, progress
from app.persistence.db import init_db


# ============================================================
# Lifespan
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


# ============================================================
# App initialization
# ============================================================

app = FastAPI(
    title="Server Training App",
    version="0.1.0",
    lifespan=lifespan,
)

# ============================================================
# API Routers (namespace under /api)
# ============================================================

app.include_router(modules.router, prefix="/api")
app.include_router(scenarios.router, prefix="/api")
app.include_router(quiz.router, prefix="/api")
app.include_router(progress.router, prefix="/api")


# ============================================================
# Frontend Static Files
# ============================================================

ROOT_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = Path(__file__).resolve().parents[1] / "frontend"

app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static",
)


@app.get("/", include_in_schema=False)
def serve_frontend():
    """
    Serves the frontend entry point.
    """
    return FileResponse(FRONTEND_DIR / "index.html")


# ============================================================
# Health Check
# ============================================================

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "Backend running"}
