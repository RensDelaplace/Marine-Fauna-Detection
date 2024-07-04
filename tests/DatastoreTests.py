import unittest
from datastore.store import DataStore

class TestDataStore(unittest.TestCase):
    def setUp(self):
        self.datastore = DataStore(":memory:")
        # self.datastore.connect()
        # self.datastore.init()

    def tearDown(self):
        self.datastore.disconnect()

    def test_getSetting_returns_correct_value(self):
        self.datastore.setSetting("test_key", "test_value")
        self.assertEqual(self.datastore.getSetting("test_key"), "test_value")

    def test_getSetting_returns_none_for_non_existent_key(self):
        self.assertIsNone(self.datastore.getSetting("non_existent_key"))

    def test_setSetting_updates_value(self):
        self.datastore.setSetting("test_key", "test_value")
        self.datastore.setSetting("test_key", "new_value")
        self.assertEqual(self.datastore.getSetting("test_key"), "new_value")

    def test_insertVideo_returns_id(self):
        video_id = self.datastore.insertVideo("test_ref")
        self.assertIsInstance(video_id, int)

    def test_setVideoProcessed_updates_processed_status(self):
        video_id = self.datastore.insertVideo("test_ref")
        self.datastore.setVideoProcessed(video_id)
        videos = self.datastore.getVideos()
        self.assertEqual(videos[0][0], video_id)
        self.assertEqual(videos[0][1], "test_ref")

    def test_getVideos_returns_all_videos(self):
        self.datastore.insertVideo("test_ref1")
        self.datastore.insertVideo("test_ref2")
        videos = self.datastore.getVideos()
        self.assertEqual(len(videos), 2)

    def test_getVideo_returns_correct_video(self):
        video_id = self.datastore.insertVideo("test_ref")
        video = self.datastore.getVideo(video_id)
        self.assertEqual(video["ref_vid"], "test_ref")
        self.assertEqual(video["id"], video_id)

    def test_getDetections_returns_empty_dict_for_no_detections(self):
        video_id = self.datastore.insertVideo("test_ref")
        detections = self.datastore.getDetectionsCount(video_id)
        self.assertEqual(detections, {})

    def test_autoincrement(self):
        video_id1 = self.datastore.insertVideo("test_ref1")
        video_id2 = self.datastore.insertVideo("test_ref2")
        self.assertEqual(video_id1 + 1, video_id2)

    def test_latest_video_is_first(self):
        video_id1 = self.datastore.insertVideo("test_ref1")
        video_id2 = self.datastore.insertVideo("test_ref2")
        videos = self.datastore.getVideos()
        self.assertEqual(videos[0][0], video_id2)
        self.assertEqual(videos[1][0], video_id1)

    def test_singleton(self):
        ds1 = DataStore()
        ds2 = DataStore()
        self.assertIs(ds1, ds2)

    def test_insert_multiple_detections_correctly(self):
        video_id = self.datastore.insertVideo("test_ref")
        detections = {"fish1": [1, 2, 3], "fish2": [4, 5, 6]}
        self.datastore.insertDetectionsMap(video_id, detections)
        actual_detections = self.datastore.getDetections(video_id)
        self.assertEqual(len(actual_detections), 6)

    def test_handle_empty_detections_map(self):
        video_id = self.datastore.insertVideo("test_ref")
        detections = {}
        self.datastore.insertDetectionsMap(video_id, detections)
        actual_detections = self.datastore.getDetections(video_id)
        self.assertEqual(len(actual_detections), 0)

    def test_raise_exception_when_no_video_provided_for_detections(self):
        with self.assertRaises(Exception):
            self.datastore.insertDetectionsMap(None, {"fish1": [1, 2, 3]})

    def test_raise_exception_when_no_video_provided_for_getDetections(self):
        with self.assertRaises(Exception):
            self.datastore.getDetections(None)

    def test_return_correct_detections_count(self):
        video_id = self.datastore.insertVideo("test_ref")
        detections = {"fish1": [1, 2, 3], "fish2": [4, 5, 6]}
        self.datastore.insertDetectionsMap(video_id, detections)
        actual_detections_count = self.datastore.getDetectionsCount(video_id)
        self.assertEqual(actual_detections_count, {"fish1": 3, "fish2": 3})

    def test_return_empty_dict_for_video_with_no_detections(self):
        video_id = self.datastore.insertVideo("test_ref")
        actual_detections_count = self.datastore.getDetectionsCount(video_id)
        self.assertEqual(actual_detections_count, {})

    def test_raise_exception_when_no_video_provided_for_getDetectionsCount(self):
        with self.assertRaises(Exception):
            self.datastore.getDetectionsCount(None)


if __name__ == '__main__':
    unittest.main()