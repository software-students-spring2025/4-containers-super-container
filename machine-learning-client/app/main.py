from flask import Flask, request, jsonify
import os
import cv2
import base64
import uuid
from deepface import DeepFace
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 连接 MongoDB（容器名为 mongo-db）
client = MongoClient("mongodb://mongo-db:27017/")
db = client["emotion_analysis"]
collection = db["results"]


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        image_data = data["image"].split(",")[1]
        img_bytes = base64.b64decode(image_data)

        filename = f"{uuid.uuid4().hex}.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        with open(filepath, "wb") as file:
            file.write(img_bytes)

        img = cv2.imread(filepath)
        result = DeepFace.analyze(img, actions=["emotion"], enforce_detection=False)[0]

        # 保存到 MongoDB
        record = {
            "timestamp": datetime.utcnow(),
            "dominant_emotion": result["dominant_emotion"],
            "emotion_scores": result["emotion"],
            "image_path": filename,
        }
        collection.insert_one(record)

        return jsonify(
            {
                "dominant_emotion": result["dominant_emotion"],
                "emotion_scores": result["emotion"],
            }
        )

    except Exception as error:
        return jsonify({"error": str(error)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)