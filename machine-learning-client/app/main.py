"""Client script for capturing images, analyzing emotion, and saving to MongoDB."""

import os
import uuid
from datetime import datetime

import cv2  # pylint: disable=import-error
from deepface import DeepFace  # pylint: disable=import-error
from pymongo import MongoClient  # pylint: disable=import-error

IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)


def capture_image():
    """Capture an image from webcam using OpenCV."""
    try:
        cap = cv2.VideoCapture(0)  # pylint: disable=no-member
        ret, frame = cap.read()
        cap.release()
        if not ret:
            raise RuntimeError("Unable to capture from camera")
        return frame
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"❌ ERROR in capture_image(): {type(e).__name__} - {e}")
        raise


def analyze_emotion(image):
    """Analyze the emotion from an image using DeepFace."""
    try:
        result = DeepFace.analyze(image, actions=["emotion"], enforce_detection=False)
        return {
            "dominant_emotion": result[0]["dominant_emotion"],
            "emotion_scores": result[0]["emotion"],
        }
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"❌ ERROR in analyze_emotion(): {type(e).__name__} - {e}")
        raise


def save_image_to_file(image):
    """Save the captured image to disk and return its path."""
    try:
        filename = f"{uuid.uuid4().hex}.jpg"
        filepath = os.path.join(IMAGE_DIR, filename)
        max_dim = 300
        height, width = image.shape[:2]
        if max(height, width) > max_dim:
            scale = max_dim / max(height, width)
            image = cv2.resize(  # pylint: disable=no-member
                image, (int(width * scale), int(height * scale))
            )
        cv2.imwrite(filepath, image)  # pylint: disable=no-member
        return filepath
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"❌ ERROR in save_image_to_file(): {type(e).__name__} - {e}")
        raise


def save_analysis(image, analysis_result):
    """Save the analysis result and image path to MongoDB."""
    try:
        filepath = save_image_to_file(image)
        emotion_scores_raw = analysis_result["emotion_scores"]
        emotion_scores_clean = {k: float(v) for k, v in emotion_scores_raw.items()}

        client = MongoClient("mongodb://localhost:27017/")
        db = client["emotion_db"]
        collection = db["emotions"]

        doc = {
            "timestamp": datetime.utcnow(),
            "image_path": filepath,
            "dominant_emotion": analysis_result["dominant_emotion"],
            "emotion_scores": emotion_scores_clean,
        }

        collection.insert_one(doc)
        print(
            f"✅ Saved: {filepath} with emotion {analysis_result['dominant_emotion']}"
        )
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"❌ ERROR in save_analysis(): {type(e).__name__} - {e}")
        raise


def run():
    """Run the full process: capture image, analyze, and save."""
    image = capture_image()
    result = analyze_emotion(image)
    save_analysis(image, result)


if __name__ == "__main__":
    try:
        run()
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"❌ ERROR in run(): {type(e).__name__} - {e}")
