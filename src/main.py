# -*- coding: utf-8 -*-
import sys
from PySide2.QtWidgets import QApplication
from window.login_window import LoginWindow
 
# 程序入口
if __name__ == "__main__":
  # 初始化QApplication，界面展示要包含在QApplication初始化之后，结束之前
  app = QApplication(sys.argv)

  # 初始化并展示我们的界面组件
  window = LoginWindow()
  window.show()

  # 结束QApplication
  sys.exit(app.exec_())
  # 注意，在PySide6中，需要使用app.exec()
  # sys.exit(app.exec())