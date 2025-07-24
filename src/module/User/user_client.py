# -*- coding: utf-8 -*-
import json
from PySide6.QtCore import QObject, Signal, QUrl
from PySide6.QtNetwork import QNetworkRequest, QNetworkReply
import src.client.common as common
from src.network_manager.ExtendedNetworkManager.ExtendedNetworkManager import ExtendedNetworkManager


class UserClient(QObject):
    loginFinished = Signal(dict)        # 登录完成信号
    registerFinished = Signal(dict)     # 注册完成信号
    forgetFinished = Signal(dict)       # 忘记密码完成信号
    sendCodeFinished = Signal(dict)     # 发送验证码完成信号
    infoFinished = Signal(dict)         # 用户信息获取完成信号

    def __init__(self, parent=None):
        super().__init__(parent)
        self.network_manager = ExtendedNetworkManager(self)
        self.network_manager.finished.connect(self._handle_reply)
        self.current_callback = None
        self.request_type = None
        self.finished_map = {
            "login": self.loginFinished,
            "register": self.registerFinished,
            "forget": self.forgetFinished,
            "send_code": self.sendCodeFinished,
            "get_user_info": self.infoFinished
        }

    def login(self, username, password):
        """用户登录"""
        url = common.BASE_URL + "/user/login"
        request = QNetworkRequest(QUrl(url))
        request.setRawHeader(b"Content-Type", b"application/json")
        # 准备数据
        data = {
            'username': username,
            'password': password
        }
        # 存储回调信息
        self.request_type = "login"
        self.current_callback = self.finished_map[self.request_type]
        # 发送异步请求
        self.network_manager.post(request, json.dumps(data).encode('utf-8'))

    def register(self, username, password, nickname, validator_code, invite_code):
        """用户注册"""
        url = common.BASE_URL + "/user/register?verifyCode=" + str(validator_code)
        if invite_code is not None and invite_code != "":
            url = url + "&inviteCode=" + str(invite_code)
        request = QNetworkRequest(QUrl(url))
        request.setRawHeader(b"Content-Type", b"application/json")
        # 准备数据
        data = {
            'username': username,
            'password': password,
            'nickName': nickname
        }
        # 存储回调信息
        self.request_type = "register"
        self.current_callback = self.finished_map[self.request_type]
        # 发送异步请求
        self.network_manager.post(request, json.dumps(data).encode('utf-8'))

    def forget_password(self, username, password, validator_code):
        """忘记密码"""
        url = common.BASE_URL + "/user/forgetPassword?verifyCode=" + str(validator_code)
        request = QNetworkRequest(QUrl(url))
        request.setRawHeader(b"Content-Type", b"application/json")
        # 准备数据
        data = {
            'username': username,
            'password': password
        }
        # 存储回调信息
        self.request_type = "forget"
        self.current_callback = self.finished_map[self.request_type]
        # 发送异步请求
        self.network_manager.patch(request, json.dumps(data).encode('utf-8'))

    def send_validator_code(self, phone):
        """发送验证码"""
        url = common.BASE_URL + "/user/verificationCode"
        request = QNetworkRequest(QUrl(url))
        request.setRawHeader(b"Content-Type", b"application/json")
        # 准备数据
        data = {
            'phone': phone
        }
        # 存储回调信息
        self.request_type = "send_code"
        self.current_callback = self.finished_map[self.request_type]
        # 发送异步请求
        self.network_manager.post(request, json.dumps(data).encode('utf-8'))

    def get_user_info(self, username, token):
        """获取用户信息"""
        url = common.BASE_URL + "/user/info?username=" + str(username)
        request = QNetworkRequest(QUrl(url))
        request.setRawHeader(b"Authorization", token.encode())
        # 存储回调信息
        self.request_type = "get_user_info"
        self.current_callback = self.finished_map[self.request_type]
        # 发送异步请求
        self.network_manager.get(request)

    def _handle_reply(self, reply: QNetworkReply):
        """统一处理网络响应"""
        current_callback = self.current_callback
        try:
            if reply.error() == QNetworkReply.NetworkError.NoError:
                data = reply.readAll().data().decode('utf-8')
                result = json.loads(data)
                current_callback.emit(result)
            else:
                error_message = reply.errorString()
                if reply.error() == QNetworkReply.NetworkError.OperationCanceledError:
                    error_message = "连接服务器异常，请稍后重试"
                elif reply.error() == QNetworkReply.NetworkError.TimeoutError:
                    error_message = "连接服务器超时，请稍后重试"
                elif reply.error() in [QNetworkReply.NetworkError.ConnectionRefusedError,
                                       QNetworkReply.NetworkError.UnknownServerError,
                                       QNetworkReply.NetworkError.UnknownNetworkError]:
                    error_message = "连接服务器异常，请稍后重试"
                error_result = {"code": 1, "msg": error_message}
                current_callback.emit(error_result)
        except Exception as e:
            error_result = {"code": 1, "msg": f"处理响应时出错: {str(e)}"}
            if current_callback:  # 额外安全检查
                current_callback.emit(error_result)
        finally:
            reply.deleteLater()
            self.request_type = None
            self.current_callback = None
