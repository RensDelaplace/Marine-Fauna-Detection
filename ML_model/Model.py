import csv
from ultralytics import YOLO
import os
from torch.cuda import is_available
import cv2
import time
import threading
import numpy as np
from supervision import Detections
from api.logic.progress import *
from datastore.store import DataStore
from utils.file_manager import PROJECT_DIR


class ModelYolo:
    def __init__(self, version=None):

        # version is only defined in test cases
        if version is None:
            version = DataStore().getSetting('model')

        # version isn't changed by user
        if version is None:

            # PROJECT_DIR = temp folder when using exe
            version = os.path.join(PROJECT_DIR,"models/latest")

        print("changed model")
        print("model:", version)
        self.model_pt = YOLO(os.path.join(version, 'weights', 'best.pt'))
        if is_available():
            self.model_pt.to('cuda')
        self.classes = np.array(list(self.model_pt.names.values()))
        print("classes, in MODELYOLO:",self.classes)



    async def infer_video(self, video,index, n_conf=0.5):
        
        coo_x = np.array([], dtype=np.float32)
        coo_y = np.array([], dtype=np.float32)
        counts = dict.fromkeys(self.classes, 0)
        timestamps = dict.fromkeys(self.classes, np.array([]))

        cap = cv2.VideoCapture(video)
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_rate = cap.get(cv2.CAP_PROP_FPS)
        cap.release()
        print("lenght = "+str(length))
        updateProgress(index,0,length+1)
        await logic_progress_updateFrontendProgress(None)
        
        frame = 1

        from utils.file_manager import VIDEO_RESULTS_DIR
        results =self.model_pt.predict(video, conf=n_conf, save=True, stream=True, project=VIDEO_RESULTS_DIR, name="videos")

        started_at = time.monotonic()
        interval_start = started_at
        
        # Process each analysed frame
        for r in results:
            current_time = time.monotonic()
            if(current_time - interval_start > 5):
                if(threading.current_thread().stopped()):
                    return None
                updateProgress(index,frame,length+1)
                await logic_progress_updateFrontendProgress(None)
                
                interval_start = current_time
            
            detections = Detections.from_ultralytics(r)
            coords = detections.xyxy
            
            names = self.classes[detections.class_id]
    
            for i in range(int(names.size)):
                curr1 = coords[i][0]
                curr2 = coords[i][1]
                name = names[i]
        
                cmp = np.intersect1d(np.where(np.abs(coo_x - curr1) < 50)[0], np.where(np.abs(coo_y - curr2) < 50)[0])
                #print(cmp)
                if cmp.size > 0:# and name in self.classes[cmp]:
                    coo_x[cmp[0]] = curr1
                    coo_y[cmp[0]] = curr2
        
                else:
                    coo_x = np.append(coo_x, curr1)
                    coo_y = np.append(coo_y, curr2)
                    counts[name] += 1
                    timestamps[name] = np.append(timestamps[name], frame)
                    #if timestamps.keys().__contains__(frame):
                    #    timestamps[frame] = np.append(timestamps[frame], name)
                    #else:
                    #    timestamps[frame] = np.array([name])
            frame += 1
        else:
            # Makes sure progress bar ends at 100%
            updateProgress(index,frame,length+1)
            await logic_progress_updateFrontendProgress(None)
            
            ds = DataStore()
            dir_name = r.save_dir.replace("\\", "/") + '/' + os.path.basename(video).split('.')[0]
            loc = dir_name + '.mp4'
            relative_loc = "/results/" + loc.split("/results/")[-1]
            video_id = ds.insertVideo(relative_loc, frame_rate)
            ds.insertDetectionsMap(video_id, timestamps)
            
            await write_counts_to_csv(f"{dir_name}_counts.csv", counts)
            await write_timestamps_to_csv(f"{dir_name}_timestamps.csv", timestamps, frame_rate)
            
        totaltime = time.monotonic() - started_at
        #print("time: "+str(totaltime))
        return loc


    

    async def train(self, yaml_file, n_epochs=5, n_batch=8, n_name='latest'):
        self.model_pt.train(data = yaml_file, epochs = n_epochs, batch = n_batch, project = os.path.join(PROJECT_DIR,"models"), name = n_name)

    def getCLasses(self):
        return self.classes


async def write_counts_to_csv(csv_path, counts):

    with open(csv_path, mode='w', newline='') as csv_file:
        fieldnames = ['Fish', 'Count']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for fish, count in counts.items():
            writer.writerow({'Fish': fish, 'Count': count})


def to_HHMMSS(sec_num):
    hours = int(sec_num // 3600)
    minutes = int((sec_num % 3600) // 60)
    seconds = int(sec_num % 60)
    
    return f"{hours:02}:{minutes:02}:{seconds:02}"

async def write_timestamps_to_csv(csv_path, timestamps, frame_rate):
    print(timestamps)
    with open(csv_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # Write header
        max_timestamps = max(len(ts_list) for ts_list in timestamps.values())

        # Write rows
        for vissen in timestamps.items():
            fish, ts_list = vissen
            print(fish, ts_list)
            if ts_list.size > 0:
                # Divide by frame_rate and convert to HH:MM:SS
                adjusted_ts_list = [to_HHMMSS(ts / frame_rate) for ts in ts_list]
                # Create a row with the fish name and the time stamps, padding with empty strings if necessary
                row = [fish] + adjusted_ts_list + [''] * (max_timestamps - len(adjusted_ts_list))
                writer.writerow(row)

