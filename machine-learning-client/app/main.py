"""
main.py - 摄像头图像采集 + 情绪识别 + 存储到 MongoDB
"""

import base64
import time
from datetime import datetime

import cv2
from deepface import DeepFace
from pymongo import MongoClient


def connect_mongo():
    client = MongoClient("mongodb://mongo:27017/")
    db = client["emotion_db"]
    return db["emotion_records"]


def analyze_emotion(frame):
    result = DeepFace.analyze(
        frame, actions=["emotion"], enforce_detection=False
    )
    return result[0]["dominant_emotion"]


def encode_image(frame):
    _, buffer = cv2.imencode(".jpg", frame)  # pylint: disable=no-member
    return base64.b64encode(buffer).decode("utf-8")


def create_record(img_base64, emotion):
    return {
        "image": img_base64,
        "emotion": emotion,
        "timestamp": datetime.now(),
    }


def process_and_store_frame(frame, collection):
    emotion = analyze_emotion(frame)
    img_base64 = encode_image(frame)
    record = create_record(img_base64, emotion)
    collection.insert_one(record)
    print(f"[{record['timestamp']}] Emotion: {emotion}")
    return record


def run_loop():
    collection = connect_mongo()
    cap = cv2.VideoCapture(0)  # pylint: disable=no-member

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        try:
            process_and_store_frame(frame, collection)
            time.sleep(5)
        except Exception as err:  # pylint: disable=broad-exception-caught
            print("Error:", err)

    cap.release()


if __name__ == "__main__":
    run_loop()