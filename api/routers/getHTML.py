#Import
from fastapi import APIRouter, Request, Depends
from ..logic.model import videos, data_dir, currentModel, results_dir, yolo_model
from ..utils import template
import numpy as np
from datastore.store import DataStore

router = APIRouter()

# route for rendering app.html
@router.get("/{page}")
def home(page: str, request: Request):
    return template.TemplateResponse(
        "app.html", {"request": request}
    )

# get html for other pages after the websocket connects
# in order to load the page after the websocket connection to the backend has been established, we fetch the html
# using this endpoint to load the page after the connection is formed. 
@router.get("/getHTML/{page}")
async def get_html(page: str, request: Request):
    ds = DataStore()
    advanced = ds.getSetting("advanced");
    if advanced is None:
        advanced = 0

    if page == "retrain":
        currentModelName = ds.getSetting('model')
        if currentModelName:
            currentModelName = currentModelName.split('\\').pop()
        else:
            currentModelName = "latest"

        # use function to get classes, without it wasn't updated properly when model changed
        from ..logic.model import getCLasses
        return template.TemplateResponse(
            "retrain.html", {"request": request, "dataset": data_dir, "currentModel": currentModelName, "classes": np.array(getCLasses()).tolist(), "advanced": advanced}
        )
    elif page == "upload":
        return template.TemplateResponse(
            "upload.html", {"request": request, "advanced": advanced}
        )
    elif page == "settings":
        model = ds.getSetting('model')
        exportPath = ds.getSetting('exportPath')
        if model == None:
            model = currentModel
        return template.TemplateResponse(
            "settings.html", {"request": request, "results_path": results_dir, "dataset_dir": data_dir, "model_dir": model, "advanced": advanced, "exportPath": exportPath}
        )
    elif page == "results":
        current_video_index = 0  # Placeholder for the currently selected video index
        return template.TemplateResponse(
            "results.html", {"request": request, "video_results": videos, "current_video_index": current_video_index, "advanced": advanced}
        )
    else:
        return {"message": "Page not found"}, 404

