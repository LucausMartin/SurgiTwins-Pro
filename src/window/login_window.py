# -*- coding: utf-8 -*-
import sys
from PySide2.QtWidgets import QApplication, QWidget, QMessageBox, QLineEdit
from ui.login_ui import LoginUI
from window.home_window import HomeWindow
from utils.auth_manager import AuthManager

class LoginWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.ui = LoginUI()
    self.ui.setupUi(self)
    self.auth_manager = AuthManager()

    # 连接登录按钮的点击事件
    self.ui.pushButton.clicked.connect(self.handle_login)
    # 连接回车键事件（可选）
    self.ui.lineEdit_2.returnPressed.connect(self.handle_login)

    # 检查是否有保存的登录信息
    self.check_saved_login()
    
  # 处理登录按钮点击事件
  def handle_login(self):
    valid_users = {
      "admin": {
        "name": "管理员",
        "password": "123456"
      },
      "user": {
        "name": "普通用户",
        "password": "password"
      },
      "surgitwins": {
        "name": "SurgiTwins",
        "password": "pro2024"
      }
    }
    # 验证是否存在账号
    def validate_username(username):
      return username in valid_users
    
    # 已经存在的账号密码是否匹配
    def validate_credentials(username, password):
      return valid_users.get(username).get("password") == password
  
    username = self.ui.lineEdit.text().strip()
    password = self.ui.lineEdit_2.text().strip()
    # 简单的验证逻辑
    if not username or not password:
      QMessageBox.warning(self, "输入错误", "请输入账号和密码！")
      return
    
    # 这里可以添加您的验证逻辑
    if validate_username(username) and validate_credentials(username, password):
      QMessageBox.information(self, "登录成功", f"欢迎，{valid_users.get(username).get('name')}！")
      # 保存登录信息
      remember_me = self.ui.checkBox.isChecked()
      self.auth_manager.save_login_info(username, remember_me)
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

  def check_saved_login(self):
    """检查是否有保存的登录信息"""
    saved_info = self.auth_manager.get_saved_login_info()
    if saved_info["remember_me"] and saved_info["username"]:
      # 自动填充用户名
      self.ui.lineEdit.setText(saved_info["username"])
      # 自动勾选保持登录选项
      self.ui.checkBox.setChecked(True)
      # 将焦点设置到密码输入框
      self.ui.lineEdit_2.setFocus()