#!/usr/bin/env python3
"""
Flask Web App for displaying sensor data and ML analysis results
"""

import os
from flask import Flask, render_template, jsonify
from pymongo import MongoClient

# Create Flask app
app = Flask(__name__)

# MongoDB connection
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "sensor_data"
COLLECTION_NAME = "readings"


def get_mongodb_collection():
    """Connect to MongoDB and return the collection"""
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    return collection


@app.route("/")
def index():
    """Render the home page with latest readings"""
    try:
        collection = get_mongodb_collection()
        # Get the latest 10 readings, sorted by timestamp
        latest_readings = list(collection.find().sort("timestamp", -1).limit(10))

        # Format timestamps for display
        for reading in latest_readings:
            if "timestamp" in reading:
                reading["timestamp"] = reading["timestamp"].strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            if "analyzed_at" in reading:
                reading["analyzed_at"] = reading["analyzed_at"].strftime(
                    "%Y-%m-%d %H:%M:%S %Z"
                )

        return render_template("index.html", readings=latest_readings)
    except Exception as e:
        # Broad exception is acceptable for web views to prevent crashes
        return render_template("error.html", error=str(e))


@app.route("/api/readings")
def get_readings():
    """API endpoint to get readings as JSON"""
    try:
        collection = get_mongodb_collection()
        # Get the latest 50 readings, sorted by timestamp
        readings = list(collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(50))

        # Convert datetime objects to strings for JSON serialization
        for reading in readings:
            if "timestamp" in reading:
                reading["timestamp"] = reading["timestamp"].strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            if "analyzed_at" in reading:
                reading["analyzed_at"] = reading["analyzed_at"].strftime(
                    "%Y-%m-%d %H:%M:%S %Z"
                )

        return jsonify({"success": True, "readings": readings})
    except Exception as e:
        # Broad exception is acceptable for API to return meaningful errors
        return jsonify({"success": False, "error": str(e)})


@app.route("/api/stats")
def get_stats():
    """API endpoint to get statistics about the readings"""
    try:
        collection = get_mongodb_collection()

        # Get the total count of readings
        total_count = collection.count_documents({})

        # Get the latest reading time
        latest_reading = collection.find_one({}, sort=[("timestamp", -1)])
        latest_time = latest_reading.get("timestamp") if latest_reading else None

        # Get counts of different environment predictions
        hot_count = collection.count_documents({"ml_environment_prediction": "Hot"})
        cold_count = collection.count_documents({"ml_environment_prediction": "Cold"})
        comfortable_count = collection.count_documents(
            {"ml_environment_prediction": "Comfortable"}
        )

        stats = {
            "total_readings": total_count,
            "latest_reading_time": latest_time.strftime("%Y-%m-%d %H:%M:%S %Z")
            if latest_time
            else None,
            "environment_counts": {
                "hot": hot_count,
                "cold": cold_count,
                "comfortable": comfortable_count,
            },
        }

        return jsonify({"success": True, "stats": stats})
    except Exception as e:
        # Broad exception is acceptable for API to return meaningful errors
        return jsonify({"success": False, "error": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=5000)
