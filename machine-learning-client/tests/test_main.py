
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import io
import base64
import tempfile
import pytest
from app.main import app

# 模拟图像（可以替换为任意小图片的 base64 编码）
DUMMY_IMAGE_PATH = "tests/test_image.jpg"

@pytest.fixture
def client():
    app.config["TESTING"] = True
    client = app.test_client()
    yield client

def test_analyze_success(client, monkeypatch):
    # 生成一张测试图像并编码为 base64
    with open(DUMMY_IMAGE_PATH, "rb") as img_file:
        img_bytes = img_file.read()
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")
    data = {"image": f"data:image/jpeg;base64,{img_base64}"}

    # 模拟 DeepFace.analyze 的返回值
    fake_result = [{
        "dominant_emotion": "happy",
        "emotion": {"happy": 0.95, "sad": 0.01, "neutral": 0.04}
    }]
    monkeypatch.setattr("app.main.DeepFace.analyze", lambda *args, **kwargs: fake_result)

    response = client.post("/analyze", json=data)
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data["dominant_emotion"] == "happy"
    assert "emotion_scores" in json_data

def test_analyze_missing_image_key(client):
    response = client.post("/analyze", json={})
    assert response.status_code == 500
    assert "error" in response.get_json()

def test_analyze_invalid_base64(client):
    data = {"image": "data:image/jpeg;base64,INVALIDBASE64"}
    response = client.post("/analyze", json=data)
    assert response.status_code == 500
    assert "error" in response.get_json()
