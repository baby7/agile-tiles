from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPixmap, QPainter, QBrush, QColor
from PySide6.QtCore import Qt, QRect, Signal, QUrl


class ImagePreviewWidget(QWidget):
    """自定义图片预览小部件"""
    deleteClicked = Signal()  # 添加信号声明

    def __init__(self, image_path, show_delete_button=True, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.show_delete_button = show_delete_button
        self.network_manager = QNetworkAccessManager(self)  # 添加网络管理器
        self.network_manager.finished.connect(self.on_image_loaded)
        self.pixmap = None  # 图片缓存
        self.setFixedSize(100, 100)
        self.setStyleSheet("""
            background-color: #F5F7FA;
            border: 1px dashed #C0C4CC;
            border-radius: 6px;
        """)
        self.delete_btn_rect = QRect(0, 0, 0, 0)  # 初始化删除按钮区域
        self.load_image()  # 新增图片加载方法

    def load_image(self):
        if self.image_path.startswith(("http://", "https://")):
            # 网络图片
            request = QNetworkRequest(QUrl(self.image_path))
            self.network_manager.get(request)
        else:
            # 本地图片
            self.pixmap = QPixmap(self.image_path)
            self.update()  # 触发重绘

    def on_image_loaded(self, reply):
        if reply.error() == QNetworkReply.NoError:
            data = reply.readAll()
            self.pixmap = QPixmap()
            self.pixmap.loadFromData(data)
            self.update()  # 更新显示
        reply.deleteLater()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制背景
        bg_rect = QRect(0, 0, self.width(), self.height())
        painter.setBrush(QBrush(QColor("#F5F7FA")))
        painter.drawRoundedRect(bg_rect, 6, 6)

        # 绘制图片
        if self.pixmap and not self.pixmap.isNull():
            pixmap = self.pixmap.scaled(90, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            x = (self.width() - pixmap.width()) // 2
            y = (self.height() - pixmap.height()) // 2
            painter.drawPixmap(x, y, pixmap)

        # 绘制删除按钮 (保存按钮区域)
        if self.show_delete_button:
            self.delete_btn_rect = QRect(self.width() - 22, 2, 20, 20)
            painter.setBrush(QBrush(QColor("#F56C6C")))
            painter.drawEllipse(self.delete_btn_rect)
            painter.setPen(QColor(Qt.white))
            painter.drawText(self.delete_btn_rect, Qt.AlignCenter, "×")

    def mousePressEvent(self, event):
        """处理鼠标点击事件"""
        if self.show_delete_button and self.delete_btn_rect.contains(event.pos()):
            self.deleteClicked.emit()  # 点击删除按钮时发出信号
        else:
            super().mousePressEvent(event)  # 其他区域保持默认行为
