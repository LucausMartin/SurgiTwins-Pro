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


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1665, 1034)
        font = QFont()
        font.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font.setPointSize(14)
        Form.setFont(font)
        Form.setStyleSheet(u"background-color: #EBEFFF;")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(184, 174, 301, 91))
        font1 = QFont()
        font1.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font1.setPointSize(39)
        font1.setBold(True)
        font1.setWeight(75)
        self.label.setFont(font1)
        self.label.setStyleSheet(u"color: rgb(66, 0, 255);\n"
"font-weight: 600;")
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(494, 174, 91, 91))
        self.label_2.setFont(font1)
        self.label_2.setStyleSheet(u"font-weight: 600;")
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(184, 254, 641, 41))
        font2 = QFont()
        font2.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font2.setPointSize(21)
        font2.setBold(True)
        font2.setWeight(75)
        self.label_3.setFont(font2)
        self.label_3.setStyleSheet(u"color: #404040;\n"
"font-weight: 600;")
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(204, 344, 141, 31))
        font3 = QFont()
        font3.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font3.setPointSize(15)
        font3.setBold(True)
        font3.setWeight(62)
        self.label_4.setFont(font3)
        self.label_4.setStyleSheet(u"color: #404040;\n"
"font-weight:500;")
        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(204, 464, 121, 31))
        self.label_5.setFont(font3)
        self.label_5.setStyleSheet(u"color: #404040;\n"
"font-weight:500;")
        self.lineEdit = QLineEdit(Form)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(194, 384, 411, 51))
        font4 = QFont()
        font4.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font4.setPointSize(12)
        self.lineEdit.setFont(font4)
        self.lineEdit.setStyleSheet(u"border: 1px solid #DCD7D7;\n"
"border-radius: 10px;\n"
"padding: 10px;\n"
"background-color: #ffffff;")
        self.lineEdit_2 = QLineEdit(Form)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(194, 504, 411, 51))
        self.lineEdit_2.setFont(font4)
        self.lineEdit_2.setStyleSheet(u"border: 1px solid #DCD7D7;\n"
"border-radius: 10px;\n"
"padding: 10px;\n"
"background-color: #ffffff;")
        self.checkBox = QCheckBox(Form)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(204, 584, 221, 21))
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
        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(194, 634, 241, 51))
        font6 = QFont()
        font6.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        self.pushButton.setFont(font6)
        self.pushButton.setStyleSheet(u"color: #ffffff;\n"
"background-color: #4200FF;\n"
"border-radius: 10px;\n"
"font-size: 16px")
        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(194, 694, 281, 21))
        font7 = QFont()
        font7.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font7.setPointSize(11)
        self.label_6.setFont(font7)
        self.label_6.setStyleSheet(u"color: #404040;")
        self.label_7 = QLabel(Form)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(484, 694, 61, 21))
        self.label_7.setFont(font7)
        self.label_7.setStyleSheet(u"color: #4200FF;")
        self.label_8 = QLabel(Form)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(850, 60, 771, 741))
        self.label_8.setPixmap(QPixmap(u"./img/login_doctor.png"))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
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

