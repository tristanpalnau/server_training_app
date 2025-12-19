"""Import fastapi class from library and import module.py and scenarios.py from
   routers folder"""
from fastapi import FastAPI
from app.routers import modules, scenarios, quiz

# Create FastAPI application object
app = FastAPI()

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

# This decorator tells fastAPI to trigger the following function at root URL.
"""The following function returns a Python dictionary that fastAPI will convert
   to a JSON file. It's a quick sanity check to confirm the API is running."""
@app.get("/")
def home():
    return {"message": "Server Training Backend Running!"}
