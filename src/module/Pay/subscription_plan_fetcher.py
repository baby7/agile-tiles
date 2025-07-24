import json

from PySide6.QtCore import QObject, Signal, QUrl
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

import src.client.common as common


class SubscriptionPlanFetcher(QObject):
    """订阅计划获取器 (使用 QNetworkAccessManager)"""
    fetched = Signal(object)
    error = Signal(str)

    def __init__(self, use_parent):
        super().__init__()
        self.use_parent = use_parent
        self.manager = QNetworkAccessManager(self)
        self.manager.finished.connect(self.handle_response)

    def fetch(self):
        """发起获取订阅计划的请求"""
        url = common.BASE_URL + "/subscriptionPlan"
        request = QNetworkRequest(QUrl(url))
        request.setRawHeader(b"Authorization", self.use_parent.token.encode())

        self.manager.get(request)

    def handle_response(self, reply: QNetworkReply):
        """处理网络响应"""
        try:
            if reply.error() == QNetworkReply.NoError:
                data = reply.readAll().data()
                json_data = json.loads(data)

                if json_data.get('code') == 0:
                    subscript_list = json_data.get('data', [])
                    result_list = [s for s in subscript_list if s.get('active')]
                    self.fetched.emit(result_list)
                else:
                    self.error.emit(f"获取订阅计划失败: {json_data.get('msg')}")
            else:
                self.error.emit(f"网络错误: {reply.errorString()}")
        except Exception as e:
            self.error.emit(f"处理响应出错: {str(e)}")
        finally:
            reply.deleteLater()