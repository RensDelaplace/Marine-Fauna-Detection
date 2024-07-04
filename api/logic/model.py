from fastapi import WebSocket
from ML_model.Model import ModelYolo
import json
import os
import threading
import asyncio
import yaml
import time
import csv
import glob

from .progress import *
from ..logic.websocketManager import websSocketManager
from .stoppableThreading import StoppableThread
from ..utils import base_dir
from utils.file_manager import copy_ML_model
from datastore.store import DataStore
from utils.file_manager import PROJECT_DIR

videos = []
data_dir = None
yolo_model = None

results_dir_name = "results/videos"
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(os.path.dirname(script_dir))
results_dir = os.path.join(project_dir, results_dir_name)
currentModel = os.path.join(project_dir, 'models', 'latest')

currentThread = None
lock = threading.Lock()
isBusy = False
ds = DataStore()

# Copy selected model in project dir before making model object
model_path = ds.getSetting("model")
if model_path:
    print("Copying model")
    copy_ML_model(model_path)

yolo_model = ModelYolo()

async def logic_model_abort(args):
    global currentThread
    if currentThread is not None:
        currentThread.stop()
        currentThread = None
        clearProgress()

async def logic_model_analyse(args):
    clearProgress()
    initializeProgress(args)
    global currentThread
    currentThread = StoppableThread(target=asyncio.run, args=(infer(args),))
    currentThread.start()

async def logic_model_getBusyState(args):
    await websSocketManager.broadcast(json.dumps({"function": "upload_receiveBusyState", "args": isBusy}))

async def infer(args):
    global isBusy
    with lock:
        isBusy = True
    try:
        for index, input in enumerate(args):
            results = await yolo_model.infer_video(input, int(index))
            print(f"Result: {results}")
            if results is not None:
                videos.append(results)
            if threading.current_thread().stopped():
                return None
    except Exception as e:
        print(e)
    finally:
        with lock:
            currentThread = None
            isBusy = False
            await logic_model_getBusyState(None)

async def logic_model_train(args):
    yaml_file = 'data.yaml'
    yaml_file_path = os.path.join(data_dir, yaml_file)

    # Read the yaml file
    with open(yaml_file_path, 'r') as file:
        data = yaml.safe_load(file)

    # Get the 'nc' value
    batches = data.get('nc', 8)  # Default to 1 if 'nc' is not found

    name = args['name']
    epochs = args['epochs']

    # Create a thread to execute the training process
    train_thread = threading.Thread(target=train_model, args=(yaml_file_path, name, epochs, batches))
    train_thread.start()

    models_dir = os.path.join(PROJECT_DIR, "models")

    await websSocketManager.broadcast(json.dumps({"function": "retrain_feedback", "args": "Scanning dataset..."}))
    time.sleep(10)
    # Search for folders with the model_name pattern and select the most recently modified folder
    model_dirs = [d for d in os.listdir(models_dir) if d.startswith(name)]
    recent_model_dir = max(model_dirs, key=lambda d: os.path.getmtime(os.path.join(models_dir, d)))
    csv_filename = os.path.join(models_dir, recent_model_dir, "results.csv")
    epoch_completed = 0

    while epoch_completed < epochs:
        await asyncio.sleep(8)  # Wait before checking the file again
        # Check if the CSV file exists
        if os.path.isfile(csv_filename):
            with open(csv_filename, mode='r') as csv_file:
                reader = csv.reader(csv_file)
                rows = list(reader)  # Get all rows from the file
                if rows:  # If there are rows in the file
                    last_row = rows[-1]  # Take the last row
                    epoch_completed = int(last_row[0])  # Take the first element of the last row

            await websSocketManager.broadcast(json.dumps({"function": "retrain_feedback", "args": f"Epochs completed: {epoch_completed}/{epochs}"}))

        # Check if a file starting with 'train_batch' exists
        if glob.glob(os.path.join(models_dir, recent_model_dir, "train_batch*")):
            await websSocketManager.broadcast(json.dumps({"function": "retrain_feedback", "args": f"Epochs completed: {epoch_completed}/{epochs}"}))

        # Break the loop if epochs are completed
        if epoch_completed >= epochs:
            break
        
    await websSocketManager.broadcast(json.dumps({"function": "retrain_feedback", "args": "Model successfully retrained!"}))

# Function to execute the training process
def train_model(yaml_file_path, name, epochs, batches):
    # Run the training
    asyncio.run(yolo_model.train(yaml_file_path, n_name=name, n_epochs=epochs, n_batch=batches))
    
    models_dir = os.path.join(PROJECT_DIR, "models")
    model_dirs = [d for d in os.listdir(models_dir) if d.startswith(name)]
    recent_model_dir = max(model_dirs, key=lambda d: os.path.getmtime(os.path.join(models_dir, d)))

    from utils.file_manager import save_retrained_model
    global ds
    exportPath = ds.getSetting("exportPath")
    if not exportPath:
        exportPath = os.path.expanduser("~/Desktop/MARED_Marine_fauna_detection")

    save_retrained_model(exportPath, model_name=os.path.basename(recent_model_dir))

async def logic_model_resultsDir(path):
    ds.setSetting('exportPath', path)

async def logic_model_dataDir(path):
    global data_dir
    data_dir = path

async def logic_model_changeModel(path):
    global yolo_model
    ds.setSetting('model', path)
    print("changed model settings to:",path)
    from utils.file_manager import copy_ML_model
    copy_ML_model(path)
    yolo_model = ModelYolo()

def getCLasses():
    global yolo_model
    return yolo_model.getCLasses()

