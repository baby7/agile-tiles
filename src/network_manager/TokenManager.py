import json
from PySide6.QtCore import QObject, Signal, QUrl
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

from src.client import common


class TokenManager(QObject):
    tokenRefreshed = Signal(str)  # 新accessToken信号
    refreshFailed = Signal()  # 刷新失败信号
    use_parent = None
    access_token = None
    refresh_token = None

    def __init__(self, parent=None, use_parent=None):
        super().__init__(parent)
        self.network_manager = QNetworkAccessManager(self)
        self.use_parent = use_parent

    def get_access_token(self):
        return self.access_token

    def get_refresh_token(self):
        return self.refresh_token

    def save_tokens(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token

    def clear_tokens(self):
        self.access_token = None
        self.refresh_token = None

    def is_logged_in(self):
        return bool(self.get_access_token() and self.get_refresh_token())

    def refresh_access_token(self):
        """使用Refresh Token获取新的Access Token"""
        refresh_token = self.get_refresh_token()
        if not refresh_token:
            self.refreshFailed.emit()
            return

        url = f"{common.BASE_URL}/auth/normal/refresh"
        request = QNetworkRequest(QUrl(url))
        request.setRawHeader(b"Authorization", bytes(self.use_parent.access_token, "utf-8"))
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")

        data = json.dumps({"refreshToken": refresh_token}).encode()
        reply = self.network_manager.post(request, data)
        reply.finished.connect(lambda: self.handle_refresh_response(reply))

    def handle_refresh_response(self, reply):
        try:
            if reply.error() == QNetworkReply.NoError:
                data = json.loads(reply.readAll().data().decode())
                new_access_token = data.get("accessToken")

                if new_access_token:
                    # 保存新token
                    self.access_token = new_access_token
                    self.tokenRefreshed.emit(new_access_token)
                else:
                    self.refreshFailed.emit()
            else:
                # 401 未授权或其他错误
                if reply.attribute(QNetworkRequest.HttpStatusCodeAttribute) == 401:
                    self.clear_tokens()
                self.refreshFailed.emit()
        finally:
            reply.deleteLater()