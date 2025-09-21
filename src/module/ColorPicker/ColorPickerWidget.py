from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QPainter, QColor, QGuiApplication, QPixmap
from PySide6.QtCore import Qt, QPoint, QRect


def get_virtual_geo():
    # 获取所有屏幕计算最大的宽度和高度
    screens = QGuiApplication.screens()
    desktop_width = 0
    desktop_height = 0
    for screen in screens:
        # 获取屏幕的几何信息（逻辑像素）
        geometry = screen.geometry()
        # 获取设备像素比（缩放因子）
        device_pixel_ratio = screen.devicePixelRatio()
        # 计算物理分辨率
        physical_x = round(geometry.x() * device_pixel_ratio)
        physical_y = round(geometry.y() * device_pixel_ratio)
        physical_width = round(geometry.width() * device_pixel_ratio)
        physical_height = round(geometry.height() * device_pixel_ratio)
        # 计算相对于0坐标的顶点坐标
        screen_width = physical_x + physical_width
        screen_height = physical_y + physical_height
        # 更新最大宽高
        if screen_width > desktop_width:
            desktop_width = screen_width
        if screen_height > desktop_height:
            desktop_height = screen_height
    return QRect(0, 0, desktop_width, desktop_height)


def grab_screens():
    """截取所有屏幕，并拼接成一张大图"""
    screens = QGuiApplication.screens()
    virtual_geo = get_virtual_geo()
    result = QPixmap(virtual_geo.size())
    result.fill(Qt.GlobalColor.transparent)

    painter = QPainter(result)
    for screen in screens:
        # 获取屏幕的几何信息（逻辑像素）
        geometry = screen.geometry()
        # 获取设备像素比（缩放因子）
        device_pixel_ratio = screen.devicePixelRatio()
        # 计算物理分辨率
        physical_x = round(geometry.x() * device_pixel_ratio)
        physical_y = round(geometry.y() * device_pixel_ratio)
        physical_width = round(geometry.width() * device_pixel_ratio)
        physical_height = round(geometry.height() * device_pixel_ratio)
        physical_geometry = QRect(physical_x, physical_y, physical_width, physical_height)
        # 获取屏幕的像素
        pix = screen.grabWindow(0)
        pix.setDevicePixelRatio(1)
        # pix 已经是逻辑大小（Qt 会自动考虑 DPR）
        target_rect = physical_geometry.topLeft() - virtual_geo.topLeft()
        painter.drawPixmap(target_rect, pix)
    painter.end()
    return result, virtual_geo


class ScreenColorPicker(QWidget):
    """屏幕取色器组件"""

    def __init__(self, parent=None, main_object=None):
        super().__init__(parent=None)
        self.main_object = main_object
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setMouseTracking(True)

        # 获取屏幕截图
        self.screen_count = len(QGuiApplication.screens())
        if self.screen_count == 1:
            self.fullscreen_pixmap = QGuiApplication.primaryScreen().grabWindow(0)
            screen_geometry = QGuiApplication.primaryScreen().virtualGeometry()
            self.dpr = self.devicePixelRatioF()
        else:
            self.fullscreen_pixmap, screen_geometry = grab_screens()
            self.dpr = 1

        self.setGeometry(screen_geometry)

        # 创建提示标签 - 使用布局来组织颜色块和文本
        self.tip_label = QWidget(self)
        self.tip_label.setStyleSheet(
            "background-color: rgba(255, 255, 255, 220); "
            "color: black; "
            "padding: 5px; "
            "border-radius: 3px;"
        )
        self.tip_label.setFixedSize(280, 100)
        self.tip_label.hide()

        # 创建颜色显示区域
        self.color_display = QLabel(self.tip_label)
        self.color_display.setFixedSize(60, 60)
        self.color_display.setStyleSheet("border: 1px solid black;")

        # 创建文本标签
        self.text_label = QLabel(self.tip_label)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # 设置布局
        layout = QHBoxLayout(self.tip_label)
        layout.addWidget(self.color_display)
        layout.addWidget(self.text_label)
        layout.setSpacing(10)
        layout.setContentsMargins(5, 5, 5, 5)

    def paintEvent(self, event):
        """绘制事件"""
        painter = QPainter(self)

        # 绘制屏幕截图
        if self.screen_count > 1:
            painter.drawPixmap(0, 0, self.fullscreen_pixmap)
        else:
            win_size = self.size()
            scaled_pixmap = self.fullscreen_pixmap.scaled(
                win_size * self.dpr,
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            painter.drawPixmap(0, 0, win_size.width(), win_size.height(), scaled_pixmap)

    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        pos = event.position().toPoint()

        # 获取鼠标位置的颜色
        if self.screen_count > 1:
            color = self.fullscreen_pixmap.toImage().pixelColor(pos)
        else:
            dpr_pos = pos * self.dpr
            color = self.fullscreen_pixmap.toImage().pixelColor(dpr_pos)

        # 更新颜色显示区域
        self.color_display.setStyleSheet(
            f"background-color: {color.name(QColor.NameFormat.HexArgb)}; border: 1px solid black;")

        # 更新文本信息
        rgb_text = f"RGB: {color.red()}, {color.green()}, {color.blue()}, {color.alpha()}"
        hex_text = f"HEX: {color.name(QColor.NameFormat.HexArgb)}"
        pos_text = f"坐标: {pos.x()}, {pos.y()}"

        self.text_label.setText(f"{rgb_text}\n{hex_text}\n{pos_text}")

        # 定位提示标签在鼠标右下方
        label_pos = pos + QPoint(20, 20)
        screen_rect = self.geometry()
        if label_pos.x() + self.tip_label.width() > screen_rect.right():
            label_pos.setX(pos.x() - self.tip_label.width() - 10)
        if label_pos.y() + self.tip_label.height() > screen_rect.bottom():
            label_pos.setY(pos.y() - self.tip_label.height() - 10)

        self.tip_label.move(label_pos)
        self.tip_label.show()

        self.update()

    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position().toPoint()
            # 获取点击位置的颜色
            if self.screen_count > 1:
                color = self.fullscreen_pixmap.toImage().pixelColor(pos)
            else:
                dpr_pos = pos * self.dpr
                color = self.fullscreen_pixmap.toImage().pixelColor(dpr_pos)
            # 隐藏取色器窗口
            self.hide()
            # 显示颜色转换器
            self.main_object.color_picker_captured(color)
            # 明确接受事件，防止继续传递
            event.accept()
        else:
            # 对于非左键事件，调用父类处理
            super().mousePressEvent(event)

    def close_trigger(self, text=None):
        try:
            self.main_object.cancel_color_picker()
        except Exception:
            pass
        try:
            self.close()
        except Exception:
            pass

    def keyPressEvent(self, event):
        """键盘事件处理"""
        if event.key() == Qt.Key.Key_Escape:
            self.close_trigger()