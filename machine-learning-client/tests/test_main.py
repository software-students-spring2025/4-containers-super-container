import sys
import os

# Add parent directory to Python path so 'app.main' can be imported properly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import os
import pytest
import base64
import json
from app.main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def encode_image(path):
    with open(path, "rb") as img_file:
        b64_str = base64.b64encode(img_file.read()).decode("utf-8")
    return f"data:image/jpeg;base64,{b64_str}"


def test_analyze_real_image(client):
    image_path = "tests/test_image.jpg"  # 你自己的测试图像路径
    assert os.path.exists(image_path), "测试图像不存在！"

    image_data = encode_image(image_path)

    response = client.post(
        "/analyze",
        data=json.dumps({"image": image_data}),
        content_type="application/json",
    )

    assert response.status_code in (200, 500)  # 如果模型出错，也能抓住
    data = response.get_json()
    if response.status_code == 200:
        assert "dominant_emotion" in data
        assert "emotion_scores" in data
    else:
        assert "error" in data
