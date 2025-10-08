from PySide6.QtWidgets import QProgressBar
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import Qt, QRect

class MyProgressBar(QProgressBar):

    bg_color = QColor(0, 0, 0, 50)
    chunk_color = QColor(0, 0, 0, 0)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.min_chunk_width = 10  # 最小宽度（圆角直径）

    def set_color(self, bg_color, chunk_color):
        self.bg_color = bg_color
        self.chunk_color = chunk_color

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # 绘制背景
        painter.setBrush(self.bg_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 5, 5)
        # 计算进度块宽度
        progress = (self.value() - self.minimum()) / (self.maximum() - self.minimum())
        total_width = self.width()
        chunk_width = max(int(progress * total_width), self.min_chunk_width)
        # 绘制进度块
        chunk_rect = QRect(0, 0, chunk_width, self.height())
        painter.setBrush(self.chunk_color)
        painter.drawRoundedRect(chunk_rect, 5, 5)
        painter.end()