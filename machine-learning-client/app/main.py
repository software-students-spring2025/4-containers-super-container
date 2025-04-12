from flask import Flask, request, jsonify
import os
import cv2
import base64
import uuid
from deepface import DeepFace
from pymongo import MongoClient
import datetime

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 连接 MongoDB（容器名为 mongo-db）
client = MongoClient("mongodb://mongo-db:27017/")
db = client["emotion_analysis"]
collection = db["results"]


# MongoDB connection
MONGO_URI = "mongodb+srv://js12154:js12154@simpletask.7k4oz.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["EmotionDetector"]
collection = db["emotions"]


# Route handles POST requests to analyze facial emotions
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

        # Prepare record
        dom = {"dominant_emotion": result["dominant_emotion"]}
        emo = result["emotion"]
        time = {"timestamp": datetime.datetime.utcnow()}
        merge = dom | emo | time
        insert = collection.insert_one(merge)
        print(insert)

        # Return dominant emotion and emotion score dictionary
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
