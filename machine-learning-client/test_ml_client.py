#!/usr/bin/env python3
"""
Tests for the Machine Learning Client
"""

import unittest
from unittest.mock import patch, MagicMock
import datetime
from main import (
    generate_sensor_data,
    analyze_data,
    save_to_mongodb,
    connect_to_mongodb,
)


class TestMlClient(unittest.TestCase):
    """Tests for the Machine Learning Client functions"""

    def test_generate_sensor_data(self):
        """Test the sensor data generation function"""
        sensor_data = generate_sensor_data()

        # Check that all expected keys exist
        self.assertIn("temperature", sensor_data)
        self.assertIn("humidity", sensor_data)
        self.assertIn("timestamp", sensor_data)

        # Check that values are within expected ranges
        self.assertTrue(15.0 <= sensor_data["temperature"] <= 40.0)
        self.assertTrue(30.0 <= sensor_data["humidity"] <= 90.0)
        self.assertIsInstance(sensor_data["timestamp"], datetime.datetime)

    def test_analyze_data_hot(self):
        """Test analyze_data function with hot temperature"""
        # Create test sensor data with hot temperature
        sensor_data = {
            "temperature": 35.0,
            "humidity": 60.0,
            "timestamp": datetime.datetime.now(),
        }

        result = analyze_data(sensor_data)

        # Check results
        self.assertEqual(result["temperature_status"], "Hot")
        self.assertEqual(result["humidity_status"], "Normal")
        self.assertIn(
            result["ml_environment_prediction"], ["Cold", "Comfortable", "Hot"]
        )
        self.assertTrue(0 <= result["confidence"] <= 100)
        self.assertIsInstance(result["analyzed_at"], datetime.datetime)

    def test_analyze_data_cold(self):
        """Test analyze_data function with cold temperature"""
        # Create test sensor data with cold temperature
        sensor_data = {
            "temperature": 16.0,
            "humidity": 45.0,
            "timestamp": datetime.datetime.now(),
        }

        result = analyze_data(sensor_data)

        # Check results
        self.assertEqual(result["temperature_status"], "Cold")
        self.assertEqual(result["humidity_status"], "Normal")
        self.assertIn(
            result["ml_environment_prediction"], ["Cold", "Comfortable", "Hot"]
        )
        self.assertTrue(0 <= result["confidence"] <= 100)

    def test_analyze_data_normal(self):
        """Test analyze_data function with normal temperature"""
        # Create test sensor data with normal temperature
        sensor_data = {
            "temperature": 25.0,
            "humidity": 50.0,
            "timestamp": datetime.datetime.now(),
        }

        result = analyze_data(sensor_data)

        # Check results
        self.assertEqual(result["temperature_status"], "Normal")
        self.assertEqual(result["humidity_status"], "Normal")
        self.assertIn(
            result["ml_environment_prediction"], ["Cold", "Comfortable", "Hot"]
        )
        self.assertTrue(0 <= result["confidence"] <= 100)

    @patch("pymongo.MongoClient")  # 注意 patch 的路径要根据 main.py 的实际导入路径
    def test_connect_to_mongodb(self, mock_client):
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_client.return_value.__getitem__.return_value = mock_db
        mock_db.__getitem__.return_value = mock_collection

        result = connect_to_mongodb()

        self.assertEqual(result, mock_collection)

    @patch("pymongo.collection.Collection.insert_one")
    def test_save_to_mongodb(self, mock_insert):
        """Test saving data to MongoDB"""
        # Setup mocks
        mock_collection = MagicMock()
        mock_insert.return_value.inserted_id = "test_id"
        mock_collection.insert_one.return_value.inserted_id = "test_id"

        # Test data
        sensor_data = {"temperature": 25.0, "humidity": 50.0}
        analysis_result = {"temperature_status": "Normal"}
        data = {**sensor_data, **analysis_result}  #

        # Call function
        result = save_to_mongodb(mock_collection, data)

        # Verify
        self.assertEqual(result, "test_id")
        mock_collection.insert_one.assert_called_once()
        # Check that insert_one was called with the correct merged data
        args, _ = mock_collection.insert_one.call_args
        self.assertEqual(args[0]["temperature"], 25.0)
        self.assertEqual(args[0]["humidity"], 50.0)
        self.assertEqual(args[0]["temperature_status"], "Normal")
