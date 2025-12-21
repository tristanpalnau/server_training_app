"""Import fastapi class from library and import module.py and scenarios.py from
   routers folder"""
from fastapi import FastAPI
from app.routers import modules, scenarios, quiz
import json
from pathlib import Path

# Create FastAPI application object
app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
MODULES_DIR = BASE_DIR / "content" / "modules"

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Built in FastAPI methods collect all related HTTP routes
app.include_router(modules.router)
app.include_router(scenarios.router)
app.include_router(quiz.router)

# ================= Endpoints ==========================
"""The following function returns a Python dictionary that fastAPI will convert
   to a JSON file. It's a quick sanity check to confirm the API is running."""
@app.get("/")
def home():
    return {"message": "Server Training Backend Running!"}

@app.get("/modules")
def list_modules():
   return load_module_metadata()


# ================= Helper Functions ===================
def load_module_metadata():
   modules = []

   for file in MODULES_DIR.glob("*.json"):
      with open(file, "r", encoding="utf-8") as f:
         data = json.load(f)

         modules.append({
            "id": data["id"],
            "title": data["title"],
            "description": data["description"],
            "estimated_minutes": data["estimated_minutes"],
            "version": data["version"]
         })
   
   return modules
   