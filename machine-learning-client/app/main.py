import os
import uuid
import cv2
from deepface import DeepFace
from pymongo import MongoClient
from datetime import datetime

# 图片保存目录
IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)


def capture_image():
    cap = cv2.VideoCapture(0)  # pylint: disable=no-member
    ret, frame = cap.read()
    cap.release()
    if not ret:
        raise RuntimeError("Unable to capture from camera")
    return frame


def analyze_emotion(image):
    result = DeepFace.analyze(image, actions=["emotion"], enforce_detection=False)
    return {
        "dominant_emotion": result[0]["dominant_emotion"],
        "emotion_scores": result[0]["emotion"],
    }


def save_image_to_file(image):
    # 生成唯一文件名
    filename = f"{uuid.uuid4().hex}.jpg"
    filepath = os.path.join(IMAGE_DIR, filename)
    # 可选择压缩图像
    max_dim = 300
    height, width = image.shape[:2]
    if max(height, width) > max_dim:
        scale = max_dim / max(height, width)
        image = cv2.resize(
            image, (int(width * scale), int(height * scale))
        )  # pylint: disable=no-member
    # 保存图像到本地
    cv2.imwrite(filepath, image)  # pylint: disable=no-member
    return filepath


def save_analysis(image, analysis_result):
    filepath = save_image_to_file(image)

    # 强制将所有数值转换为 Python float
    emotion_scores_raw = analysis_result["emotion_scores"]
    emotion_scores_clean = {k: float(v) for k, v in emotion_scores_raw.items()}

    client = MongoClient("mongodb://localhost:27017/")
    db = client["emotion_db"]
    collection = db["emotions"]

    doc = {
        "timestamp": datetime.utcnow(),
        "image_path": filepath,
        "dominant_emotion": analysis_result["dominant_emotion"],
        "emotion_scores": emotion_scores_clean,
    }

    collection.insert_one(doc)
    print(f"✅ Saved: {filepath} with emotion {analysis_result['dominant_emotion']}")


def run():
    image = capture_image()
    result = analyze_emotion(image)
    save_analysis(image, result)


if __name__ == "__main__":
    run()
