from PySide6.QtWidgets import QLabel, QWidget
from PySide6.QtGui import QPainter, QColor, QPen, QGuiApplication
from PySide6.QtCore import Qt, QRect, QPoint


class ScreenshotOverlay(QWidget):
    """全屏遮罩层，用于选择截图区域"""
    card_object = None

    def __init__(self, parent=None, card_object=None):
        super().__init__(parent)
        self.card_object = card_object
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
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
        self.tip_label = QLabel("拖动鼠标选择区域 | ESC取消 | 右键完成", self)
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
                self.close()
                self.card_object.screenshot_captured(self.captured_pixmap)
            else:
                self.close()
                self.card_object.cancel_screenshot()

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
                self.close()
                self.card_object.screenshot_captured(self.captured_pixmap)

    def keyPressEvent(self, event):
        """键盘事件处理"""
        if event.key() == Qt.Key.Key_Escape:
            self.close()
            self.card_object.cancel_screenshot()
