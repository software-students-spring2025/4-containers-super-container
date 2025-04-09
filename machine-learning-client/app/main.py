# Import necessary modules
from flask import Flask, request, jsonify
import os
import cv2
import base64
import uuid
from deepface import DeepFace

# Initialize Flask application
app = Flask(__name__)

# Set upload folder and create a new one if it doesn't exist
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Route handles POST requests to analyze facial emotions
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        # Parse the image data from the incoming JSON
        data = request.get_json()
        image_data = data["image"].split(",")[1]
        img_bytes = base64.b64decode(image_data)

        # Save the image to the uploads directory with a unique filename
        filename = f"{uuid.uuid4().hex}.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        with open(filepath, "wb") as file:
            file.write(img_bytes)

        # Load the image using OpenCV
        img = cv2.imread(filepath)

        # Analyze the image with DeepFace
        # Set 'enforce_detection' to false to avoid errors on poor-quality images
        result = DeepFace.analyze(img, actions=["emotion"], enforce_detection=False)[0]

        # Return dominant emotion and emotion score dictionary
        return jsonify(
            {
                "dominant_emotion": result["dominant_emotion"],
                "emotion_scores": result["emotion"],
            }
        )

    # Catch and return any unexpected error as JSON with HTTP 500
    except Exception as error:
        return jsonify({"error": str(error)}), 500


# Run the Flask app at port 5002
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
