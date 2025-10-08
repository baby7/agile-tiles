from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Signal


class MyQLabel(QLabel):

    # 自定义单击信号
    clicked = Signal()
    # 自定义双击信号
    DoubleClicked = Signal()

    def __init__(self, parent):
        super().__init__(parent=parent)

    # 重写鼠标单击事件
    def mousePressEvent(self, QMouseEvent):  # 单击
        self.clicked.emit()

    # 重写鼠标双击事件
    def mouseDoubleClickEvent(self, e):  # 双击
        self.DoubleClicked.emit()
