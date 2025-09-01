import sys

from PySide6 import QtCore
from PySide6.QtCore import Qt, Signal, Property
from PySide6.QtGui import QPainter, QPainterPath, QColor, QMouseEvent, QPaintEvent, QPen, QPixmap
from PySide6.QtWidgets import QWidget, QApplication, QLabel, QGraphicsOpacityEffect

from src.ui import style_util


class ThemeSwitchButton(QWidget):
    clicked = Signal(bool)

    def __init__(self, parent=None, is_test=False, default_theme=False):
        super().__init__(parent)
        self.is_test = is_test
        self.setStyleSheet("background-color: transparent; border: none;")
        self.raise_()  # 将控件提升到最上层
        self.m_checked = default_theme  # 使用 default_theme 参数设置默认值
        self.m_animation = True             # 动画开关
        self.m_space = 2                    # 间隔
        self.m_radius = 5                   # 滑块半径
        self.m_borderWidth = 2.5            # 边框粗细
        self.BORDER_OFFSET = 1              # 防裁剪偏移量
        self.SLIDER_SIZE_OFFSET = 6         # 滑块尺寸补偿值
        self.SLIDER_POS_OFFSET = 1          # 滑块位置补偿值
        self.TEXT_HORIZONTAL_MARGIN = 5     # 文本左右边距
        self.LABEL_AND_SLIDER_WIDTH = 1     # label和滑块之间的距离
        self.m_imageMargin = 5              # 图片标签边距
        self.m_startY = 0                   # 滑块起始位置
        self.m_endY = 0                     # 滑块结束位置
        self.progress = 1 if self.m_checked else 0                   # 当前滑块位置
        self.original_start_y = 0           # 原始滑块起始位置
        self.stop_paint = False
        # 图片标签
        self.sun_label = QLabel(self)
        self.sun_label.setPixmap(style_util.get_pixmap_by_path("Weather/sun-one", is_dark=False))
        self.sun_label.setScaledContents(True)
        self.moon_label = QLabel(self)
        self.moon_label.setPixmap(style_util.get_pixmap_by_path("Weather/moon", is_dark=True))
        self.moon_label.setScaledContents(True)
        # 动画
        self.animation = QtCore.QPropertyAnimation(self, b"sliderPosition")
        self.animation.setDuration(200)  # 设置动画持续时间
        self.animation.valueChanged.connect(self.draw_icons)  # 绑定信号

    def getSliderPosition(self):
        return self.m_startY

    def setSliderPosition(self, value):
        self.m_startY = value
        self.draw_icons()  # 调用 draw_icons() 更新图标不透明度
        self.update()  # 触发重绘

    sliderPosition = Property(float, getSliderPosition, setSliderPosition)

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self.updateImageLabels()
        self.draw_icons()
        # 初始化位置计算
        rect = self.rect().adjusted(self.BORDER_OFFSET, self.BORDER_OFFSET, -self.BORDER_OFFSET, -self.BORDER_OFFSET)
        border_radius = min(rect.width(), rect.height()) / 2
        slider_size = 2 * (border_radius - self.m_space) - self.SLIDER_SIZE_OFFSET
        if self.m_checked:
            self.m_startY = self.height() - border_radius - slider_size / 2  # 初始位置设为底部
            self.original_start_y = self.m_startY  # 初始化 original_start_y
            self.m_endY = self.m_startY  # 初始化 m_endY
        else:
            self.m_startY = 0                  # 初始位置为顶部
            self.original_start_y = self.m_startY
            self.m_endY = self.m_startY

    def resize(self, size):
        super().resize(size)
        self.updateImageLabels()
        self.draw_icons()
        # 初始化位置计算
        rect = self.rect().adjusted(self.BORDER_OFFSET, self.BORDER_OFFSET, -self.BORDER_OFFSET, -self.BORDER_OFFSET)
        border_radius = min(rect.width(), rect.height()) / 2
        slider_size = 2 * (border_radius - self.m_space) - self.SLIDER_SIZE_OFFSET
        if self.m_checked:
            self.m_startY = self.height() - border_radius - slider_size / 2  # 初始位置设为底部
            self.original_start_y = self.m_startY  # 初始化 original_start_y
            self.m_endY = self.m_startY  # 初始化 m_endY
        else:
            self.m_startY = 0                  # 初始位置为顶部
            self.original_start_y = self.m_startY
            self.m_endY = self.m_startY

    def updateImageLabels(self):
        """更新图片标签位置（上下布局）"""
        img_size = int((min(self.width(),
                            self.height()) - 2 * self.m_space - self.SLIDER_SIZE_OFFSET) - self.LABEL_AND_SLIDER_WIDTH * 2)
        sun_x = (self.width() - img_size) // 2
        sun_y = self.m_imageMargin
        self.sun_label.setGeometry(sun_x, sun_y, img_size, img_size)
        moon_y = self.height() - self.m_imageMargin - img_size
        self.moon_label.setGeometry(sun_x, moon_y, img_size, img_size)

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing)
        self.draw_background(painter)
        self.draw_slider(painter)

    def resizeEvent(self, event):
        self.updateImageLabels()
        super().resizeEvent(event)

    def draw_background(self, painter: QPainter):
        painter.save()
        border_color = QColor(0, 0, 0) if self.m_checked else QColor(255, 255, 255)
        rect = self.rect().adjusted(self.BORDER_OFFSET, self.BORDER_OFFSET, -self.BORDER_OFFSET, -self.BORDER_OFFSET)
        side = min(rect.width(), rect.height())
        path = QPainterPath()
        radius = side / 2
        path.addRoundedRect(rect, radius, radius)
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)
        border_pen = QPen(border_color, self.m_borderWidth)
        border_pen.setCosmetic(True)
        painter.setPen(border_pen)
        painter.drawPath(path)
        painter.restore()

    def draw_slider(self, painter: QPainter):
        painter.save()
        rect = self.rect().adjusted(self.BORDER_OFFSET, self.BORDER_OFFSET, -self.BORDER_OFFSET, -self.BORDER_OFFSET)
        border_radius = min(rect.width(), rect.height()) / 2
        slider_size = 2 * (border_radius - self.m_space) - self.SLIDER_SIZE_OFFSET
        # 垂直方向计算
        top_center_y = border_radius - slider_size / 2
        bottom_center_y = self.height() - border_radius - slider_size / 2
        valid_y = max(top_center_y, min(bottom_center_y, self.m_startY))
        slider_x = (self.width() - slider_size) // 2
        slider_rect = QtCore.QRectF(slider_x, valid_y, slider_size, slider_size)
        slider_color = QColor(4, 5, 6) if self.m_checked else QColor(249, 250, 251)
        painter.setPen(QPen(slider_color, self.m_borderWidth))
        painter.setBrush(slider_color.lighter(150))
        painter.drawEllipse(slider_rect)
        painter.restore()

    def mousePressEvent(self, event: QMouseEvent):
        self.m_checked = not self.m_checked
        self.clicked.emit(self.m_checked)
        rect = self.rect().adjusted(self.BORDER_OFFSET, self.BORDER_OFFSET, -self.BORDER_OFFSET, -self.BORDER_OFFSET)
        border_radius = min(rect.width(), rect.height()) / 2
        slider_size = 2 * (border_radius - self.m_space) - self.SLIDER_SIZE_OFFSET
        # 计算垂直终点位置
        self.m_endY = (self.height() - border_radius - slider_size / 2) if self.m_checked else (
                    border_radius - slider_size / 2)
        self.original_start_y = self.m_startY
        if self.m_animation:
            self.animation.setStartValue(self.m_startY)
            self.animation.setEndValue(self.m_endY)
            self.animation.start()
        else:
            self.m_startY = self.m_endY
            self.update()

    def draw_icons(self):
        # 检查是否会发生除零错误
        if self.m_endY == self.original_start_y:
            sun_opacity = 1.0 if self.m_checked else 0.0
            moon_opacity = 1.0 - sun_opacity
        else:
            progress = (self.m_startY - self.original_start_y) / (self.m_endY - self.original_start_y)
            if self.m_checked:
                sun_opacity = progress
                moon_opacity = 1.0 - progress
            else:
                moon_opacity = progress
                sun_opacity = 1.0 - progress

        # 确保不透明度在 [0, 1] 范围内
        sun_opacity = max(0.0, min(1.0, sun_opacity))
        moon_opacity = max(0.0, min(1.0, moon_opacity))

        # 设置图标的不透明度
        sun_opacity_effect = QGraphicsOpacityEffect(self.sun_label)
        sun_opacity_effect.setOpacity(sun_opacity)
        self.sun_label.setGraphicsEffect(sun_opacity_effect)
        self.sun_label.setVisible(sun_opacity > 0.01)

        moon_opacity_effect = QGraphicsOpacityEffect(self.moon_label)
        moon_opacity_effect.setOpacity(moon_opacity)
        self.moon_label.setGraphicsEffect(moon_opacity_effect)
        self.moon_label.setVisible(moon_opacity > 0.01)

        # 强制重绘标签（解决控件较多时刷新不及时的问题）
        self.sun_label.repaint()
        self.moon_label.repaint()

    def click(self):
        """外部调用的点击方法，用于切换主题"""
        # 反转当前选中状态
        self.m_checked = not self.m_checked

        # 触发点击信号
        self.clicked.emit(self.m_checked)

        # 计算滑块目标位置
        rect = self.rect().adjusted(self.BORDER_OFFSET, self.BORDER_OFFSET,
                                    -self.BORDER_OFFSET, -self.BORDER_OFFSET)
        border_radius = min(rect.width(), rect.height()) / 2
        slider_size = 2 * (border_radius - self.m_space) - self.SLIDER_SIZE_OFFSET

        # 计算终点位置
        self.m_endY = (self.height() - border_radius - slider_size / 2) if self.m_checked \
            else (border_radius - slider_size / 2)
        self.original_start_y = self.m_startY

        # 执行动画
        if self.m_animation:
            self.animation.setStartValue(self.m_startY)
            self.animation.setEndValue(self.m_endY)
            self.animation.start()
        else:
            self.m_startY = self.m_endY
            self.update()

        # 强制更新图标状态
        self.draw_icons()

# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Vertical Switch Demo")
#         self.setGeometry(300, 300, 500, 500)
#         self.setStyleSheet("background-color: #333333;")
#         self.switch = ThemeSwitchButton(self, True, default_theme=False)  # 设置 default_theme 为 False
#         # 设置垂直方向尺寸（宽40，高80）
#         self.switch.setGeometry(QtCore.QRect(100, 100, 40, 80))
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())
