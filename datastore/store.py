#Imports
import sqlite3 as sl
from typing import List, Tuple, Dict, Any


class DataStore:

    _instance = None

    def __new__(cls, conn_str="datastore.db"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.conn_str = conn_str
            cls._instance.conn = None
            cls._instance.connect()
            cls._instance.init()
        return cls._instance


    def connect(self):
        print("making datastore")
        self.conn = sl.connect(self.conn_str, check_same_thread=False)

    def init(self):
        print("creating tables")
        c = self.conn.cursor()
        c.execute(
            "CREATE TABLE IF NOT EXISTS video (id INTEGER PRIMARY KEY AUTOINCREMENT, ref_vid VARCHAR, processed INTEGER, frame_rate REAL);")
        c.execute(
            "CREATE TABLE IF NOT EXISTS detections (id INTEGER PRIMARY KEY AUTOINCREMENT, video_id INTEGER, class VARCHAR, frame INTEGER);")
        c.execute("CREATE TABLE IF NOT EXISTS fish_count (video_id INTEGER, class VARCHAR, count INTEGER, PRIMARY KEY (video_id, class));")
        c.execute(
            "CREATE TABLE IF NOT EXISTS settings (key VARCHAR PRIMARY KEY, value VARCHAR);"
        )
        self.conn.commit()
        c.close()

    def getSetting(self, key: str) -> str:
        """
        Get a specific setting from the datastore
        :param key: key of the setting
        :return: value of the setting
        """
        c = self.conn.cursor()
        c.execute("SELECT value FROM settings WHERE key = ?;", (key,))
        result = c.fetchone()
        c.close()
        return result[0] if result else None

    def setSetting(self, key: str, value: str):
        """
        Set a specific setting in the datastore
        :param key: key of the setting
        :param value: value of the setting
        """
        c = self.conn.cursor()
        c.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?);", (key, value))
        self.conn.commit()
        c.close()

    def insertVideo(self, ref: str, frame_rate: float) -> int:
        """
        Insert a new video reference in the local datastore
        :param ref: reference to video file
        """
        c = self.conn.cursor()
        c.execute("INSERT INTO video (ref_vid, processed, frame_rate) VALUES (?, 1, ?);", (ref,frame_rate))
        self.conn.commit()
        video_id = c.lastrowid
        c.close()
        return video_id

    def setVideoProcessed(self, id: int):
        """
        Set processed value in datastore to true for specific video
        :param id: id of video in datastore
        """
        c = self.conn.cursor()
        self.conn.execute("UPDATE video SET processed = 1 WHERE id = ?;", (id,))
        self.conn.commit()
        c.close()

    def getVideos(self) -> List[Tuple[int, str, float]]:
        """
        Get all saved videos from datastore
        :return: a list of tuples, each describing a video
        """
        c = self.conn.cursor()
        c.execute("SELECT id, ref_vid, frame_rate FROM video ORDER BY id desc;")
        result = c.fetchall()
        c.close()
        return result

    def getVideo(self, id: int):
        """
        Get a specific video from the datastore
        :param id: id of the video
        :return: a dictionary describing the video (path and id)
        """
        c = self.conn.cursor()
        c.execute("SELECT ref_vid, id FROM video WHERE id = ?;", (id,))
        result = c.fetchone()
        c.close()
        if result:
            return {"ref_vid": result[0], "id": result[1]}
        return {"ref_vid": None, "id": None}

    def getDetectionsCount(self, video_id: int) -> Dict[str, int]:
        """
        Get number of fund fish per class for a specific video
        :param video_id: id of the video
        :return: a dictionary that maps a class to a count
        """
        if not video_id:
            raise Exception("No video provided for detections")
        c = self.conn.cursor()
        # c.execute("SELECT class, count FROM fish_count WHERE video_id = ? order by count desc;", (video_id,))
        c.execute("SELECT class, count(*) as count FROM detections WHERE video_id = ? GROUP BY class, video_id order by count desc;", (video_id,))
        resultList = c.fetchall()
        c.close()
        return {result[0]: result[1] for result in resultList}

    def insertDetectionsMap(self, video_id: int, detections: Dict[str, List[int]]):
        """
        Insert multiple detections for a specific video
        Args:
            video_id: The id of the video in which the detections took place
            detections: A dictionary of the types that are detected mapped to a list of frame numbers
        """
        print(detections)
        for detection in detections.items():
            print(detection)
        if not video_id:
            raise Exception("No video provided for detections")
        c = self.conn.cursor()
        for type in detections.items():
            for frame_number in type[1]:
                c.execute("INSERT INTO detections (video_id, class, frame) VALUES (?, ?, ?);", (video_id, type[0], frame_number))

        self.conn.commit()
        c.close()

    def getDetections(self, video_id: int) -> List[Tuple[int, str]]:
        """
        Get the detections for a specific video ordered by frame number
        Args:
            video_id: The video_id of the detections

        Returns: a list of tuples, each containing the class and frame number of a detection

        """
        if not video_id:
            raise Exception("No video provided for detections")
        c = self.conn.cursor()
        c.execute("SELECT frame, class FROM detections WHERE video_id = ? ORDER BY frame;", (video_id,))
        result = c.fetchall()
        return result


    def clearResults(self) -> None:
        c = self.conn.cursor()
        c.execute("DELETE FROM fish_count WHERE TRUE; ")
        c.execute("DELETE FROM video WHERE TRUE;")
        print("removing all results from database for cleanup")

        self.conn.commit()
        c.close()

    def disconnect(self):
        self.conn.close()


