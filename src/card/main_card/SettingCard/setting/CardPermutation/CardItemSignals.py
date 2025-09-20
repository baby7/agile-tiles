# coding:utf-8
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsItem, QStyle, QGraphicsProxyWidget, QLabel
from PySide6.QtCore import Signal, QObject, Qt, QUrl
from PySide6.QtGui import QColor, QPen, QPainter, QPixmap
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from src.client import card_store_client


class CardItemSignals(QObject):
    """卡片项的自定义信号类"""
    moveRequested = Signal(int, int, int, int, int, int)  # 移动请求信号


class CardDesignItem(QGraphicsRectItem, QObject):
    """可移动的卡片图形项"""
    network_manager = None
    round_radius = 10
    card_data = None
    is_dark = None
    card_store_client = None

    def __init__(self, use_parent, card_data, col, row, cols, rows, grid_size, is_dark=False):
        # 显式调用父类构造函数
        QGraphicsRectItem.__init__(self)
        QObject.__init__(self)
        self.use_parent = use_parent

        # 初始化
        self.setZValue(1)
        self.card_data = card_data
        self.col = col
        self.row = row
        self.cols = cols
        self.rows = rows
        self.grid_size = grid_size
        self.is_dark = is_dark
        self.setRect(0, 0, cols * grid_size, rows * grid_size)
        self.setPos(col * grid_size, row * grid_size)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

        # 设置颜色和边框
        if self.is_dark:
            self.setBrush(QColor(34, 34, 34, 160))
            self.setPen(QPen(QColor(34, 34, 34, 170), 1))
        else:
            self.setBrush(QColor(255, 255, 255, 160))
            self.setPen(QPen(QColor(255, 255, 255, 170), 1))

        # 创建图片显示组件
        self.proxy = QGraphicsProxyWidget(self)
        self.label = QLabel()
        self.label.setScaledContents(True)

        # 设置样式
        style = "border-radius: 12px; border: 1px solid %s; background-color: transparent;"
        border_color = "rgba(38, 41, 52, 170)" if is_dark else "rgba(255, 255, 255, 170)"
        self.label.setStyleSheet(style % border_color)

        # 设置标签尺寸
        less_width = 2
        label_size = (cols * grid_size - 2 * less_width, rows * grid_size - 2 * less_width)
        self.label.setGeometry(less_width, less_width, *label_size)
        self.proxy.setWidget(self.label)

        # 初始化信号
        self.signals = CardItemSignals()

        # QtNetwork方案
        self.network_manager = QNetworkAccessManager()

        # 获取并加载网络图片
        self.card_store_client = card_store_client.CardStoreClient(self.use_parent)
        self.card_store_client.version_image_received.connect(self.load_image)
        card_size = f"{self.cols}_{self.rows}"
        self.card_store_client.fetch_store_version_image(self.card_data["name"], card_size)

    def load_image(self, response):
        """加载图片"""
        image_url = response["darkUrl" if self.is_dark else "lightUrl"]
        pixmap = self.use_parent.image_cache_manager.get_pixmap_by_url(image_url)
        if pixmap is not None:
            self.label.setPixmap(pixmap)
        else:
            self.load_network_image(response)

    def load_network_image(self, response):
        """异步加载网络图片"""
        image_url = response["darkUrl" if self.is_dark else "lightUrl"]
        request = QNetworkRequest(QUrl(image_url))
        reply = self.network_manager.get(request)
        reply.finished.connect(lambda: self.on_image_loaded(reply, image_url))  # 通过lambda传递reply

    def on_image_loaded(self, reply, image_url):
        """图片加载完成回调"""
        try:
            if reply.error() == QNetworkReply.NoError:
                data = reply.readAll()
                pixmap = QPixmap()
                if pixmap.loadFromData(data) and self is not None and hasattr(self, 'label'):
                    self.label.setPixmap(pixmap)
                    # 缓存图片
                    self.use_parent.image_cache_manager.save_pixmap_by_url(image_url, pixmap)
            else:
                print(f"图片加载失败: {reply.errorString()}")
        finally:
            reply.deleteLater()

    # 以下原有方法保持不变
    def get_card_data(self):
        return self.card_data

    def get_col(self):
        scene_pos = self.scenePos()
        return round(scene_pos.x() / self.grid_size)

    def get_row(self):
        scene_pos = self.scenePos()
        return round(scene_pos.y() / self.grid_size)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        new_col = self.get_col()
        new_row = self.get_row()
        self.signals.moveRequested.emit(self.col, self.row, new_col, new_row, self.cols, self.rows)

    def paint(self, painter, option, widget=None):
        painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        painter.setBrush(self.brush())
        painter.setPen(self.pen())
        rect = self.rect().adjusted(2, 2, -2, -2)
        painter.drawRoundedRect(rect, self.round_radius, self.round_radius)

        if option.state & QStyle.StateFlag.State_Selected:
            pen_color = QColor(Qt.GlobalColor.white) if self.is_dark else QColor(Qt.GlobalColor.black)
            painter.setPen(QPen(pen_color, 1, Qt.PenStyle.SolidLine))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRect(self.rect().adjusted(1, 1, -1, -1))