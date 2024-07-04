# Import
from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse
from ..logic.get_path import get_path


router = APIRouter()

# home page
@router.get("/")
def home(request: Request):
    return RedirectResponse(url="/upload")

# open file explorer
@router.post("/")
async def openFiles():
    print(get_path())
