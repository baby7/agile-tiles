from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QAction, QGuiApplication
from PySide6.QtWidgets import QLabel, QMenu, QFileDialog

from src.my_component.BaseAcrylicWindow.BaseAcrylicWindow import BaseAcrylicWindow


class TopImageAcrylicWindow(BaseAcrylicWindow):
    """ A frameless window with acrylic effect """

    screenshot_pixmap = None
    display_pixmap = None

    def __init__(self, parent=None, screenshot_pixmap=None):
        super().__init__(parent=parent)
        try:
            # 窗口设置
            self.titleBar.hide()
            # 数值设置
            self.original_pixmap = screenshot_pixmap
            self.display_pixmap = self.original_pixmap.copy()
            self.rotation_angle = 0
            self.show_shadow = True
            self.dragging = False
            self.drag_position = QPoint()
            self.scale_factor = 1.0
            self.resize_edge = None  # 用于跟踪当前调整大小的边缘
            self.resize_start_pos = None
            self.resize_start_geometry = None
            self.default_shadow_width = 10
            # 边缘检测阈值
            self.edge_margin = 8
            # 布局设置
            self.init_base_ui()
            # 置顶
            self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        except Exception as e:
            print(e)

    def init_base_ui(self):
        # 背景
        self.label_background = QLabel(self)
        self.label_background.setPixmap(self.display_pixmap)
        self.label_background.setScaledContents(True)
        # 根据截图大小设置窗口大小
        self.update_window_size()
        # 设置右键菜单
        self.label_background.setContextMenuPolicy(Qt.CustomContextMenu)
        self.label_background.customContextMenuRequested.connect(self.show_context_menu)

    def resizeEvent(self, event):
        """ 重写窗口大小改变事件 """
        super().resizeEvent(event)
        # 同步更新背景标签尺寸
        if self.label_background:
            self.label_background.resize(self.width(), self.height())

    def show_context_menu(self, position):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #f5f5f5;
                color: #333333;
                border: 1px solid #d0d0d0;
                border-radius: 5px;
                padding: 5px;
            }
            QMenu::item:selected {
                background-color: #e0e0e0;
            }
        """)

        close_action = QAction("关闭", self)
        close_action.triggered.connect(self.close)

        copy_action = QAction("复制", self)
        copy_action.triggered.connect(self.copy_to_clipboard)

        save_as_action = QAction("另存为", self)
        save_as_action.triggered.connect(self.save_as)

        menu.addAction(close_action)
        menu.addAction(copy_action)
        menu.addAction(save_as_action)

        menu.exec_(self.mapToGlobal(position))

    def copy_to_clipboard(self):
        clipboard = QGuiApplication.clipboard()
        clipboard.setPixmap(self.display_pixmap)

    def save_as(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存截图",
            "屏幕截图.png",
            "PNG 图片 (*.png);;JPEG 图片 (*.jpg *.jpeg)"
        )
        if file_path:
            self.display_pixmap.save(file_path)

    def wheelEvent(self, event):
        # 滚轮事件用于缩放
        delta = event.angleDelta().y()
        if delta > 0:
            # 放大
            self.scale_factor *= 1.1
        else:
            # 缩小
            self.scale_factor /= 1.1
        # 限制缩放范围
        self.scale_factor = max(0.2, min(5.0, self.scale_factor))
        # 更新显示图片
        self.display_pixmap = self.original_pixmap.scaled(
            int(self.original_pixmap.width() * self.scale_factor),
            int(self.original_pixmap.height() * self.scale_factor),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.update_window_size()
        self.update()

    def update_window_size(self):
        pixmap_size = self.display_pixmap.size()
        window_width = int(pixmap_size.width() / self.original_pixmap.devicePixelRatio())
        window_height = int(pixmap_size.height() / self.original_pixmap.devicePixelRatio())
        self.setFixedSize(window_width, window_height)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # 开始拖拽
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        # 处理拖拽
        if event.buttons() == Qt.LeftButton and self.dragging:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            self.resize_edge = None
            self.resize_start_pos = None
            self.resize_start_geometry = None
            event.accept()


def show_top_image_dialog(main_object, pixmap=None):
    print("show_top_image_dialog")
    dialog = TopImageAcrylicWindow(parent=None, screenshot_pixmap=pixmap)
    dialog.show()
    return dialog