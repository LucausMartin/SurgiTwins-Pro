# -*- coding: utf-8 -*-
import sys
from PySide2.QtWidgets import QApplication, QWidget, QMessageBox, QLineEdit
from ui.login_ui import LoginUI
from window.home_window import HomeWindow

class LoginWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.ui = LoginUI()
    self.ui.setupUi(self)

    # 连接登录按钮的点击事件
    self.ui.pushButton.clicked.connect(self.handle_login)
    # 连接回车键事件（可选）
    self.ui.lineEdit_2.returnPressed.connect(self.handle_login)
    
  # 处理登录按钮点击事件
  def handle_login(self):
    valid_users = {
      "admin": "123456",
      "user": "password",
      "surgitwins": "pro2024"
    }
    # 验证是否存在账号
    def validate_username(username):
      return username in valid_users
    
    # 已经存在的账号密码是否匹配
    def validate_credentials(username, password):
      return valid_users.get(username) == password
  
    username = self.ui.lineEdit.text().strip()
    password = self.ui.lineEdit_2.text().strip()
    # 简单的验证逻辑
    if not username or not password:
      QMessageBox.warning(self, "输入错误", "请输入账号和密码！")
      return
    
    # 这里可以添加您的验证逻辑
    if validate_username(username) and validate_credentials(username, password):
      QMessageBox.information(self, "登录成功", f"欢迎，{username}！")
      # 登录成功后的操作，比如打开主窗口等
      self.open_main_window()
    else:
      if validate_username(username):
        QMessageBox.critical(self, "登录失败", "密码错误！")
      else:
        QMessageBox.critical(self, "登录失败", "账号不存在！")

  def open_main_window(self):
    self.main_window = HomeWindow()
    self.main_window.show()
    self.close()  # 关闭登录界面