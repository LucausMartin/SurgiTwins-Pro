# -*- coding: utf-8 -*-
import sys
from PySide2.QtWidgets import QWidget, QMessageBox, QPushButton
from ui.home_ui import HomeUI
from utils.auth_manager import AuthManager

class HomeWindow(QWidget):
  def __init__(self, username=None):
    super().__init__()
    self.ui = HomeUI()
    self.ui.setupUi(self)
    self.auth_manager = AuthManager()

    # 设置用户名显示
    if username:
        self.ui.set_user_name(username)
    else:
        # 如果没有传入用户名，尝试从保存的登录信息中获取
        saved_info = self.auth_manager.get_saved_login_info()
        if saved_info["real_name"]:
            self.ui.set_user_name(saved_info["real_name"])

        # 创建下拉菜单
        self.create_dropdown_menu()

        # 连接头像和用户名的点击事件
        self.ui.user_avatar_label.mousePressEvent = self.show_dropdown_menu
        self.ui.user_name_label.mousePressEvent = self.show_dropdown_menu

  def create_dropdown_menu(self):
    """创建下拉菜单"""
    from PySide2.QtWidgets import QMenu, QAction

    self.dropdown_menu = QMenu(self)
    self.dropdown_menu.setStyleSheet("""
        QMenu {
            background-color: white;
            border: 1px solid #E0E0E0;
            border-radius: 4px;
            padding: 4px;
            min-width: 140px;
        }
        QMenu::item {
            padding: 6px 8px;
            border-radius: 4px;
            font-family: "微软雅黑";
            font-size: 14px;
            margin: 1px;
            background-color: #4200FF;
            color: white;
            text-align: center;
            min-width: 130px;
            min-height: 24px;
        }
        QMenu::item:selected {
            background-color: #3500D0;
        }
    """)

    # 添加退出登录选项
    logout_action = QAction("退出登录", self)
    logout_action.triggered.connect(self.handle_logout)
    self.dropdown_menu.addAction(logout_action)

  def show_dropdown_menu(self, event):
    """显示下拉菜单"""
    # 计算菜单显示位置（在头像下方，并确保不超出窗口）
    global_pos = self.ui.user_avatar_label.mapToGlobal(self.ui.user_avatar_label.rect().bottomLeft())

    # 获取窗口尺寸和位置
    window_geometry = self.geometry()
    menu_size = self.dropdown_menu.sizeHint()

    # 计算相对于窗口的位置
    window_right = window_geometry.x() + window_geometry.width()

    # 如果菜单会超出窗口右侧，调整到左侧显示
    if global_pos.x() + menu_size.width() > window_right:
        # 计算头像右侧位置
        avatar_right = self.ui.user_avatar_label.mapToGlobal(self.ui.user_avatar_label.rect().bottomRight()).x()
        # 将菜单位置调整到头像左侧
        global_pos.setX(avatar_right - menu_size.width())

    # 如果菜单会超出屏幕底部，调整到上方显示
    screen_geometry = self.screen().availableGeometry()
    if global_pos.y() + menu_size.height() > screen_geometry.bottom():
        global_pos.setY(global_pos.y() - self.ui.user_avatar_label.height() - menu_size.height())

    self.dropdown_menu.exec_(global_pos)

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