from app.main import analyze_image
import numpy as np
import cv2
import os

def test_analyze_image_creates_expected_result(tmp_path):
    # 创建一张亮图像
    test_image = tmp_path / "bright.jpg"
    img_array = np.full((50, 50), 200, dtype=np.uint8)
    cv2.imwrite(str(test_image), img_array)

    result = analyze_image(str(test_image))
    assert result["average_pixel_value"] > 150
    assert result["is_dark"] is False
