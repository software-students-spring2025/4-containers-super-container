"""Test suite for main Flask application."""

import pytest
from flask import Flask
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<html" in response.data  # 或者你可以检查标题、内容等


def test_analyze_success(client, monkeypatch):
    # 模拟 ml-client 返回的 JSON
    dummy_response = {"dominant_emotion": "happy"}

    class MockResponse:
        def json(self):
            return dummy_response

    # 替换 requests.post
    monkeypatch.setattr(
        "app.main.requests.post", lambda *args, **kwargs: MockResponse()
    )

    response = client.post("/analyze", json={"image": "data:image/jpeg;base64,fake"})
    assert response.status_code == 200
    assert response.get_json() == dummy_response


def test_analyze_failure(client, monkeypatch):
    def raise_error(*args, **kwargs):
        raise requests.exceptions.RequestException("ml-client error")

    monkeypatch.setattr("app.main.requests.post", raise_error)

    response = client.post("/analyze", json={"image": "data:image/jpeg;base64,fake"})
    assert response.status_code == 500
    assert "error" in response.get_json()
