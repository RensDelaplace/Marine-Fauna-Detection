# FastAPI and related imports
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Standard library imports
import os

# import the endpoints
from .routers import choose_export_path, getHTML, home, websockets, results

# region define Directory paths
base_dir = os.path.abspath(os.path.dirname(__file__))

# region Configure FastAPI app
app = FastAPI()

# Mount static files
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(base_dir, "frontend\\static")),
    name="static",
)

app.mount(
    "/models",
    StaticFiles(directory=os.path.join(base_dir, "../models")),
    name="models"
)

# Include the router
app.include_router(choose_export_path.router)
app.include_router(home.router)
'''
app.include_router(upload.router)
app.include_router(results.router)
app.include_router(retrain.router)
app.include_router(settings.router)
app.include_router(upload.router)
'''
app.include_router(websockets.router)
app.include_router(getHTML.router)
app.include_router(results.router)