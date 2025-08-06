import json

from PySide6.QtCore import QUrl, Signal, QTimer, QUrlQuery, QObject
from PySide6.QtNetwork import QNetworkRequest
from PySide6.QtWebSockets import QWebSocket

from src.client.common import WS_BASE_URL


class PaymentWebSocketClient(QObject):
    connected = Signal()
    disconnected = Signal()
    message_received = Signal(dict)  # 接收解析后的JSON消息
    error_occurred = Signal(str)  # 错误消息信号

    def __init__(self, use_parent):
        super().__init__()
        self.use_parent = use_parent
        self.websocket = None
        self.current_order_no = None
        self.reconnect_timer = QTimer()
        self.reconnect_timer.setInterval(3000)  # 3秒重连间隔
        self.reconnect_timer.timeout.connect(self._reconnect)

    def connect_to_server(self, order_no):
        """建立到支付结果服务器的WebSocket连接"""
        self.current_order_no = order_no
        self._close_websocket()

        # 构建带订单号的URL
        url = QUrl(f"{WS_BASE_URL}/websocket/normal/payment")
        query = QUrlQuery()
        # query.addQueryItem("Authorization", self.use_parent.access_token)
        query.addQueryItem("outTradeNo", self.current_order_no)
        url.setQuery(query)

        # 创建WebSocket连接
        self.websocket = QWebSocket()
        self.websocket.connected.connect(self._on_connected)
        self.websocket.disconnected.connect(self._on_disconnected)
        self.websocket.textMessageReceived.connect(self._on_message_received)
        self.websocket.error.connect(self._on_error)

        # 创建带认证头的网络请求
        request = QNetworkRequest(url)
        request.setRawHeader(b"Authorization", self.use_parent.access_token.encode())

        # 连接服务器
        print("开始连接")
        self.websocket.open(request)

    def disconnect_from_server(self):
        """主动断开连接"""
        self._close_websocket()

    def _on_connected(self):
        """连接成功处理"""
        self.connected.emit()
        print("websocket连接成功，停止重连定时器")
        self.reconnect_timer.stop()

    def _on_disconnected(self):
        """连接断开处理"""
        self.disconnected.emit()
        print("websocket连接断开，启动重连定时器")
        self.reconnect_timer.start()  # 启动重连定时器

    def _on_error(self, error):
        """错误处理"""
        error_msg = f"WebSocket错误: {error} ({self.websocket.errorString()})"
        # error_msg = f"WebSocket错误: {error}"
        self.error_occurred.emit(error_msg)
        print(f"websocket连接错误，启动重连定时器，错误信息:{error_msg}")
        self.reconnect_timer.start()  # 启动重连定时器

    def _on_message_received(self, message):
        """消息接收处理"""
        try:
            print(f"接收到消息:{message}")
            data = json.loads(message)
            self.message_received.emit(data)
        except json.JSONDecodeError:
            self.error_occurred.emit("无效的JSON消息格式")

    def _reconnect(self):
        """重连机制"""
        if self.current_order_no:
            print(f"尝试重新连接订单: {self.current_order_no}")
            self.connect_to_server(self.current_order_no)

    def _close_websocket(self):
        """安全关闭WebSocket连接"""
        if self.websocket:
            print("断开连接")
            try:
                self.websocket.connected.disconnect()
                self.websocket.disconnected.disconnect()
                self.websocket.textMessageReceived.disconnect()
                self.websocket.error.disconnect()
                self.websocket.close()
                self.websocket.deleteLater()
            except RuntimeError:
                pass  # 忽略已删除对象的错误
            finally:
                self.websocket = None
                self.reconnect_timer.stop()
