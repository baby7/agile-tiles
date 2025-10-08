import json
import traceback

from src.util import my_shiboken_util
from PySide6.QtCore import QUrl, QByteArray
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

from src.client import common


class TicketSystem:
    """工单系统管理类"""
    reply = None

    def __init__(self, parent):
        self.parent = parent
        self.network_manager = QNetworkAccessManager(parent)
        self.tickets = []  # 存储工单列表

    def fetch_tickets(self, callback):
        """获取用户工单列表"""
        url = QUrl(f"{common.BASE_URL}/tickets/normal")
        request = QNetworkRequest(url)
        request.setRawHeader(b"Authorization", self.parent.access_token.encode())

        self.reply = self.network_manager.get(request)
        self.reply.finished.connect(lambda: self._handle_ticket_response(callback))

    def fetch_ticket_details(self, ticket_id, callback):
        """获取工单详情"""
        url = QUrl(f"{common.BASE_URL}/tickets/normal/{ticket_id}")
        request = QNetworkRequest(url)
        request.setRawHeader(b"Authorization", self.parent.access_token.encode())

        self.reply = self.network_manager.get(request)
        self.reply.finished.connect(lambda: self._handle_ticket_details_response(callback))

    def add_response(self, ticket_id, content, images, callback):
        """添加工单回复"""
        url = QUrl(f"{common.BASE_URL}/tickets/normal/{ticket_id}/responses")
        request = QNetworkRequest(url)
        request.setRawHeader(b"Content-Type", b"application/json")
        request.setRawHeader(b"Authorization", self.parent.access_token.encode())

        data = {
            "content": content,
            "images": images
        }
        json_data = QByteArray(json.dumps(data).encode('utf-8'))

        self.reply = self.network_manager.post(request, json_data)
        self.reply.finished.connect(lambda: self._handle_add_response(callback))

    def close_ticket(self, ticket_id, callback):
        """关闭工单"""
        url = QUrl(f"{common.BASE_URL}/tickets/normal/{ticket_id}/close")
        request = QNetworkRequest(url)
        request.setRawHeader(b"Authorization", self.parent.access_token.encode())

        self.reply = self.network_manager.post(request, QByteArray())
        self.reply.finished.connect(lambda: self._handle_close_ticket(callback))

    def _handle_ticket_response(self, callback):
        """处理工单列表响应"""
        if self.reply.error() == QNetworkReply.NoError:
            data = self.reply.readAll().data()
            if data is None or len(data) == 0:
                callback(False, "获取工单列表失败")
                return
            try:
                response = json.loads(data.decode('utf-8'))
                if "code" in response and response.get('code') == 0:
                    self.tickets = response.get('data', [])
                    callback(True, self.tickets)
                else:
                    callback(False, response.get('message', '获取工单列表失败'))
            except Exception as e:
                callback(False, f"解析工单列表失败")
                traceback.print_exc()
        else:
            callback(False, f"网络错误")
        # 在执行删除操作前，检查C++对象是否存活
        if self.reply is not None and my_shiboken_util.is_qobject_valid(self.reply):
            self.reply.deleteLater()
        self.reply = None

    def _handle_ticket_details_response(self, callback):
        """处理工单详情响应"""
        if self.reply.error() == QNetworkReply.NoError:
            data = self.reply.readAll().data()
            if data is None or len(data) == 0:
                callback(False, "获取工单详情失败")
                return
            try:
                response = json.loads(data.decode('utf-8'))
                print(f"response:{response}")
                if "code" in response and response.get('code') == 0:
                    callback(True, response['data'])
                else:
                    callback(False, response.get('message', '获取工单详情失败'))
            except Exception as e:
                callback(False, f"解析工单详情失败")
                traceback.print_exc()
        else:
            callback(False, f"网络错误")
        # 在执行删除操作前，检查C++对象是否存活
        if self.reply is not None and my_shiboken_util.is_qobject_valid(self.reply):
            self.reply.deleteLater()
        self.reply = None

    def _handle_add_response(self, callback):
        """处理添加回复响应"""
        if self.reply.error() == QNetworkReply.NoError:
            data = self.reply.readAll().data()
            if data is None or len(data) == 0:
                callback(False, "添加回复失败")
                return
            try:
                response = json.loads(data.decode('utf-8'))
                if "code" in response and response.get('code') == 0:
                    callback(True, "回复添加成功")
                else:
                    callback(False, response.get('message', '添加回复失败'))
            except Exception as e:
                callback(False, f"解析添加回复响应失败")
                traceback.print_exc()
        else:
            callback(False, f"网络错误")
        # 在执行删除操作前，检查C++对象是否存活
        if self.reply is not None and my_shiboken_util.is_qobject_valid(self.reply):
            self.reply.deleteLater()
        self.reply = None

    def _handle_close_ticket(self, callback):
        """处理关闭工单响应"""
        if self.reply.error() == QNetworkReply.NoError:
            data = self.reply.readAll().data()
            if data is None or len(data) == 0:
                callback(False, "关闭工单失败")
                return
            try:
                response = json.loads(data.decode('utf-8'))
                if "code" in response and response.get('code') == 0:
                    callback(True, "工单已关闭")
                else:
                    callback(False, response.get('message', '关闭工单失败'))
            except Exception as e:
                callback(False, f"解析关闭工单响应失败")
                traceback.print_exc()
                print(data)
        else:
            callback(False, f"网络错误")
        # 在执行删除操作前，检查C++对象是否存活
        if self.reply is not None and my_shiboken_util.is_qobject_valid(self.reply):
            self.reply.deleteLater()
        self.reply = None