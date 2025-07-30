import json
from PySide6.QtCore import QUrl, QByteArray
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

from src.client import common


class TicketSystem:
    """工单系统管理类"""

    def __init__(self, parent, access_token):
        self.parent = parent
        self.access_token = access_token
        self.network_manager = QNetworkAccessManager(parent)
        self.tickets = []  # 存储工单列表

    def fetch_tickets(self, callback):
        """获取用户工单列表"""
        url = QUrl(f"{common.BASE_URL}/tickets/normal")
        request = QNetworkRequest(url)
        request.setRawHeader(b"Authorization", self.access_token.encode())

        reply = self.network_manager.get(request)
        reply.finished.connect(lambda: self._handle_ticket_response(reply, callback))

    def fetch_ticket_details(self, ticket_id, callback):
        """获取工单详情"""
        url = QUrl(f"{common.BASE_URL}/tickets/normal/{ticket_id}")
        request = QNetworkRequest(url)
        request.setRawHeader(b"Authorization", self.access_token.encode())

        reply = self.network_manager.get(request)
        reply.finished.connect(lambda: self._handle_ticket_details_response(reply, callback))

    def add_response(self, ticket_id, content, images, callback):
        """添加工单回复"""
        url = QUrl(f"{common.BASE_URL}/tickets/normal/{ticket_id}/responses")
        request = QNetworkRequest(url)
        request.setRawHeader(b"Content-Type", b"application/json")
        request.setRawHeader(b"Authorization", self.access_token.encode())

        data = {
            "content": content,
            "images": images
        }
        json_data = QByteArray(json.dumps(data).encode('utf-8'))

        reply = self.network_manager.post(request, json_data)
        reply.finished.connect(lambda: self._handle_add_response(reply, callback))

    def close_ticket(self, ticket_id, callback):
        """关闭工单"""
        url = QUrl(f"{common.BASE_URL}/tickets/normal/{ticket_id}/close")
        request = QNetworkRequest(url)
        request.setRawHeader(b"Authorization", self.access_token.encode())

        reply = self.network_manager.post(request, QByteArray())
        reply.finished.connect(lambda: self._handle_close_ticket(reply, callback))

    def _handle_ticket_response(self, reply, callback):
        """处理工单列表响应"""
        if reply.error() == QNetworkReply.NoError:
            data = reply.readAll().data()
            try:
                response = json.loads(data.decode('utf-8'))
                if "code" in response and response.get('code') == 0:
                    self.tickets = response.get('data', [])
                    callback(True, self.tickets)
                else:
                    callback(False, response.get('message', '获取工单列表失败'))
            except Exception as e:
                callback(False, f"解析工单列表失败: {str(e)}")
        else:
            callback(False, f"网络错误: {reply.errorString()}")
        reply.deleteLater()

    def _handle_ticket_details_response(self, reply, callback):
        """处理工单详情响应"""
        if reply.error() == QNetworkReply.NoError:
            data = reply.readAll().data()
            try:
                response = json.loads(data.decode('utf-8'))
                print(f"response:{response}")
                if "code" in response and response.get('code') == 0:
                    callback(True, response['data'])
                else:
                    callback(False, response.get('message', '获取工单详情失败'))
            except Exception as e:
                callback(False, f"解析工单详情失败: {str(e)}")
        else:
            callback(False, f"网络错误: {reply.errorString()}")
        reply.deleteLater()

    def _handle_add_response(self, reply, callback):
        """处理添加回复响应"""
        if reply.error() == QNetworkReply.NoError:
            data = reply.readAll().data()
            try:
                response = json.loads(data.decode('utf-8'))
                if "code" in response and response.get('code') == 0:
                    callback(True, "回复添加成功")
                else:
                    callback(False, response.get('message', '添加回复失败'))
            except Exception as e:
                callback(False, f"解析添加回复响应失败: {str(e)}")
        else:
            callback(False, f"网络错误: {reply.errorString()}")
        reply.deleteLater()

    def _handle_close_ticket(self, reply, callback):
        """处理关闭工单响应"""
        if reply.error() == QNetworkReply.NoError:
            data = reply.readAll().data()
            try:
                response = json.loads(data.decode('utf-8'))
                if "code" in response and response.get('code') == 0:
                    callback(True, "工单已关闭")
                else:
                    callback(False, response.get('message', '关闭工单失败'))
            except Exception as e:
                callback(False, f"解析关闭工单响应失败: {str(e)}")
        else:
            callback(False, f"网络错误: {reply.errorString()}")
        reply.deleteLater()