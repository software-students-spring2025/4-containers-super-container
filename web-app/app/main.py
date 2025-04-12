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


# Route for the homepage
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    try:
        response = requests.post("http://ml-client:5002/analyze", json=data)
        return jsonify(response.json())
    except Exception as error:
        return jsonify({"error": str(error)}), 500


# Load data history
@app.route("/view-data")
def view_data():
    try:
        data = list(collection.find())
        return render_template("index.html", data=data)
    except Exception as error:
        return f"Error: {str(error)}"


# Start the Flask app on host 0.0.0.0 and port 8888
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
