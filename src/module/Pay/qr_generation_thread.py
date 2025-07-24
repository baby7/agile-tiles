import json

from PySide6.QtCore import QObject, Signal, QUrl
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

import src.client.common as common


class QRGenerationManager(QObject):
    # 信号类型改为传递二维码数据字符串
    finished = Signal(object)  # 传递二维码数据
    error = Signal(str)

    def __init__(self, use_parent):
        super().__init__()
        self.use_parent = use_parent
        self.manager = QNetworkAccessManager(self)
        self.current_reply = None  # 当前活动的网络请求

    def fetch_qr_code(self, subscription_plan_code):
        """发起异步网络请求获取二维码数据"""
        # 取消任何正在进行的请求
        self.cancel()

        # 准备请求
        user_id = self.use_parent.current_user["id"]
        url = f'{common.BASE_URL}/api/prePayment/qrCode?subscriptionPlanType={subscription_plan_code}&userId=' + str(user_id)
        request = QNetworkRequest(QUrl(url))
        request.setRawHeader(b"Content-Type", b"application/json")
        request.setRawHeader(b"Authorization", self.use_parent.token.encode())

        # 发送请求
        self.current_reply = self.manager.post(request, b"")
        self.current_reply.finished.connect(self.handle_response)

    def handle_response(self):
        """处理网络响应"""
        reply = self.current_reply
        self.current_reply = None

        try:
            if reply.error() == QNetworkReply.NetworkError.NoError:
                data = reply.readAll().data()
                json_data = json.loads(data)
                qr_data = json_data.get('data', '')

                if qr_data:
                    self.finished.emit(qr_data)
                else:
                    self.error.emit("无效的二维码数据")
            else:
                self.error.emit(f"网络错误: {reply.errorString()}")
        except Exception as e:
            self.error.emit(f"解析响应出错: {str(e)}")
        finally:
            reply.deleteLater()

    def cancel(self):
        """取消当前请求"""
        if self.current_reply and self.current_reply.isRunning():
            self.current_reply.abort()
            if self.current_reply is not None:
                self.current_reply.deleteLater()
            self.current_reply = None
