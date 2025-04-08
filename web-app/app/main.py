"""Main application file for Flask server serving emotion data."""

from flask import Flask, render_template, send_from_directory
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://mongo:27017/")

db = client["emotion_db"]
collection = db["emotions"]


@app.route("/")
def index():
    """Render the homepage with latest emotion records."""
    try:
        records = list(collection.find().sort("timestamp", -1))
        return render_template("index.html", records=records)
    except Exception as e:  # pylint: disable=broad-exception-caught
        app.logger.error("Error in index(): %s - %s", type(e).__name__, e)
        return render_template("error.html", error=str(e))


@app.route("/images/<path:filename>")
def serve_image(filename):
    """Serve the image file from the client image directory."""
    try:
        return send_from_directory("../machine-learning-client/images", filename)
    except Exception as e:  # pylint: disable=broad-exception-caught
        app.logger.error("Error in serve_image(): %s - %s", type(e).__name__, e)
        return "Image not found", 404


if __name__ == "__main__":
    try:
        app.run(debug=True, host="0.0.0.0", port=5000)
    except Exception as e:  # pylint: disable=broad-exception-caught
        app.logger.error("Error starting Flask app: %s - %s", type(e).__name__, e)
