"""Main application file for Flask server serving emotion data."""

import os  # Standard library first
from flask import Flask, render_template, send_from_directory  # Third-party
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://mongo:27017/")  # 或 localhost，如在本地测试

db = client["emotion_db"]
collection = db["emotions"]


@app.route("/")
def index():
    try:
        records = list(collection.find().sort("timestamp", -1))
        return render_template("index.html", records=records)
    except Exception as e:
        app.logger.error(f"Error in index(): {type(e).__name__} - {e}")
        return render_template("error.html", error=str(e))


@app.route("/images/<path:filename>")
def serve_image(filename):
    try:
        return send_from_directory("../machine-learning-client/images", filename)
    except Exception as e:
        app.logger.error(f"Error in serve_image(): {type(e).__name__} - {e}")
        return "Image not found", 404


if __name__ == "__main__":
    try:
        app.run(debug=True, host="0.0.0.0", port=5000)
    except Exception as e:
        app.logger.error(f"Error starting Flask app: {type(e).__name__} - {e}")
