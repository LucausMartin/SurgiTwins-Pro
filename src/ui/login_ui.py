# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class LoginUI(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1450, 800)
        Form.setMinimumSize(QSize(900, 600))  # Increased minimum width to ensure title visibility
        font = QFont()
        font.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font.setPointSize(14)
        Form.setFont(font)
        Form.setStyleSheet(u"background-color: #EBEFFF;")
        # Main layout - centered vertically
        self.main_layout = QHBoxLayout(Form)
        self.main_layout.setAlignment(Qt.AlignCenter)

        # Left side - login form
        self.left_widget = QWidget(Form)
        self.left_widget.setMinimumWidth(450)  # Ensure minimum width for title
        self.left_widget.setMaximumWidth(700)  # Prevent excessive width
        self.left_layout = QVBoxLayout(self.left_widget)
        self.left_layout.setAlignment(Qt.AlignTop)  # Keep content at top, prevent vertical expansion

        # Title section - fixed width for SurgiTwins and Pro
        self.title_widget = QWidget(Form)
        self.title_widget.setFixedWidth(400)  # Fixed total width for both labels (300 + 80 + 20px buffer)
        self.title_layout = QHBoxLayout(self.title_widget)
        self.title_layout.setSpacing(0)  # No spacing between SurgiTwins and Pro
        self.title_layout.setContentsMargins(0, 0, 0, 0)  # Remove any margins

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font1.setPointSize(39)
        font1.setBold(True)
        font1.setWeight(75)
        self.label.setFont(font1)
        self.label.setStyleSheet(u"color: rgb(66, 0, 255);\n"
"font-weight: 600;")
        self.label.setFixedWidth(300)  # Fixed width for "SurgiTwins"
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font1)
        self.label_2.setStyleSheet(u"font-weight: 600;")
        self.label_2.setFixedWidth(100)  # Fixed width for "Pro"
        self.label_2.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.title_layout.addWidget(self.label)
        self.title_layout.addWidget(self.label_2)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        font2 = QFont()
        font2.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font2.setPointSize(21)
        font2.setBold(True)
        font2.setWeight(75)
        self.label_3.setFont(font2)
        self.label_3.setStyleSheet(u"color: #404040;\n"
"font-weight: 600;")
        # Add title section to left layout
        self.left_layout.addWidget(self.title_widget)
        self.left_layout.addWidget(self.label_3)
        self.left_layout.addSpacing(40)

        # Form fields
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        font3 = QFont()
        font3.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font3.setPointSize(15)
        font3.setBold(True)
        font3.setWeight(62)
        self.label_4.setFont(font3)
        self.label_4.setStyleSheet(u"color: #404040;\n"
"font-weight:500;")
        self.left_layout.addWidget(self.label_4)

        self.lineEdit = QLineEdit(Form)
        self.lineEdit.setObjectName(u"lineEdit")
        font4 = QFont()
        font4.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font4.setPointSize(12)
        self.lineEdit.setFont(font4)
        self.lineEdit.setStyleSheet(u"border: 1px solid #DCD7D7;\n"
"border-radius: 10px;\n"
"padding: 10px;\n"
"background-color: #ffffff;")
        self.lineEdit.setMinimumHeight(51)
        self.lineEdit.setMaximumWidth(400)  # Set maximum width
        self.left_layout.addWidget(self.lineEdit)
        self.left_layout.addSpacing(20)

        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font3)
        self.label_5.setStyleSheet(u"color: #404040;\n"
"font-weight:500;")
        self.left_layout.addWidget(self.label_5)

        self.lineEdit_2 = QLineEdit(Form)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setFont(font4)
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.lineEdit_2.setStyleSheet(u"border: 1px solid #DCD7D7;\n"
"border-radius: 10px;\n"
"padding: 10px;\n"
"background-color: #ffffff;")
        self.lineEdit_2.setMinimumHeight(51)
        self.lineEdit_2.setMaximumWidth(400)  # Set maximum width
        self.left_layout.addWidget(self.lineEdit_2)
        self.left_layout.addSpacing(20)

        self.checkBox = QCheckBox(Form)
        self.checkBox.setObjectName(u"checkBox")
        font5 = QFont()
        font5.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font5.setPointSize(12)
        font5.setBold(True)
        font5.setWeight(62)
        self.checkBox.setFont(font5)
        self.checkBox.setStyleSheet(u"color: #404040;\n"
"font-weight: 500;")
        self.checkBox.setIconSize(QSize(20, 20))
        self.checkBox.setCheckable(True)
        self.checkBox.setChecked(False)
        self.left_layout.addWidget(self.checkBox)
        self.left_layout.addSpacing(20)

        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName(u"pushButton")
        font6 = QFont()
        font6.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        self.pushButton.setFont(font6)
        self.pushButton.setStyleSheet(u"color: #ffffff;\n"
"background-color: #4200FF;\n"
"border-radius: 10px;\n"
"font-size: 16px")
        self.pushButton.setMinimumHeight(51)
        self.pushButton.setMaximumWidth(300)  # Set maximum width smaller than input fields
        self.left_layout.addWidget(self.pushButton)
        self.left_layout.addSpacing(20)

        # Sign up link
        self.signup_layout = QHBoxLayout()
        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")
        font7 = QFont()
        font7.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font7.setPointSize(11)
        self.label_6.setFont(font7)
        self.label_6.setStyleSheet(u"color: #404040;")
        self.label_7 = QLabel(Form)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font7)
        self.label_7.setStyleSheet(u"color: #4200FF;")
        self.signup_layout.addWidget(self.label_6)
        self.signup_layout.addWidget(self.label_7)
        self.signup_layout.addStretch()
        self.left_layout.addLayout(self.signup_layout)

        # Right side - image with aspect ratio preservation
        self.label_8 = QLabel(Form)
        self.label_8.setObjectName(u"label_8")

        # Load the original pixmap
        original_pixmap = QPixmap(u"./img/login_doctor.png")

        # Create a scaled pixmap that maintains aspect ratio
        scaled_pixmap = original_pixmap.scaled(600, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label_8.setPixmap(scaled_pixmap)

        # Disable automatic scaling to prevent distortion
        self.label_8.setScaledContents(False)

        # Set size policy to maintain aspect ratio
        self.label_8.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.label_8.setStyleSheet(u"background-color: transparent;")
        self.label_8.setAlignment(Qt.AlignCenter)  # Center the image

        # Set minimum and maximum size to prevent extreme scaling
        self.label_8.setMinimumSize(300, 300)
        self.label_8.setMaximumSize(800, 800)

        # Store original pixmap for dynamic scaling
        self.original_pixmap = original_pixmap

        # Add widgets to main layout
        self.main_layout.addWidget(self.left_widget, 1)
        self.main_layout.addWidget(self.label_8, 1)

        # Store reference to form for resize handling
        self.form = Form
        Form.resizeEvent = self.on_resize

        # Set margins and spacing
        self.main_layout.setContentsMargins(30, 50, 30, 50)  # Reduced side margins for smaller screens
        self.main_layout.setSpacing(30)  # Reduced spacing for smaller screens
        self.left_layout.setContentsMargins(20, 20, 20, 20)
        self.left_layout.setSpacing(10)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def on_resize(self, event):
        """Handle window resize to maintain image aspect ratio and control text wrapping"""
        # Get current window size
        window_width = self.label_8.width()
        window_height = self.label_8.height()

        # Calculate the maximum size that fits within the available space while maintaining aspect ratio
        max_size = min(window_width, window_height, 800)  # Cap at 800px
        target_size = max(max_size, 300)  # Ensure at least 300px

        # Scale pixmap while maintaining aspect ratio
        scaled_pixmap = self.original_pixmap.scaled(target_size, target_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label_8.setPixmap(scaled_pixmap)

        # Control label_3 word wrap based on available width
        # Estimate text width for "The Intelligent Surgical Digital Twin Platform" at 21pt font
        # Approximate width calculation: ~60 characters * ~15px per character = ~900px
        text_estimated_width = 900
        # Available width for label_3 is the actual width of the label itself
        available_width = self.label_3.width()

        # Enable word wrap only when available width is less than estimated text width
        if available_width < text_estimated_width:
            self.label_3.setWordWrap(True)
        else:
            self.label_3.setWordWrap(False)

        # Call the original resize event
        if hasattr(self, 'form'):
            QWidget.resizeEvent(self.form, event)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"SurgiTwins Pro", None))
        self.label.setText(QCoreApplication.translate("Form", u"SurgiTwins", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Pro", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"The Intelligent Surgical Digital Twin Platform", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Account  ID", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Password", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("Form", u"Enter your account ID", None))
        self.lineEdit_2.setPlaceholderText(QCoreApplication.translate("Form", u"Enter your account ID", None))
        self.checkBox.setText(QCoreApplication.translate("Form", u"Keep me signed in", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"Log In", None))
        self.label_6.setText(QCoreApplication.translate("Form", u" Become member of SurgiTwins  pro?", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Sign up", None))
        self.label_8.setText("")
    # retranslateUi

