from PySide6.QtCore import Qt, QRectF, QPropertyAnimation, Property
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtWidgets import QLabel
from PySide6 import QtGui


class LoadAnimation(QLabel):
    _angle = 0  # 旋转角度（0-360）

    def __init__(self, parent=None, theme="Light"):
        super().__init__(parent)
        self.theme = theme
        self.update_theme_color()
        self.arc_pen = self.create_arc_pen()
        # 计算笔触宽度
        self.pen_with = self.width() / 30

    def create_arc_pen(self):
        """创建笔触"""
        pen = QPen(QColor(self.arc_color))
        pen.setCapStyle(Qt.RoundCap)
        return pen

    def update_theme_color(self):
        """根据主题选择颜色"""
        if self.theme == "Light":
            self.arc_color = "#7d7d7d"
        else:
            self.arc_color = "#7d7d7d"

    @Property(float)
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value % 360  # 保持角度在0-360之间
        self.update()

    def load(self):
        # 创建动画
        self.animation = QPropertyAnimation(self, b'angle')
        self.animation.setDuration(2000)  # 2秒完成一圈
        self.animation.setStartValue(0)
        self.animation.setEndValue(360)
        self.animation.setLoopCount(-1)  # 无限循环
        self.animation.start()

    def set_theme(self, is_light):
        # 更新主题颜色
        self.theme = "Light" if is_light else "Dark"
        self.update_theme_color()
        self.arc_pen = self.create_arc_pen()
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        # 动态计算笔触宽度
        self.pen_with = self.width() / 30
        self.arc_pen.setWidth(self.pen_with)
        # 定义内外圆弧的矩形
        outer_rect = QRectF(
            self.pen_with / 2,
            self.pen_with / 2,
            self.width() - self.pen_with,
            self.height() - self.pen_with
        )
        inner_rect = QRectF(
            self.pen_with * 1.5,
            self.pen_with * 1.5,
            self.width() - self.pen_with * 3,
            self.height() - self.pen_with * 3
        )
        # 设置统一的圆弧跨度
        span_angle = -270 * 16  # 顺时针270度
        # 绘制外层正向旋转圆弧
        start_outer = int((90 + self._angle) * 16)
        painter.setPen(self.arc_pen)
        painter.drawArc(outer_rect, start_outer, span_angle)
        # 绘制内层反向旋转圆弧
        start_inner = int((90 - self._angle) * 16)
        painter.drawArc(inner_rect, start_inner, span_angle)
