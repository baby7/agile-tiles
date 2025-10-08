# -*- coding: utf-8 -*-
import json
from src.util import my_shiboken_util

from PySide6.QtCore import QObject, Signal, QUrl
from PySide6.QtNetwork import QNetworkRequest, QNetworkReply

import src.client.common as common
from src.constant import version_constant
from src.network_manager.ExtendedNetworkManager.ExtendedNetworkManager import ExtendedNetworkManager


class UserClient(QObject):
    loginFinished = Signal(dict)        # 登录完成信号
    registerFinished = Signal(dict)     # 注册完成信号
    logoutFinished = Signal(dict)       # 注销完成信号
    forgetFinished = Signal(dict)       # 忘记密码完成信号
    sendCodeFinished = Signal(dict)     # 发送验证码完成信号
    infoFinished = Signal(dict)         # 用户信息获取完成信号
    refreshFinished = Signal(dict)      # 刷新令牌完成信号

    login_reply = None        # 登录请求
    register_reply = None     # 注册请求
    logout_reply = None       # 注销请求
    forget_reply = None       # 忘记密码请求
    send_code_reply = None     # 发送验证码请求
    info_reply = None         # 用户信息获取请求
    refresh_reply = None      # 刷新令牌请求

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

    def login(self, username, password, hardware_id, os_version=None):
        """用户登录"""
        print(f"用户登录...{hardware_id}")
        url = common.BASE_URL + "/user/public/login"
        request = QNetworkRequest(QUrl(url))
        request.setRawHeader(b"Content-Type", b"application/json")
        # 准备数据
        data = {
            'username': username,
            'password': password,
            'deviceId': hardware_id,
            'version': str(version_constant.get_current_version())
        }
        if os_version is not None:
            data['osVersion'] = os_version
        # 发送异步请求
        self.login_reply = self.network_manager_login.post(request, json.dumps(data).encode('utf-8'))

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
        self.register_reply = self.network_manager_register.post(request, json.dumps(data).encode('utf-8'))

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
        self.logout_reply = self.network_manager_register.post(request, json.dumps(data).encode('utf-8'))

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
        self.forget_reply = self.network_manager_forget.patch(request, json.dumps(data).encode('utf-8'))

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
        self.send_code_reply = self.network_manager_send_code.post(request, json.dumps(data).encode('utf-8'))

    def get_user_info(self, username, token):
        """获取用户信息"""
        if username == "LocalUser":
            return  # 本地用户不进行登录和信息交互
        try:
            url = common.BASE_URL + "/user/normal/info?username=" + str(username)
            request = QNetworkRequest(QUrl(url))
            request.setRawHeader(b"Authorization", token.encode())
            # 发送异步请求
            self.info_reply = self.network_manager_info.get(request)
        except Exception as e:
            print(e)

    def refresh(self, username, refresh_token, hardware_id, os_version=None):
        """刷新令牌"""
        if username == "LocalUser":
            return  # 本地用户不进行登录和信息交互
        print(f"正在刷新令牌...{hardware_id}")
        url = common.BASE_URL + "/user/public/refresh"
        request = QNetworkRequest(QUrl(url))
        request.setRawHeader(b"Content-Type", b"application/json")
        # 准备数据
        data = {
            'username': username,
            'refreshToken': refresh_token,
            'deviceId': hardware_id,
            'version': str(version_constant.get_current_version())
        }
        if os_version is not None:
            data['osVersion'] = os_version
        # 发送异步请求
        self.refresh_reply = self.network_manager_refresh.post(request, json.dumps(data).encode('utf-8'))

    def _handle_reply_login(self):
        self._handle_reply(self.login_reply, self.loginFinished)
        if self.login_reply is not None and my_shiboken_util.is_qobject_valid(self.login_reply):
            self.login_reply.deleteLater()
        self.login_reply = None

    def _handle_reply_register(self):
        self._handle_reply(self.register_reply, self.registerFinished)
        if self.register_reply is not None and my_shiboken_util.is_qobject_valid(self.register_reply):
            self.register_reply.deleteLater()
        self.register_reply = None

    def _handle_reply_logout(self):
        self._handle_reply(self.logout_reply, self.logoutFinished)
        if self.logout_reply is not None and my_shiboken_util.is_qobject_valid(self.logout_reply):
            self.logout_reply.deleteLater()
        self.logout_reply = None

    def _handle_reply_forget(self):
        self._handle_reply(self.forget_reply, self.forgetFinished)
        if self.forget_reply is not None and my_shiboken_util.is_qobject_valid(self.forget_reply):
            self.forget_reply.deleteLater()
        self.forget_reply = None

    def _handle_reply_send_code(self):
        self._handle_reply(self.send_code_reply, self.sendCodeFinished)
        if self.send_code_reply is not None and my_shiboken_util.is_qobject_valid(self.send_code_reply):
            self.send_code_reply.deleteLater()
        self.send_code_reply = None

    def _handle_reply_info(self):
        self._handle_reply(self.info_reply, self.infoFinished)
        if self.info_reply is not None and my_shiboken_util.is_qobject_valid(self.info_reply):
            self.info_reply.deleteLater()
        self.info_reply = None

    def _handle_reply_refresh(self):
        self._handle_reply(self.refresh_reply, self.refreshFinished)
        if self.refresh_reply is not None and my_shiboken_util.is_qobject_valid(self.refresh_reply):
            self.refresh_reply.deleteLater()
        self.refresh_reply = None

    def _handle_reply(self, reply: QNetworkReply, finished):
        """统一处理网络响应"""
        try:
            if reply.error() == QNetworkReply.NetworkError.NoError:
                # 获取 HTTP 状态码
                status_code = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
                if status_code:
                    if status_code == 401:
                        error_result = {"code": 1, "msg": "未授权，请重新登录"}
                        finished.emit(error_result)
                        return
                    elif status_code == 403:
                        error_result = {"code": 1, "msg": "禁止访问，权限不足"}
                        finished.emit(error_result)
                        return
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
