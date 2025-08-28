from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QHBoxLayout, QFileDialog, QApplication
from PySide6.QtGui import QPainter, QColor, QPen, QGuiApplication, QPixmap
from PySide6.QtCore import Qt, QRect, QPoint, Signal


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


class ScreenshotOverlay(QWidget):
    """全屏遮罩层，用于选择截图区域"""
    main_object = None

    def __init__(self, parent=None, main_object=None):
        super().__init__(parent=None)
        self.main_object = main_object
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)  # 允许接收键盘事件
        self.setMouseTracking(True)

        # 获取所有屏幕的总体矩形 + 截图
        self.fullscreen_pixmap, screen_geometry = grab_screens()
        self.setGeometry(screen_geometry)

        # 截图相关变量
        self.start_point = QPoint()
        self.end_point = QPoint()
        self.dragging = False
        self.captured_pixmap = None

        # 提示文本
        self.tip_label = QLabel("拖动鼠标选择区域 | ESC取消", self)
        self.tip_label.setStyleSheet(
            "background-color: rgba(0, 0, 0, 120); "
            "color: white; "
            "padding: 5px; "
            "border-radius: 5px;"
        )
        self.tip_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tip_label.setGeometry(
            screen_geometry.width() // 2 - 150,
            30,
            300,
            30
        )

        # 尺寸信息显示
        self.size_label = QLabel("", self)
        self.size_label.setStyleSheet(
            "background-color: rgba(0, 0, 0, 150); "
            "color: white; "
            "padding: 3px;"
        )
        self.size_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.size_label.setFixedSize(100, 24)
        self.size_label.hide()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.fullscreen_pixmap)  # 背景

        # 半透明遮罩
        painter.fillRect(self.rect(), QColor(0, 0, 0, 120))

        if self.dragging:
            # 计算选区矩形
            rect = QRect(self.start_point, self.end_point).normalized()

            # 从截图中裁剪区域
            selected_pix = self.fullscreen_pixmap.copy(rect)

            # 绘制选区
            painter.drawPixmap(rect.topLeft(), selected_pix)

            # 绘制选区边框
            painter.setPen(QPen(QColor(255, 50, 50), 2))
            painter.drawRect(rect)

            # 更新尺寸标签
            self.size_label.setText(f"{rect.width()} x {rect.height()}")
            self.size_label.move(rect.bottomRight().x() - 50, rect.bottomRight().y() + 10)
            self.size_label.show()
        else:
            self.size_label.hide()

    def mousePressEvent(self, event):
        """鼠标按下事件处理"""
        if event.button() == Qt.MouseButton.LeftButton:
            # 使用原始坐标
            self.start_point = event.position().toPoint()
            self.end_point = self.start_point
            self.dragging = True
            self.tip_label.show()
            self.update()

    def mouseMoveEvent(self, event):
        """鼠标移动事件处理"""
        if self.dragging:
            # 使用原始坐标
            self.end_point = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event):
        """鼠标释放事件处理"""
        if event.button() == Qt.MouseButton.LeftButton and self.dragging:
            # 使用原始坐标
            self.end_point = event.position().toPoint()
            self.dragging = False

            # 获取选区矩形
            rect = QRect(self.start_point, self.end_point).normalized()

            # 确保选区有效
            if rect.width() > 10 and rect.height() > 10:
                self.captured_pixmap = self.fullscreen_pixmap.copy(rect)
                self.show_toolbar(rect)
            else:
                self.close_trigger()

        # 右键完成截图
        elif event.button() == Qt.MouseButton.RightButton and self.dragging:
            self.end_point = event.position().toPoint()
            self.dragging = False
            rect = QRect(self.start_point, self.end_point).normalized()

            if rect.width() > 10 and rect.height() > 10:
                self.captured_pixmap = self.fullscreen_pixmap.copy(rect)
                self.show_toolbar(rect)

    def show_toolbar(self, rect):
        """显示工具栏"""
        # 创建工具栏窗口
        try:
            self.toolbar = ScreenshotToolbar(
                main_object=self.main_object,
                pixmap=self.captured_pixmap,
                screenshot_rect=rect,
                screenshot_overlay=self
            )
            self.toolbar.close_signal.connect(self.close_trigger)
            self.toolbar.show()
        except Exception:
            pass

    def close_trigger(self, text=None):
        try:
            self.toolbar.close()
        except Exception:
            pass
        try:
            self.main_object.cancel_screenshot()
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


class ScreenshotToolbar(QWidget):
    """截图工具栏"""

    close_signal = Signal(str)

    def __init__(self, main_object, pixmap, screenshot_rect, parent=None, screenshot_overlay=None):
        super().__init__(parent)
        self.main_object = main_object
        self.pixmap = pixmap
        self.screenshot_rect = screenshot_rect
        self.screenshot_overlay = screenshot_overlay

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(50, 50, 50, 200);
                border-radius: 5px;
            }
            QPushButton {
                background-color: rgba(70, 70, 70, 200);
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: rgba(90, 90, 90, 200);
            }
            QPushButton:pressed {
                background-color: rgba(110, 110, 110, 200);
            }
        """)

        # 创建按钮
        self.translate_btn = QPushButton("识别文字并翻译")
        self.save_btn = QPushButton("另存为图片")
        self.copy_btn = QPushButton("复制截图到剪贴板")

        # 连接信号
        self.translate_btn.clicked.connect(self.translate_screenshot)
        self.save_btn.clicked.connect(self.save_screenshot)
        self.copy_btn.clicked.connect(self.copy_screenshot)

        # 布局
        layout = QHBoxLayout()
        layout.addWidget(self.translate_btn)
        layout.addWidget(self.save_btn)
        layout.addWidget(self.copy_btn)
        layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(layout)

        # 调整大小
        self.adjustSize()

        # 定位工具栏到截图区域附近
        self.position_toolbar(screenshot_rect)

    def position_toolbar(self, rect):
        screen_geometry = QGuiApplication.primaryScreen().virtualGeometry()

        # 计算工具栏位置
        x = rect.center().x() - self.width() // 2
        y = rect.bottom() + 10

        # 如果下方空间不足，则显示在区域上方
        if y + self.height() > screen_geometry.bottom():
            y = rect.top() - self.height() - 10

        x = max(screen_geometry.left(), min(x, screen_geometry.right() - self.width()))
        y = max(screen_geometry.top(), min(y, screen_geometry.bottom() - self.height()))

        self.move(x, y)

    def save_screenshot(self):
        """保存截图到文件"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存截图",
            "",
            "PNG Images (*.png);;JPEG Images (*.jpg *.jpeg);;All Files (*)"
        )
        if file_path:
            self.pixmap.save(file_path)
        self.close_signal.emit("")

    def translate_screenshot(self):
        """翻译截图"""
        self.main_object.screenshot_captured(self.pixmap)
        self.close_signal.emit("")

    def copy_screenshot(self):
        """复制截图到剪贴板"""
        QApplication.clipboard().setPixmap(self.pixmap)
        self.close_signal.emit("")

    def mousePressEvent(self, event):
        """点击工具栏外部关闭"""
        if event.button() == Qt.MouseButton.LeftButton:
            # 检查点击是否在工具栏内部
            if not self.rect().contains(event.pos()):
                self.close_signal.emit("")