# Imports
import json
from datastore.store import DataStore
from ..logic.websocketManager import websSocketManager

# Return video to frontend
# Called from websocket
async def logic_videos(args):
    
    ds = DataStore()
    await websSocketManager.broadcast(json.dumps({"function": "logic_videos", "args": ds.getVideos()}))

# Return result to frontend
# Called from websocket
async def logic_result(args):
    ds = DataStore()
    await websSocketManager.broadcast(json.dumps({"function": "logic_result",
                                                  "args": {"detections": ds.getDetectionsCount(args),
                                                           "timestamps": ds.getDetections(args)}}))
