"""Test suite for main Flask application."""

import sys
import os
import pytest
from unittest.mock import patch

# 添加 app 路径到导入路径中
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app"))
)

from main import app, collection  # pylint: disable=import-error


@pytest.fixture
def client_fixture():
    """Create a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_route(client_fixture):
    """Test the index route with mocked database records."""
    mock_record = {
        "timestamp": "2025-04-06T12:00:00Z",
        "dominant_emotion": "happy",
        "image_path": "images/fake.jpg",
    }

    with patch.object(collection, "find") as mock_find:
        mock_find.return_value.sort.return_value = [mock_record]
        response = client_fixture.get("/")
        assert response.status_code == 200
        assert b"happy" in response.data
        assert b"images/fake.jpg" in response.data


def test_serve_image_route(client_fixture):
    """Test the image-serving route with mock send_from_directory."""
    with patch("main.send_from_directory") as mock_send:
        mock_send.return_value = "mocked image"
        response = client_fixture.get("/images/fake.jpg")
        assert response.status_code == 200
