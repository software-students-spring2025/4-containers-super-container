"""Test suite for main Flask application."""

import pytest
from flask import Flask
import sys, os

# Add the parent directory to sys.path in order to import the app module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.main import app


# Create a test client for Flask
@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


# Test the index route and ensure it loads correctly
def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<html" in response.data  


# Test the analyze route with a successful mock response
def test_analyze_success(client, monkeypatch):
    # Simulates the JSON returned by the ml-client
    dummy_response = {"dominant_emotion": "happy"}

    # Define a MockResponse class
    class MockResponse:
        def json(self):
            return dummy_response

    # Replace requests.post
    monkeypatch.setattr(
        "app.main.requests.post", lambda *args, **kwargs: MockResponse()
    )

    # Simulate a POST request to the /analyze endpoint with fake image data
    response = client.post("/analyze", json={"image": "data:image/jpeg;base64,fake"})
    assert response.status_code == 200
    assert response.get_json() == dummy_response


# Test the analyze route when an error occurs
def test_analyze_failure(client, monkeypatch):
    def raise_error(*args, **kwargs):
        raise requests.exceptions.RequestException("ml-client error")

    monkeypatch.setattr("app.main.requests.post", raise_error)

    # Simulate a POST request to the /analyze endpoint
    response = client.post("/analyze", json={"image": "data:image/jpeg;base64,fake"})
    assert response.status_code == 500  # Should return a server error
    assert "error" in response.get_json()  # Error message should be included
