import os
import unittest
from unittest.mock import Mock

from fastapi import WebSocket
from ML_model.Model import ModelYolo
from datastore.store import DataStore
import asyncio

class TestModelYolo(unittest.TestCase):
    def setUp(self):
        # remove the database file if it exists
        if os.path.exists('datastore.db'):
            os.remove('datastore.db')
        # remove the annotated video if it exists
        if os.path.exists('results/videos/vis_kort.mp4'):
            os.remove('results/videos/vis_kort.mp4')
        self.model = ModelYolo('../ML_model/best.pt')
        self.datastore = DataStore()

    def test_video_inference_and_db_insertion(self):
        # Mock the WebSocket
        ws = Mock(spec=WebSocket)

        # Call the infer_video method
        video_path = 'test_media/vis_kort.mp4'
        result_path = 'results/videos/vis_kort.mp4'
        expected_video_id = asyncio.run(self.model.infer_video(video_path, 0, ws))

        # id is 1st of getVideos() list
        videos = self.datastore.getVideos()
        actual_video = videos[0]

        # Check if the video is inserted correctly in the database
        self.assertIsNotNone(actual_video)
        self.assertEqual(actual_video[1], result_path)

        # Retrieve the detections from the database
        actual_detections = self.datastore.getDetectionsCount(actual_video[0])

        # Check if the detections are inserted correctly in the database
        self.assertIsNotNone(actual_detections)

        # check that there is at least one Terapon-puta
        self.assertTrue(actual_detections['Terapon-puta'] > 0)

        # check if the annotated video is created
        self.assertTrue(os.path.exists(result_path))

if __name__ == '__main__':
    unittest.main()