#!/usr/bin/env python3
"""
Tests for the Flask Web App
"""

import unittest
from unittest.mock import patch, MagicMock
import json
import pytest
from app import app


@pytest.fixture
def test_client():
    """Create a test client for the Flask app"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestApp(unittest.TestCase):
    """Tests for the Flask Web App"""

    def setUp(self):
        """Set up the test client"""
        app.config["TESTING"] = True
        self.client = app.test_client()

    @patch("app.get_mongodb_collection")
    def test_index_route(self, mock_get_collection):
        """Test the index route"""
        # Create a mock collection with sample data
        mock_collection = MagicMock()
        mock_readings = [
            {
                "temperature": 25.5,
                "humidity": 60.0,
                "light_level": 500.0,
                "timestamp": MagicMock(),
                "temperature_status": "Normal",
                "humidity_status": "Normal",
                "ml_environment_prediction": "Comfortable",
                "confidence": 95.5,
                "analyzed_at": MagicMock(),
            }
        ]

        # Set up the mock to return our test data
        mock_collection.find.return_value.sort.return_value.limit.return_value = (
            mock_readings
        )
        mock_get_collection.return_value = mock_collection

        # Mock the timestamp strftime method
        mock_readings[0]["timestamp"].strftime.return_value = "2023-01-01 12:00:00"
        mock_readings[0]["analyzed_at"].strftime.return_value = "2023-01-01 12:00:01"

        # Make the request
        response = self.client.get("/")

        # Check the response
        self.assertEqual(response.status_code, 200)

        # Verify the mocks were called correctly
        mock_get_collection.assert_called_once()
        mock_collection.find.assert_called_once()
        mock_collection.find.return_value.sort.assert_called_once_with("timestamp", -1)
        mock_collection.find.return_value.sort.return_value.limit.assert_called_once_with(
            10
        )

    @patch("app.get_mongodb_collection")
    def test_api_readings_route(self, mock_get_collection):
        """Test the API readings route"""
        # Create a mock collection with sample data
        mock_collection = MagicMock()
        mock_readings = [
            {
                "temperature": 25.5,
                "humidity": 60.0,
                "light_level": 500.0,
                "timestamp": MagicMock(),
                "temperature_status": "Normal",
                "humidity_status": "Normal",
                "ml_environment_prediction": "Comfortable",
                "confidence": 95.5,
                "analyzed_at": MagicMock(),
            }
        ]

        # Set up the mock to return our test data
        mock_collection.find.return_value.sort.return_value.limit.return_value = (
            mock_readings
        )
        mock_get_collection.return_value = mock_collection

        # Mock the timestamp strftime method
        mock_readings[0]["timestamp"].strftime.return_value = "2023-01-01 12:00:00"
        mock_readings[0]["analyzed_at"].strftime.return_value = "2023-01-01 12:00:01"

        # Make the request
        response = self.client.get("/api/readings")

        # Check the response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data["success"])
        self.assertIn("readings", data)

        # Verify the mocks were called correctly
        mock_get_collection.assert_called_once()

    @patch("app.get_mongodb_collection")
    def test_api_stats_route(self, mock_get_collection):
        """Test the API stats route"""
        # Create a mock collection
        mock_collection = MagicMock()
        mock_collection.count_documents.side_effect = [
            10,  # total readings
            3,  # hot readings
            2,  # cold readings
            5,  # comfortable readings
        ]

        # Set up the mock for latest reading
        mock_latest = {"timestamp": MagicMock()}
        mock_latest["timestamp"].strftime.return_value = "2023-01-01 12:00:00"
        mock_collection.find_one.return_value = mock_latest

        mock_get_collection.return_value = mock_collection

        # Make the request
        response = self.client.get("/api/stats")

        # Check the response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data["success"])
        self.assertIn("stats", data)
        self.assertEqual(data["stats"]["total_readings"], 10)
        self.assertEqual(data["stats"]["environment_counts"]["hot"], 3)
        self.assertEqual(data["stats"]["environment_counts"]["cold"], 2)
        self.assertEqual(data["stats"]["environment_counts"]["comfortable"], 5)

        # Verify the mocks were called correctly
        mock_get_collection.assert_called_once()

    @patch("app.get_mongodb_collection")
    def test_index_route_db_error(self, mock_get_collection):
        """Test the index route when database error occurs"""
        # Make the mock raise an exception
        mock_get_collection.side_effect = Exception("Database error")

        # Make the request
        response = self.client.get("/")

        # Check the response - should still return 200 but with error template
        self.assertEqual(response.status_code, 200)

        # Check that response contains error message
        self.assertIn(b"Database error", response.data)

        # Verify the mock was called
        mock_get_collection.assert_called_once()