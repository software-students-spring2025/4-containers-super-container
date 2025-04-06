import os
import pytest
import numpy as np
import cv2
from unittest.mock import patch, MagicMock
import app.main as main  # pylint: disable=import-error


def test_capture_image_mock(monkeypatch):
    # 模拟摄像头返回
    class DummyCapture:
        def read(self):
            return True, "fake_frame"

        def release(self):
            pass

    monkeypatch.setattr("cv2.VideoCapture", lambda _: DummyCapture())
    frame = main.capture_image()
    assert frame == "fake_frame"


def test_analyze_emotion_mock():
    # 模拟 DeepFace 返回情绪分析
    with patch("app.main.DeepFace.analyze") as mock_analyze:
        mock_analyze.return_value = [
            {
                "dominant_emotion": "happy",
                "emotion": {"happy": np.float32(95.5), "sad": np.float32(3.2)},
            }
        ]
        result = main.analyze_emotion("dummy_img")
        assert result["dominant_emotion"] == "happy"
        assert isinstance(result["emotion_scores"]["happy"], np.float32)


def test_save_image_to_file_creates_image(tmp_path):
    dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)
    # 改变保存路径
    old_dir = main.IMAGE_DIR
    main.IMAGE_DIR = tmp_path
    path = main.save_image_to_file(dummy_image)
    assert os.path.exists(path)
    main.IMAGE_DIR = old_dir


def test_save_analysis(monkeypatch, tmp_path):
    dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)
    dummy_result = {
        "dominant_emotion": "sad",
        "emotion_scores": {"happy": np.float32(88.8), "sad": np.float32(11.2)},
    }

    # 模拟 MongoDB 插入
    class DummyCollection:
        def insert_one(self, doc):
            assert isinstance(doc["timestamp"], object)
            assert doc["dominant_emotion"] == "sad"
            assert isinstance(doc["emotion_scores"]["happy"], float)

    class DummyDB:
        def __getitem__(self, name):
            return DummyCollection()

    class DummyClient:
        def __getitem__(self, name):
            return DummyDB()

    monkeypatch.setattr("app.main.MongoClient", lambda _: DummyClient())

    # 设置临时图像目录
    old_dir = main.IMAGE_DIR
    main.IMAGE_DIR = tmp_path
    main.save_analysis(dummy_image, dummy_result)
    main.IMAGE_DIR = old_dir
