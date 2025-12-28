"""
FastAPI application entry point for the Server Training App backend.

This module is responsible only for:
- Creating the FastAPI application instance
- Configuring global middleware
- Registering API routers
- Exposing a basic health check endpoint

Business logic, data loading, and scenario execution are intentionally
delegated to routers, engines, and loaders.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import modules, scenarios, quiz


# ============================================================
# FastAPI application initialization
# ============================================================

app = FastAPI(
    title="Server Training Backend",
    version="0.1.0",  # Backend API version, not tied to training content versions
)

# ============================================================
# Middleware (dev-friendly CORS)
# ============================================================
# NOTE: Open CORS configuration for local development.
# This should be restricted before any production deployment.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# API routers
# ============================================================
# Routers are organized by domain responsibility (modules, scenarios, quizzes)
# and should remain thin request/response layers.

app.include_router(modules.router)
app.include_router(scenarios.router)
app.include_router(quiz.router)


# ============================================================
# Health check
# ============================================================

@app.get("/")
def health_check():
    """
    Basic health check endpoint used to verify that the backend is running.
    """
    return {"status": "ok", "message": "Server Training Backend Running"}
