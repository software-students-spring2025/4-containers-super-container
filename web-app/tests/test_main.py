"""Test suite for main Flask application."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from flask import Flask
from unittest.mock import patch, MagicMock
import app.main
from app.main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    """测试主页渲染"""
    response = client.get("/")
    assert response.status_code == 200


@patch("app.main.requests.post")
def test_analyze_success(mock_post, client):
    """模拟转发成功"""
    mock_post.return_value.json.return_value = {
        "dominant_emotion": "happy",
        "emotion_scores": {"happy": 99.0, "sad": 1.0},
    }
    mock_post.return_value.status_code = 200

    response = client.post("/analyze", json={"image": "test"})
    assert response.status_code == 200
    assert "dominant_emotion" in response.json


@patch("app.main.requests.post", side_effect=Exception("ml-client error"))
def test_analyze_failure(mock_post, client):
    """模拟转发失败"""
    response = client.post("/analyze", json={"image": "test"})
    assert response.status_code == 500
    assert "error" in response.json


@patch("app.main.collection.find")
def test_history_success(mock_find, client):
    """测试历史记录读取"""
    mock_find.return_value.sort.return_value.limit.return_value = [
        {"_id": "fakeid", "dominant_emotion": "angry"}
    ]
    response = client.get("/history")
    assert response.status_code == 200
    assert isinstance(response.json, list)


@patch("app.main.collection.find", side_effect=Exception("DB error"))
def test_history_failure(mock_find, client):
    """测试历史读取失败情况"""
    response = client.get("/history")
    assert response.status_code == 500
    assert "error" in response.json
