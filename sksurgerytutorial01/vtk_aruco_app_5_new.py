import os.path
import sys
import numpy as np
import cv2
from PySide2.QtWidgets import QApplication
from ui.common_overlay_apps import OverlayBaseWidget
from sksurgeryarucotracker.arucotracker import ArUcoTracker
from sksurgeryvtk.models.vtk_surface_model_directory_loader import VTKSurfaceModelDirectoryLoader
import vtk
from sksurgeryvtk.models.vtk_surface_model import VTKSurfaceModel
from sksurgeryvtk.widgets.vtk_overlay_window import VTKOverlayWindow
from vtk.util import numpy_support
import xmltodict
import shutil

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
        # self.video_source = video_source
        # if isinstance(video_source, str):
        #     self.video_source = cv2.VideoCapture(video_source)
        #     if not self.video_source.isOpened():
        #         print(f"Error: Unable to open video file {video_source}.")
        #         sys.exit(1)

        self.image_source = video_source
        if isinstance(video_source, str):
            self.image_source = load_image(video_source)

            if self.image_source is None:
                print(f"Error: Unable to load image from {video_source}.")
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

        # ret, image = self.video_source.read()
        # if not ret:
        #     print("Error: Unable to read next frame.")
        #     sys.exit(1)
        # image = cv2.resize(image, (3840, 2160), interpolation=cv2.INTER_LINEAR)
        # image = cv2.flip(image, -1)
        # print("image:", image.shape)
        # self._aruco_detect_and_follow(image)

        # 定义您的旋转和平移（R/T）矩阵
        # rt_matrix = self.get_rt_matrix()
        # 将变换应用于 mesh actors
        centroid = [6.206837407663198, 12.723509714808971, 10.825843492581809]

        # self.apply_transformation_to_mesh(rt_matrix, centroid)

        # 调整相机裁剪范围
        # self.vtk_overlay_window.set_camera_state({"ClippingRange": [10, 800]})
        self.vtk_overlay_window.set_video_image(self.image_source)
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
        # if isinstance(self.video_source, cv2.VideoCapture):
        #     self.video_source.release()
        if self.image_source is not None:
            del self.image_source
            self.image_source = None
        event.accept()

    def add_vtk_models_from_dir(self, directory, camera_matrix=None, ligament_indices=None, ridge_indices=None):
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

        if camera_matrix is not None:
            self.vtk_overlay_window.camera_matrix = camera_matrix
            print(f"reset camera_matrix!!!")


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

        # self.set_model_color(ligament_indices, ridge_indices)
        self.set_model_color_from_txt(color_txt="vertex_colors.txt")
        # 将模型添加到渲染窗口
        self.vtk_overlay_window.add_vtk_models(self.models, layer=1)

    def set_model_color(self, ligament_indices=None, ridge_indices=None):
        for model in self.models:
            # 获取 vtkPolyData
            mapper = model.actor.GetMapper()
            poly_data = mapper.GetInput()

            # 创建颜色数组
            color_array = vtk.vtkUnsignedCharArray()
            color_array.SetNumberOfComponents(3)  # RGB
            color_array.SetName("Colors")

            # 为每个顶点设置颜色
            num_vertices = model.get_number_of_points()
            random_colors = np.ones((num_vertices, 3)) * 255
            if ligament_indices is not None:
                random_colors[ligament_indices] = [0, 0, 255]  # 红色
            if ridge_indices is not None:
                random_colors[ridge_indices] = [255, 0, 0]  # 蓝色
            colors = random_colors.astype(np.uint8)
            for color in colors:
                color_array.InsertNextTuple3(int(color[0]), int(color[1]), int(color[2]))
            print("color_array:", color_array)
            # 将颜色数组添加到顶点数据
            poly_data.GetPointData().SetScalars(color_array)
            # 更新 Mapper
            mapper.Update()

    def set_model_color_from_txt(self, color_txt="vertex_colors.txt"):
        """
        读取 <vertex_index>,<R>,<G>,<B> 的 txt，并将颜色应用到 model 的 vtkPolyData。
        假设所有 model 的顶点数都和 txt 文件一致，或者你只对第一个 model 做处理。
        """
        # 1. 读取 txt 里的颜色
        vertex_index_list = []
        rgb_list = []
        with open("vertex_colors.txt", "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) != 4:
                    continue
                idx = int(parts[0])
                r = int(parts[1])
                g = int(parts[2])
                b = int(parts[3])
                vertex_index_list.append(idx)
                rgb_list.append((r, g, b))

        # 转成 numpy array 便于后续处理
        vertex_index_list = np.array(vertex_index_list, dtype=np.int32)
        rgb_array = np.array(rgb_list, dtype=np.uint8)  # (N,3)

        # 排序或保证 index 递增 (可选)
        # 如果 txt 中 index 顺序混乱，需要排序使其对齐
        # sort_indices = np.argsort(vertex_index_list)
        # vertex_index_list = vertex_index_list[sort_indices]
        # rgb_array = rgb_array[sort_indices]

        # 2. 给 models 里的第一个 model 应用颜色 (或遍历所有model)
        for model in self.models:
            mapper = model.actor.GetMapper()
            poly_data = mapper.GetInput()

            num_vertices = model.get_number_of_points()
            if num_vertices != len(vertex_index_list):
                print(f"WARNING: model顶点数({num_vertices})与txt记录数({len(vertex_index_list)})不一致！")
                # 这里可以选择忽略 or 做截断/扩展等逻辑
                min_count = min(num_vertices, len(vertex_index_list))
            else:
                min_count = num_vertices

            # 创建颜色数组
            color_array = vtk.vtkUnsignedCharArray()
            color_array.SetNumberOfComponents(3)
            color_array.SetName("Colors")

            # 构造顶点对应的颜色
            #   如果需要简化，可直接使用 for i in range(num_vertices): ...
            #   这里我们假设 vertex_index_list[i] == i，或者我们按顺序一一对应
            #   只处理前 min_count 个
            for i in range(min_count):
                # i 是顺序 index
                # vtx_index = vertex_index_list[i] # 如果有排序
                # color = rgb_array[i]
                # 但通常 txt 里0~(N-1) 按顺序存
                color = rgb_array[i]
                color_array.InsertNextTuple3(int(color[0]), int(color[1]), int(color[2]))

            # 如果 txt 行数 < model的顶点数，可额外补白色 or 0
            # if min_count < num_vertices:
            #     for _ in range(num_vertices - min_count):
            #         color_array.InsertNextTuple3(255,255,255)

            # 将颜色数组添加到 vtkPolyData
            poly_data.GetPointData().SetScalars(color_array)
            mapper.Update()
            print(f"Applied txt-based colors to model with {num_vertices} points.")

def load_image(image_path):
    """
    使用 OpenCV 加载单张图像。
    :param image_path: 图像文件路径
    :return: 图像的 NumPy 数组
    """
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"无法加载图像：{image_path}")
    return image


def load_xml(file_path="/mnt/data/LiCZ/Data/P2ILF/camera_parameters/patient1/calibration.xml"):
    with open(file_path, 'r', encoding='utf-8') as xml_file:
        xml_data = xml_file.read()
    camera_data_dict = xmltodict.parse(xml_data, disable_entities=True)

    return camera_data_dict


def parse_contour_xml(contour_file):
    xml_data = load_xml(contour_file)
    # print(xml_data)
    numOfContours = int(xml_data["contours"]["numOfContours"])
    contour_list = xml_data["contours"]["contour"]
    points_dict = {}
    for contour in contour_list:
        contour_type = contour["contourType"]
        if contour_type not in points_dict:
            points_dict[contour_type] = []
        # print(contour_type, points_dict[contour_type])
        num_img_points = int(contour["imagePoints"]["numOfPoints"])
        img_pointx_list = contour['imagePoints']['x'].split(",")
        img_pointy_list = contour['imagePoints']['y'].split(",")
        points = {}
        points["image"] = []
        for i in range(num_img_points):
            points["image"].append((float(img_pointx_list[i]), float(img_pointy_list[i])))

        if "modelPoints" in contour:
            points["model"] = []
            num_model_points = int(contour["modelPoints"]["numOfPoints"])
            # points["model"] = contour["modelPoints"]["vertices"].split(",")
            points_3d_vertices = contour["modelPoints"]["vertices"].split(",")
            points["model"] = [int(i) for i in points_3d_vertices]

        points_dict[contour_type].append(points)

    return points_dict


def load_camera_parameters_xml(camera_param_path, scale_factor=1.0):
    import xml.etree.ElementTree as ET
    tree = ET.parse( camera_param_path )
    root = tree.getroot()

    fx = float(root.find("fx").text)
    fy = float(root.find("fy").text)
    cx = float(root.find("cx").text)
    cy = float(root.find("cy").text)
    calib = {}
    params = ["width", "height", "fx", "fy", "cx", "cy", "k1", "k2", "k3", "k4", "p1", "p2", "skew"]
    for name in params:
        val = float(root.find(name).text)
        calib[name] = val

    calib["fx"] = scale_factor*calib["fx"]
    calib["fy"] = scale_factor*calib["fy"]
    calib["cx"] = scale_factor*calib["cx"]
    calib["cy"] = scale_factor*calib["cy"]
    calib["width"] = scale_factor*calib["width"]
    calib["height"] = scale_factor*calib["height"]

    #print("camera params:", fx, fy, cx, cy)
    return calib


def construct_camera_matrix(params):

    K = np.zeros((3,3), dtype=np.float32)
    K[0, 0] = params["fx"]
    K[1, 1] = params["fy"]
    K[2, 2] = 1
    K[0, 2] = params["cx"]
    K[1, 2] = params["cy"]
    return K


def load_contour_3D(contour_path):
    ligament_indices = []
    ridge_indices = []
    contour_pts = parse_contour_xml(contour_path)

    if "Ligament" in contour_pts:
        for i in range(len(contour_pts["Ligament"])):
            pts = contour_pts["Ligament"][i]
            pts_model = pts["model"]
            ligament_indices.extend(pts_model)

    if "Ridge" in contour_pts:
        for i in range(len(contour_pts["Ridge"])):
            pts = contour_pts["Ridge"][i]
            pts_model = pts["model"]
            ridge_indices.extend(pts_model)

    return ligament_indices, ridge_indices


if __name__ == '__main__':
    app = QApplication([])

    # 指定本地视频文件路径
    # video_path = '../data/0.mp4'
    # video_path = '../data/p2ilf-3-IPCAI-10.mp4'
    # video_path = 1
    # video_path = '/mnt/data/LiCZ/Projects/Codes/registration/related/clean-pvnet/data/P2ILF/patient1/mp4/P2ILF22_patient1_1.mp4'
    # viewer = OverlayApp(video_path)

    patients = ['patient1', 'patient2', 'patient3', 'patient5', 'patient6', 'patient7', 'patient8', 'patient9',
                'patient10']
    contours_pat = [22, 25, 20, 15, 22, 25, 8, 21, 9]
    pat_id = 0
    contour_id = 1

    # camera
    camera_path = f"D:/scikit-surgery/Data/20250221/camera_parameters/{patients[pat_id]}/calibration.xml"
    camera_params = load_camera_parameters_xml(camera_path, scale_factor=1.0)
    camera_matrix = construct_camera_matrix(camera_params)
    # print(camera_matrix)

    # contour
    contour_path = f"D:/scikit-surgery/Data/20250221/p2ilf-train-save/{patients[pat_id]}/2D-3D_contours/P2ILF22_{patients[pat_id]}_{contour_id}.xml"
    ligament_indices, ridge_indices = load_contour_3D(contour_path)
    print("ligament_indices:", ligament_indices)
    print("ridge_indices:", ridge_indices)
    ligament_indices = [458, 483, 543, 519, 484, 538, 577, 642, 641, 695, 739, 731, 826, 862, 815, 738, 842, 816, 781, 856, 855, 891, 892]
    # ligament_indices = []
    ridge_indices = [13, 18, 27, 32, 40, 42, 49, 60, 61, 64, 70, 79, 71, 80, 88, 89, 97, 87, 128, 111, 138, 167, 146, 186, 215, 187, 182, 194, 180, 195, 221, 254, 214, 255, 284, 253, 230, 283, 324, 275, 238, 351, 310, 273, 339, 298, 325, 349, 308, 299, 422, 388, 371, 455, 415, 457, 501, 481, 523, 550]
    # ligament_indices=[1573, 1758, 1796, 1825, 1827, 1900, 1901, 1934, 1975, 1870, 4021, 1935, 2050, 2025, 1902, 2023, 2022, 2087, 2024, 2088, 2156, 2158, 2157, 2192, 2193, 2228, 2257, 2226, 2285, 2350, 2415, 2310, 2413, 2351, 2414, 2410, 2411, 2512, 2561, 2490, 2564, 2591, 2633, 2567, 2634, 2635, 2697, 2696, 2655, 2694, 2734, 2789, 2836, 2790, 2917, 2916, 2878, 2979, 2980, 2981, 2984, 3075, 3148, 3149, 3146]
    # ridge_indices=[106, 121, 141, 140, 142, 154, 159, 155, 190, 162, 170, 196, 175, 181, 195, 191, 194, 209, 246, 220, 235, 245, 271, 278, 276, 258, 277, 288, 299, 312, 323, 322, 356, 370, 364, 371, 379, 407, 396, 436, 437, 481, 504, 480, 490, 513, 512, 527, 505, 537, 557, 570, 602, 538, 568, 600, 588, 623, 642, 599, 640, 686, 681, 711, 710, 682, 680, 730, 709, 683, 684, 685, 748, 679, 728, 729, 814, 753, 807, 806, 826, 727, 750, 781, 752, 834, 784, 773, 778, 751, 813, 772, 776, 774, 804, 775, 808, 827, 777, 810, 829, 780, 811, 812, 892, 805, 809, 917, 881, 876, 825, 879, 891, 882, 884, 918, 943, 1007, 883, 1081, 890, 944, 945, 1073, 976, 977, 1076, 1046, 1137, 1074, 1045, 1186, 1252, 1182, 1080, 1078, 1136, 1285, 1184, 1189, 1286, 1287, 4010, 1402, 1401, 1465, 1695, 4011]
    print("ligament_indices, ridge_indices:", ligament_indices)
    img_path = (f'D:/scikit-surgery/Data/20250221/p2ilf-train-save/{patients[pat_id]}/img_label_fusion/P2ILF22_{patients[pat_id]}_{contour_id}.jpg')
    viewer = OverlayApp('../data/000.jpg')     # '../data/p2ilf-4-13-img.mp4'

    #
    mesh_root = "D:/scikit-surgery/Data/20250221/meshes"
    os.makedirs(os.path.join(mesh_root, patients[pat_id]), exist_ok=True)

    src_mesh = f"D:/scikit-surgery/Data/20250221/meshes/stl/{patients[pat_id]}/liver.obj"
    dst_mesh = os.path.join(mesh_root, patients[pat_id], "liver.obj")
    if os.path.exists(dst_mesh):
        os.remove(dst_mesh)
    shutil.copy2(src_mesh, dst_mesh)

    # 指定模型目录路径
    model_dir = '../data/stl'
    model_dir = os.path.join(mesh_root, patients[pat_id])
    viewer.add_vtk_models_from_dir(model_dir, camera_matrix, ligament_indices, ridge_indices)
    viewer.fix_align()#自动对齐

    viewer.show()
    viewer.start()

    sys.exit(app.exec_())
