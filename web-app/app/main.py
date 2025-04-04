from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://mongodb:27017/")
db = client["ml_database"]
collection = db["image_analysis"]

@app.route("/")
def index():
    data = list(collection.find({}, {"_id": 0}))
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
