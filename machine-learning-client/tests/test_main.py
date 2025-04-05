
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import main # pylint: disable=import-error
import base64
import pytest
import mongomock
import numpy as np
from unittest.mock import patch, MagicMock


@pytest.fixture
def dummy_frame():
    # 创建一个模拟的图像帧（灰色图片）
    return np.ones((100, 100, 3), dtype=np.uint8) * 127


def test_encode_image(dummy_frame):
    img_base64 = main.encode_image(dummy_frame)
    assert isinstance(img_base64, str)
    # 解码检查格式
    decoded = base64.b64decode(img_base64)
    assert decoded[:3] == b"\xff\xd8\xff"  # JPEG 文件头


@patch("app.main.DeepFace.analyze")
def test_analyze_emotion(mock_analyze, dummy_frame):
    mock_analyze.return_value = [{"dominant_emotion": "happy"}]
    result = main.analyze_emotion(dummy_frame)
    assert result == "happy"


def test_create_record_structure():
    record = main.create_record("fake_base64", "sad")
    assert "image" in record
    assert "emotion" in record
    assert "timestamp" in record
    assert record["emotion"] == "sad"
    assert isinstance(record["image"], str)


@patch("app.main.encode_image")
@patch("app.main.analyze_emotion")
def test_process_and_store_frame(mock_analyze, mock_encode, dummy_frame):
    # 模拟返回
    mock_analyze.return_value = "angry"
    mock_encode.return_value = "imgdata=="

    collection = mongomock.MongoClient().db.collection
    result = main.process_and_store_frame(dummy_frame, collection)

    assert result["emotion"] == "angry"
    assert collection.count_documents({}) == 1

@patch("app.main.MongoClient")
def test_connect_mongo(mock_mongo):
    mock_collection = MagicMock()
    mock_mongo.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection

    result = main.connect_mongo()

    # 验证最终返回的 collection 对象
    assert result == mock_collection

@patch("app.main.cv2.VideoCapture")
@patch("app.main.process_and_store_frame")
@patch("app.main.connect_mongo")
def test_run_loop_once(mock_connect, mock_process, mock_capture, dummy_frame):
    # 模拟摄像头读取一帧，然后结束
    mock_cap_instance = MagicMock()
    mock_cap_instance.read.side_effect = [(True, dummy_frame), (False, None)]
    mock_capture.return_value = mock_cap_instance

    mock_connect.return_value = mongomock.MongoClient().db.collection

    main.run_loop()

    mock_process.assert_called_once()
    mock_capture.return_value.release.assert_called_once()