# tests/test_main.py
import unittest
from unittest.mock import patch, MagicMock
from app.main import analyze
# 如果 main.py 与 test_main.py 在同一层级，需要把父目录加入到 python path。
# 如果你的项目有 __init__.py 并正确安装为包，可不需要这一步。
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestMain(unittest.TestCase):
    """
    针对 main.py 的逻辑进行单元测试/集成测试示例。
    """

    @patch('cv2.VideoCapture')
    @patch('analysis.emotion_analyzer.DeepFace.analyze')
    def test_main_loop(self, mock_deepface_analyze, mock_videocapture):
        """
        测试 main.py 主循环中是否能正确调用 DeepFace 分析并处理结果。
        """
        # 1. 模拟摄像头读取
        # mock_videocapture.return_value 为一个 MagicMock 对象，可自定义其行为
        mock_cap_instance = MagicMock()
        # 让 cap.read() 返回 (True, frame_data)
        mock_cap_instance.read.side_effect = [
            (True, 'fake_frame'),  # 第一次循环
            (True, 'fake_frame'),  # 第二次循环
            (False, None)         # 第三次循环 - 模拟读不到图像，跳出循环
        ]
        mock_videocapture.return_value = mock_cap_instance

        # 2. 模拟 DeepFace.analyze
        # 让 DeepFace.analyze 返回一个伪结果
        mock_deepface_analyze.return_value = {
            "dominant_emotion": "happy",
            "region": {"x": 100, "y": 50, "w": 150, "h": 150}
        }

        # 3. 由于 main.py 通常会启动一个无限循环等待键盘事件退出，我们可以在测试时“跳过”这个逻辑。
        # 可以用 patch 替换 cv2.waitKey，让其在循环中检查到某条件时跳出。
        with patch('cv2.waitKey', side_effect=[-1, -1, ord('q')]):
            # 调用 main.main()，这会触发上述 mock 行为。
            main.main()

        # 4. 验证：是否按预期调用了摄像头读取，以及 DeepFace 分析
        self.assertTrue(mock_cap_instance.read.called)
        # DeepFace.analyze 在每一帧都可能被调用两次(取决于你 main.py 代码)，
        # 这里仅断言它至少被调用一次:
        self.assertTrue(mock_deepface_analyze.called)

    @patch('cv2.VideoCapture')
    def test_main_camera_not_opened(self, mock_videocapture):
        """
        测试如果摄像头无法正常打开时，main.py 能否优雅退出或打印提示。
        """
        # 模拟 isOpened() 返回 False
        mock_cap_instance = MagicMock()
        mock_cap_instance.isOpened.return_value = False
        mock_videocapture.return_value = mock_cap_instance

        # 捕获 print 输出（如果你想验证错误提示）
        with patch('builtins.print') as mock_print:
            main.main()
            mock_print.assert_any_call("无法打开摄像头。")

        # 验证 read() 从未被调用
        mock_cap_instance.read.assert_not_called()

    # 你可以根据项目更多场景扩展测试用例，比如：
    # - DeepFace 没检测到人脸 -> analyze 返回空的结果
    # - 分析失败异常捕获 -> analyze 抛出异常
    # - 检测到多张人脸 -> analyze 返回列表
    # - etc.

if __name__ == '__main__':
    unittest.main()
