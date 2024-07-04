#Import
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..logic.get_path import get_path


router = APIRouter()

@router.get("/choose_export_path")
async def choose_export_path():
    # Open file dialog and get selected path
    path = get_path()
    return JSONResponse(content={"path": path})