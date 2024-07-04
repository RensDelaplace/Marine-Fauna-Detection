# Imports
from fastapi import WebSocket
from .get_path import get_path
import json
from ..logic.websocketManager import websSocketManager

# Global variable cache
files =[]

# Clear cache
# Called from websocket
async def logic_files_clearFiles(args):
    await logic_files_updateUpload(args)

# Return up to date info to frontend
# Called from websocket
async def logic_files_updateUpload(args):
   await websSocketManager.broadcast(json.dumps({"function":"upload_showFilePath","args":files}))

# Add file to cache
# Called from websocket
async def logic_files_addFiles(args):
    data = get_path()
    if(data!=None):
        for path in data:
            if path not in files and path != None:
                files.append(path)
        await logic_files_updateUpload(args)

# Remove file from cache
# Called from websocket        
async def logic_files_removeFiles(args):
    index = int(args[0])
    if len(files)>index:
        files.remove(files[index])
        await logic_files_updateUpload(args)

