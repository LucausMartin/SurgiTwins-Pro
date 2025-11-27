# -*- coding: utf-8 -*-
import sys
from PySide2.QtWidgets import QApplication
from window.login_window import LoginWindow
from window.home_window import HomeWindow
from utils.auth_manager import AuthManager

# 程序入口
if __name__ == "__main__":
  # 初始化QApplication，界面展示要包含在QApplication初始化之后，结束之前
  app = QApplication(sys.argv)

  # 检查是否有保存的登录信息
  auth_manager = AuthManager()
  saved_info = auth_manager.get_saved_login_info()

  if saved_info["remember_me"] and saved_info["username"]:
    # 有保持登录的用户信息，直接打开主窗口
    window = HomeWindow()
    window.show()
  else:
    # 没有保持登录信息，打开登录窗口
    window = LoginWindow()
    window.show()

  # 结束QApplication
  sys.exit(app.exec_())
  # 注意，在PySide6中，需要使用app.exec()
  # sys.exit(app.exec())