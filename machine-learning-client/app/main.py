from flask import Flask, request, jsonify
import os
import cv2
import base64
import uuid
from deepface import DeepFace

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        image_data = data["image"].split(",")[1]
        img_bytes = base64.b64decode(image_data)

        filename = f"{uuid.uuid4().hex}.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        with open(filepath, "wb") as f:
            f.write(img_bytes)

        img = cv2.imread(filepath)
        result = DeepFace.analyze(img, actions=["emotion"], enforce_detection=False)[0]

        return jsonify({
            "dominant_emotion": result["dominant_emotion"],
            "emotion_scores": result["emotion"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)