from flask import Flask, render_template
from pymongo import MongoClient
import base64

app = Flask(__name__)

client = MongoClient("mongodb://mongo:27017/")
db = client["emotion_db"]
collection = db["emotion_records"]

@app.route('/')
def index():
    records = collection.find().sort("timestamp", -1).limit(10)
    data = [
        {
            "image": f"data:image/jpeg;base64,{rec['image']}",
            "emotion": rec["emotion"],
            "timestamp": rec["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
        }
        for rec in records
    ]
    return render_template("index.html", data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)