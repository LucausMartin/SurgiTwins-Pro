# -*- coding: utf-8 -*-
# 导入sys
import os
import sys
# 任何一个PySide界面程序都需要使用QApplication
# 我们要展示一个普通的窗口，所以需要导入QWidget，用来让我们自己的类继承
from PySide2.QtWidgets import QApplication, QWidget, QMessageBox, QLineEdit
# 导入我们生成的界面
from ui.login_ui import Ui_Form
 
# 继承QWidget类，以获取其属性和方法
class MyWidget(QWidget):
  def __init__(self):
    super().__init__()
    # 设置界面为我们生成的界面
    self.ui = Ui_Form()
    self.ui.setupUi(self)

    # 连接登录按钮的点击事件
    self.ui.pushButton.clicked.connect(self.handle_login)
    # 连接回车键事件（可选）
    self.ui.lineEdit_2.returnPressed.connect(self.handle_login)
    
  # 处理登录按钮点击事件
  def handle_login(self):
    # 验证账号密码函数
    def validate_credentials(username, password):
      valid_users = {
        "admin": "123456",
        "user": "password",
        "surgitwins": "pro2024"
      }
      return valid_users.get(username) == password
  
    username = self.ui.lineEdit.text().strip()
    password = self.ui.lineEdit_2.text().strip()
    # 简单的验证逻辑
    if not username or not password:
      QMessageBox.warning(self, "输入错误", "请输入账号和密码！")
      return
    
    # 这里可以添加您的验证逻辑
    if validate_credentials(username, password):
      QMessageBox.information(self, "登录成功", f"欢迎，{username}！")
      # 登录成功后的操作，比如打开主窗口等
      self.open_main_window()
    else:
      QMessageBox.critical(self, "登录失败", "账号或密码错误！")

  def open_main_window(self):
    # 登录成功后打开主窗口
    # 这里可以添加打开新窗口的代码
    print("登录成功，打开主窗口...")
    # 例如：self.main_window = MainWindow()  
    #       self.main_window.show()
    #       self.close()

# 程序入口
if __name__ == "__main__":
  # 初始化QApplication，界面展示要包含在QApplication初始化之后，结束之前
  app = QApplication(sys.argv)

  # 初始化并展示我们的界面组件
  window = MyWidget()
  window.show()

  # 结束QApplication
  sys.exit(app.exec_())
  # 注意，在PySide6中，需要使用app.exec()
  # sys.exit(app.exec())