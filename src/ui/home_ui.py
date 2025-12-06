# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QTimer, QUrl, Qt)
from PySide2.QtWidgets import *
from PySide2.QtGui import *

class ClippedSection(QFrame):
    def __init__(self, parent=None, radius=8):
        super().__init__(parent)
        self._radius = radius
        self.setAttribute(Qt.WA_StyledBackground, True)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        path = QPainterPath()
        path.addRoundedRect(self.rect(), self._radius, self._radius)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)


class SliderWidget(QWidget):
    """自定义滑轨和滑块控件"""
    def __init__(self, label, min_value, max_value, default_value, unit="", parent=None):
        super().__init__(parent)
        self.label = label
        self.min_value = min_value
        self.max_value = max_value
        self.unit = unit
        self.setup_ui()
        self.set_value(default_value)

    def setup_ui(self):
        """设置UI布局"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 2, 0, 2)  # 减小上下边距
        layout.setSpacing(2)  # 减小间距

        # 上方：属性标签和数值显示（水平排列）
        self.top_widget = QWidget()
        top_layout = QHBoxLayout(self.top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(0)  # 文字间距为0

        # 左侧：属性标签
        self.label_widget = QLabel(self.label)
        self.label_widget.setStyleSheet(u"color: #707070; font-size: 16px; font-weight: 400; font-family: \"微软雅黑\";")
        top_layout.addWidget(self.label_widget)

        # 中间：弹簧
        top_layout.addStretch()

        # 右侧：数值显示
        self.value_widget = QLabel()
        self.value_widget.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.value_widget.setStyleSheet(u"color: #707070; font-size: 16px; font-weight: 400; font-family: \"微软雅黑\";")
        top_layout.addWidget(self.value_widget)

        layout.addWidget(self.top_widget)

        # 下方：滑轨
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(self.min_value)
        self.slider.setMaximum(self.max_value)
        self.slider.setFixedHeight(20)
        self.slider.setStyleSheet(u"""
            QSlider::groove:horizontal {
                background: #E5E7EB;
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #4200FF;
                width: 16px;
                height: 16px;
                margin: -4px 0;
                border-radius: 8px;
            }
            QSlider::handle:horizontal:hover {
                background: #5A1AFF;
            }
            QSlider::handle:horizontal:pressed {
                background: #2E00CC;
            }
        """)
        layout.addWidget(self.slider)

        # 连接信号
        self.slider.valueChanged.connect(self.update_value_display)

    def set_value(self, value):
        """设置滑块值"""
        self.slider.setValue(value)

    def get_value(self):
        """获取当前值"""
        return self.slider.value()

    def update_value_display(self, value):
        """更新数值显示"""
        self.value_widget.setText(f"{value}{self.unit}")


class HomeUI(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1200, 800)
        Form.setMinimumSize(QSize(800, 600))

        # Main vertical layout
        self.main_layout = QVBoxLayout(Form)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Top part - Tap Bar
        self.tap_bar = QWidget(Form)
        self.tap_bar.setObjectName(u"tap_bar")
        self.tap_bar.setMinimumHeight(60)
        self.tap_bar.setMaximumHeight(60)
        self.tap_bar.setStyleSheet(u"background-color: white;")
        # Ensure tap bar is above content area
        self.tap_bar.raise_()

        # Tap bar layout
        self.tap_bar_layout = QHBoxLayout(self.tap_bar)
        self.tap_bar_layout.setContentsMargins(20, 0, 20, 0)

        # Left side - Icon and Text
        self.left_section = QWidget(self.tap_bar)
        self.left_layout = QHBoxLayout(self.left_section)
        self.left_layout.setSpacing(10)
        self.left_layout.setContentsMargins(0, 0, 0, 0)

        # Icon
        self.icon_label = QLabel(self.left_section)
        self.icon_label.setObjectName(u"icon_label")
        self.icon_label.setFixedSize(32, 32)
        # Load and set actual icon
        icon_pixmap = QPixmap(u"./img/colorfilter.png")
        self.icon_label.setPixmap(icon_pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # Text - SurgiTwins and Pro with different colors
        self.surgitwins_label = QLabel(self.left_section)
        self.surgitwins_label.setObjectName(u"surgitwins_label")
        font = QFont()
        font.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.surgitwins_label.setFont(font)
        self.surgitwins_label.setStyleSheet(u"color: #4200FF;")

        self.pro_label = QLabel(self.left_section)
        self.pro_label.setObjectName(u"pro_label")
        self.pro_label.setFont(font)
        self.pro_label.setStyleSheet(u"color: #404040;")

        # Add to left layout
        self.left_layout.addWidget(self.icon_label)
        self.left_layout.addWidget(self.surgitwins_label)
        self.left_layout.addWidget(self.pro_label)

        # Add left section to tap bar layout
        self.tap_bar_layout.addWidget(self.left_section)
        self.tap_bar_layout.addStretch()  # Push left section to the left

        # Right side - User Info
        self.right_section = QWidget(self.tap_bar)
        self.right_layout = QHBoxLayout(self.right_section)
        self.right_layout.setSpacing(10)
        self.right_layout.setContentsMargins(0, 0, 0, 0)

        # User name
        self.user_name_label = QLabel(self.right_section)
        self.user_name_label.setObjectName(u"user_name_label")
        font2 = QFont()
        font2.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font2.setPointSize(12)
        self.user_name_label.setFont(font2)
        self.user_name_label.setStyleSheet(u"color: #404040;")
        self.user_name_label.setCursor(Qt.PointingHandCursor)  # 设置鼠标手型

        # User avatar
        self.user_avatar_label = QLabel(self.right_section)
        self.user_avatar_label.setObjectName(u"user_avatar_label")
        self.user_avatar_label.setFixedSize(32, 32)
        # Load and set user avatar with background color
        avatar_pixmap = QPixmap(u"./img/user_avatar.png")
        self.user_avatar_label.setPixmap(avatar_pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.user_avatar_label.setStyleSheet(u"background-color: #4200FF; border-radius: 16px;")
        self.user_avatar_label.setCursor(Qt.PointingHandCursor)  # 设置鼠标手型

        # Add to right layout
        self.right_layout.addWidget(self.user_name_label)
        self.right_layout.addWidget(self.user_avatar_label)

        # Add right section to tap bar layout
        self.tap_bar_layout.addWidget(self.right_section)

        # Bottom part - Content Area (split into left and right)
        self.content_area = QWidget(Form)
        self.content_area.setObjectName(u"content_area")

        # Content area layout
        self.content_layout = QHBoxLayout(self.content_area)
        self.content_layout.setSpacing(0)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        # Left part - 70% width
        self.left_content = QWidget(self.content_area)
        self.left_content.setObjectName(u"left_content")
        self.left_content.setStyleSheet(u"background-color: #ecf2fb;")  # Light blue

        # Right part - Fixed width with scroll area
        self.right_scroll_area = QScrollArea(self.content_area)
        self.right_scroll_area.setObjectName(u"right_scroll_area")
        self.right_scroll_area.setFixedWidth(408)  # 400px content + 8px scrollbar
        self.right_scroll_area.setWidgetResizable(True)
        self.right_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Always show to prevent width shift
        self.right_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.right_scroll_area.setStyleSheet(u"""
            QScrollArea {
                border: none;
                background-color: #FFF2E8;
            }
            QScrollBar:vertical {
                background-color: #F0F0F0;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #C0C0C0;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #A0A0A0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)

        # Scroll area content widget
        self.right_content = QWidget()
        self.right_content.setObjectName(u"right_content")
        self.right_content.setStyleSheet(u"background-color: #FFFFFF;")  # White background

        # Right content layout
        self.right_content_layout = QVBoxLayout(self.right_content)
        self.right_content_layout.setSpacing(10)
        self.right_content_layout.setContentsMargins(15, 15, 15, 15)  # 15px left + 8px scrollbar

        # Section 1
        self.section1 = ClippedSection(self.right_content, radius=8)
        self.section1.setObjectName(u"section1")
        self.section1.setStyleSheet(u"""
            background-color: #FFFFFF;
            border-radius: 8px;
            border: 2px solid #E8E8E8;
        """)
        self.section1_layout = QVBoxLayout(self.section1)
        self.section1_layout.setSpacing(0)
        self.section1_layout.setContentsMargins(0, 0, 0, 0)

        # Section 1 header
        self.section1_header = QWidget(self.section1)
        self.section1_header.setObjectName(u"section1_header")
        self.section1_header.setCursor(Qt.PointingHandCursor)  # 设置手型光标
        self.section1_header.setStyleSheet(u"""
            border-radius: 0;
            border-bottom: 1px solid #CCCCCC;
            border-top: none;
            border-left: none;
            border-right: none;
            background-color: none;
        """)
        self.section1_header.enterEvent = lambda event: self.section1_header.setStyleSheet(u"""
            border-radius: 0;
            border-bottom: 1px solid #CCCCCC;
            border-top: none;
            border-left: none;
            border-right: none;
            background-color: #faf9fb;
        """)
        self.section1_header.leaveEvent = lambda event: self.section1_header.setStyleSheet(u"""
            border-radius: 0;
            border-bottom: 1px solid #CCCCCC;
            border-top: none;
            border-left: none;
            border-right: none;
            background-color: none;
        """)
        self.section1_header_layout = QHBoxLayout(self.section1_header)
        self.section1_header_layout.setContentsMargins(15, 15, 15, 15)

        self.section1_title = QLabel(self.section1_header)
        self.section1_title.setObjectName(u"section1_title")
        font_section = QFont()
        font_section.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font_section.setPointSize(12)
        font_section.setBold(True)
        self.section1_title.setFont(font_section)
        self.section1_title.setStyleSheet(u"color: #404040; border: none;")
        self.section1_title.setCursor(Qt.PointingHandCursor)

        self.section1_expand_icon = QLabel(self.section1_header)
        self.section1_expand_icon.setObjectName(u"section1_expand_icon")
        self.section1_expand_icon.setStyleSheet(u"border: none;")
        self.section1_expand_icon.setFixedSize(16, 16)
        expand_pixmap = QPixmap(u"./img/Icon_angle-down.png")
        self.section1_expand_icon.setPixmap(expand_pixmap.scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.section1_expand_icon.setCursor(Qt.PointingHandCursor)

        self.section1_header_layout.addWidget(self.section1_title)
        self.section1_header_layout.addStretch()
        self.section1_header_layout.addWidget(self.section1_expand_icon)

        # Section 1 content
        self.section1_content = QWidget(self.section1)
        self.section1_content.setObjectName(u"section1_content")
        self.section1_content.setStyleSheet(u"margin: 5px; border: none;")
        self.section1_content_layout = QVBoxLayout(self.section1_content)
        self.section1_content_layout.setContentsMargins(10, 10, 10, 10)

        # Add slider controls for brightness, contrast, and sharpness
        self.brightness_slider_widget = self.create_slider_widget("Brightness", 0, 100, 50, "%")
        self.contrast_slider_widget = self.create_slider_widget("Contrast", 0, 100, 50, "%")
        self.sharpness_slider_widget = self.create_slider_widget("Overlay Opacity", 0, 100, 50)

        self.section1_content_layout.addWidget(self.brightness_slider_widget)
        self.section1_content_layout.addWidget(self.contrast_slider_widget)
        self.section1_content_layout.addWidget(self.sharpness_slider_widget)

        # 添加按钮
        self.apply_button = QPushButton("Reset Parameters")
        self.apply_button.setStyleSheet(u"""
            QPushButton {
                background-color: #FFFFFF;
                border: 1px solid #CCCCCC;
                border-radius: 8px;
                color: #404040;
                font-size: 14px;
                font-family: "微软雅黑";
                padding: 0;
            }
            QPushButton:hover {
                background-color: #F0F0F0;
            }
            QPushButton:pressed {
                background-color: #E0E0E0;
            }
        """)
        self.apply_button.setFixedHeight(50)

        self.section1_content_layout.addWidget(self.apply_button)
        self.section1_content_layout.addStretch()

        self.section1_layout.addWidget(self.section1_header)
        self.section1_layout.addWidget(self.section1_content)

        # Section 2
        self.section2 = ClippedSection(self.right_content, radius=8)
        self.section2.setObjectName(u"section2")
        self.section2.setStyleSheet(u"""
            background-color: #FFFFFF;
            border-radius: 8px;
            border: 2px solid #E8E8E8;
        """)
        self.section2_layout = QVBoxLayout(self.section2)
        self.section2_layout.setSpacing(0)
        self.section2_layout.setContentsMargins(0, 0, 0, 0)

        # Section 2 header
        self.section2_header = QWidget(self.section2)
        self.section2_header.setObjectName(u"section2_header")
        self.section2_header.setCursor(Qt.PointingHandCursor)  # 设置手型光标
        self.section2_header.setStyleSheet(u"""
            border-radius: 0;
            border-bottom: 1px solid #CCCCCC;
            border-top: none;
            border-left: none;
            border-right: none;
            background-color: none;
        """)
        self.section2_header.enterEvent = lambda event: self.section2_header.setStyleSheet(u"""
            border-radius: 0;
            border-bottom: 1px solid #CCCCCC;
            border-top: none;
            border-left: none;
            border-right: none;
            background-color: #faf9fb;
        """)
        self.section2_header.leaveEvent = lambda event: self.section2_header.setStyleSheet(u"""
            border-radius: 0;
            border-bottom: 1px solid #CCCCCC;
            border-top: none;
            border-left: none;
            border-right: none;
            background-color: none;
        """)
        self.section2_header_layout = QHBoxLayout(self.section2_header)
        self.section2_header_layout.setContentsMargins(15, 15, 15, 15)

        self.section2_title = QLabel(self.section2_header)
        self.section2_title.setObjectName(u"section2_title")
        self.section2_title.setFont(font_section)
        self.section2_title.setStyleSheet(u"color: #404040; border: none;")
        self.section2_title.setCursor(Qt.PointingHandCursor)

        self.section2_expand_icon = QLabel(self.section2_header)
        self.section2_expand_icon.setObjectName(u"section2_expand_icon")
        self.section2_expand_icon.setStyleSheet(u"border: none;")
        self.section2_expand_icon.setFixedSize(16, 16)
        self.section2_expand_icon.setPixmap(expand_pixmap.scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.section2_expand_icon.setCursor(Qt.PointingHandCursor)

        self.section2_header_layout.addWidget(self.section2_title)
        self.section2_header_layout.addStretch()
        self.section2_header_layout.addWidget(self.section2_expand_icon)

        # Section 2 content
        self.section2_content = QWidget(self.section2)
        self.section2_content.setObjectName(u"section2_content")
        self.section2_content.setStyleSheet(u"margin: 10px; border: none;")
        self.section2_content_layout = QVBoxLayout(self.section2_content)
        self.section2_content_layout.setContentsMargins(10, 10, 10, 10)

        # Add sample content
        self.section2_sample = QLabel(self.section2_content)
        self.section2_sample.setObjectName(u"section2_sample")
        self.section2_sample.setText(u"Section 2 内容区域\n\n这是 Section 2 的详细内容\n• 功能 A\n• 功能 B\n• 功能 C\n• 功能 D\n• 功能 E\n• 功能 F\n• 功能 G\n• 功能 H\n• 功能 I\n• 功能 J")
        self.section2_sample.setStyleSheet(u"color: #404040;")
        self.section2_sample.setWordWrap(True)
        self.section2_content_layout.addWidget(self.section2_sample)

        self.section2_layout.addWidget(self.section2_header)
        self.section2_layout.addWidget(self.section2_content)

        # Section 3
        self.section3 = ClippedSection(self.right_content, radius=8)
        self.section3.setObjectName(u"section3")
        self.section3.setStyleSheet(u"""
            background-color: #FFFFFF;
            border-radius: 8px;
            border: 2px solid #E8E8E8;
        """)
        self.section3_layout = QVBoxLayout(self.section3)
        self.section3_layout.setSpacing(0)
        self.section3_layout.setContentsMargins(0, 0, 0, 0)

        # Section 3 header
        self.section3_header = QWidget(self.section3)
        self.section3_header.setObjectName(u"section3_header")
        self.section3_header.setCursor(Qt.PointingHandCursor)  # 设置手型光标
        self.section3_header.setStyleSheet(u"""
            border-radius: 0;
            border-bottom: 1px solid #CCCCCC;
            border-top: none;
            border-left: none;
            border-right: none;
            background-color: none;
        """)
        self.section3_header.enterEvent = lambda event: self.section3_header.setStyleSheet(u"""
            border-radius: 0;
            border-bottom: 1px solid #CCCCCC;
            border-top: none;
            border-left: none;
            border-right: none;
            background-color: #faf9fb;
        """)
        self.section3_header.leaveEvent = lambda event: self.section3_header.setStyleSheet(u"""
            border-radius: 0;
            border-bottom: 1px solid #CCCCCC;
            border-top: none;
            border-left: none;
            border-right: none;
            background-color: none;
        """)
        self.section3_header_layout = QHBoxLayout(self.section3_header)
        self.section3_header_layout.setContentsMargins(15, 15, 15, 15)

        self.section3_title = QLabel(self.section3_header)
        self.section3_title.setObjectName(u"section3_title")
        self.section3_title.setFont(font_section)
        self.section3_title.setStyleSheet(u"color: #404040; border: none;")
        self.section3_title.setCursor(Qt.PointingHandCursor)

        self.section3_expand_icon = QLabel(self.section3_header)
        self.section3_expand_icon.setObjectName(u"section3_expand_icon")
        self.section3_expand_icon.setStyleSheet(u"border: none;")
        self.section3_expand_icon.setFixedSize(16, 16)
        self.section3_expand_icon.setPixmap(expand_pixmap.scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.section3_expand_icon.setCursor(Qt.PointingHandCursor)

        self.section3_header_layout.addWidget(self.section3_title)
        self.section3_header_layout.addStretch()
        self.section3_header_layout.addWidget(self.section3_expand_icon)

        # Section 3 content
        self.section3_content = QWidget(self.section3)
        self.section3_content.setObjectName(u"section3_content")
        self.section3_content.setStyleSheet(u"margin: 10px; border: none;")
        self.section3_content_layout = QVBoxLayout(self.section3_content)
        self.section3_content_layout.setContentsMargins(10, 10, 10, 10)

        # Add sample content
        self.section3_sample = QLabel(self.section3_content)
        self.section3_sample.setObjectName(u"section3_sample")
        self.section3_sample.setText(u"Section 3 内容区域\n\n这是 Section 3 的详细内容\n• 设置 1\n• 设置 2\n• 设置 3\n• 设置 4\n• 设置 5\n• 设置 6\n• 设置 7\n• 设置 8\n• 设置 9\n• 设置 10\n• 设置 11\n• 设置 12\n• 设置 13\n• 设置 14\n• 设置 15")
        self.section3_sample.setStyleSheet(u"color: #404040;")
        self.section3_sample.setWordWrap(True)
        self.section3_content_layout.addWidget(self.section3_sample)

        self.section3_layout.addWidget(self.section3_header)
        self.section3_layout.addWidget(self.section3_content)

        # Section 4
        self.section4 = ClippedSection(self.right_content, radius=8)
        self.section4.setObjectName(u"section4")
        self.section4.setStyleSheet(u"""
            background-color: #FFFFFF;
            border-radius: 8px;
            border: 2px solid #E8E8E8;
        """)
        self.section4_layout = QVBoxLayout(self.section4)
        self.section4_layout.setSpacing(0)
        self.section4_layout.setContentsMargins(0, 0, 0, 0)

        # Section 4 header
        self.section4_header = QWidget(self.section4)
        self.section4_header.setObjectName(u"section4_header")
        self.section4_header.setCursor(Qt.PointingHandCursor)  # 设置手型光标
        self.section4_header.setStyleSheet(u"""
            border-radius: 0;
            border-bottom: 1px solid #CCCCCC;
            border-top: none;
            border-left: none;
            border-right: none;
            background-color: none;
        """)
        self.section4_header.enterEvent = lambda event: self.section4_header.setStyleSheet(u"""
            border-radius: 0;
            border-bottom: 1px solid #CCCCCC;
            border-top: none;
            border-left: none;
            border-right: none;
            background-color: #faf9fb;
        """)
        self.section4_header.leaveEvent = lambda event: self.section4_header.setStyleSheet(u"""
            border-radius: 0;
            border-bottom: 1px solid #CCCCCC;
            border-top: none;
            border-left: none;
            border-right: none;
            background-color: none;
        """)
        self.section4_header_layout = QHBoxLayout(self.section4_header)
        self.section4_header_layout.setContentsMargins(15, 15, 15, 15)

        self.section4_title = QLabel(self.section4_header)
        self.section4_title.setObjectName(u"section4_title")
        self.section4_title.setFont(font_section)
        self.section4_title.setStyleSheet(u"color: #404040; border: none;")
        self.section4_title.setCursor(Qt.PointingHandCursor)

        self.section4_expand_icon = QLabel(self.section4_header)
        self.section4_expand_icon.setObjectName(u"section4_expand_icon")
        self.section4_expand_icon.setStyleSheet(u"border: none;")
        self.section4_expand_icon.setFixedSize(16, 16)
        self.section4_expand_icon.setPixmap(expand_pixmap.scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.section4_expand_icon.setCursor(Qt.PointingHandCursor)

        self.section4_header_layout.addWidget(self.section4_title)
        self.section4_header_layout.addStretch()
        self.section4_header_layout.addWidget(self.section4_expand_icon)

        # Section 4 content
        self.section4_content = QWidget(self.section4)
        self.section4_content.setObjectName(u"section4_content")
        self.section4_content.setStyleSheet(u"margin: 10px; border: none;")
        self.section4_content_layout = QVBoxLayout(self.section4_content)
        self.section4_content_layout.setContentsMargins(10, 10, 10, 10)

        # Add sample content
        self.section4_sample = QLabel(self.section4_content)
        self.section4_sample.setObjectName(u"section4_sample")
        self.section4_sample.setText(u"Section 4 内容区域\n\n这是 Section 4 的详细内容\n• 工具 1\n• 工具 2\n• 工具 3\n• 工具 4\n• 工具 5\n• 工具 6\n• 工具 7\n• 工具 8\n• 工具 9\n• 工具 10")
        self.section4_sample.setStyleSheet(u"color: #404040;")
        self.section4_sample.setWordWrap(True)
        self.section4_content_layout.addWidget(self.section4_sample)

        self.section4_layout.addWidget(self.section4_header)
        self.section4_layout.addWidget(self.section4_content)

        # Add sections to right layout
        self.right_content_layout.addWidget(self.section1)
        self.right_content_layout.addWidget(self.section2)
        self.right_content_layout.addWidget(self.section3)
        self.right_content_layout.addWidget(self.section4)
        self.right_content_layout.addStretch()  # Push sections to the top

        # Connect click events
        self.section1_title.mousePressEvent = lambda event: self.toggle_section1()
        self.section1_expand_icon.mousePressEvent = lambda event: self.toggle_section1()
        self.section1_header.mousePressEvent = lambda event: self.toggle_section1()
        self.section2_title.mousePressEvent = lambda event: self.toggle_section2()
        self.section2_expand_icon.mousePressEvent = lambda event: self.toggle_section2()
        self.section2_header.mousePressEvent = lambda event: self.toggle_section2()
        self.section3_title.mousePressEvent = lambda event: self.toggle_section3()
        self.section3_expand_icon.mousePressEvent = lambda event: self.toggle_section3()
        self.section3_header.mousePressEvent = lambda event: self.toggle_section3()
        self.section4_title.mousePressEvent = lambda event: self.toggle_section4()
        self.section4_expand_icon.mousePressEvent = lambda event: self.toggle_section4()
        self.section4_header.mousePressEvent = lambda event: self.toggle_section4()

        # Set scroll area widget
        self.right_scroll_area.setWidget(self.right_content)

        # Add to content layout
        self.content_layout.addWidget(self.left_content)  # Left takes remaining space
        self.content_layout.addWidget(self.right_scroll_area)  # Right has fixed width with scroll

        # Shadow element between tap bar and content area
        self.shadow_element = QWidget(Form)
        self.shadow_element.setObjectName(u"shadow_element")
        self.shadow_element.setFixedHeight(4)
        self.shadow_element.setStyleSheet(u"""
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(0, 0, 0, 0.20),
                stop:0.4 rgba(0, 0, 0, 0.08),
                stop:1 rgba(0, 0, 0, 0));
        """)

        # Add widgets to main layout
        self.main_layout.addWidget(self.tap_bar)
        self.main_layout.addWidget(self.shadow_element)
        self.main_layout.addWidget(self.content_area)

        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def set_user_name(self, username):
        """设置用户名显示"""
        self.user_name_label.setText(username)

    def create_slider_widget(self, label, min_value, max_value, default_value, unit=""):
        """创建滑轨和滑块控件"""
        return SliderWidget(label, min_value, max_value, default_value, unit)

    def toggle_section1(self):
        """切换 Section 1 的展开/折叠状态"""
        if self.section1_content.isVisible():
            self.section1_content.hide()
            # 隐藏 header 的 border-bottom
            self.section1_header.setStyleSheet(u"""
                border-radius: 0;
                border-bottom: none;
                border-top: none;
                border-left: none;
                border-right: none;
                background-color: #faf9fb;
            """)
            self.section1_header.leaveEvent = lambda event: self.section1_header.setStyleSheet(u"""
                border-radius: 0;
                border-bottom: none;
                border-top: none;
                border-left: none;
                border-right: none;
                background-color: none;
            """)
            self.section1_header.enterEvent = lambda event: self.section1_header.setStyleSheet(u"""
                border-radius: 0;
                border-bottom: none;
                border-top: none;
                border-left: none;
                border-right: none;
                background-color: #faf9fb;
            """)
            # 旋转图标为折叠状态（左旋转90度）
            expand_pixmap = QPixmap(u"./img/Icon_angle-down.png")
            rotated_pixmap = expand_pixmap.transformed(QTransform().rotate(-90))
            self.section1_expand_icon.setPixmap(rotated_pixmap.scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.section1_header.leaveEvent = lambda event: self.section1_header.setStyleSheet(u"""
                border-radius: 0;
                border-bottom: 1px solid #E8E8E8;
                border-top: none;
                border-left: none;
                border-right: none;
                background-color: none;
            """)
            self.section1_header.enterEvent = lambda event: self.section1_header.setStyleSheet(u"""
                border-radius: 0;
                border-bottom: none;
                border-top: none;
                border-left: none;
                border-right: none;
                background-color: #faf9fb;
            """)
            self.section1_content.show()
            # 显示 header 的 border-bottom
            self.section1_header.setStyleSheet(u"""
                border-radius: 0;
                border-bottom: 1px solid #E8E8E8;
                border-top: none;
                border-left: none;
                border-right: none;
                background-color: #faf9fb;
            """)
            # 旋转图标为展开状态（恢复原状）
            expand_pixmap = QPixmap(u"./img/Icon_angle-down.png")
            self.section1_expand_icon.setPixmap(expand_pixmap.scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def toggle_section2(self):
        """切换 Section 2 的展开/折叠状态"""
        if self.section2_content.isVisible():
            self.section2_content.hide()
            # 隐藏 header 的 border-bottom
            self.section2_header.setStyleSheet(u"""
                border-radius: 0;
                border-bottom: none;
                border-top: none;
                border-left: none;
                border-right: none;
                background-color: #faf9fb;
            """)
            self.section2_header.leaveEvent = lambda event: self.section2_header.setStyleSheet(u"""
                border-radius: 0;
                border-bottom: none;
                border-top: none;
                border-left: none;
                border-right: none;
                background-color: none;
            """)
            self.section2_header.enterEvent = lambda event: self.section2_header.setStyleSheet(u"""
                border-radius: 0;
                border-bottom: none;
                border-top: none;
                border-left: none;
                border-right: none;
                background-color: #faf9fb;
            """)
            # 旋转图标为折叠状态（左旋转90度）
            expand_pixmap = QPixmap(u"./img/Icon_angle-down.png")
            rotated_pixmap = expand_pixmap.transformed(QTransform().rotate(-90))
            self.section2_expand_icon.setPixmap(rotated_pixmap.scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.section2_content.show()
            # 显示 header 的 border-bottom
            self.section2_header.setStyleSheet(u"""
                border-radius: 0;
                border-bottom: 1px solid #E8E8E8;
                border-top: none;
                border-left: none;
                border-right: none;
                background-color: #faf9fb;
            """)
            self.section2_header.leaveEvent = lambda event: self.section2_header.setStyleSheet(u"""
                border-radius: 0;
                border-bottom: none;
                border-top: none;
                border-left: none;
                border-right: none;
                background-color: none;
            """)
            self.section2_header.enterEvent = lambda event: self.section2_header.setStyleSheet(u"""
                border-radius: 0;
                border-bottom: none;
                border-top: none;
                border-left: none;
                border-right: none;
                background-color: #faf9fb;
            """)
            # 旋转图标为展开状态（恢复原状）
            expand_pixmap = QPixmap(u"./img/Icon_angle-down.png")
            self.section2_expand_icon.setPixmap(expand_pixmap.scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def toggle_section3(self):
        """切换 Section 3 的展开/折叠状态"""
        if self.section3_content.isVisible():
            self.section3_content.hide()
            # 隐藏 header 的 border-bottom
            self.section3_header.setStyleSheet(u"""
                border-radius: 0;
                border-bottom: none;
                border-top: none;
                border-left: none;
                border-right: none;
                background-color: #faf9fb;
            """)
            self.section3_header.leaveEvent = lambda event: self.section3_header.setStyleSheet(u"""
                border-radius: 0;
                border-bottom: none;
                border-top: none;
                border-left: none;
                border-right: none;
                background-color: none;
            """)
            self.section3_header.enterEvent = lambda event: self.section3_header.setStyleSheet(u"""
                border-radius: 0;
                border-bottom: none;
                border-top: none;
                border-left: none;
                border-right: none;
                background-color: #faf9fb;
            """)
            # 旋转图标为折叠状态（左旋转90度）
            expand_pixmap = QPixmap(u"./img/Icon_angle-down.png")
            rotated_pixmap = expand_pixmap.transformed(QTransform().rotate(-90))
            self.section3_expand_icon.setPixmap(rotated_pixmap.scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.section3_content.show()
            # 显示 header 的 border-bottom
            self.section3_header.setStyleSheet(u"""
                border-radius: 0;
                border-bottom: 1px solid #E8E8E8;
                border-top: none;
                border-left: none;
                border-right: none;
                background-color: #faf9fb;
            """)
            self.section3_header.leaveEvent = lambda event: self.section3_header.setStyleSheet(u"""
                border-radius: 0;
                border-bottom: none;
                border-top: none;
                border-left: none;
                border-right: none;
                background-color: none;
            """)
            self.section3_header.enterEvent = lambda event: self.section3_header.setStyleSheet(u"""
                border-radius: 0;
                border-bottom: none;
                border-top: none;
                border-left: none;
                border-right: none;
                background-color: #faf9fb;
            """)
            # 旋转图标为展开状态（恢复原状）
            expand_pixmap = QPixmap(u"./img/Icon_angle-down.png")
            self.section3_expand_icon.setPixmap(expand_pixmap.scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def toggle_section4(self):
        """切换 Section 4 的展开/折叠状态"""
        if self.section4_content.isVisible():
            self.section4_content.hide()
            # 隐藏 header 的 border-bottom
            self.section4_header.setStyleSheet(u"""
                border-radius: 0;
                border-bottom: none;
                border-top: none;
                border-left: none;
                border-right: none;
                background-color: #faf9fb;
            """)
            self.section4_header.leaveEvent = lambda event: self.section4_header.setStyleSheet(u"""
                border-radius: 0;
                border-bottom: none;
                border-top: none;
                border-left: none;
                border-right: none;
                background-color: none;
            """)
            self.section4_header.enterEvent = lambda event: self.section4_header.setStyleSheet(u"""
                border-radius: 0;
                border-bottom: none;
                border-top: none;
                border-left: none;
                border-right: none;
                background-color: #faf9fb;
            """)
            # 旋转图标为折叠状态（左旋转90度）
            expand_pixmap = QPixmap(u"./img/Icon_angle-down.png")
            rotated_pixmap = expand_pixmap.transformed(QTransform().rotate(-90))
            self.section4_expand_icon.setPixmap(rotated_pixmap.scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.section4_content.show()
            # 显示 header 的 border-bottom
            self.section4_header.setStyleSheet(u"""
                border-radius: 0;
                border-bottom: 1px solid #E8E8E8;
                border-top: none;
                border-left: none;
                border-right: none;
                background-color: #faf9fb;
            """)
            self.section4_header.leaveEvent = lambda event: self.section4_header.setStyleSheet(u"""
                border-radius: 0;
                border-bottom: none;
                border-top: none;
                border-left: none;
                border-right: none;
                background-color: none;
            """)
            self.section4_header.enterEvent = lambda event: self.section4_header.setStyleSheet(u"""
                border-radius: 0;
                border-bottom: none;
                border-top: none;
                border-left: none;
                border-right: none;
                background-color: #faf9fb;
            """)
            # 旋转图标为展开状态（恢复原状）
            expand_pixmap = QPixmap(u"./img/Icon_angle-down.png")
            self.section4_expand_icon.setPixmap(expand_pixmap.scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))


    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"SurgiTwins Pro", None))
        self.surgitwins_label.setText(QCoreApplication.translate("Form", u"SurgiTwins", None))
        self.pro_label.setText(QCoreApplication.translate("Form", u"Pro", None))
        self.user_name_label.setText(QCoreApplication.translate("Form", u"User Name", None))
        self.section1_title.setText(QCoreApplication.translate("Form", u"Parameter Adjustment", None))
        self.section2_title.setText(QCoreApplication.translate("Form", u"Operation Settings", None))
        self.section3_title.setText(QCoreApplication.translate("Form", u"System Log", None))
        self.section4_title.setText(QCoreApplication.translate("Form", u"Surgery Recording & Analysis", None))
    # retranslateUi

