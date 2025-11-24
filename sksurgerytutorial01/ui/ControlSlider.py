from PySide2.QtGui import QFont, QKeyEvent
from PySide2.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSlider,
    QLabel,
    QProgressBar, QApplication, QSpinBox
)
from PySide2.QtCore import Qt, Signal

# 自定义SpinBox类来处理回车事件
class CustomSpinBox(QSpinBox):
    enterPressed = Signal(int)  # 添加回车信号

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.enterPressed.emit(self.value())
        super().keyPressEvent(event)


class ControlSlider(QWidget):
    # 自定义信号，用于传递滑块值
    value_changed = Signal(int)
    slider_release = Signal(int)
    spinbox_changed = Signal(int)

    def __init__(self,
                 label_text="滑块值：",
                 min_val=0,
                 max_val=100,
                 default_val=50,
                 font_size=18):
        super().__init__()
        # 创建主布局
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # 创建字体对象并设置字体大小
        font = QFont()
        font.setPointSize(font_size)

        # 创建滑块
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(min_val)  # 最小值
        self.slider.setMaximum(max_val)  # 最大值
        self.slider.setValue(default_val)  # 默认值
        self.slider.setTickPosition(QSlider.TicksBelow)  # 显示刻度
        self.slider.setTickInterval((max_val - min_val) // 10)  # 刻度间隔

        # 创建数值输入框
        self.spinbox = CustomSpinBox()
        self.spinbox.setRange(min_val, max_val)
        self.spinbox.setValue(self.slider.value())
        self.spinbox.setFont(font)

        # 添加组件到布局
        main_layout.addWidget(self.slider)

        # 创建水平布局显示数值
        value_layout = QHBoxLayout()
        label=QLabel(label_text)
        label.setFont(font)
        value_layout.addWidget(label)
        value_layout.addWidget(self.spinbox)
        main_layout.addLayout(value_layout)

        # 连接滑块值变化信号
        self.slider.valueChanged.connect(self.update_display)
        self.slider.sliderReleased.connect(self.show_release)
        self.spinbox.enterPressed.connect(self.updata_spinbox)

        self.slider_updating = False

    def updata_spinbox(self, value):
        if not self.slider_updating:
            self.spinbox.setValue(value)
            self.spinbox_changed.emit(value)

    def show_release(self):
        """发送滑块释放信号"""
        self.slider_release.emit(self.slider.value())

    def update_display(self, value):
        """发送滑块改变信号"""
        self.slider_updating=True
        # 修改数值输入框
        self.spinbox.setValue(value)
        self.slider_updating=False
        # 发送自定义信号
        self.value_changed.emit(value)

    def set_value(self, value):
        """设置滑块值"""
        self.slider.setValue(value)
        self.spinbox.setValue(value)

    def get_value(self):
        """获取当前滑块值"""
        return self.slider.value()

if __name__ == '__main__':
    app = QApplication([])
    widget = ControlSlider()
    widget.show()
    app.exec_()