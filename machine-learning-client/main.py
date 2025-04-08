#!/usr/bin/env python3
"""
Machine Learning Client for the container app.
This module simulates sensor data collection, performs simple analysis,
and saves results to MongoDB.
"""

import time
import random
import datetime
import os
import logging
from pymongo import MongoClient
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import requests
import pytz

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("ml-client")

# MongoDB connection
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "sensor_data"
COLLECTION_NAME = "readings"


def connect_to_mongodb():
    """Connect to MongoDB and return the collection object."""
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        logger.info("Successfully connected to MongoDB")
        return collection
    except Exception as e:
        logger.error("Failed to connect to MongoDB: %s", e)
        raise


def generate_sensor_data():
    """获取真实天气数据"""
    # 直接使用原来有效的API密钥
    API_KEY = os.getenv("WEATHER_API_KEY")
    city = "New York"  # 可以改为任何城市
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url, timeout=10)  # 添加10秒超时
        data = response.json()

        # 提取需要的数据
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        # 直接使用云量百分比
        cloud_percent = data.get("clouds", {}).get("all", 0)  # 云量百分比 0-100

        # 使用纽约时区
        ny_timezone = pytz.timezone("America/New_York")
        now = datetime.datetime.now(datetime.timezone.utc).astimezone(ny_timezone)

        sensor_data = {
            "temperature": temperature,
            "humidity": humidity,
            "cloud_cover": cloud_percent,  # 云量百分比
            "timestamp": now,
        }

        logger.info("Retrieved weather data: %s", sensor_data)
        return sensor_data
    except Exception as e:
        logger.error("API raw response: %s", response.text)
        logger.error("Failed to get weather data: %s", e)
        # 出错时回退到随机生成数据
        return generate_random_data()


def generate_random_data():
    """生成随机数据作为备份"""
    temperature = round(random.uniform(15.0, 40.0), 2)
    humidity = round(random.uniform(30.0, 90.0), 2)
    cloud_cover = round(random.uniform(0.0, 100.0), 0)  # 云量百分比 0-100

    # 使用纽约时区
    ny_timezone = pytz.timezone("America/New_York")
    now = datetime.datetime.now(datetime.timezone.utc).astimezone(ny_timezone)

    return {
        "temperature": temperature,
        "humidity": humidity,
        "cloud_cover": cloud_cover,
        "timestamp": now,
    }


def analyze_data(sensor_data):
    """Analyze the data."""
    temperature = sensor_data["temperature"]
    humidity = sensor_data["humidity"]

    if temperature > 30:
        temp_status = "Hot"
    elif temperature < 20:
        temp_status = "Cold"
    else:
        temp_status = "Normal"

    if humidity > 70:
        humidity_status = "Humid"
    elif humidity < 40:
        humidity_status = "Dry"
    else:
        humidity_status = "Normal"

    x_train = np.array(
        [
            [15, 40],
            [18, 45],
            [20, 50],
            [22, 55],
            [25, 60],
            [28, 65],
            [30, 70],
            [33, 75],
            [35, 80],
            [38, 85],
        ]
    )
    y_train = np.array([0, 0, 1, 1, 1, 1, 2, 2, 2, 2])

    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(x_train, y_train)

    features = np.array([[temperature, humidity]])
    prediction = model.predict(features)[0]

    ml_prediction = {0: "Cold", 1: "Comfortable", 2: "Hot"}[prediction]

    confidence = round(max(model.predict_proba(features)[0]) * 100, 2)

    ny_timezone = pytz.timezone("America/New_York")
    now = datetime.datetime.now(datetime.timezone.utc).astimezone(ny_timezone)

    return {
        "temperature_status": temp_status,
        "humidity_status": humidity_status,
        "ml_environment_prediction": ml_prediction,
        "confidence": confidence,
        "analyzed_at": now,
    }


def save_to_mongodb(collection, data):
    """
    Save merged sensor + analysis data to MongoDB.
    Args:
        collection: MongoDB collection object
        data (dict): The full data document
    """
    try:
        result = collection.insert_one(data)
        logger.info("Saved to MongoDB with ID: %s", result.inserted_id)
        return result.inserted_id
    except Exception as e:
        logger.error("Failed to save to MongoDB: %s", e)
        raise


def main_loop():
    """Main execution loop for the ML client."""
    collection = connect_to_mongodb()

    while True:
        try:
            # Generate and analyze sensor data
            data = generate_sensor_data()
            data.update(analyze_data(data))

            # Save to MongoDB
            save_to_mongodb(collection, data)

            # Wait before next iteration
            time.sleep(10)  # Collect data every 10 seconds

        except KeyboardInterrupt:
            logger.info("Stopping ML client")
            break
        except Exception as e:
            logger.error("Error in main loop: %s", e)
            time.sleep(5)


if __name__ == "__main__":
    logger.info("Starting ML client")
    main_loop()
