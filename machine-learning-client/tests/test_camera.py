import cv2

cap = cv2.VideoCapture(0) # pylint: disable=no-member

if not cap.isOpened():
    print("❌ 摄像头打不开！")
else:
    print("✅ 摄像头打开成功！")
    ret, frame = cap.read()
    if ret:
        cv2.imwrite("test_frame.jpg", frame) # pylint: disable=no-member
        print("📸 成功捕获并保存 test_frame.jpg")
    else:
        print("⚠️ 打开成功但没有读取到图像")
    cap.release()