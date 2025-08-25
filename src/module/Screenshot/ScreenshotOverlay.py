from PySide6.QtWidgets import (QLabel, QWidget, QPushButton, QHBoxLayout,
                               QVBoxLayout, QFileDialog, QApplication)
from PySide6.QtGui import QPainter, QColor, QPen, QGuiApplication, QPixmap
from PySide6.QtCore import Qt, QRect, QPoint, QTimer, Signal


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

        # 获取所有屏幕的总体矩形
        screen_geometry = QGuiApplication.primaryScreen().virtualGeometry()
        self.setGeometry(screen_geometry)

        # 截图相关变量
        self.start_point = QPoint()
        self.end_point = QPoint()
        self.dragging = False
        self.captured_pixmap = None

        # 截取整个屏幕作为背景
        self.fullscreen_pixmap = QGuiApplication.primaryScreen().grabWindow(0)
        self.dpr = self.devicePixelRatioF()  # 获取设备像素比

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
        """绘制遮罩层和选区 - 修复模糊问题"""
        painter = QPainter(self)

        # 获取窗口大小
        win_size = self.size()

        # 绘制屏幕截图背景（考虑DPI缩放）
        scaled_pixmap = self.fullscreen_pixmap.scaled(
            win_size * self.dpr,
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        painter.drawPixmap(0, 0, win_size.width(), win_size.height(), scaled_pixmap)

        # 绘制半透明遮罩层
        painter.fillRect(self.rect(), QColor(0, 0, 0, 120))

        if self.dragging:
            # 计算选区矩形
            rect = QRect(self.start_point, self.end_point).normalized()

            # 修复：从原始图像中拷贝区域（不缩放）
            dpr_rect = QRect(
                rect.topLeft() * self.dpr,
                rect.size() * self.dpr
            )
            selected_pix = self.fullscreen_pixmap.copy(dpr_rect)

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
                # 考虑设备像素比调整选区
                dpr_rect = QRect(
                    rect.topLeft() * self.dpr,
                    rect.size() * self.dpr
                )

                # 从全屏截图中裁剪选区
                self.captured_pixmap = self.fullscreen_pixmap.copy(dpr_rect)
                self.show_toolbar(rect)
            else:
                self.main_object.cancel_screenshot()
                self.close()

        # 右键完成截图
        elif event.button() == Qt.MouseButton.RightButton and self.dragging:
            self.end_point = event.position().toPoint()
            self.dragging = False

            rect = QRect(self.start_point, self.end_point).normalized()
            if rect.width() > 10 and rect.height() > 10:
                dpr_rect = QRect(
                    rect.topLeft() * self.dpr,
                    rect.size() * self.dpr
                )
                self.captured_pixmap = self.fullscreen_pixmap.copy(dpr_rect)
                self.show_toolbar(rect)

    def show_toolbar(self, rect):
        """显示工具栏"""
        # 创建工具栏窗口
        self.toolbar = ScreenshotToolbar(main_object=self.main_object, pixmap=self.captured_pixmap, screenshot_rect=rect, screenshot_overlay=self)
        self.toolbar.close_signal.connect(self.close_trigger)
        self.toolbar.show()

    def close_trigger(self, text):
        self.toolbar.close()
        self.main_object.cancel_screenshot()
        self.close()

    def keyPressEvent(self, event):
        """键盘事件处理"""
        if event.key() == Qt.Key.Key_Escape:
            self.main_object.cancel_screenshot()
            self.close()


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
        """定位工具栏到截图区域附近"""
        # 获取屏幕几何信息
        screen_geometry = QGuiApplication.primaryScreen().geometry()

        # 计算工具栏位置
        x = rect.center().x() - self.width() // 2
        y = rect.bottom() + 10

        # 如果下方空间不足，则显示在区域上方
        if y + self.height() > screen_geometry.bottom():
            y = rect.top() - self.height() - 10

        # 确保工具栏不会超出屏幕边界
        x = max(0, min(x, screen_geometry.width() - self.width()))
        y = max(0, min(y, screen_geometry.height() - self.height()))

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