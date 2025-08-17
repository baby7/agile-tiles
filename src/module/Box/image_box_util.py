from PySide6.QtGui import QPixmap, Qt, QWheelEvent, QMouseEvent
from PySide6.QtCore import Slot, QUrl, QTimer, QPoint
from PySide6.QtNetwork import QNetworkReply, QNetworkAccessManager, QNetworkRequest
from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QApplication, QFileDialog, QHBoxLayout, QScrollArea, \
    QFrame, QSizePolicy

from src.component.AgileTilesAcrylicWindow.AgileTilesAcrylicWindow import AgileTilesAcrylicWindow
from src.component.LoadAnimation.LoadAnimation import LoadAnimation
from src.ui import style_util


class ImagePopup(AgileTilesAcrylicWindow):
    def __init__(self, parent=None, use_parent=None, title=None, image_url=None, screen=None, link=None):
        super().__init__(parent=parent, is_dark=use_parent.is_dark, form_theme_mode=use_parent.form_theme_mode,
                         form_theme_transparency=use_parent.form_theme_transparency)
        try:
            self.setWindowTitle("图片查看" if title is None else title)
            # 初始化缩放和拖动相关变量
            self.original_pixmap = None  # 保存原始图片
            self.scale_factor = 1.0  # 当前缩放比例
            self.min_scale = 0.1  # 最小缩放比例
            self.max_scale = 5.0  # 最大缩放比例
            self.zoom_step = 0.1  # 缩放步长
            self.last_mouse_pos = QPoint()  # 用于拖动图片
            self.is_dragging = False  # 是否正在拖动图片
            self.mouse_position = QPoint()  # 存储鼠标位置用于缩放中心点

            self.init_ui()
            if link:
                self.standard_title_bar.setLink(link)
            self.url = image_url
            self.screen = screen

            # QtNetwork方案
            self.network_manager = QNetworkAccessManager()
            self.current_reply = None  # 用于跟踪当前请求
            # 创建网络请求
            request = QNetworkRequest(QUrl(self.url))
            request.setMaximumRedirectsAllowed(5)  # 设置最大重定向次数

            self.current_reply = self.network_manager.get(request)
            self.current_reply.finished.connect(self.on_request_finished)

            # 横向布局
            h_layout = QHBoxLayout()
            h_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            # 竖向布局
            v_layout = QVBoxLayout()
            v_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            v_layout.addLayout(h_layout)
            # 加载动画
            self.loading_animation = LoadAnimation(self, theme="Dark" if self.is_dark else "Light")
            self.loading_animation.setFixedSize(40, 40)  # 设置合适尺寸

            # 设置容器大小策略
            self.image_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

            self.scroll_area.setWidget(self.image_container)
            self.image_container.setLayout(v_layout)  # 设置布局
            h_layout.addWidget(self.loading_animation)
            self.loading_animation.load()  # 启动动画

            # 设置初始窗口大小
            self.setMinimumSize(400, 300)

            # 延迟居中加载动画
            QTimer.singleShot(100, self.center_loading_animation)
        except Exception as e:
            print(e)

    def center_loading_animation(self):
        """确保加载动画在窗口中心显示"""
        # 添加属性存在性检查
        if not hasattr(self, 'loading_animation') or self.loading_animation is None:
            return

        # 获取滚动区域视口大小
        viewport_size = self.scroll_area.viewport().size()

        # 计算居中位置
        x = (viewport_size.width() - self.loading_animation.width()) // 2
        y = (viewport_size.height() - self.loading_animation.height()) // 2

        # 移动加载动画到中心
        self.loading_animation.move(x, y)

    def init_ui(self):
        # 创建滚动区域
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(style_util.scroll_bar_style)
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 创建容器用于放置图片标签
        self.image_container = QFrame()
        self.image_container.setStyleSheet(style_util.transparent_style)
        self.image_container.setLayout(QVBoxLayout())
        self.image_container.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_container.layout().setContentsMargins(0, 0, 0, 0)
        self.image_container.layout().setSpacing(0)

        # 图片标签
        self.image_label = QLabel(self.image_container)
        self.image_label.setStyleSheet(style_util.transparent_style)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.font().setPointSize(12)
        self.image_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.image_container.layout().addWidget(self.image_label)

        # 内容布局
        self.image_layout = QVBoxLayout()
        self.image_layout.addWidget(self.scroll_area)

        # 创建按钮
        self.save_button = QPushButton("另存为图片", self)
        self.zoom_in_button = QPushButton("放大", self)
        self.zoom_out_button = QPushButton("缩小", self)
        self.reset_zoom_button = QPushButton("重置缩放", self)

        # 设置按钮大小
        button_size = (80, 30)
        self.save_button.setMinimumSize(*button_size)
        self.zoom_in_button.setMinimumSize(*button_size)
        self.zoom_out_button.setMinimumSize(*button_size)
        self.reset_zoom_button.setMinimumSize(*button_size)

        # 设置按钮样式
        button_style = style_util.normal_dark_button_style if self.is_dark else style_util.normal_light_button_style
        self.save_button.setStyleSheet(button_style)
        self.zoom_in_button.setStyleSheet(button_style)
        self.zoom_out_button.setStyleSheet(button_style)
        self.reset_zoom_button.setStyleSheet(button_style)

        # 按钮布局
        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.zoom_out_button)
        self.button_layout.addWidget(self.zoom_in_button)
        self.button_layout.addWidget(self.reset_zoom_button)
        self.button_layout.addWidget(self.save_button)
        self.button_layout.addStretch()

        self.image_layout.addLayout(self.button_layout)
        # 主布局
        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.image_layout)
        self.widget_base.setLayout(self.main_layout)
        # 连接按钮的点击信号
        self.save_button.clicked.connect(self.save_image)
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.reset_zoom_button.clicked.connect(self.reset_zoom)

        # 隐藏所有按钮直到图片加载完成
        self.save_button.hide()
        self.zoom_in_button.hide()
        self.zoom_out_button.hide()
        self.reset_zoom_button.hide()

        # 启用滚轮事件和鼠标事件
        self.image_label.setFocusPolicy(Qt.StrongFocus)
        self.image_label.wheelEvent = self.image_wheel_event
        self.image_label.mousePressEvent = self.image_mouse_press_event
        self.image_label.mouseMoveEvent = self.image_mouse_move_event
        self.image_label.mouseReleaseEvent = self.image_mouse_release_event

        self.update()

    def image_mouse_press_event(self, event: QMouseEvent):
        """鼠标按下事件 - 开始拖动"""
        if event.button() == Qt.LeftButton:
            self.last_mouse_pos = event.globalPosition().toPoint()
            self.is_dragging = True
            self.image_label.setCursor(Qt.ClosedHandCursor)
            event.accept()

    def image_mouse_move_event(self, event: QMouseEvent):
        """鼠标移动事件 - 拖动图片"""
        if self.is_dragging and self.original_pixmap:
            current_pos = event.globalPosition().toPoint()
            delta = current_pos - self.last_mouse_pos
            self.last_mouse_pos = current_pos

            # 移动滚动条
            h_scroll = self.scroll_area.horizontalScrollBar()
            v_scroll = self.scroll_area.verticalScrollBar()
            h_scroll.setValue(h_scroll.value() - delta.x())
            v_scroll.setValue(v_scroll.value() - delta.y())
            event.accept()
        else:
            # 更新鼠标位置用于缩放中心点
            self.mouse_position = event.position().toPoint()
            self.image_label.setCursor(Qt.OpenHandCursor if self.is_dragging else Qt.ArrowCursor)

    def image_mouse_release_event(self, event: QMouseEvent):
        """鼠标释放事件 - 停止拖动"""
        if event.button() == Qt.LeftButton:
            self.is_dragging = False
            self.image_label.setCursor(Qt.ArrowCursor)
            event.accept()

    def image_wheel_event(self, event: QWheelEvent):
        """处理图片区域的滚轮事件进行缩放 - 基于鼠标位置"""
        if self.original_pixmap is None:
            return

        # 获取滚轮滚动方向
        delta = event.angleDelta().y()
        self.mouse_position = event.position().toPoint()  # 获取鼠标在图片上的位置

        # 获取当前滚动条位置
        h_scroll = self.scroll_area.horizontalScrollBar()
        v_scroll = self.scroll_area.verticalScrollBar()
        scroll_pos = QPoint(h_scroll.value(), v_scroll.value())

        # 计算缩放前鼠标在图片上的位置
        label_size = self.image_label.size()
        pixmap_size = self.image_label.pixmap().size() / self.image_label.devicePixelRatio()
        pixmap_x = (label_size.width() - pixmap_size.width()) / 2
        pixmap_y = (label_size.height() - pixmap_size.height()) / 2

        # 鼠标在图片上的位置（相对于图片左上角）
        img_pos_before = QPoint(
            int(self.mouse_position.x() - pixmap_x),
            int(self.mouse_position.y() - pixmap_y)
        )

        # 执行缩放
        if delta > 0:
            self.zoom_in()
        elif delta < 0:
            self.zoom_out()

        # 缩放后重新计算鼠标位置
        pixmap_size = self.image_label.pixmap().size() / self.image_label.devicePixelRatio()
        pixmap_x = (label_size.width() - pixmap_size.width()) / 2
        pixmap_y = (label_size.height() - pixmap_size.height()) / 2

        # 计算缩放后鼠标应该在的位置
        img_pos_after = QPoint(
            int(img_pos_before.x() * self.scale_factor),
            int(img_pos_before.y() * self.scale_factor)
        )

        # 计算新的滚动位置以保持鼠标位置不变
        new_scroll_pos = QPoint(
            int(scroll_pos.x() + (self.mouse_position.x() - (pixmap_x + img_pos_after.x()))),
            int(scroll_pos.y() + (self.mouse_position.y() - (pixmap_y + img_pos_after.y())))
        )

        # 应用新的滚动位置
        h_scroll.setValue(new_scroll_pos.x())
        v_scroll.setValue(new_scroll_pos.y())

        event.accept()

    def zoom_in(self):
        """放大图片"""
        if self.original_pixmap is None:
            return

        new_scale = self.scale_factor + self.zoom_step
        if new_scale <= self.max_scale:
            self.scale_factor = new_scale
            self.update_image_display()

    def zoom_out(self):
        """缩小图片"""
        if self.original_pixmap is None:
            return

        new_scale = self.scale_factor - self.zoom_step
        if new_scale >= self.min_scale:
            self.scale_factor = new_scale
            self.update_image_display()

    def reset_zoom(self):
        """重置缩放比例"""
        if self.original_pixmap is None:
            return

        self.scale_factor = 1.0
        self.update_image_display()
        # 重置后居中图片
        self.center_image()

    def center_image(self):
        """确保图片在滚动区域中居中显示"""
        # 使用定时器确保在UI更新后执行居中
        QTimer.singleShot(50, self._do_center_image)

    def _do_center_image(self):
        """实际执行居中操作"""
        if not self.scroll_area:
            return

        # 获取滚动条
        h_scroll = self.scroll_area.horizontalScrollBar()
        v_scroll = self.scroll_area.verticalScrollBar()

        # 计算居中位置
        h_max = h_scroll.maximum()
        v_max = v_scroll.maximum()

        # 设置滚动条位置到中间
        if h_max > 0:
            h_scroll.setValue(h_max // 2)
        if v_max > 0:
            v_scroll.setValue(v_max // 2)

    def update_image_display(self):
        """根据当前缩放比例更新图片显示"""
        if self.original_pixmap is None:
            return

        # 获取设备像素比（解决高DPI屏幕模糊问题）
        device_pixel_ratio = self.image_label.devicePixelRatio()

        # 计算精确尺寸（考虑DPI缩放）
        new_width = int(self.original_pixmap.width() * self.scale_factor * device_pixel_ratio)
        new_height = int(self.original_pixmap.height() * self.scale_factor * device_pixel_ratio)

        # 创建高质量缩放图片
        scaled_pixmap = self.original_pixmap.scaled(
            new_width,
            new_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        # 设置设备像素比（关键修复）
        scaled_pixmap.setDevicePixelRatio(device_pixel_ratio)

        # 更新图片显示
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.setFixedSize(scaled_pixmap.size() / device_pixel_ratio)  # 注意尺寸调整

        # 确保容器大小适应图片
        self.image_container.setMinimumSize(scaled_pixmap.size() / device_pixel_ratio)
        self.image_container.adjustSize()

    def center_on_screen(self):
        self.refresh_geometry(self.screen)

    @Slot()
    def on_request_finished(self):
        reply = self.sender()
        if reply.error() == QNetworkReply.NoError:
            data = reply.readAll()
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            self.on_image_loaded(pixmap)
        else:
            print(f"Request failed: {reply.errorString()}")
            self.on_image_loaded(None)

        reply.deleteLater()
        self.current_reply = None

    @Slot(QPixmap)
    def on_image_loaded(self, pixmap):
        # 移除加载动画
        if hasattr(self, 'loading_animation'):
            self.loading_animation.deleteLater()
            del self.loading_animation

        if pixmap is None or pixmap.isNull():
            self.image_label.setText("加载图片失败")
            return

        # 保存原始图片
        self.original_pixmap = pixmap

        # 初始显示（按比例缩放以适应窗口）
        screen = QApplication.primaryScreen().availableGeometry()
        max_width = screen.width() * 0.8
        max_height = screen.height() * 0.8

        # 计算初始缩放比例
        self.scale_factor = min(
            max_width / pixmap.width(),
            max_height / pixmap.height(),
            1.0  # 初始不超过原始大小
        )

        # 设置初始窗口大小
        space_width = 10
        space_height = 100  # 标题栏和按钮区域高度
        initial_width = min(int(pixmap.width() * self.scale_factor) + space_width * 2 + 50, int(screen.width() * 0.9))
        initial_height = min(int(pixmap.height() * self.scale_factor) + space_height + 50, int(screen.height() * 0.9))
        self.resize(initial_width, initial_height)

        # 更新图片显示
        self.update_image_display()

        # 显示所有按钮
        self.save_button.show()
        self.zoom_in_button.show()
        self.zoom_out_button.show()
        self.reset_zoom_button.show()

        # 窗口居中
        self.center_on_screen()

        # 初始居中图片
        self.center_image()
        self.update()

    def save_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.jpg);;All Files (*)",
                                                   options=options)
        if file_path:
            pixmap = self.image_label.pixmap()
            if pixmap:
                pixmap.save(file_path)

    def closeEvent(self, event):
        if self.current_reply and self.current_reply.isRunning():
            self.current_reply.abort()
        super().closeEvent(event)


def show_image_dialog(main_object, title, image_url, link):
    screen = main_object.toolkit.resolution_util.get_screen(main_object)
    dialog = ImagePopup(None, use_parent=main_object, title=title, image_url=image_url, screen=screen, link=link)
    dialog.refresh_geometry(screen)
    dialog.show()
    return dialog