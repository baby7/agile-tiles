# -*- coding: utf-8 -*-
import json
from PySide6.QtCore import QObject, Signal, QUrl
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
import src.client.common as common


class DataClient(QObject):
    pushFinished = Signal(dict)  # 异步推送完成信号
    pullFinished = Signal(dict)  # 异步拉取完成信号

    def __init__(self, parent=None):
        super().__init__(parent)
        self.network_manager = QNetworkAccessManager(self)
        self.network_manager.finished.connect(self._handle_reply)
        self.current_callback = None
        self.request_type = None

    def push_data(self, username, token, user_data):
        """异步推送数据到服务器"""
        url = common.BASE_URL + "/userData/normal/push"
        request = QNetworkRequest(QUrl(url))
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")
        request.setRawHeader(b"Authorization", token.encode())

        # 准备数据
        data = {
            'username': username,
            'timestamp': user_data["timestamp"],
            'data': json.dumps(user_data, ensure_ascii=False)
        }
        json_data = json.dumps(data).encode('utf-8')

        # 存储回调信息
        self.request_type = "push"
        self.current_callback = self.pushFinished

        # 发送异步请求
        self.network_manager.put(request, json_data)

    def pull_data(self, username, token):
        """异步从服务器拉取数据"""
        url = common.BASE_URL + "/userData/normal/pull?username=" + username
        request = QNetworkRequest(QUrl(url))
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")
        request.setRawHeader(b"Authorization", token.encode())

        # 存储回调信息
        self.request_type = "pull"
        self.current_callback = self.pullFinished

        # 发送异步请求
        self.network_manager.get(request)

    def _handle_reply(self, reply: QNetworkReply):
        """统一处理网络响应"""
        current_callback = self.current_callback
        try:
            if reply.error() == QNetworkReply.NoError:
                data = reply.readAll().data().decode('utf-8')
                result = json.loads(data)
                current_callback.emit(result)
            else:
                error_result = {"code": 1, "msg": reply.errorString()}
                current_callback.emit(error_result)
        except Exception as e:
            error_result = {"code": 1, "msg": f"处理响应时出错: {str(e)}"}
            if current_callback:  # 额外安全检查
                current_callback.emit(error_result)
        finally:
            reply.deleteLater()
            self.request_type = None
            self.current_callback = None
