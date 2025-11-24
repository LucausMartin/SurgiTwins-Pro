import sys
import numpy as np
import cv2
from PySide2.QtWidgets import QApplication
from ui.common_overlay_apps import OverlayBaseWidget
from sksurgeryarucotracker.arucotracker import ArUcoTracker
from sksurgeryvtk.models.vtk_surface_model_directory_loader import VTKSurfaceModelDirectoryLoader
import vtk

class OverlayApp(OverlayBaseWidget):
    """Inherits from OverlayBaseWidget, and adds methods to
    detect aruco tags and move the model to follow."""

    def __init__(self, video_source):
        """Override the default constructor to set up sksurgeryarucotracker"""

        # 配置 ArUco Tracker
        ar_config = {
            "tracker type": "aruco",
            "video source": 'none',
            "debug": False,
            "aruco dictionary": 'DICT_4X4_50',
            "marker size": 50,  # in mm
            # "camera projection": np.array([[990.528, 0.0, 890.333], [0.0, 992.737, 606.317], [0.0, 0.0, 1.0]], dtype=np.float32),
            "camera projection": np.array([[2606.479, 0.0, 1925.195], [0.0, 2606.479, 1038.779], [0.0, 0.0, 1.0]], dtype=np.float32),
            "camera distortion": np.zeros((1, 4), np.float32)
        }
        self.tracker = ArUcoTracker(ar_config)
        # self.tracker.start_tracking()

        # 使用 OpenCV 来读取本地视频文件
        self.video_source = video_source
        if isinstance(video_source, str):
            self.video_source = cv2.VideoCapture(video_source)
            if not self.video_source.isOpened():
                print(f"Error: Unable to open video file {video_source}.")
                sys.exit(1)

        # 调用基类构造函数
        if sys.version_info > (3, 0):
            super().__init__(video_source)
        else:
            OverlayBaseWidget.__init__(self, video_source)

        # 记录模型的质心位置
        self.centroid = [0,0,0]
        self.new_centroid =self.centroid.copy()
        # 记录模型的旋转角度
        self.rotation_matrix = np.zeros((4,4))

        # 修改模型的角度
        self.x_slider.value_changed.connect(self.try_rotate)
        self.y_slider.value_changed.connect(self.try_rotate)
        self.z_slider.value_changed.connect(self.try_rotate)
        self.x_slider.slider_release.connect(self.rotate_x)
        self.x_slider.spinbox_changed.connect(self.rotate_x)
        self.y_slider.slider_release.connect(self.rotate_y)
        self.y_slider.spinbox_changed.connect(self.rotate_y)
        self.z_slider.slider_release.connect(self.rotate_z)
        self.z_slider.spinbox_changed.connect(self.rotate_z)

        # 修改模型的透明度
        self.transparency_slider.value_changed.connect(self.update_transparency)
        self.transparency_slider.text_changed.connect(self.get_current_transparency)

        # 显示关闭模型按钮
        self.is_visible= True
        self.on_off_button.clicked.connect(self.on_off_models)

        # 自动对齐按钮
        self.auto_align_button.clicked.connect(self.auto_align)

        # 平移模型
        self.x_move_slider.value_changed.connect(self.try_move_x)
        self.y_move_slider.value_changed.connect(self.try_move_y)
        self.z_move_slider.value_changed.connect(self.try_move_z)
        self.x_move_slider.slider_release.connect(self.move_x)
        self.y_move_slider.slider_release.connect(self.move_y)
        self.z_move_slider.slider_release.connect(self.move_z)
        self.x_move_slider.spinbox_changed.connect(self.move_x)
        self.y_move_slider.spinbox_changed.connect(self.move_y)
        self.z_move_slider.spinbox_changed.connect(self.move_z)

    def move_x(self, value):
        """Apply final X translation and reset slider"""
        temp = self.centroid[:]
        temp[0] = self.centroid[0]+value  # Use the preview position
        self.apply_transformation_to_mesh(self.rotation_matrix, self.new_centroid, temp)
        self.centroid = temp[:]  # Update stored centroid
        self.x_move_slider.set_value(0)

    def try_move_x(self, value):
        """Preview X translation without committing"""
        temp = self.centroid[:]
        temp[0] = self.centroid[0] + value
        self.apply_transformation_to_mesh(self.rotation_matrix, self.new_centroid, temp)
        self.new_centroid = temp[:]  # Store preview position

    def move_y(self, value):
        """Apply final Y translation and reset slider"""
        temp = self.centroid[:]
        temp[1] = self.centroid[1]+value  # Use the preview position
        self.apply_transformation_to_mesh(self.rotation_matrix, self.new_centroid, temp)
        self.centroid = temp[:]  # Update stored centroid
        self.y_move_slider.set_value(0)

    def try_move_y(self, value):
        """Preview Y translation without committing"""
        temp = self.centroid[:]
        temp[1] = self.centroid[1] + value
        self.apply_transformation_to_mesh(self.rotation_matrix, self.new_centroid, temp)
        self.new_centroid = temp[:]  # Store preview position

    def move_z(self, value):
        """Apply final Z translation and reset slider"""
        temp = self.centroid[:]
        temp[2] = self.centroid[2]+value  # Use the preview position
        self.apply_transformation_to_mesh(self.rotation_matrix, self.new_centroid, temp)
        self.centroid = temp[:]  # Update stored centroid
        self.z_move_slider.set_value(0)

    def try_move_z(self, value):
        """Preview Z translation without committing"""
        temp = self.centroid[:]
        temp[2] = self.centroid[2] + value
        self.apply_transformation_to_mesh(self.rotation_matrix, self.new_centroid, temp)
        self.new_centroid = temp[:]  # Store preview position

    def fix_align(self):
        """自动对齐模型"""
        self.centroid=[6.206837407663198, 12.723509714808971, 10.825843492581809]
        self.new_centroid = self.centroid.copy()
        self.rotation_matrix = np.array([
            [0.3, 0.200, 0.5, 0.0],
            [0.50, 0.5931, -0.5, 0.0],
            [-0.37, 0.3, 0.3, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ]).T
        self.apply_transformation_to_mesh(self.rotation_matrix, self.centroid)

    def auto_align(self):
        """自动对齐模型"""
        self.centroid=[6.206837407663198, 12.723509714808971, 10.825843492581809]
        self.new_centroid = self.centroid.copy()
        self.rotation_matrix=np.array([
            [0.7140, 0.1200, 0.6898, 0.0],
            [0.3490, 0.7931, -0.4993, 0.0],
            [-0.6070, 0.5972, 0.5243, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ]).T
        self.apply_transformation_to_mesh(self.rotation_matrix, self.centroid)


    def get_current_transparency(self,value):
        name=self.transparency_slider.get_current_choices()
        if name=="ALL":
            pass
        else:
            for model in self.models:
                if model.name==name:
                    actor = model.actor
                    if actor:
                        self.transparency_slider.set_value(actor.GetProperty().GetOpacity()*100)


    def update_transparency(self, value):
        """修改模型的透明度"""
        name=self.transparency_slider.get_current_choices()
        if name=="ALL":
            for model in self.models:
                actor = model.actor
                if actor:
                    actor.GetProperty().SetOpacity(value / 100.0)
        else:
            for model in self.models:
                if model.name==name:
                    actor = model.actor
                    if actor:
                        actor.GetProperty().SetOpacity(value / 100.0)

    def on_off_models(self):
        self.transparency_slider.choices.setCurrentText("ALL")
        """显示/隐藏模型"""
        if not self.is_visible:
            self.transparency_slider.set_value(30)
            self.is_visible=True
        else:
            self.transparency_slider.set_value(0)
            self.is_visible=False

    def rotate_x(self,value):
        alpha =value

        # 创建旋转矩阵
        rt_matrix = self.rotation_matrix_from_xyz_angles(alpha, 0, 0)
        # 更新旋转矩阵
        raw_rt_matrix = self.rotation_matrix
        # 保存旋转矩阵
        self.rotation_matrix = raw_rt_matrix.dot(rt_matrix)
        # 将变换应用于 mesh actors
        self.apply_transformation_to_mesh(self.rotation_matrix, self.centroid)
        self.x_slider.set_value(0)

    def rotate_y(self,value):
        beta = value

        # 创建旋转矩阵
        rt_matrix = self.rotation_matrix_from_xyz_angles(0, beta, 0)
        # 更新旋转矩阵
        raw_rt_matrix = self.rotation_matrix
        # 保存旋转矩阵
        self.rotation_matrix = raw_rt_matrix.dot(rt_matrix)
        # 将变换应用于 mesh actors
        self.apply_transformation_to_mesh(self.rotation_matrix, self.centroid)
        self.y_slider.set_value(0)

    def rotate_z(self,value):
        gamma = value

        # 创建旋转矩阵
        rt_matrix = self.rotation_matrix_from_xyz_angles(0, 0, gamma)
        # 更新旋转矩阵
        raw_rt_matrix = self.rotation_matrix
        # 保存旋转矩阵
        self.rotation_matrix = raw_rt_matrix.dot(rt_matrix)
        # 将变换应用于 mesh actors
        self.apply_transformation_to_mesh(self.rotation_matrix, self.centroid)
        self.z_slider.set_value(0)

    # 尝试旋转，并不记录旋转角度
    def try_rotate(self):
        # 定义旋转角度
        alpha = self.x_slider.get_value()
        beta = self.y_slider.get_value()
        gamma = self.z_slider.get_value()

        # 创建旋转矩阵
        rt_matrix = self.rotation_matrix_from_xyz_angles(alpha, beta, gamma)
        # 更新旋转矩阵
        raw_rt_matrix = self.rotation_matrix
        # 计算出旋转矩阵
        rt_matrix = raw_rt_matrix.dot(rt_matrix)
        # 将变换应用于 mesh actors
        self.apply_transformation_to_mesh(rt_matrix, self.centroid)



    def rotation_matrix_from_xyz_angles(self,alpha, beta, gamma):
        """
        根据围绕x、y、z轴的旋转角度(alpha, beta, gamma)构造齐次旋转矩阵。
        假设旋转顺序为：先绕X轴旋转alpha, 再绕Y轴旋转beta, 最后绕Z轴旋转gamma。
        """
        alpha = np.radians(alpha)
        beta = np.radians(beta)
        gamma = np.radians(gamma)

        # 绕X轴旋转矩阵
        Rx = np.array([
            [1, 0, 0],
            [0, np.cos(alpha), -np.sin(alpha)],
            [0, np.sin(alpha), np.cos(alpha)]
        ])

        # 绕Y轴旋转矩阵
        Ry = np.array([
            [np.cos(beta), 0, np.sin(beta)],
            [0, 1, 0],
            [-np.sin(beta), 0, np.cos(beta)]
        ])

        # 绕Z轴旋转矩阵
        Rz = np.array([
            [np.cos(gamma), -np.sin(gamma), 0],
            [np.sin(gamma), np.cos(gamma), 0],
            [0, 0, 1]
        ])

        # 总旋转矩阵 R = Rz * Ry * Rx
        R = Rz.dot(Ry).dot(Rx)

        # 将3x3旋转矩阵扩展为4x4齐次矩阵
        R_hom = np.eye(4)
        R_hom[:3, :3] = R

        return R_hom

    def get_rt_matrix(self):
        """创建一个用于旋转和平移 mesh 的特定 R/T 矩阵。"""

        # 绕 x 轴旋转 90° 的旋转矩阵
        # rotation_matrix = np.array([
        #     [1.0, 0.0, 0.0, 0.0],
        #     [0.0, 0.0, -1.0, 0.0],
        #     [0.0, 1.0, 0.0, 0.0],
        #     [0.0, 0.0, 0.0, 1.0]
        # ])
        # 绕 y 轴旋转 90° 的旋转矩阵
        # rotation_matrix = np.array([
        #     [0.0, 0.0, 1.0, 0.0],
        #     [0.0, 1.0, 0.0, 0.0],
        #     [-1.0, 0.0, 0.0, 0.0],
        #     [0.0, 0.0, 0.0, 1.0]
        # ])
        # 绕 z 轴旋转 90° 的旋转矩阵
        # rotation_matrix = np.array([
        #     [0.0, -1.0, 0.0, 0.0],
        #     [1.0, 0.0, 0.0, 0.0],
        #     [0.0, 0.0, 1.0, 0.0],
        #     [0.0, 0.0, 0.0, 1.0]
        # ])



        rotation_matrix = np.array([
            [0.7140,  0.1200,  0.6898, 0.0],
            [0.3490,  0.7931, -0.4993, 0.0],
            [-0.6070,  0.5972,  0.5243, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ]).T
        return rotation_matrix



    def apply_transformation_to_mesh(self, rt_matrix, centroid,next_centroid=None):
        """将 R/T 矩阵应用于 mesh actors，并围绕模型的质心进行旋转。"""
        if next_centroid is None:
            next_centroid = centroid
        # 将 numpy 数组转换为 vtkMatrix4x4
        vtk_matrix = vtk.vtkMatrix4x4()
        for i in range(4):
            for j in range(4):
                vtk_matrix.SetElement(i, j, rt_matrix[i, j])

        # 创建平移矩阵，将质心移至原点
        translation_to_origin = vtk.vtkTransform()
        translation_to_origin.Translate(-centroid[0], -centroid[1], -centroid[2])

        # 创建反向平移矩阵，将模型平移回指定位置
        translation_back = vtk.vtkTransform()
        translation_back.Translate(next_centroid[0], next_centroid[1], next_centroid[2])

        # 创建旋转矩阵的变换对象
        rotation_transform = vtk.vtkTransform()
        rotation_transform.SetMatrix(vtk_matrix)  # 应用旋转矩阵

        # 创建最终的变换
        final_transform = vtk.vtkTransform()

        # 先进行平移到原点，再进行旋转，最后平移回原位
        final_transform.Concatenate(translation_to_origin)  # 将模型移到原点
        final_transform.Concatenate(rotation_transform)  # 应用旋转
        final_transform.Concatenate(translation_back)  # 将模型平移回原位

        # 将变换应用于每个 mesh actor
        for model in self.models:
            actor = model.actor
            if actor:
                # SetUserTransform 会覆盖之前的变换
                actor.SetUserTransform(final_transform)

    def update_view(self):
        """Update the background render with a new frame and
        scan for aruco tags"""

        ret, image = self.video_source.read()
        if not ret:
            print("Error: Unable to read next frame.")
            sys.exit(1)
        # image = cv2.resize(image, (3840, 2160), interpolation=cv2.INTER_LINEAR)
        # image = cv2.flip(image, -1)
        print("image:", image.shape)
        # self._aruco_detect_and_follow(image)

        # 定义您的旋转和平移（R/T）矩阵
        # rt_matrix = self.get_rt_matrix()
        # 将变换应用于 mesh actors
        centroid = [6.206837407663198, 12.723509714808971, 10.825843492581809]

        # self.apply_transformation_to_mesh(rt_matrix, centroid)

        # 调整相机裁剪范围
        # self.vtk_overlay_window.set_camera_state({"ClippingRange": [10, 800]})
        self.vtk_overlay_window.set_video_image(image)
        self.vtk_overlay_window.Render()

    # def _aruco_detect_and_follow(self, image):
    #     """Detect any aruco tags present using sksurgeryarucotracker"""
    #
    #     # 获取跟踪数据
    #     _port_handles, _timestamps, _frame_numbers, tag2camera, \
    #     _tracking_quality = self.tracker.get_frame(image)
    #
    #     # 如果检测到标签，更新模型位置
    #     if tag2camera:
    #         self._move_camera(tag2camera[0])
    #     # 下面是传入空的列表，代表相机的位置不动，但是要变换肝脏mesh
    #     # else:
    #     #     print("tag2camera:", tag2camera)
    #     #     self._move_camera_only(np.eye(4))
    # def _move_camera(self, tag2camera):
    #     """Internal method to move the rendered models"""
    #     transform_manager = TransformManager()
    #     transform_manager.add("tag2camera", tag2camera)
    #     camera2tag = transform_manager.get("camera2tag")
    #
    #     # 移动渲染模型
    #     self.vtk_overlay_window.set_camera_pose(camera2tag)
    #
    # def _move_camera_only(self, camera2tag):
    #     """Internal method to move the rendered models"""
    #
    #
    #     # 移动渲染模型
    #     self.vtk_overlay_window.set_camera_pose(camera2tag)

    def closeEvent(self, event):
        """Close the video capture when the window is closed."""
        if isinstance(self.video_source, cv2.VideoCapture):
            self.video_source.release()
        event.accept()

    def add_vtk_models_from_dir(self, directory):
        """Add models from the specified directory and set transparency."""
        # 加载模型
        model_loader = VTKSurfaceModelDirectoryLoader(directory)
        self.models = model_loader.models

        # 在下拉列表中添加模型部件的名称
        for model in self.models:
            self.transparency_slider.choices.addItem(model.name)

        # 为每个模型设置透明度（例如，50% 透明度）
        for model in self.models:
            # print("model:", model.name)
            actor = model.actor
            if actor:
                actor.GetProperty().SetOpacity(0.35)  # 设置不透明度为 50%

        camera_projection = np.array([
            [2606.479, 0.0, 1925.195],
            [0.0, 2606.479, 1038.779],
            [0.0, 0.0, 1.0]
        ], dtype=np.float32)
        self.vtk_overlay_window.camera_matrix = camera_projection


        camera_to_world = np.array([
            [1, 0, 0, 0],  # X轴不变
            [0, 1, 0, 0],  # Y轴不变
            [0, 0, 1, 1],  # Z轴翻转，原来是朝-z轴，现在是朝+z轴，且位置保持原点
            [0, 0, 0, 1]  # 齐次坐标部分
        ], dtype=np.float32)
        self.vtk_overlay_window.camera_to_world = camera_to_world

        camera_properties = {
            "Position": [0, 0, -200],  # 设置与PyTorch3D一致的相机位置
            "FocalPoint": [0, 0, 1],  # 设置焦点位置，通常为原点
            # "ViewUp": [0, 1, 0],  # 设置相机上方向
            # "ViewAngle": 72.0,  # 设置视场角
            # # "ClippingRange": [10, 11]  # 设置裁剪范围，视您的实际需求
            "ClippingRange": [0.0, 0.1]  # 设置裁剪范围，视您的实际需求
        }

        #将相机参数传入AR系统
        self.vtk_overlay_window.set_camera_state(camera_properties)

        # 将模型添加到渲染窗口
        self.vtk_overlay_window.add_vtk_models(self.models, layer=1)


if __name__ == '__main__':
    app = QApplication([])

    # 指定本地视频文件路径
    # video_path = '../data/0.mp4'
    video_path = '../data/p2ilf-3-IPCAI-12.mp4' # p2ilf-3-IPCAI-08.mp4, p2ilf-3-IPCAI-10.mp4, p2ilf-4-13-img.mp4, p2ilf-3-IPCAI-12.mp4
    # video_path = 1
    viewer = OverlayApp(video_path)

    # 指定模型目录路径
    # model_dir = '../data/stl'
    # model_dir = '../data/stl-ipcai-1'
    # model_dir = '../data/stl-3dircadb-1'
    model_dir = '../data/stl-3dircadb-16-couinaud'
    #
    # model_dir = '../data/stl-ipcai-1'
    viewer.add_vtk_models_from_dir(model_dir)
    viewer.fix_align()#自动对齐

    viewer.show()
    viewer.start()

    sys.exit(app.exec_())
