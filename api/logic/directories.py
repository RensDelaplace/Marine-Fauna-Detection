# Imports
from .get_path import get_directory, get_model_directory
import json
from .model import logic_model_changeModel, logic_model_dataDir, logic_model_resultsDir
from ..logic.websocketManager import websSocketManager

# Open file explorer to get dataset directory path
# Called from websocket
async def logic_directories_chooseDataset(args):
    path = get_directory()
    if(path!=None):
        await logic_model_dataDir(path)
        await websSocketManager.broadcast(json.dumps({"function":"retrain_setDirectory","args":path}))

# Open file explorer to get model directory path
# Called from websocket       
async def logic_directories_chooseModel(args):
    path = get_model_directory()
    if(path!=None):
        await websSocketManager.broadcast(json.dumps({"function":"settings_setModel","args":path}))
        await logic_model_changeModel(path)

# Open file explorer to get result directory path
# Called from websocket    
async def logic_directories_chooseDir(args):
    path = get_directory()
    if(path!=None):
        await logic_model_resultsDir(path)
        await websSocketManager.broadcast(json.dumps({"function":"settings_setDirectory","args":path}))

