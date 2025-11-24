from PySide2.QtGui import QFont
from PySide2.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSlider,
    QLabel,
    QProgressBar, QApplication, QSpinBox, QComboBox
)
from PySide2.QtCore import Qt, Signal
class TransparencySlider(QWidget):
    # 自定义信号，用于传递滑块值
    value_changed = Signal(int)
    text_changed = Signal(str)

    def __init__(self,
                 label_text="滑块值：",
                 box_text="部件名称：",
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
        self.spinbox = QSpinBox()
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
        
        # 创建水平布局显示部件名称
        self.choices = QComboBox()
        self.choices.setFont(font)
        self.choices.addItem("ALL")
        name_layout = QHBoxLayout()
        name_label=QLabel(box_text)
        name_label.setFont(font)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.choices)
        main_layout.addLayout(name_layout)

        
        # 连接滑块值变化信号
        self.slider.valueChanged.connect(self.update_display)
        self.spinbox.valueChanged.connect(self.update_display)
        self.choices.currentIndexChanged.connect(self.change_box_name)

    def change_box_name(self):
        self.text_changed.emit(self.choices.currentText())

    def update_display(self, value):
        """发送信号"""
        # 修改数值输入框
        self.spinbox.setValue(value)
        # 发送自定义信号
        self.value_changed.emit(value)

    def set_value(self, value):
        """设置滑块值"""
        self.slider.setValue(value)
        self.spinbox.setValue(value)

    def get_value(self):
        """获取当前滑块值"""
        return self.slider.value()

    def set_choices(self,choices):
        for choice in choices:
            self.choices.addItem(choice)

    def get_current_choices(self):
        return self.choices.currentText()

if __name__ == '__main__':
    app = QApplication([])
    widget = TransparencySlider()
    widget.show()
    app.exec_()