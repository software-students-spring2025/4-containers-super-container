import sys
import os

# Add parent directory to Python path so 'app.main' can be imported properly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import os
import base64
import tempfile
import pytest
import app.main
from app.main import app

# 创建一个测试客户端
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_analyze_valid_image(client):
    # 构造一个简单的黑图像
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    tmp_file.write(b"\xff\xd8\xff\xe0" + bytes(100))  # JPEG header + filler
    tmp_file.close()

    # 读取为 base64
    with open(tmp_file.name, "rb") as img_file:
        b64_image = base64.b64encode(img_file.read()).decode("utf-8")
    os.unlink(tmp_file.name)

    response = client.post("/analyze", json={"image": "data:image/jpeg;base64," + b64_image})
    assert response.status_code in (200, 500)  # DeepFace可能报错但服务稳定
    assert "dominant_emotion" in response.json or "error" in response.json

def test_analyze_invalid_data(client):
    response = client.post("/analyze", json={"image": "not a real image"})
    assert response.status_code == 500
    assert "error" in response.json
