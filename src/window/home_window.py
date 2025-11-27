# -*- coding: utf-8 -*-
import sys
from PySide2.QtWidgets import QWidget, QMessageBox, QPushButton
from ui.home_ui import HomeUI
from utils.auth_manager import AuthManager

class HomeWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.ui = HomeUI()
    self.ui.setupUi(self)
    self.auth_manager = AuthManager()

    # 连接登录按钮的点击事件（在home窗口中可能不需要，可以注释掉）
    # self.ui.pushButton.clicked.connect(self.handle_login)
    # 连接回车键事件（可选）
    # self.ui.lineEdit_2.returnPressed.connect(self.handle_login)

    # 添加退出登录按钮
    self.logout_button = QPushButton("退出登录", self)
    self.logout_button.setGeometry(1400, 50, 100, 40)
    self.logout_button.setStyleSheet("""
        QPushButton {
            background-color: #FF4444;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 8px 12px;
            font-size: 12px;
        }
        QPushButton:hover {
            background-color: #CC3333;
        }
    """)
    self.logout_button.clicked.connect(self.handle_logout)
    
  # 处理登录按钮点击事件（在home窗口中可能不需要，可以注释掉）
  # def handle_login(self):
  #   valid_users = {
  #     "admin": "123456",
  #     "user": "password",
  #     "surgitwins": "pro2024"
  #   }
  #   # 验证是否存在账号
  #   def validate_username(username):
  #     return username in valid_users
  #
  #   # 已经存在的账号密码是否匹配
  #   def validate_credentials(username, password):
  #     return valid_users.get(username) == password
  #
  #   username = self.ui.lineEdit.text().strip()
  #   password = self.ui.lineEdit_2.text().strip()
  #   # 简单的验证逻辑
  #   if not username or not password:
  #     QMessageBox.warning(self, "输入错误", "请输入账号和密码！")
  #     return
  #
  #   # 这里可以添加您的验证逻辑
  #   if validate_username(username) and validate_credentials(username, password):
  #     QMessageBox.information(self, "登录成功", f"欢迎，{username}！")
  #     # 登录成功后的操作，比如打开主窗口等
  #   else:
  #     if validate_username(username):
  #       QMessageBox.critical(self, "登录失败", "密码错误！")
  #     else:
  #       QMessageBox.critical(self, "登录失败", "账号不存在！")

  def handle_logout(self):
    """处理退出登录"""
    from PySide2.QtWidgets import QMessageBox

    reply = QMessageBox.question(self, "确认退出", "确定要退出登录吗？",
                                QMessageBox.Yes | QMessageBox.No,
                                QMessageBox.No)

    if reply == QMessageBox.Yes:
      # 清除保持登录状态
      saved_info = self.auth_manager.get_saved_login_info()
      if saved_info["remember_me"]:
        # 如果用户之前选择了保持登录，现在清除这个状态
        self.auth_manager.clear_login_info()

      # 关闭主窗口并重新打开登录窗口
      from window.login_window import LoginWindow
      self.login_window = LoginWindow()
      self.login_window.show()
      self.close()