"""Mock-based tests for the machine learning client."""

import os
import sys
import json
import base64
import unittest
from unittest.mock import patch, MagicMock, mock_open

# Mock modules before importing the app
sys.modules['cv2'] = MagicMock()
sys.modules['deepface'] = MagicMock()
sys.modules['deepface.DeepFace'] = MagicMock()
sys.modules['pymongo'] = MagicMock()
sys.modules['pymongo.MongoClient'] = MagicMock()
sys.modules['numpy'] = MagicMock()
sys.modules['random'] = MagicMock()

# Add parent directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Now import the app with mocked dependencies
import app.main
from app.main import app


class TestMLClient(unittest.TestCase):
    """Test suite for the ML client using mocks."""

    def setUp(self):
        """Set up test client."""
        self.app = app.test_client()
        # Configure app for testing
        app.config['TESTING'] = True

    @patch('app.main.DeepFace.analyze')
    @patch('app.main.cv2.imread')
    @patch('app.main.collection.insert_one')
    @patch('builtins.open', new_callable=mock_open, read_data=b'test_image_content')
    @patch('os.path.join')
    @patch('uuid.uuid4')
    def test_analyze_success(self, mock_uuid, mock_path_join, mock_file_open, mock_insert, 
                            mock_imread, mock_deepface_analyze):
        """Test successful image analysis."""
        # Mock UUID
        mock_uuid.return_value.hex = 'test_uuid'
        
        # Mock file path
        mock_path_join.return_value = 'uploads/test_uuid.jpg'
        
        # Mock image reading
        mock_imread.return_value = 'fake_image_data'
        
        # Mock DeepFace analysis result
        mock_deepface_analyze.return_value = [{
            'dominant_emotion': 'happy',
            'emotion': {
                'happy': 95.0,
                'sad': 2.0,
                'neutral': 1.0,
                'fear': 0.5,
                'angry': 0.5,
                'surprise': 0.5,
                'disgust': 0.5
            },
            'region': {'x': 0, 'y': 0, 'w': 320, 'h': 240},
            'face_confidence': 0.99
        }]
        
        # Mock MongoDB insertion
        insert_result = MagicMock()
        insert_result.inserted_id = "test_id"
        mock_insert.return_value = insert_result
        
        # Test data
        test_image_base64 = base64.b64encode(b'test_image_content').decode('utf-8')
        
        # Make request to the analyze endpoint
        response = self.app.post(
            '/analyze',
            json={'image': f'data:image/jpeg;base64,{test_image_base64}'},
            content_type='application/json'
        )
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['dominant_emotion'], 'happy')
        self.assertEqual(data['emotion_scores']['happy'], 95.0)
        
        # Verify mocks were called correctly
        mock_path_join.assert_called_once()
        mock_file_open.assert_called_once()
        mock_imread.assert_called_once_with('uploads/test_uuid.jpg')
        mock_deepface_analyze.assert_called_once()
        mock_insert.assert_called_once()

    @patch('builtins.open', side_effect=IOError("Failed to write file"))
    def test_analyze_file_write_error(self, mock_open):
        """Test error handling when file writing fails."""
        # Create test data
        test_image_base64 = base64.b64encode(b'test_image_content').decode('utf-8')
        
        # Make request to the analyze endpoint
        response = self.app.post(
            '/analyze',
            json={'image': f'data:image/jpeg;base64,{test_image_base64}'},
            content_type='application/json'
        )
        
        # Verify response
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertIn('error', data)

    @patch('app.main.cv2.imread', return_value=None)
    @patch('builtins.open', new_callable=mock_open)
    def test_analyze_image_read_error(self, mock_open, mock_imread):
        """Test error handling when image reading fails."""
        # Create test data
        test_image_base64 = base64.b64encode(b'test_image_content').decode('utf-8')
        
        # Make request to the analyze endpoint
        response = self.app.post(
            '/analyze',
            json={'image': f'data:image/jpeg;base64,{test_image_base64}'},
            content_type='application/json'
        )
        
        # Verify response
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertIn('error', data)

    @patch('app.main.DeepFace.analyze', side_effect=Exception("Analysis failed"))
    @patch('app.main.cv2.imread')
    @patch('builtins.open', new_callable=mock_open)
    def test_analyze_deepface_error(self, mock_open, mock_imread, mock_deepface_analyze):
        """Test error handling when DeepFace analysis fails."""
        # Create test data
        test_image_base64 = base64.b64encode(b'test_image_content').decode('utf-8')
        
        # Make request to the analyze endpoint
        response = self.app.post(
            '/analyze',
            json={'image': f'data:image/jpeg;base64,{test_image_base64}'},
            content_type='application/json'
        )
        
        # Verify response
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_analyze_invalid_request(self):
        """Test error handling for invalid request format."""
        # Test with missing image field
        response = self.app.post(
            '/analyze',
            json={'not_image': 'invalid_data'},
            content_type='application/json'
        )
        
        # Verify response
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_analyze_invalid_base64(self):
        """Test error handling for invalid base64 data."""
        # Test with invalid base64 data
        response = self.app.post(
            '/analyze',
            json={'image': 'not-valid-base64-data'},
            content_type='application/json'
        )
        
        # Verify response
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertIn('error', data)


if __name__ == '__main__':
    unittest.main() 