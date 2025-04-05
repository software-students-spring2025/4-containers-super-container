import cv2
from deepface import DeepFace

# 打开摄像头
cap = cv2.VideoCapture(0)# pylint: disable=no-member
ret, frame = cap.read()
cap.release()

if ret:
    print("✅ 成功捕获一帧图像，开始进行情绪识别...")

    try:
        result = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
        dominant_emotion = result[0]['dominant_emotion']
        print("🧠 识别结果：", result)
        print("😃 主要情绪：", dominant_emotion)

    except Exception as e: # pylint: disable=broad-exception-caught
        print("❌ DeepFace 分析失败：", str(e))
else:
    print("⚠️ 摄像头图像读取失败")