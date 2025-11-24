import sys
import numpy as np
import cv2
from PySide2.QtWidgets import QApplication
from sksurgeryutils.common_overlay_apps import OverlayBaseWidget
from sksurgerycore.transforms.transform_manager import TransformManager
from sksurgeryarucotracker.arucotracker import ArUcoTracker

class OverlayApp(OverlayBaseWidget):
    """Inherits from OverlayBaseWidget, and adds methods to
    detect aruco tags and move the model to follow."""

    def __init__(self, video_source):
        """Override the default constructor to set up sksurgeryarucotracker"""

        # 配置 ArUco Tracker，使用视频文件路径
        ar_config = {
            "tracker type": "aruco",
            "video source": 'none',  # 这里我们不再用摄像头，视频源为文件
            "debug": False,
            "aruco dictionary" : 'DICT_4X4_50',
            "marker size": 50,  # in mm
            "camera projection": np.array([[560.0, 0.0, 320.0],
                                          [0.0, 560.0, 240.0],
                                          [0.0, 0.0, 1.0]], dtype=np.float32),
            "camera distortion": np.zeros((1, 4), np.float32)
        }
        self.tracker = ArUcoTracker(ar_config)
        self.tracker.start_tracking()

        # 使用TimestampedVideoSource来读取本地视频文件
        self.video_source = video_source  # 传递的是视频路径，而不是摄像头ID
        if isinstance(video_source, str):
            self.video_source = cv2.VideoCapture(video_source)
            if not self.video_source.isOpened():
                print(f"Error: Unable to open video file {video_source}.")
                sys.exit(1)

        # 调用基类构造函数
        if sys.version_info > (3, 0):
            super().__init__(video_source)  # 传入视频源
        else:
            OverlayBaseWidget.__init__(self, video_source)

    def update_view(self):
        """Update the background render with a new frame and
        scan for aruco tags"""
        ret, image = self.video_source.read()
        if not ret:
            print("Error: Unable to read next frame.")
            sys.exit(1)
        self._aruco_detect_and_follow(image)

        # 调整相机裁剪范围
        self.vtk_overlay_window.set_camera_state({"ClippingRange": [10, 800]})
        self.vtk_overlay_window.set_video_image(image)
        self.vtk_overlay_window.Render()

    def _aruco_detect_and_follow(self, image):
        """Detect any aruco tags present using sksurgeryarucotracker"""

        # 获取跟踪数据
        _port_handles, _timestamps, _frame_numbers, tag2camera, \
        _tracking_quality = self.tracker.get_frame(image)

        # 如果检测到标签，更新模型位置
        if tag2camera:
            self._move_camera(tag2camera[0])

    def _move_camera(self, tag2camera):
        """Internal method to move the rendered models"""

        transform_manager = TransformManager()
        transform_manager.add("tag2camera", tag2camera)
        camera2tag = transform_manager.get("camera2tag")

        # 移动渲染模型
        self.vtk_overlay_window.set_camera_pose(camera2tag)

    def closeEvent(self, event):
        """Close the video capture when the window is closed."""
        if isinstance(self.video_source, cv2.VideoCapture):
            self.video_source.release()  # 释放视频文件资源
        event.accept()

if __name__ == '__main__':
    app = QApplication([])

    # 指定本地视频文件路径
    video_path = r'../data/0.mp4'
    # video_path = 0
    viewer = OverlayApp(video_path)

    # model_dir = '../models'
    model_dir = '../data/stl'
    viewer.add_vtk_models_from_dir(model_dir)

    viewer.show()
    viewer.start()

    sys.exit(app.exec_())
