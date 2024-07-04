# Imports
import json
from fastapi import WebSocket, APIRouter, WebSocketDisconnect
from ..logic.files import *
from ..logic.get_results import *
from ..logic.get_path import *
from ..logic.model import *
from ..logic.advanced import *
from ..logic.directories import *
from ..logic.progress import *
from ..logic.websocketManager import websSocketManager
router = APIRouter()



@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    listens to websocket for remote function calls from frontend to backend

    To call function from frontend, send a json using the folowing format:
    {"function":*function name*,"args": *array of arguments*}
    Functions that can accept a remote call, use the folowing format:
    async def *function name*(*array of argument strings*)
    """
    try:
        await websSocketManager.connect(websocket)
        while True:
            #call command
            commandtext = await websocket.receive_text()
            try:
                command = json.loads(commandtext)
                
                await globals()[command["function"]](command["args"])
            except Exception as e:
                print(f'error : {e}')
            
    except WebSocketDisconnect:
        websSocketManager.disconnect(websocket)
        print("websocket disconected")



