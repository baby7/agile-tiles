# -*- coding: utf-8 -*-
import json
from PySide6.QtCore import QObject, Signal, QUrl
from PySide6.QtNetwork import QNetworkRequest, QNetworkReply
import src.client.common as common
from src.network_manager.ExtendedNetworkManager.ExtendedNetworkManager import ExtendedNetworkManager


class UserClient(QObject):
    loginFinished = Signal(dict)        # 登录完成信号
    registerFinished = Signal(dict)     # 注册完成信号
    logoutFinished = Signal(dict)       # 注销完成信号
    forgetFinished = Signal(dict)       # 忘记密码完成信号
    sendCodeFinished = Signal(dict)     # 发送验证码完成信号
    infoFinished = Signal(dict)         # 用户信息获取完成信号
    refreshFinished = Signal(dict)      # 刷新令牌完成信号

    def __init__(self, parent=None):
        super().__init__(parent)
        self.network_manager_login = ExtendedNetworkManager(self)
        self.network_manager_login.finished.connect(self._handle_reply_login)
        self.network_manager_register = ExtendedNetworkManager(self)
        self.network_manager_register.finished.connect(self._handle_reply_register)
        self.network_manager_logout = ExtendedNetworkManager(self)
        self.network_manager_logout.finished.connect(self._handle_reply_logout)
        self.network_manager_forget = ExtendedNetworkManager(self)
        self.network_manager_forget.finished.connect(self._handle_reply_forget)
        self.network_manager_send_code = ExtendedNetworkManager(self)
        self.network_manager_send_code.finished.connect(self._handle_reply_send_code)
        self.network_manager_info = ExtendedNetworkManager(self)
        self.network_manager_info.finished.connect(self._handle_reply_info)
        self.network_manager_refresh = ExtendedNetworkManager(self)
        self.network_manager_refresh.finished.connect(self._handle_reply_refresh)

    def login(self, username, password, hardware_id):
        """用户登录"""
        print(f"用户登录...{hardware_id}")
        url = common.BASE_URL + "/user/public/login"
        request = QNetworkRequest(QUrl(url))
        request.setRawHeader(b"Content-Type", b"application/json")
        # 准备数据
        data = {
            'username': username,
            'password': password,
            'deviceId': hardware_id
        }
        # 发送异步请求
        self.network_manager_login.post(request, json.dumps(data).encode('utf-8'))

    def register(self, username, password, nickname, validator_code, invite_code):
        """用户注册"""
        url = common.BASE_URL + "/user/public/register?verifyCode=" + str(validator_code)
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
        # 发送异步请求
        self.network_manager_register.post(request, json.dumps(data).encode('utf-8'))

    def logout(self, user_id, hardware_id):
        """用户注销"""
        url = common.BASE_URL + "/normal/logout"
        request = QNetworkRequest(QUrl(url))
        request.setRawHeader(b"Content-Type", b"application/json")
        # 准备数据
        data = {
            'id': user_id,
            'deviceId': hardware_id
        }
        # 发送异步请求
        self.network_manager_register.post(request, json.dumps(data).encode('utf-8'))

    def forget_password(self, username, password, validator_code, hardware_id):
        """忘记密码"""
        url = common.BASE_URL + "/user/public/forgetPassword?verifyCode=" + str(validator_code)
        request = QNetworkRequest(QUrl(url))
        request.setRawHeader(b"Content-Type", b"application/json")
        # 准备数据
        data = {
            'username': username,
            'password': password,
            'deviceId': hardware_id
        }
        # 发送异步请求
        self.network_manager_forget.patch(request, json.dumps(data).encode('utf-8'))

    def send_validator_code(self, phone):
        """发送验证码"""
        url = common.BASE_URL + "/user/public/verificationCode"
        request = QNetworkRequest(QUrl(url))
        request.setRawHeader(b"Content-Type", b"application/json")
        # 准备数据
        data = {
            'phone': phone
        }
        # 发送异步请求
        self.network_manager_send_code.post(request, json.dumps(data).encode('utf-8'))

    def get_user_info(self, username, token):
        """获取用户信息"""
        url = common.BASE_URL + "/user/normal/info?username=" + str(username)
        request = QNetworkRequest(QUrl(url))
        request.setRawHeader(b"Authorization", token.encode())
        # 发送异步请求
        self.network_manager_info.get(request)

    def refresh(self, username, refresh_token, hardware_id):
        """刷新令牌"""
        print(f"正在刷新令牌...{hardware_id}")
        url = common.BASE_URL + "/user/public/refresh"
        request = QNetworkRequest(QUrl(url))
        request.setRawHeader(b"Content-Type", b"application/json")
        # 准备数据
        data = {
            'username': username,
            'refreshToken': refresh_token,
            'deviceId': hardware_id
        }
        # 发送异步请求
        self.network_manager_refresh.post(request, json.dumps(data).encode('utf-8'))

    def _handle_reply_login(self, reply: QNetworkReply):
        self._handle_reply(reply, self.loginFinished)

    def _handle_reply_register(self, reply: QNetworkReply):
        self._handle_reply(reply, self.registerFinished)

    def _handle_reply_logout(self, reply: QNetworkReply):
        self._handle_reply(reply, self.logoutFinished)

    def _handle_reply_forget(self, reply: QNetworkReply):
        self._handle_reply(reply, self.forgetFinished)

    def _handle_reply_send_code(self, reply: QNetworkReply):
        self._handle_reply(reply, self.sendCodeFinished)

    def _handle_reply_info(self, reply: QNetworkReply):
        self._handle_reply(reply, self.infoFinished)

    def _handle_reply_refresh(self, reply: QNetworkReply):
        self._handle_reply(reply, self.refreshFinished)

    def _handle_reply(self, reply: QNetworkReply, finished):
        """统一处理网络响应"""
        try:
            if reply.error() == QNetworkReply.NetworkError.NoError:
                data = reply.readAll().data().decode('utf-8')
                result = json.loads(data)
                finished.emit(result)
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
                finished.emit(error_result)
        except Exception as e:
            error_result = {"code": 1, "msg": f"处理响应时出错: {str(e)}"}
            if finished:  # 额外安全检查
                finished.emit(error_result)
        finally:
            reply.deleteLater()
