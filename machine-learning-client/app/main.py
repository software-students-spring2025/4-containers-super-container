import os
import cv2
import numpy as np
from pymongo import MongoClient
from datetime import datetime

def analyze_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    avg_pixel = float(np.mean(image))
    return {
        "filename": os.path.basename(image_path),
        "average_pixel_value": avg_pixel,
        "is_dark": avg_pixel < 100
    }

def main():
    client = MongoClient("mongodb://mongodb:27017/")
    db = client["ml_database"]
    collection = db["image_analysis"]

    image_dir = "sample_images"
    os.makedirs(image_dir, exist_ok=True)

    # 示例图像路径（可替换为你自己的）
    test_image_path = os.path.join(image_dir, "sample.jpg")

    if not os.path.exists(test_image_path):
        # 创建一张灰色图像
        cv2.imwrite(test_image_path, np.full((100, 100), 120, dtype=np.uint8))

    result = analyze_image(test_image_path)
    result["timestamp"] = datetime.utcnow()
    collection.insert_one(result)
    print("Inserted:", result)

if __name__ == "__main__":
    main()
