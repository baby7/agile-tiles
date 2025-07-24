from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PySide6.QtCore import QByteArray, QObject
from typing import Optional, Union


class ExtendedNetworkManager(QNetworkAccessManager):
    """
    扩展的网络访问管理器，支持完整的 HTTP 方法

    使用方法与原生 QNetworkAccessManager 完全一致，但增加了：
    - patch()
    - deleteResource() [更名自 delete()]
    - head()
    - options()

    注意：为避免与 Python 关键字冲突，删除方法命名为 deleteResource()
    """

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)

    def patch(self, request: QNetworkRequest, data: Optional[Union[QByteArray, bytes]] = None) -> QNetworkReply:
        """
        发送 PATCH 请求

        参数:
            request: QNetworkRequest - 包含 URL 和请求头的请求对象
            data: QByteArray | bytes | None - 要发送的数据

        返回:
            QNetworkReply - 网络响应对象
        """
        if data is None:
            data = QByteArray()
        elif isinstance(data, bytes):
            data = QByteArray(data)
        return self.sendCustomRequest(request, b"PATCH", data)

    def delete(self, request: QNetworkRequest,
                       data: Optional[Union[QByteArray, bytes]] = None) -> QNetworkReply:
        """
        发送 DELETE 请求

        参数:
            request: QNetworkRequest - 包含 URL 和请求头的请求对象
            data: QByteArray | bytes | None - 要发送的数据（可选）

        返回:
            QNetworkReply - 网络响应对象
        """
        if data is None:
            data = QByteArray()
        elif isinstance(data, bytes):
            data = QByteArray(data)
        return self.sendCustomRequest(request, b"DELETE", data)

    def head(self, request: QNetworkRequest) -> QNetworkReply:
        """
        发送 HEAD 请求

        参数:
            request: QNetworkRequest - 包含 URL 和请求头的请求对象

        返回:
            QNetworkReply - 网络响应对象
        """
        return self.sendCustomRequest(request, b"HEAD")

    def options(self, request: QNetworkRequest) -> QNetworkReply:
        """
        发送 OPTIONS 请求

        参数:
            request: QNetworkRequest - 包含 URL 和请求头的请求对象

        返回:
            QNetworkReply - 网络响应对象
        """
        return self.sendCustomRequest(request, b"OPTIONS")