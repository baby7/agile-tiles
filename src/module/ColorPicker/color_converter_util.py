import math
import re
from PySide6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout,
                               QPushButton, QLineEdit, QFrame, QGroupBox, QApplication)
from PySide6.QtGui import QPainter, QColor, QPolygonF, QIcon, QPolygonF, QPixmap
from PySide6.QtCore import Qt, QRect, QPoint, Signal, QSettings, QPointF, QSize

from src.component.AgileTilesAcrylicWindow.AgileTilesAcrylicWindow import AgileTilesAcrylicWindow
from src.module.Box import message_box_util
from src.ui import style_util


class ColorPickerWidget(QWidget):
    """颜色选择器组件 - 高分辨率优化版本"""
    colorChanged = Signal(QColor)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(300, 300)
        self.hue = 0
        self.saturation = 255
        self.value = 255
        self.alpha = 255
        self.color = QColor.fromHsv(self.hue, self.saturation, self.value, self.alpha)

        # 每个圆环的扇形数量（从内到外）
        self.ring_sectors = [10, 20, 30, 45, 60, 75, 90, 120, 150, 180]
        self.rings = len(self.ring_sectors)

        # 缓存相关变量
        self.color_wheel_pixmap = None
        self.pixmap_size = QSize(0, 0)
        self.pixmap_dirty = True
        self.scale_factor = 2  # 缩放因子，使用2倍大小绘制

        # 设置背景为透明，避免重绘时闪烁
        self.setAttribute(Qt.WA_OpaquePaintEvent, False)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 检查是否需要重新生成颜色圆盘缓存
        current_size = self.size()
        if (self.pixmap_dirty or
                self.color_wheel_pixmap is None or
                self.pixmap_size != current_size):
            self.generate_color_wheel_pixmap(current_size)
            self.pixmap_dirty = False
            self.pixmap_size = current_size

        # 绘制缓存的颜色圆盘（缩小到实际大小）
        if self.color_wheel_pixmap:
            # 使用平滑变换缩放图像
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            target_rect = QRect(0, 0, current_size.width(), current_size.height())
            painter.drawPixmap(target_rect, self.color_wheel_pixmap)

        # 绘制当前选择的颜色指示器（这部分需要动态绘制）
        self.draw_color_indicator(painter)

    def generate_color_wheel_pixmap(self, size):
        """生成颜色圆盘的QPixmap缓存（使用2倍大小）"""
        if size.width() <= 0 or size.height() <= 0:
            return

        # 创建2倍大小的pixmap
        scaled_size = QSize(size.width() * self.scale_factor, size.height() * self.scale_factor)
        self.color_wheel_pixmap = QPixmap(scaled_size)
        self.color_wheel_pixmap.fill(Qt.transparent)

        pixmap_painter = QPainter(self.color_wheel_pixmap)
        pixmap_painter.setRenderHint(QPainter.Antialiasing)

        # 在2倍大小的画布上绘制HSV颜色选择圆盘
        center = QPoint(scaled_size.width() // 2, scaled_size.height() // 2)
        radius = min(scaled_size.width(), scaled_size.height()) / 2 - 10 * self.scale_factor

        # 使用三角形填充圆盘，避免边缘空隙
        for ring in range(self.rings):
            inner_radius = radius * ring / self.rings
            outer_radius = radius * (ring + 1) / self.rings

            # 当前圆环的扇形数量
            sectors = self.ring_sectors[ring]

            for sector in range(sectors):
                # 计算扇形的角度
                angle1 = sector * 2 * math.pi / sectors
                angle2 = (sector + 1) * 2 * math.pi / sectors

                # 确保最后一个扇形闭合到第一个扇形
                if sector == sectors - 1:
                    angle2 = 2 * math.pi

                overlap = 10  # 像素重叠

                # 计算三角形的四个顶点（使用2倍坐标）
                x1 = center.x() + inner_radius * math.cos(angle1) - overlap * math.cos(angle1)
                y1 = center.y() + inner_radius * math.sin(angle1) - overlap * math.sin(angle1)

                x2 = center.x() + outer_radius * math.cos(angle1) - overlap * math.cos(angle1)
                y2 = center.y() + outer_radius * math.sin(angle1) - overlap * math.sin(angle1)

                x3 = center.x() + outer_radius * math.cos(angle2) - overlap * math.cos(angle1)
                y3 = center.y() + outer_radius * math.sin(angle2) - overlap * math.sin(angle1)

                x4 = center.x() + inner_radius * math.cos(angle2) - overlap * math.cos(angle1)
                y4 = center.y() + inner_radius * math.sin(angle2) - overlap * math.sin(angle1)

                # 计算颜色 - 使用HSV颜色模型
                hue = sector * 360 / sectors
                saturation = (ring + 1) * 255 / self.rings

                color = QColor.fromHsv(int(hue), int(saturation), 255, 255)
                pixmap_painter.setPen(Qt.NoPen)
                pixmap_painter.setBrush(color)

                # 绘制两个三角形组成扇形
                triangle1 = QPolygonF([
                    QPointF(x1, y1),
                    QPointF(x2, y2),
                    QPointF(x4, y4)
                ])

                triangle2 = QPolygonF([
                    QPointF(x2, y2),
                    QPointF(x3, y3),
                    QPointF(x4, y4)
                ])

                pixmap_painter.drawPolygon(triangle1)
                pixmap_painter.drawPolygon(triangle2)

        pixmap_painter.end()

    def draw_color_indicator(self, painter):
        """绘制颜色指示器（动态部分）"""
        center = self.rect().center()
        radius = min(self.width(), self.height()) / 2 - 10

        # 计算指示器位置
        angle = self.hue * math.pi / 180
        x = center.x() + radius * math.cos(angle) * (self.saturation / 255)
        y = center.y() + radius * math.sin(angle) * (self.saturation / 255)

        # 绘制指示器
        painter.setPen(Qt.black)
        painter.setBrush(Qt.white)
        painter.drawEllipse(QPoint(round(x), round(y)), 5, 5)

    def mousePressEvent(self, event):
        self.update_color(event.position().toPoint())

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.update_color(event.position().toPoint())

    def update_color(self, pos):
        center = self.rect().center()
        dx = pos.x() - center.x()
        dy = pos.y() - center.y()

        # 计算角度和距离
        angle = math.atan2(dy, dx) * 180 / math.pi
        if angle < 0:
            angle += 360

        distance = math.sqrt(dx * dx + dy * dy)
        max_distance = min(self.width(), self.height()) / 2 - 10

        # 更新HSV值
        old_hue = self.hue
        old_saturation = self.saturation

        self.hue = int(angle)
        self.saturation = min(255, int(255 * distance / max_distance))

        # 如果颜色有变化，才更新并发射信号
        if old_hue != self.hue or old_saturation != self.saturation:
            # 更新颜色，保持原有透明度
            self.color = QColor.fromHsv(self.hue, self.saturation, self.value, self.alpha)
            self.colorChanged.emit(self.color)

            # 只更新需要重绘的区域（指示器移动的区域）
            self.update()

    def resizeEvent(self, event):
        """窗口大小改变时重新生成缓存"""
        super().resizeEvent(event)
        self.pixmap_dirty = True

    def set_hue(self, hue):
        """设置色调"""
        if 0 <= hue <= 360 and self.hue != hue:
            self.hue = hue
            self.color = QColor.fromHsv(self.hue, self.saturation, self.value, self.alpha)
            self.colorChanged.emit(self.color)
            self.update()

    def set_saturation(self, saturation):
        """设置饱和度"""
        if 0 <= saturation <= 255 and self.saturation != saturation:
            self.saturation = saturation
            self.color = QColor.fromHsv(self.hue, self.saturation, self.value, self.alpha)
            self.colorChanged.emit(self.color)
            self.update()

    def set_value(self, value):
        """设置亮度"""
        if 0 <= value <= 255 and self.value != value:
            self.value = value
            self.color = QColor.fromHsv(self.hue, self.saturation, self.value, self.alpha)
            self.colorChanged.emit(self.color)
            # 亮度改变不需要重绘圆盘，因为圆盘是固定亮度的
            self.update()

    def set_alpha(self, alpha):
        """设置透明度"""
        if 0 <= alpha <= 255 and self.alpha != alpha:
            self.alpha = alpha
            self.color = QColor.fromHsv(self.hue, self.saturation, self.value, self.alpha)
            self.colorChanged.emit(self.color)
            # 透明度改变不需要重绘圆盘
            self.update()

    def get_color(self):
        """获取当前颜色"""
        return self.color

    def set_scale_factor(self, factor):
        """设置缩放因子，可以动态调整分辨率"""
        if factor > 0 and self.scale_factor != factor:
            self.scale_factor = factor
            self.pixmap_dirty = True
            self.update()


class HorizontalValueSlider(QWidget):
    """横向亮度滑块组件"""
    valueChanged = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(15)
        self.value = 255

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制亮度渐变
        gradient_rect = QRect(10, 5, self.width() - 20, 10)

        for i in range(gradient_rect.width()):
            value = int(255 * i / gradient_rect.width())
            color = QColor.fromHsv(0, 0, value)
            painter.setPen(color)
            painter.drawLine(gradient_rect.left() + i, gradient_rect.top(),
                             gradient_rect.left() + i, gradient_rect.bottom())

        # 绘制当前值指示器
        x = gradient_rect.left() + gradient_rect.width() * self.value / 255
        painter.setPen(Qt.black)
        painter.setBrush(Qt.white)
        painter.drawEllipse(QRect(int(x) - 5, 5, 9, 9))

    def mousePressEvent(self, event):
        self.update_value(event.position().toPoint())

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.update_value(event.position().toPoint())

    def update_value(self, pos):
        gradient_rect = QRect(10, 5, self.width() - 20, 5)
        x = max(gradient_rect.left(), min(gradient_rect.right(), pos.x()))

        # 修复计算，确保可以到达最大值255
        ratio = (x - gradient_rect.left()) / gradient_rect.width()
        self.value = min(255, round(ratio * 256))  # 使用256确保可以到达255
        self.valueChanged.emit(self.value)
        self.update()


class HorizontalAlphaSlider(QWidget):
    """横向透明度滑块组件"""
    valueChanged = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(15)
        self.value = 255
        self.base_color = QColor(255, 0, 0)  # 默认红色，会在使用时更新

    def set_base_color(self, color):
        """设置基础颜色（用于透明度渐变的显示）"""
        self.base_color = QColor(color.red(), color.green(), color.blue(), 255)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制透明度渐变
        gradient_rect = QRect(10, 5, self.width() - 20, 10)

        # 绘制透明度渐变
        for i in range(gradient_rect.width()):
            alpha = int(255 * i / gradient_rect.width())
            color = QColor(self.base_color)
            color.setAlpha(alpha)
            painter.setPen(color)
            painter.drawLine(gradient_rect.left() + i, gradient_rect.top(),
                             gradient_rect.left() + i, gradient_rect.bottom())

        # 绘制当前值指示器
        x = gradient_rect.left() + gradient_rect.width() * self.value / 255
        painter.setPen(Qt.black)
        painter.setBrush(Qt.white)
        painter.drawEllipse(QRect(int(x) - 5, 5, 9, 9))

    def mousePressEvent(self, event):
        self.update_value(event.position().toPoint())

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.update_value(event.position().toPoint())

    def update_value(self, pos):
        gradient_rect = QRect(10, 5, self.width() - 20, 5)
        x = max(gradient_rect.left(), min(gradient_rect.right(), pos.x()))

        # 修复计算，确保可以到达最大值255
        ratio = (x - gradient_rect.left()) / gradient_rect.width()
        self.value = min(255, round(ratio * 256))  # 使用256确保可以到达255
        self.valueChanged.emit(self.value)
        self.update()


class ColorConverterDialog(AgileTilesAcrylicWindow):
    def __init__(self, parent=None, use_parent=None, title=None, content=None, initial_color=None):
        super().__init__(parent=parent, is_dark=use_parent.is_dark, form_theme_mode=use_parent.form_theme_mode,
                         form_theme_transparency=use_parent.form_theme_transparency)
        # 初始化
        self.parent = parent
        self.use_parent = use_parent
        # 设置标题栏
        self.setWindowTitle(title)  # 设置到标题栏
        self.titleBar.minBtn.close()
        self.titleBar.maxBtn.close()
        self.setMinimumSize(700, 400)
        # 初始化界面
        self.color = initial_color
        # 初始化 QSettings
        self.settings = QSettings(self.use_parent.app_name, "Tool" + "ColorConverter")
        if self.color is None:
            self.color = QColor(self.settings.value("color", "#FF0000"))
        else:
            self.settings.setValue("color", self.color.name())
        self.init_ui()
        self.update_color_displays(self.color)
        # 设置样式
        style_util.set_dialog_control_style(self, self.is_dark)

    def init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setSpacing(15)
        self.widget_base.setLayout(main_layout)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # 左侧颜色选择区域
        left_frame = QFrame()
        left_frame.setFrameStyle(QFrame.Box)
        left_layout = QVBoxLayout(left_frame)

        # 颜色选择器
        self.color_picker = ColorPickerWidget()
        self.color_picker.colorChanged.connect(self.on_color_changed)
        left_layout.addWidget(self.color_picker, alignment=Qt.AlignmentFlag.AlignCenter)

        # 创建滑块容器，添加标签
        sliders_widget = QWidget()
        sliders_layout = QVBoxLayout(sliders_widget)
        sliders_layout.setSpacing(10)

        # 亮度滑块和标签
        brightness_widget = QWidget()
        brightness_layout = QHBoxLayout(brightness_widget)
        brightness_layout.setContentsMargins(0, 0, 0, 0)
        brightness_label = QLabel("亮度:")
        brightness_label.setMaximumWidth(40)
        brightness_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.value_slider = HorizontalValueSlider()
        self.value_slider.valueChanged.connect(self.on_value_changed)
        brightness_layout.addWidget(brightness_label)
        brightness_layout.addWidget(self.value_slider)
        sliders_layout.addWidget(brightness_widget)

        # 透明度滑块和标签
        alpha_widget = QWidget()
        alpha_layout = QHBoxLayout(alpha_widget)
        alpha_layout.setContentsMargins(0, 0, 0, 0)
        alpha_label = QLabel("透明度:")
        alpha_label.setMaximumWidth(40)
        alpha_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.alpha_slider = HorizontalAlphaSlider()
        self.alpha_slider.valueChanged.connect(self.on_alpha_changed)
        alpha_layout.addWidget(alpha_label)
        alpha_layout.addWidget(self.alpha_slider)
        sliders_layout.addWidget(alpha_widget)

        left_layout.addWidget(sliders_widget)

        # 右侧颜色格式区域
        right_frame = QFrame()
        right_layout = QVBoxLayout(right_frame)

        # 颜色展示区域 - 添加棋盘背景以显示透明度
        self.color_display_bg = QFrame()
        self.color_display_bg.setFixedHeight(100)
        self.color_display_bg.setFixedWidth(300)
        self.color_display_bg.setStyleSheet(
            "background-color: transparent; border: 1px solid black;")

        self.color_display = QFrame(self.color_display_bg)
        self.color_display.setGeometry(0, 0, self.color_display_bg.width(), self.color_display_bg.height())
        self.color_display.setStyleSheet(f"background-color: {self.color.name(QColor.NameFormat.HexArgb)};")

        right_layout.addWidget(self.color_display_bg)

        # 颜色格式输入框
        format_group = QGroupBox("颜色格式")
        format_group.setStyleSheet("QGroupBox{border: 1px solid rgba(125, 125, 125, 125); padding-top: 8px;}")
        format_group.setMinimumWidth(300)
        format_layout = QVBoxLayout(format_group)

        # HEX格式
        hex_widget = QWidget()
        hex_layout = QHBoxLayout(hex_widget)
        hex_layout.setContentsMargins(0, 0, 0, 0)
        hex_layout.addWidget(QLabel("HEX:"))
        self.hex_edit = QLineEdit()
        self.hex_edit.textEdited.connect(self.hex_changed)
        hex_layout.addWidget(self.hex_edit)
        self.hex_copy_btn = QPushButton("复制")
        self.hex_copy_btn.setFixedWidth(50)
        self.hex_copy_btn.clicked.connect(lambda: self.copy_to_clipboard(self.hex_edit.text()))
        hex_layout.addWidget(self.hex_copy_btn)
        format_layout.addWidget(hex_widget)

        # RGB格式
        rgb_widget = QWidget()
        rgb_layout = QHBoxLayout(rgb_widget)
        rgb_layout.setContentsMargins(0, 0, 0, 0)
        rgb_layout.addWidget(QLabel("RGB:"))
        self.rgb_edit = QLineEdit()
        self.rgb_edit.setPlaceholderText("rgb(r, g, b) 或 rgba(r, g, b, a)")
        self.rgb_edit.textEdited.connect(self.rgb_changed)
        rgb_layout.addWidget(self.rgb_edit)
        self.rgb_copy_btn = QPushButton("复制")
        self.rgb_copy_btn.setFixedWidth(50)
        self.rgb_copy_btn.clicked.connect(lambda: self.copy_to_clipboard(self.rgb_edit.text()))
        rgb_layout.addWidget(self.rgb_copy_btn)
        format_layout.addWidget(rgb_widget)

        # HSL格式
        hsl_widget = QWidget()
        hsl_layout = QHBoxLayout(hsl_widget)
        hsl_layout.setContentsMargins(0, 0, 0, 0)
        hsl_layout.addWidget(QLabel("HSL:"))
        self.hsl_edit = QLineEdit()
        self.hsl_edit.setPlaceholderText("hsl(h, s%, l%) 或 hsla(h, s%, l%, a)")
        self.hsl_edit.textEdited.connect(self.hsl_changed)
        hsl_layout.addWidget(self.hsl_edit)
        self.hsl_copy_btn = QPushButton("复制")
        self.hsl_copy_btn.setFixedWidth(50)
        self.hsl_copy_btn.clicked.connect(lambda: self.copy_to_clipboard(self.hsl_edit.text()))
        hsl_layout.addWidget(self.hsl_copy_btn)
        format_layout.addWidget(hsl_widget)

        # HSV格式
        hsv_widget = QWidget()
        hsv_layout = QHBoxLayout(hsv_widget)
        hsv_layout.setContentsMargins(0, 0, 0, 0)
        hsv_layout.addWidget(QLabel("HSV:"))
        self.hsv_edit = QLineEdit()
        self.hsv_edit.setPlaceholderText("hsv(h, s%, v%) 或 hsva(h, s%, v%, a)")
        self.hsv_edit.textEdited.connect(self.hsv_changed)
        hsv_layout.addWidget(self.hsv_edit)
        self.hsv_copy_btn = QPushButton("复制")
        self.hsv_copy_btn.setFixedWidth(50)
        self.hsv_copy_btn.clicked.connect(lambda: self.copy_to_clipboard(self.hsv_edit.text()))
        hsv_layout.addWidget(self.hsv_copy_btn)
        format_layout.addWidget(hsv_widget)

        # HWB格式
        hwb_widget = QWidget()
        hwb_layout = QHBoxLayout(hwb_widget)
        hwb_layout.setContentsMargins(0, 0, 0, 0)
        hwb_layout.addWidget(QLabel("HWB:"))
        self.hwb_edit = QLineEdit()
        self.hwb_edit.setPlaceholderText("hwb(h, w%, b%) 或 hwba(h, w%, b%, a)")
        self.hwb_edit.textEdited.connect(self.hwb_changed)
        hwb_layout.addWidget(self.hwb_edit)
        self.hwb_copy_btn = QPushButton("复制")
        self.hwb_copy_btn.setFixedWidth(50)
        self.hwb_copy_btn.clicked.connect(lambda: self.copy_to_clipboard(self.hwb_edit.text()))
        hwb_layout.addWidget(self.hwb_copy_btn)
        format_layout.addWidget(hwb_widget)

        right_layout.addWidget(format_group)

        main_layout.addWidget(left_frame, 2)
        main_layout.addWidget(right_frame, 1)

    def copy_to_clipboard(self, text):
        """复制文本到剪贴板"""
        QApplication.clipboard().setText(text)
        message_box_util.box_information(self.use_parent, "提示", "成功复制到剪贴板")

    def on_color_changed(self, color):
        """颜色选择器颜色改变时的处理"""
        h, s, v, a = color.hue(), color.saturation(), color.value(), color.alpha()
        self.value_slider.value = v
        self.value_slider.update()

        self.alpha_slider.value = a
        self.alpha_slider.set_base_color(color)
        self.alpha_slider.update()

        # 更新颜色
        self.color = color
        self.update_color_displays(color)

    def on_value_changed(self, value):
        """亮度滑块值改变时的处理"""
        # 更新颜色
        self.color = QColor.fromHsv(self.color.hue(), self.color.saturation(), value, self.color.alpha())
        self.update_color_displays(self.color)

    def on_alpha_changed(self, value):
        """透明度滑块值改变时的处理"""
        # 更新颜色
        self.color.setAlpha(value)
        self.update_color_displays(self.color)

    def update_color_displays(self, color):
        """更新所有颜色显示"""
        self.color = color
        self.settings.setValue("color", self.color)

        # 更新颜色展示区域
        self.color_display.setStyleSheet(f"background-color: {color.name(QColor.NameFormat.HexArgb)};")

        # 更新HEX
        self.hex_edit.blockSignals(True)
        if color.alpha() < 255:
            self.hex_edit.setText(color.name(QColor.NameFormat.HexArgb))
        else:
            self.hex_edit.setText(color.name(QColor.NameFormat.HexRgb))
        self.hex_edit.blockSignals(False)

        # 更新RGB
        self.rgb_edit.blockSignals(True)
        if color.alpha() < 255:
            self.rgb_edit.setText(
                f"rgba({color.red()}, {color.green()}, {color.blue()}, {color.alpha() / 255:.2f})")
        else:
            self.rgb_edit.setText(f"rgb({color.red()}, {color.green()}, {color.blue()})")
        self.rgb_edit.blockSignals(False)

        # 更新HSL
        h, s, l = self.rgb_to_hsl(color.red(), color.green(), color.blue())
        self.hsl_edit.blockSignals(True)
        if color.alpha() < 255:
            self.hsl_edit.setText(
                f"hsla({round(h)}, {round(s * 100)}%, {round(l * 100)}%, {color.alpha() / 255:.2f})")
        else:
            self.hsl_edit.setText(f"hsl({round(h)}, {round(s * 100)}%, {round(l * 100)}%)")
        self.hsl_edit.blockSignals(False)

        # 更新HSV
        hsv_h, hsv_s, hsv_v = color.hue(), color.saturation(), color.value()
        self.hsv_edit.blockSignals(True)
        if color.alpha() < 255:
            self.hsv_edit.setText(
                f"hsva({hsv_h if hsv_h >= 0 else 0}, {round(hsv_s / 255 * 100)}%, {round(hsv_v / 255 * 100)}%, {color.alpha() / 255:.2f})")
        else:
            self.hsv_edit.setText(
                f"hsv({hsv_h if hsv_h >= 0 else 0}, {round(hsv_s / 255 * 100)}%, {round(hsv_v / 255 * 100)}%)")
        self.hsv_edit.blockSignals(False)

        # 更新HWB
        h, w, b = self.rgb_to_hwb(color.red(), color.green(), color.blue())
        self.hwb_edit.blockSignals(True)
        if color.alpha() < 255:
            self.hwb_edit.setText(
                f"hwba({round(h)}, {round(w * 100)}%, {round(b * 100)}%, {color.alpha() / 255:.2f})")
        else:
            self.hwb_edit.setText(f"hwb({round(h)}, {round(w * 100)}%, {round(b * 100)}%)")
        self.hwb_edit.blockSignals(False)

        # 更新颜色选择器和亮度滑块
        self.color_picker.hue = color.hue()
        self.color_picker.saturation = color.saturation()
        self.color_picker.value = color.value()
        self.color_picker.alpha = color.alpha()
        self.color_picker.color = color
        self.color_picker.update()

        self.value_slider.value = color.value()
        self.value_slider.update()

        self.alpha_slider.value = color.alpha()
        self.alpha_slider.set_base_color(color)
        self.alpha_slider.update()

    def rgb_to_hsl(self, r, g, b):
        """将RGB颜色转换为HSL"""
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        max_val = max(r, g, b)
        min_val = min(r, g, b)

        # 计算亮度
        l = (max_val + min_val) / 2.0

        if max_val == min_val:
            h = s = 0  # 灰色
        else:
            # 计算饱和度
            if l < 0.5:
                s = (max_val - min_val) / (max_val + min_val)
            else:
                s = (max_val - min_val) / (2.0 - max_val - min_val)

            # 计算色相
            if max_val == r:
                h = (g - b) / (max_val - min_val)
            elif max_val == g:
                h = 2.0 + (b - r) / (max_val - min_val)
            else:
                h = 4.0 + (r - g) / (max_val - min_val)

            h *= 60
            if h < 0:
                h += 360

        return h, s, l

    def hsl_to_rgb(self, h, s, l):
        """将HSL颜色转换为RGB"""
        h, s, l = h, s / 100.0, l / 100.0

        if s == 0:
            r = g = b = l  # 灰色
        else:
            def hue_to_rgb(p, q, t):
                if t < 0: t += 1
                if t > 1: t -= 1
                if t < 1 / 6: return p + (q - p) * 6 * t
                if t < 1 / 2: return q
                if t < 2 / 3: return p + (q - p) * (2 / 3 - t) * 6
                return p

            q = l * (1 + s) if l < 0.5 else l + s - l * s
            p = 2 * l - q
            r = hue_to_rgb(p, q, h / 360 + 1 / 3)
            g = hue_to_rgb(p, q, h / 360)
            b = hue_to_rgb(p, q, h / 360 - 1 / 3)

        return round(r * 255), round(g * 255), round(b * 255)

    def rgb_to_hwb(self, r, g, b):
        """将RGB颜色转换为HWB"""
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        max_val = max(r, g, b)
        min_val = min(r, g, b)

        # 计算色相（与HSL相同）
        if max_val == min_val:
            h = 0  # 灰色
        else:
            if max_val == r:
                h = (g - b) / (max_val - min_val)
            elif max_val == g:
                h = 2.0 + (b - r) / (max_val - min_val)
            else:
                h = 4.0 + (r - g) / (max_val - min_val)

            h *= 60
            if h < 0:
                h += 360

        # 计算白度和黑度
        w = min_val
        b_val = 1 - max_val

        return h, w, b_val

    def hwb_to_rgb(self, h, w, b):
        """将HWB颜色转换为RGB"""
        h, w, b = h, w / 100.0, b / 100.0

        if w + b >= 1:
            # 灰色比例
            gray = round(w * 255)
            return gray, gray, gray

        # 通过HSL转换
        h, s, l = h, 1.0, 0.5  # 先使用默认值
        r, g, b_val = self.hsl_to_rgb(h, s * 100, l * 100)

        # 应用白度和黑度
        r = round(r * (1 - w - b) + w * 255)
        g = round(g * (1 - w - b) + w * 255)
        b_val = round(b_val * (1 - w - b) + w * 255)

        return r, g, b_val

    def parse_color_string(self, text):
        """解析颜色字符串，支持多种格式，返回QColor对象"""
        text = text.strip()

        # 处理HEX格式
        if text.startswith("#"):
            hex_text = text[1:]
            # 支持3位、6位、8位HEX
            if len(hex_text) == 3:
                # 扩展3位HEX到6位
                hex_text = ''.join([c * 2 for c in hex_text])
                return QColor.fromRgb(int(hex_text[0:2], 16), int(hex_text[2:4], 16),
                                      int(hex_text[4:6], 16), self.color.alpha())
            elif len(hex_text) == 6:
                return QColor.fromRgb(int(hex_text[0:2], 16), int(hex_text[2:4], 16),
                                      int(hex_text[4:6], 16), self.color.alpha())
            elif len(hex_text) == 8:
                return QColor.fromRgba(int(hex_text, 16))

        # 处理RGB/RGBA格式
        rgb_match = re.match(r'rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([\d.]+)\s*)?\)', text, re.IGNORECASE)
        if rgb_match:
            r = int(rgb_match.group(1))
            g = int(rgb_match.group(2))
            b = int(rgb_match.group(3))
            if rgb_match.group(4):  # 有透明度值
                alpha_str = rgb_match.group(4)
                # 透明度值已经是小数，直接转换为0-255范围
                a = int(float(alpha_str) * 255)
                return QColor.fromRgb(r, g, b, a)
            else:
                return QColor.fromRgb(r, g, b)

        # 处理HSL/HSLA格式
        hsl_match = re.match(r'hsla?\(\s*(\d+)\s*,\s*(\d+)%\s*,\s*(\d+)%\s*(?:,\s*([\d.]+)\s*)?\)', text,
                             re.IGNORECASE)
        if hsl_match:
            h = int(hsl_match.group(1))
            s = int(hsl_match.group(2))
            l = int(hsl_match.group(3))
            r, g, b = self.hsl_to_rgb(h, s, l)
            if hsl_match.group(4):  # 有透明度值
                alpha_str = hsl_match.group(4)
                a = int(float(alpha_str) * 255)
                return QColor.fromRgb(r, g, b, a)
            else:
                return QColor.fromRgb(r, g, b)

        # 处理HSV/HSVA格式
        hsv_match = re.match(r'hsva?\(\s*(\d+)\s*,\s*(\d+)%\s*,\s*(\d+)%\s*(?:,\s*([\d.]+)\s*)?\)', text,
                             re.IGNORECASE)
        if hsv_match:
            h = int(hsv_match.group(1))
            s = int(hsv_match.group(2))
            v = int(hsv_match.group(3))
            color = QColor.fromHsv(h, int(s * 2.55), int(v * 2.55), self.color.alpha())
            if hsv_match.group(4):  # 有透明度值
                alpha_str = hsv_match.group(4)
                a = int(float(alpha_str) * 255)
                color.setAlpha(a)
            return color

        # 处理HWB/HWBA格式
        hwb_match = re.match(r'hwba?\(\s*(\d+)\s*,\s*(\d+)%\s*,\s*(\d+)%\s*(?:,\s*([\d.]+)\s*)?\)', text,
                             re.IGNORECASE)
        if hwb_match:
            h = int(hwb_match.group(1))
            w = int(hwb_match.group(2))
            b = int(hwb_match.group(3))
            r, g, b_val = self.hwb_to_rgb(h, w, b)
            if hwb_match.group(4):  # 有透明度值
                alpha_str = hwb_match.group(4)
                a = int(float(alpha_str) * 255)
                return QColor.fromRgb(r, g, b_val, a)
            else:
                return QColor.fromRgb(r, g, b_val)

        return None

    def hex_changed(self, text):
        """HEX值改变时的处理"""
        color = self.parse_color_string(text)
        if color and color.isValid():
            self.update_color_displays(color)

    def rgb_changed(self, text):
        """RGB值改变时的处理"""
        color = self.parse_color_string(text)
        if color and color.isValid():
            self.update_color_displays(color)

    def hsl_changed(self, text):
        """HSL值改变时的处理"""
        color = self.parse_color_string(text)
        if color and color.isValid():
            self.update_color_displays(color)

    def hsv_changed(self, text):
        """HSV值改变时的处理"""
        color = self.parse_color_string(text)
        if color and color.isValid():
            self.update_color_displays(color)

    def hwb_changed(self, text):
        """HWB值改变时的处理"""
        color = self.parse_color_string(text)
        if color and color.isValid():
            self.update_color_displays(color)


def show_color_converter_dialog(main_object, title, content=None, initial_color=None):
    """显示对话框"""
    dialog = ColorConverterDialog(None, main_object, title, content, initial_color)
    dialog.refresh_geometry(main_object.toolkit.resolution_util.get_screen(main_object))
    dialog.show()
    return dialog