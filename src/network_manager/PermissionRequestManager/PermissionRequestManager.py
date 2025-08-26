import json

from PySide6.QtCore import Signal, Slot, QObject, QUrl
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest

from src.client import common


class PermissionRequestManager(QObject):

    finished = Signal(str)
    errored = Signal(str)

    def __init__(self, parent=None, use_parent=None):
        super().__init__(parent)
        self.use_parent = use_parent
        # 权限请求管理器
        self.permission_manager = QNetworkAccessManager(self)

    def get_request(self, url):
        """使用QNetworkRequest获取"""
        # 创建请求
        url = QUrl(f"{common.BASE_URL}" + url)
        print(url)
        request = QNetworkRequest(url)
        request.setRawHeader(b"Authorization", self.use_parent.access_token.encode())
        # 发送GET请求
        self.current_request = self.permission_manager.get(request)
        # 连接完成信号
        self.current_request.finished.connect(lambda : self.handle_finished(self.current_request))
        self.current_request.errorOccurred.connect(lambda : self.handle_error(self.current_request))

    def post_request(self, url, post_data):
        """使用QNetworkRequest获取"""
        # 创建请求
        url = QUrl(f"{common.BASE_URL}" + url)
        print(url)
        request = QNetworkRequest(url)
        request.setRawHeader(b"Authorization", self.use_parent.access_token.encode())
        # 发送POST请求
        self.current_request = self.permission_manager.post(request, post_data)
        # 连接完成信号
        self.current_request.finished.connect(lambda : self.handle_finished(self.current_request))
        self.current_request.errorOccurred.connect(lambda : self.handle_error(self.current_request))

    @Slot(QNetworkReply)
    def handle_finished(self, reply):
        """处理上传完成"""
        try:
            # 检查是否有错误
            if reply.error() != QNetworkReply.NoError:
                return
            # 解析响应
            response_data = reply.readAll().data()
            result = json.loads(response_data.decode('utf-8'))
            print(result)
            if str(result.get('code')) == "0":
                self.finished.emit(json.dumps(result["data"]))
            else:
                self.errored.emit("请求失败")
        except Exception as e:
            print(e)
        self.current_get = None

    def handle_error(self, current_get):
        print("请求失败")
        self.errored.emit("请求失败")
