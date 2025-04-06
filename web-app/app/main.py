from flask import Flask, render_template, send_from_directory
from pymongo import MongoClient
import os

app = Flask(__name__)
client = MongoClient("mongodb://mongo:27017/")  # 或 localhost，如在本地测试

db = client["emotion_db"]
collection = db["emotions"]

@app.route('/')
def index():
    records = list(collection.find().sort("timestamp", -1))
    return render_template("index.html", records=records)

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory("../machine-learning-client/images", filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)