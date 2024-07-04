# Imports
import asyncio
import json
from typing import List
import threading
from ..logic.websocketManager import websSocketManager

# Class used to store progress of video
class Progress:
    def __init__(self, index, label,value,max):
        self.index = index
        self.label = label
        self.value = value
        self.max = max
    def toJSON(self):
        return json.dumps(self,default=lambda o: o.__dict__, sort_keys=True,indent=4)

# Global variables and cache   
analyseProgress:List[Progress] = []
lock = threading.Lock()

# Clear current progress
def clearProgress():
    with lock:
        analyseProgress.clear()

# Remove one progress object
# Called from websocket
async def logic_progress_removeProgress(args):
    with lock:
        analyseProgress.remove(analyseProgress[int(args[0])])

# Initialize progress cache
def initializeProgress(args):
    for index, input in enumerate(args):
        with lock:
            analyseProgress.append(Progress(index,input,0,10))

# Update progress in cache
def updateProgress(index,value,max):
    with lock:
        pr:Progress =  analyseProgress[index]
        pr.value = value
        pr.max = max


# Send current progress information to frontend
# Called from websocket and backend
async def logic_progress_updateFrontendProgress(args):
    with lock:
        temp = []
        for progress in analyseProgress:
            temp.append(progress.toJSON())
        await websSocketManager.broadcast(json.dumps({"function":"upload_updateProgress","args":temp}))
        await asyncio.sleep(0) #dit is nodig, zie https://websockets.readthedocs.io/en/stable/faq/asyncio.html
