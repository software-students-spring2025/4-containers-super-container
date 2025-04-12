"""Flask web application for Emotion Detection System.

This module provides the web interface for emotion detection, handling camera access,
processing images, and displaying analysis results from the ML client.
"""

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import requests

app = Flask(__name__)


client = MongoClient("mongodb://mongo-db:27017/")
db = client["emotion_analysis"]
collection = db["results"]


# MongoDB connection
client = MongoClient("mongodb+srv://js12154:js12154@simpletask.7k4oz.mongodb.net/")
db = client["EmotionDetector"]
collection = db["emotions"]


@app.route("/")
def index():
    """Render the main page with camera interface."""
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    """Process uploaded image and send to ML client for emotion analysis.

    Returns:
        JSON response with emotion analysis results or error message
    """
    data = request.get_json()
    try:
        response = requests.post("http://ml-client:5002/analyze", json=data, timeout=10)
        return jsonify(response.json())
    except Exception as error:
        return jsonify({"error": str(error)}), 500


@app.route("/history")
def history():
    """Retrieve emotion analysis history from database.

    Returns:
        JSON list of past analysis results
    """
    try:
        results = list(collection.find().sort("_id", -1).limit(10))
        for result in results:
            if "_id" in result:
                result["_id"] = str(result["_id"])
        return jsonify(results)
    except Exception as error:
        return jsonify({"error": str(error)}), 500


@app.route("/view-data")
def view_data():
    """Render page with all stored emotion analysis data.

    Returns:
        Rendered HTML template with data
    """
    try:
        data = list(collection.find())
        return render_template("index.html", data=data)
    except Exception as error:
        return f"Error: {str(error)}"


# Start the Flask app on host 0.0.0.0 and port 8888
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
