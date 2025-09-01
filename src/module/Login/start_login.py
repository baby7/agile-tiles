# coding:utf-8
import json
import sys
import traceback

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt, QMetaObject, Q_ARG, Slot
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QLineEdit

from src.client import common
from src.module.Login import login_common
from src.module.Login.login_common import refresh_theme
from src.module.Login.start_login_form import Ui_Form
from src.module.User.user_client import UserClient
from src.module.UserData.Sync.data_client import DataClient
from src.util import browser_util, winreg_util
import src.ui.style_util as style_util
import src.module.Box.message_box_util as message_box_util
from src.component.AgileTilesFramelessDialog.AgileTilesFramelessDialog import AgileTilesFramelessDialog


class StartLoginWindow(AgileTilesFramelessDialog, Ui_Form):

    use_parent = None
    is_dark = False
    # 用户信息和数据
    username = None
    password = None
    user_data_status = None
    is_login = False
    is_vip = None
    user_data = None
    main_data = None
    access_token = None
    refresh_token = None

    def __init__(self, parent=None, use_parent=None):
        super(StartLoginWindow, self).__init__()
        self.setupUi(self)
        # 初始化
        self.use_parent = use_parent
        # 布局初始化
        self.widget_base.setLayout(self.gridLayout_8)
        self.gridLayout_8.setContentsMargins(10, 10, 10, 10)
        # 设置标题栏
        self.setWindowTitle("灵卡面板")
        self.titleBar.minBtn.close()
        self.titleBar.maxBtn.close()
        # 设置样式
        style_util.set_dialog_control_style(self, self.is_dark)
        # 初始化样式
        refresh_theme(self, self.is_dark)
        # 新增覆盖层初始化
        self.init_overlay()
        # 初始化点击事件
        self.init_click_connect()
        # 初始化输入校验
        self._connect_signals()
        # 密码显示/隐藏
        self._connect_password_signals()
        # 初始化用户请求
        self.init_user_client()
        # 其他样式初始化
        self.push_button_user_register_privacy_agreement.setStyleSheet("border: none; background-color: transparent;color: rgb(20, 161, 248);")
        self.push_button_user_register_service_agreement.setStyleSheet("border: none; background-color: transparent;color: rgb(20, 161, 248);")
        self.push_button_update_soft.setStyleSheet("border: none; background-color: transparent;color: rgb(20, 161, 248);")
        # 密码框样式
        self.set_password_edit_style(self.line_edit_user_login_password_widget, self.line_edit_user_login_password,
                                     self.push_button_user_login_password_view_control)
        self.set_password_edit_style(self.line_edit_user_register_password_widget, self.line_edit_user_register_password,
                                     self.push_button_user_register_password_view_control)
        self.set_password_edit_style(self.line_edit_user_register_password_check_widget, self.line_edit_user_register_password_check,
                                     self.push_button_user_register_password_check_view_control)
        self.set_password_edit_style(self.line_edit_user_forget_password_widget, self.line_edit_user_forget_password,
                                     self.push_button_user_forget_password_view_control)
        self.set_password_edit_style(self.line_edit_user_forget_password_check_widget, self.line_edit_user_forget_password_check,
                                     self.push_button_user_forget_password_check_view_control)
        # 鼠标手型
        self.push_button_user_register_privacy_agreement.setCursor(QCursor(Qt.PointingHandCursor))
        self.push_button_user_register_service_agreement.setCursor(QCursor(Qt.PointingHandCursor))
        self.push_button_update_soft.setCursor(QCursor(Qt.PointingHandCursor))
        self.push_button_user_login.setCursor(QCursor(Qt.PointingHandCursor))
        self.push_button_user_register.setCursor(QCursor(Qt.PointingHandCursor))
        self.push_button_user_forget.setCursor(QCursor(Qt.PointingHandCursor))
        self.push_button_user_login_forget_password.setCursor(QCursor(Qt.PointingHandCursor))
        self.push_button_register_validator_code.setCursor(QCursor(Qt.PointingHandCursor))
        self.push_button_forget_validator_code.setCursor(QCursor(Qt.PointingHandCursor))
        # 登录界面的忘记密码按钮
        self.push_button_user_login_forget_password.setStyleSheet("""
        QPushButton {
            border: none;
            border-radius: 11px;
            background-color:transparent;
            padding-left: 5px;
            padding-right: 5px;
        }
        QPushButton:hover {
            background-color: rgba(125, 125, 125, 80);
        }""")
        # 设置输入焦点
        self.line_edit_user_login_username.setFocus()
        # 添加登录界面回车跳转（焦点移到下一个输入框）
        self.line_edit_user_login_username.returnPressed.connect(
            lambda: self.line_edit_user_login_password.setFocus()
        )
        # 添加注册界面回车跳转（焦点移到下一个输入框）
        self.line_edit_user_register_nickname.returnPressed.connect(
            lambda: self.line_edit_user_register_username.setFocus()
        )
        self.line_edit_user_register_username.returnPressed.connect(
            lambda: self.line_edit_register_validator_code.setFocus()
        )
        self.line_edit_register_validator_code.returnPressed.connect(
            lambda: self.line_edit_user_register_password.setFocus()
        )
        self.line_edit_user_register_password.returnPressed.connect(
            lambda: self.line_edit_user_register_password_check.setFocus()
        )
        self.line_edit_user_register_password_check.returnPressed.connect(
            lambda: self.line_edit_user_register_invite_code.setFocus()
        )
        # 添加忘记密码界面回车跳转（焦点移到下一个输入框）
        self.line_edit_user_forget_username.returnPressed.connect(
            lambda: self.line_edit_forget_validator_code.setFocus()
        )
        self.line_edit_forget_validator_code.returnPressed.connect(
            lambda: self.line_edit_user_forget_password.setFocus()
        )
        self.line_edit_user_forget_password.returnPressed.connect(
            lambda: self.line_edit_user_forget_password_check.setFocus()
        )
        # 登录界面密码输入框绑定回车触发登录函数
        self.line_edit_user_login_password.returnPressed.connect(self.push_button_user_login_click)
        # 注册界面邀请码输入框绑定回车触发注册函数
        self.line_edit_user_register_invite_code.returnPressed.connect(self.push_button_user_register_click)
        # 注册忘记密码密码确认输入框绑定回车触发忘记密码函数
        self.line_edit_user_forget_password_check.returnPressed.connect(self.push_button_user_forget_click)

    def set_password_edit_style(self, line_edit_widget, line_edit, control):
        # 密码框底部
        password_edit_style = """
        QWidget {
            border-radius: 10px;
            border: 1px solid black;
            background-color: rgba(255, 255, 255, 150);
            padding-left: 5px;
        }
        """
        password_edit_dark_style = """
        QWidget {
            border-radius: 10px;
            border: 1px solid white;
            background-color: rgb(0, 0, 0);
            padding-left: 5px;
        }
        """
        if self.is_dark:
            line_edit_widget.setStyleSheet(password_edit_dark_style)
        else:
            line_edit_widget.setStyleSheet(password_edit_style)
        # 密码框
        line_edit.setStyleSheet("border: none; background-color: transparent;")
        # 按钮控制
        push_button_style = """
        QPushButton {
            border: none;
            border-radius: 11px;
            background-color:transparent;
            padding-right: 5px;
        }
        QPushButton:hover {
            background-color: rgba(125, 125, 125, 80);
        }"""
        control.setStyleSheet(push_button_style)
        control.setIcon(style_util.get_icon_by_path("Base/preview-close-one", is_dark=self.is_dark))

    def end_login_logic(self):
        current_user = self.use_parent.get_current_user()
        self.use_parent.set_current_user(current_user)
        # 退出登录界面
        self.close()

    # *************************************************** 初始化 ****************************************************
    def init_click_connect(self):
        """
        初始化点击事件
        :param self:
        :return:
        """
        self.push_button_user_login.clicked.connect(self.push_button_user_login_click)
        self.push_button_user_register.clicked.connect(self.push_button_user_register_click)
        self.push_button_user_forget.clicked.connect(self.push_button_user_forget_click)
        self.push_button_register_validator_code.clicked.connect(self.push_button_register_validator_code_click)
        self.push_button_user_register_privacy_agreement.clicked.connect(self.push_button_setting_privacy_agreement_click)
        self.push_button_user_register_service_agreement.clicked.connect(self.push_button_setting_service_agreement_click)
        self.push_button_user_login_forget_password.clicked.connect(self.push_button_user_login_forget_password_click)
        self.push_button_forget_validator_code.clicked.connect(self.push_button_forget_validator_code_click)
        self.push_button_update_soft.clicked.connect(self.push_button_update_soft_click)

    def init_user_client(self):
        """
        初始化用户请求
        :param self:
        :return:
        """
        # 初始化用户登录请求
        self.start_user_login_client = UserClient()
        self.start_user_login_client.loginFinished.connect(self.handle_start_login_result)
        self.start_user_login_client.registerFinished.connect(self.handle_start_register_result)
        self.start_user_login_client.forgetFinished.connect(self.handle_start_forget_password_result)
        self.start_user_login_client.sendCodeFinished.connect(self.handle_start_send_code_result)
        # 初始化用户数据请求
        self.start_user_data_client = DataClient()
        self.start_user_data_client.pushFinished.connect(self.handle_start_push_result)
        self.start_user_data_client.pullFinished.connect(self.handle_start_pull_result)


    # ************************************************** 登录模块 ***************************************************

    def push_button_user_login_click(self):
        """
        登录
        """
        try:
            # 先进行输入校验
            if not self.validate_login_phone():
                return
            if not self.validate_login_password():
                return
            # 获取输入信息
            self.username = self.line_edit_user_login_username.text()
            self.password = self.line_edit_user_login_password.text()
            # 发起登录请求
            print(f"发起登录请求,密码:{self.password}")
            self.start_user_login_client.login(self.username, self.password, self.use_parent.hardware_id, self.use_parent.os_version)
            # 设置开机自启动
            try:
                if self.check_box_user_area_auto_start.isChecked():
                    winreg_util.set_auto_start(True)
                else:
                    winreg_util.set_auto_start(False)
            except Exception as e:
                traceback.print_exc()
                print(f"设置开机自启动失败: {e}", file=sys.stderr)
                message_box_util.box_information(self.use_parent, "错误", "设置开机自启动失败")
            # 显示加载层
            self.show_overlay("登录中...")
        except Exception as e:
            message_box_util.box_information(self, "错误信息", "登录失败，您可以尝试更新版本，若还有问题请联系我们:service@agiletiles.com")
            self.hide_overlay()

    def handle_start_login_result(self, result):
        """
        处理登录结果
        """
        try:
            # 判断登录结果
            if result['code'] == 1:
                message_box_util.box_information(self, "错误信息", result['msg'])
                self.user_data = None
                self.user_data_status = "login_fail"
                # 隐藏加载层
                self.hide_overlay()
                return
            # 登录成功
            self.user_data_status = "login_success"
            self.is_login = True
            self.is_vip = result["data"]['vipStatus']
            self.user_data = result["data"]
            self.access_token = "Bearer " + result["data"]["accessToken"]
            self.refresh_token = result["data"]["refreshToken"]
            # 存储用户信息
            self.use_parent.save_user(self.username, self.refresh_token)
            # 登录成功后，保存用户数据直接给刷新后无法获取数据的逻辑中使用
            self.use_parent.login_restart_data = result
            # 非vip用户直接展示成功
            if not self.is_vip:
                # 隐藏加载层
                message_box_util.box_information(self, "提示信息", "登录成功", close_seconds=2)
                self.hide_overlay()
                self.end_login_logic()
            else:
                self.user_data_status = "load_server_data"
                current_user = self.use_parent.get_current_user()
                self.use_parent.set_current_user(current_user)
                # 对于vip用户，需要进行数据同步
                self.start_user_data_client.pull_data(self.username, self.access_token)
                # 显示加载层
                self.show_overlay("vip用户数据同步中...")
        except Exception as e:
            message_box_util.box_information(self, "错误信息", "登录失败，您可以尝试更新版本，若还有问题请联系我们:service@agiletiles.com")
            self.hide_overlay()


    # ************************************************** 注册模块 ***************************************************
    def push_button_user_register_click(self):
        """
        注册
        """
        try:
            # 先进行输入校验
            if not self.validate_register_phone():
                return
            if not self.validate_register_password():
                return
            if not self.validate_register_password_check():
                return
            if not self.validate_register_nickname():
                return
            if not self.validate_register_validator_code():
                return
            if not self.validate_register_invite_code():
                return
            # 判断用户是否同意服务协议
            if not self.check_box_user_area_agree_protocol.isChecked():
                confirm = message_box_util.box_acknowledgement(
                    self.use_parent, "确认信息", "您是否已阅读并同意《隐私政策》和《用户协议》？确定即表示用户与本客户端已达成协议，自愿接受本服务条款的所有内容！")
                if not confirm:
                    return
                self.check_box_user_area_agree_protocol.setChecked(True)
            # 获取输入信息
            self.username = self.line_edit_user_register_username.text()
            self.password = self.line_edit_user_register_password.text()
            nickname = self.line_edit_user_register_nickname.text()
            validator_code = self.line_edit_register_validator_code.text()
            invite_code = self.line_edit_user_register_invite_code.text()
            # 发起注册请求
            self.start_user_login_client.register(self.username, self.password, nickname, validator_code, invite_code)
            # 显示加载层
            self.show_overlay("注册中...")
        except Exception as e:
            traceback.print_exc()
            message_box_util.box_information(self, "错误信息", "注册失败，您可以尝试更新版本，若还有问题请联系我们:service@agiletiles.com")
            self.hide_overlay()

    def handle_start_register_result(self, result):
        """
        处理注册结果
        """
        try:
            # 隐藏加载层
            self.hide_overlay()
            # 判断注册结果
            if result['code'] != 0:
                message_box_util.box_information(self, "错误信息", result['msg'])
                return
            # 注册成功
            message_box_util.box_information(self, "提示", "注册成功，请登录")
            # 给登录页面的用户密码框设置结果方便用户登录
            self.line_edit_user_login_username.setText(self.username)
            self.line_edit_user_login_password.setText(self.password)
            # 切换到登录页面
            self.tab_widget_login.setCurrentIndex(0)
        except Exception as e:
            message_box_util.box_information(self, "错误信息", "注册失败，您可以尝试更新版本，若还有问题请联系我们:service@agiletiles.com")
            self.hide_overlay()

    def push_button_register_validator_code_click(self):
        """
        发送验证码（含60秒倒计时）
        """
        try:
            # 校验手机号
            if not self.validate_register_phone():
                message_box_util.box_information(self, "错误信息", "手机号格式错误")
                return
            # 获取手机号
            phone_number = self.line_edit_user_register_username.text()
            # 发送验证码
            self.start_user_login_client.send_validator_code(phone_number)
        except Exception as e:
            message_box_util.box_information(self, "错误", "验证码发送失败，您可以尝试更新版本，若还有问题请联系我们:service@agiletiles.com")
            self.hide_overlay()

    def push_button_forget_validator_code_click(self):
        """
        发送验证码（含60秒倒计时）
        """
        try:
            # 校验手机号
            if not self.validate_forget_phone():
                message_box_util.box_information(self, "错误信息", "手机号格式错误")
                return
            # 获取手机号
            phone_number = self.line_edit_user_forget_username.text()
            # 发送验证码
            self.start_user_login_client.send_validator_code(phone_number)
        except Exception as e:
            message_box_util.box_information(self, "错误", "验证码发送失败，您可以尝试更新版本，若还有问题请联系我们:service@agiletiles.com")
            self.hide_overlay()

    def handle_start_send_code_result(self, result):
        """
        处理发送验证码的结果
        """
        try:
            if result['code'] != 0:
                message_box_util.box_information(self, "错误", result['msg'])
                return

            # ========== 新增倒计时逻辑 ==========
            reg_btn = self.push_button_register_validator_code
            reg_btn.setEnabled(False)
            forget_btn = self.push_button_forget_validator_code
            forget_btn.setEnabled(False)
            style_util.set_button_style(reg_btn, is_dark=self.is_dark)
            style_util.set_button_style(forget_btn, is_dark=self.is_dark)

            # 初始化倒计时参数
            reg_btn.countdown = 60
            forget_btn.countdown = 60

            def reg_update_countdown():
                if reg_btn.countdown > 0:
                    reg_btn.setText(f"{reg_btn.countdown}秒后重试")
                    reg_btn.countdown -= 1
                else:
                    reg_btn.timer.stop()
                    reg_btn.setText("获取验证码")
                    reg_btn.setEnabled(True)
                    style_util.set_button_style(reg_btn, self.is_dark)

            def forget_update_countdown():
                if forget_btn.countdown > 0:
                    forget_btn.setText(f"{forget_btn.countdown}秒后重试")
                    forget_btn.countdown -= 1
                else:
                    forget_btn.timer.stop()
                    forget_btn.setText("获取验证码")
                    forget_btn.setEnabled(True)
                    style_util.set_button_style(forget_btn, self.is_dark)

            # 创建定时器
            reg_btn.timer = QtCore.QTimer(self)
            reg_btn.timer.timeout.connect(reg_update_countdown)
            reg_btn.timer.start(1000)  # 每秒触发
            forget_btn.timer = QtCore.QTimer(self)
            forget_btn.timer.timeout.connect(forget_update_countdown)
            forget_btn.timer.start(1000)  # 每秒触发
            # ========== 倒计时逻辑结束 ==========

            message_box_util.box_information(self, "提示", "验证码已发送")
        except Exception as e:
            message_box_util.box_information(self, "错误", "验证码发送失败，您可以尝试更新版本，若还有问题请联系我们:service@agiletiles.com")
            self.hide_overlay()

    def push_button_setting_service_agreement_click(self):
        # 隐私政策
        browser_util.open_url(common.user_agreement_url)

    def push_button_setting_privacy_agreement_click(self):
        # 用户协议
        browser_util.open_url(common.privacy_policy_url)


    # ************************************************** 忘记密码 ***************************************************

    def push_button_user_login_forget_password_click(self):
        try:
            self.tab_widget_login.setCurrentIndex(2)
            login_name = self.line_edit_user_login_username.text()
            if login_name != "":
                self.line_edit_user_forget_username.setText(self.line_edit_user_login_username.text())
        except Exception as e:
            message_box_util.box_information(self, "错误信息", "切换到忘记密码界面失败，您可以尝试更新版本，若还有问题请联系我们:service@agiletiles.com")
            self.hide_overlay()

    def push_button_user_forget_click(self):
        """
        忘记密码
        """
        try:
            # 先进行输入校验
            if not self.validate_forget_phone():
                return
            if not self.validate_forget_password():
                return
            if not self.validate_forget_password_check():
                return
            # 获取用户输入
            self.username = self.line_edit_user_forget_username.text()
            self.password = self.line_edit_user_forget_password.text()
            validator_code = self.line_edit_forget_validator_code.text()
            # 发起忘记密码请求
            print(f"发起忘记密码请求,密码:{self.password}")
            self.start_user_login_client.forget_password(self.username, self.password, validator_code, self.use_parent.hardware_id)
            # 显示加载层
            self.show_overlay("重置密码中...")
        except Exception as e:
            message_box_util.box_information(self, "错误信息", "密码修改失败，您可以尝试更新版本，若还有问题请联系我们:service@agiletiles.com")
            self.hide_overlay()

    def handle_start_forget_password_result(self, result):
        """
        处理忘记密码结果
        """
        try:
            # 隐藏加载层
            self.hide_overlay()
            # 判断重置密码结果
            if result['code'] != 0:
                message_box_util.box_information(self, "错误信息", result['msg'])
                return
            message_box_util.box_information(self, "提示", "密码修改成功，请登录")
            self.line_edit_user_login_username.setText(self.username)
            self.line_edit_user_login_password.setText(self.password)
            # 切换到登录页面
            self.tab_widget_login.setCurrentIndex(0)
        except Exception as e:
            message_box_util.box_information(self, "错误信息", "密码修改失败，您可以尝试更新版本，若还有问题请联系我们:service@agiletiles.com")
            self.hide_overlay()

    # ************************************************** 用户数据 ***************************************************

    def handle_start_pull_result(self, result):
        json_str = json.dumps(result)  # 转换为 JSON 字符串
        # 使用 QMetaObject 确保在主线程执行
        QMetaObject.invokeMethod(
            self,
            "_safe_init",
            Qt.ConnectionType.QueuedConnection,
            Q_ARG(str, json_str)
        )

    @Slot(str)
    def _safe_init(self, result_str):
        result = json.loads(result_str)  # 解析 JSON
        # 获取云端数据失败
        if result['code'] == 1:
            self.user_data_status = "pull_data_fail"
            print(f"获取云端数据失败，原因：{result['msg']}")
            self.end_login_logic()
            return

        # 云端数据为空,不做处理
        if result["data"] is None or result["data"]["data"] is None:
            print("云端数据为空，不做处理")
            self.user_data_status = "server_data_none"
            self.end_login_logic()
            return

        # 获取云端数据成功
        server_main_data = json.loads(result["data"]["data"])

        # 如果本地数据为空
        if self.main_data is None:
            self.main_data = server_main_data
            self.user_data_status = "data_sync_success"
            print("云端数据比本地数据新，将云端数据同步到本地数据")
            self.end_login_logic()
            return

        # 云端数据比本地数据新
        if server_main_data["timestamp"] > self.main_data["timestamp"]:
            self.main_data = server_main_data
            self.user_data_status = "data_sync_success"
            print("云端数据比本地数据新，将云端数据同步到本地数据")
            self.end_login_logic()
            return

        # 云端数据比本地数据旧
        if server_main_data["timestamp"] < self.main_data["timestamp"]:
            print("本地数据比云端数据新，将本地数据同步到云端")
            self.start_user_data_client.push_data(self.user_data["username"], self.access_token, self.main_data)
            self.end_login_logic()
            return

        # 云端数据与本地数据一致
        print("云端数据与本地数据一致，无需更新本地数据")
        self.end_login_logic()
        return

    def handle_start_push_result(self, result):
        print(f"处理用户数据推送结果: {result}")

    # ************************************************** 输入校验 ***************************************************

    def _connect_signals(self):
        # 实时输入校验(登录界面)
        self.line_edit_user_login_username.textChanged.connect(self.validate_login_phone)
        # self.line_edit_user_login_password.textChanged.connect(self.validate_login_password)
        # 实时输入校验(注册界面)
        self.line_edit_user_register_nickname.textChanged.connect(self.validate_register_nickname)
        self.line_edit_user_register_username.textChanged.connect(self.validate_register_phone)
        self.line_edit_register_validator_code.textChanged.connect(self.validate_register_validator_code)
        self.line_edit_user_register_password.textChanged.connect(self.validate_register_password)
        self.line_edit_user_register_password_check.textChanged.connect(self.validate_register_password_check)
        self.line_edit_user_register_invite_code.textChanged.connect(self.validate_register_invite_code)
        # 实时输入校验(忘记密码界面)
        self.line_edit_user_forget_username.textChanged.connect(self.validate_forget_phone)
        self.line_edit_forget_validator_code.textChanged.connect(self.validate_forget_validator_code)
        self.line_edit_user_forget_password.textChanged.connect(self.validate_forget_password)
        self.line_edit_user_forget_password_check.textChanged.connect(self.validate_forget_password_check)

    def validate_login_phone(self):
        return login_common.validate_phone(self.line_edit_user_login_username, self.label_user_login_username_prompt)

    def validate_login_password(self):
        return login_common.validate_password(self.line_edit_user_login_password, self.label_user_login_password_prompt)

    def validate_register_nickname(self):
        return login_common.validate_nickname(self.line_edit_user_register_nickname, self.label_user_register_nickname_prompt)

    def validate_register_phone(self):
        return login_common.validate_phone(self.line_edit_user_register_username, self.label_user_register_username_prompt)

    def validate_register_validator_code(self):
        return login_common.validate_validator_code(self.line_edit_register_validator_code, self.label_register_validator_code_prompt)

    def validate_register_invite_code(self):
        return login_common.validate_invite_code(self.line_edit_user_register_invite_code, self.label_user_register_invite_code_prompt)

    def validate_register_password(self):
        return login_common.validate_password(self.line_edit_user_register_password, self.label_user_register_password_prompt)

    def validate_register_password_check(self):
        return login_common.validate_password_check(self.line_edit_user_register_password,
                                                   self.line_edit_user_register_password_check,
                                                   self.label_user_register_password_check_prompt)

    def validate_forget_phone(self):
        return login_common.validate_phone(self.line_edit_user_forget_username, self.label_user_forget_username_prompt)

    def validate_forget_validator_code(self):
        return login_common.validate_validator_code(self.line_edit_forget_validator_code, self.label_forget_validator_code_prompt)

    def validate_forget_password(self):
        return login_common.validate_password(self.line_edit_user_forget_password, self.label_user_forget_password_prompt)

    def validate_forget_password_check(self):
        return login_common.validate_password_check(self.line_edit_user_forget_password,
                                                   self.line_edit_user_forget_password_check,
                                                   self.label_user_forget_password_check_prompt)

    # ************************************************** 密码隐藏/展示 ***************************************************

    def _connect_password_signals(self):
        # 实时输入校验(登录界面)
        self.push_button_user_login_password_view_control.clicked.connect(self.push_button_user_login_password_view_control_click)
        # 实时输入校验(注册界面)
        self.push_button_user_register_password_view_control.clicked.connect(self.push_button_user_register_password_view_control_click)
        self.push_button_user_register_password_check_view_control.clicked.connect(self.push_button_user_register_password_check_view_control_click)
        # 实时输入校验(忘记密码界面)
        self.push_button_user_forget_password_view_control.clicked.connect(self.push_button_user_forget_password_view_control_click)
        self.push_button_user_forget_password_check_view_control.clicked.connect(self.push_button_user_forget_password_check_view_control_click)

    def push_button_user_login_password_view_control_click(self):
        self.check_line_edit(self.line_edit_user_login_password, self.push_button_user_login_password_view_control)

    def push_button_user_register_password_view_control_click(self):
        self.check_line_edit(self.line_edit_user_register_password, self.push_button_user_register_password_view_control)

    def push_button_user_register_password_check_view_control_click(self):
        self.check_line_edit(self.line_edit_user_register_password_check, self.push_button_user_register_password_check_view_control)

    def push_button_user_forget_password_view_control_click(self):
        self.check_line_edit(self.line_edit_user_forget_password, self.push_button_user_forget_password_view_control)

    def push_button_user_forget_password_check_view_control_click(self):
        self.check_line_edit(self.line_edit_user_forget_password_check, self.push_button_user_forget_password_check_view_control)

    def check_line_edit(self, line_edit, push_button):
        if line_edit.echoMode() == QLineEdit.Password:
            line_edit.setEchoMode(QLineEdit.Normal)
            push_button.setIcon(get_icon_park_path("Base/preview-open", self.is_dark))
        else:
            line_edit.setEchoMode(QLineEdit.Password)
            push_button.setIcon(get_icon_park_path("Base/preview-close-one", self.is_dark))

    # ************************************************** 软件更新 ***************************************************
    def push_button_update_soft_click(self):
        print("点击检查更新")
        self.use_parent.check_update_run(tag="Login")

    # ************************************************** 信息展示 ***************************************************

    def init_overlay(self):
        """创建覆盖层并隐藏"""
        self.overlay = QtWidgets.QWidget(self)
        self.overlay.setObjectName("overlay")
        self.overlay.setGeometry(10, 32, self.width() - 20, self.height() - 42)
        self.overlay.setStyleSheet("""
        #overlay {
            background-color: rgba(0, 0, 0, 120);
            border-radius: 10px;
        }""")
        # 添加加载动画
        self.loading_label = QtWidgets.QLabel(self.overlay)
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.setGeometry(0, 0, self.width(), self.height())
        self.loading_label.setStyleSheet("font-size: 16px; color: white;")
        # 初始隐藏
        self.overlay.hide()
        self.overlay.raise_()  # 确保在最上层

    def show_overlay(self, message="处理中..."):
        """显示覆盖层"""
        self.loading_label.setGeometry(0, 0, self.width(), self.height())
        self.loading_label.setText(message)
        self.overlay.setGeometry(10, 32, self.width() - 20, self.height() - 42)
        self.overlay.show()
        QtCore.QCoreApplication.processEvents()  # 强制刷新UI

    def hide_overlay(self):
        """隐藏覆盖层"""
        self.overlay.hide()
