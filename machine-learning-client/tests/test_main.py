import sys
import os

# Add parent directory to Python path so 'app.main' can be imported properly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import io
import base64
import tempfile
import pytest
from app.main import app

# Sample image (can be replace by any base64-encoded image)
DUMMY_IMAGE_PATH = "tests/test_image.jpg"


# Sets the app in testing mode
@pytest.fixture
def client():
    app.config["TESTING"] = True
    client = app.test_client()
    yield client


# Test the /analyze endpoint with valid base64 image input
def test_analyze_success(client, monkeypatch):
    # Load a base64-encoded sample image
    with open(DUMMY_IMAGE_PATH, "rb") as img_file:
        img_bytes = img_file.read()
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")
    data = {"image": f"data:image/jpeg;base64,{img_base64}"}

    # Simulate the return value from DeepFace.analyze
    fake_result = [
        {
            "dominant_emotion": "happy",
            "emotion": {"happy": 0.95, "sad": 0.01, "neutral": 0.04},
        }
    ]
    monkeypatch.setattr(
        "app.main.DeepFace.analyze", lambda *args, **kwargs: fake_result
    )

    # Send the POST request to /analyze and verify response
    response = client.post("/analyze", json=data)
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data["dominant_emotion"] == "happy"
    assert "emotion_scores" in json_data


# Test the /analyze endpoint when the 'image' key is missing
# Should return a 500 error with an appropriate error message
def test_analyze_missing_image_key(client):
    response = client.post("/analyze", json={})
    assert response.status_code == 500
    assert "error" in response.get_json()


# Test the /analyze endpoint with an invalid base64 string
# Should return a 500 error indicating decoding failure
def test_analyze_invalid_base64(client):
    data = {"image": "data:image/jpeg;base64,INVALIDBASE64"}
    response = client.post("/analyze", json=data)
    assert response.status_code == 500
    assert "error" in response.get_json()
