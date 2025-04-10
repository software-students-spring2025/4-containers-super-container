from flask import Flask, render_template, request, jsonify
import requests
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB 连接（容器内）
client = MongoClient("mongodb://mongo-db:27017/")
db = client["emotion_analysis"]
collection = db["results"]


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


@app.route("/history", methods=["GET"])
def history():
    try:
        # 获取最新10条记录
        records = list(collection.find().sort("timestamp", -1).limit(10))
        for record in records:
            record["_id"] = str(record["_id"])
        return jsonify(records)
    except Exception as error:
        return jsonify({"error": str(error)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
