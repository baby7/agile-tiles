import copy
import os
import subprocess
import sys

from PySide6.QtGui import QCursor

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QLabel, QVBoxLayout, QApplication

from src.client import common
from src.constant import version_constant, data_save_constant, open_source_constant
from src.module import dialog_module
from src.module.Feedback import feedback_box_util
from src.module.Ticket import ticket_box_util
from src.module.Updater.Updater import Updater
from src.module.UserData.DataBase import user_data_common
from src.module.Box import text_box_util, message_box_util
from src.card.MainCardManager.MainCard import MainCard
from src.util import browser_util
from src.ui import style_util


def get_pixmap_park_path(icon_position, is_dark, is_yellow=False):
    if is_yellow:
        return style_util.get_pixmap_by_path(icon_position, custom_color="#FFC900")
    else:
        return style_util.get_pixmap_by_path(icon_position, is_dark=is_dark)

def add_red_dot_in_button(button):
    # 创建红点Label（确保按钮有父对象）
    red_dot = QLabel(button.parentWidget())
    red_dot.setStyleSheet("""
        background-color: red;
        border-radius: 3px;
        min-width: 6px;
        min-height: 6px;
        max-width: 6px;
        max-height: 6px;
    """)
    red_dot.raise_()  # 确保在最上层
    return red_dot  # 保留引用

def add_vip_sign_in_button(button, is_dark):
    # 创建VIP的Label标识（确保按钮有父对象）
    vip_sign = QLabel(button.parentWidget())
    vip_sign.setStyleSheet("""
            background: transparent;
            border: none;
    """)
    vip_sign.setPixmap(get_pixmap_park_path("Others/vip-one", is_dark, is_yellow=True))
    vip_sign.setFixedSize(15, 15)
    vip_sign.setScaledContents(True)
    vip_sign.raise_()  # 确保在最上层
    return vip_sign  # 保留引用


class SettingCard(MainCard):

    title = "设置"
    name = "SettingCard"
    support_size_list = ["Big"]
    # 只读参数
    x = None                # 坐标x
    y = None                # 坐标y
    size = None             # 大小(1_1:Point、1_2:MiniHor、2_1MiniVer、2_2Block、2_5)
    theme = None            # 主题(Light、Dark)
    width = 0               # 宽度
    height = 0              # 高度
    fillet_corner = 0       # 圆角大小
    # 可使用
    card = None             # 卡片本体
    data = None             # 数据
    toolkit = None          # 工具箱，具体参考文档
    logger = None           # 日志记录工具
    # 可调用
    save_data_func = None   # 保存数据(传参为一个字典)
    #
    is_first = True
    need_refresh_ui = False
    setting_card_button_list = []


    def __init__(self, main_object=None, parent=None, theme=None, card=None, cache=None, data=None,
                 toolkit=None, logger=None, save_data_func=None):
        super().__init__(main_object=main_object, parent=parent, theme=theme, card=card, cache=cache, data=data,
                         toolkit=toolkit, logger=logger, save_data_func=save_data_func)
        self.setting_data = self.data.setdefault(self.hardware_id, user_data_common.setting_config)
        self.setting_card_button_list = [
            # 设置
            [self.parent.push_button_setting_system, "系统设置", "Base", "setting-two", None, None],
            [self.parent.push_button_setting_card_permutation, "卡片设计", "Build", "application", None, None],
            [self.parent.push_button_setting_screen, "界面设置", "Components", "page", None, None],
            [self.parent.push_button_setting_theme, "主题设置", "Clothes", "theme", None, None],
            # [self.parent.push_button_setting_file, "文件管理", "Office", "folder-open", None, None],
            # 问题和更新
            [self.parent.push_button_setting_version_info, "版本信息", "Communicate", "message", None, None],
            [self.parent.push_button_setting_version, "检查更新", "Base", "refresh", None, None],
            [self.parent.push_button_setting_ticket, "会员工单", "Money", "transaction", None, None],
            [self.parent.push_button_setting_feedback_opinion, "意见反馈", "Hands", "concept-sharing", None, None],
            # 关于
            [self.parent.push_button_setting_faq, "常见问题", "Character", "help", None, None],
            [self.parent.push_button_setting_service_agreement, "用户协议", "Office", "agreement", None, None],
            [self.parent.push_button_setting_privacy_agreement, "隐私协议", "Peoples", "personal-privacy", None, None],
            [self.parent.push_button_setting_about_us, "关于我们", "Character", "info", None, None],
            # 开源
            [self.parent.push_button_setting_open_source_link, "开源地址", "Brand", "github-one", None, None],
            [self.parent.push_button_setting_open_source_list, "开源许可", "Others", "certificate", None, None],
        ]

    def init_ui(self):
        super().init_ui()
        for setting_card_button in self.setting_card_button_list:
            button = setting_card_button[0]
            title = setting_card_button[1]
            button.setText("")
            button.setCursor(QCursor(Qt.PointingHandCursor))     # 鼠标手形
            # 创建一个垂直布局，将图标和文字放入其中
            button_layout = QVBoxLayout(button)
            button_layout.setContentsMargins(0, 0, 0, 0)  # 设置布局的外边距为9
            button_layout.setSpacing(0)  # 设置布局的控件间距为0
            icon_label = QLabel()  # 创建一个标签用于显示图标
            icon_label.setScaledContents(True)
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 设置图标居中对齐
            icon_label.setFixedSize(50, 40)
            icon_label.setStyleSheet("""margin-left: 20px;margin-top: 10px;border: 0px solid black;background: transparent;""")
            text_label = QLabel(title)  # 创建一个标签用于显示文字
            text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 设置文字居中对齐
            # 设置标签可点击
            icon_label.setAttribute(Qt.WA_TransparentForMouseEvents, True)
            text_label.setAttribute(Qt.WA_TransparentForMouseEvents, True)
            button_layout.addWidget(icon_label)  # 将图标标签添加到按钮的垂直布局中
            button_layout.addWidget(text_label)
            setting_card_button[4] = icon_label
            setting_card_button[5] = text_label
        # 设置
        self.parent.push_button_setting_card_permutation.clicked.connect(self.push_button_setting_card_permutation_click)
        self.parent.push_button_setting_theme.clicked.connect(self.push_button_setting_theme_click)
        self.parent.push_button_setting_system.clicked.connect(self.push_button_setting_system_click)
        self.parent.push_button_setting_screen.clicked.connect(self.push_button_setting_screen_click)
        # 问题和更新
        self.parent.push_button_setting_version_info.clicked.connect(self.push_button_setting_version_info_click)
        self.parent.push_button_setting_version.clicked.connect(self.push_button_setting_version_click)
        self.parent.push_button_setting_ticket.clicked.connect(self.push_button_setting_ticket_click)
        self.parent.push_button_setting_feedback_opinion.clicked.connect(self.push_button_setting_feedback_opinion_click)
        # 关于
        self.parent.push_button_setting_faq.clicked.connect(self.push_button_setting_faq_click)
        self.parent.push_button_setting_service_agreement.clicked.connect(self.push_button_setting_service_agreement_click)
        self.parent.push_button_setting_privacy_agreement.clicked.connect(self.push_button_setting_privacy_agreement_click)
        self.parent.push_button_setting_about_us.clicked.connect(self.push_button_setting_about_us_click)
        # 开源
        self.parent.push_button_setting_open_source_link.clicked.connect(self.push_button_setting_open_source_link_click)
        self.parent.push_button_setting_open_source_list.clicked.connect(self.push_button_setting_open_source_list_click)
        # 设置快捷键
        self.main_object.keyboard_re_init()

    def refresh_data(self, date_time_str):
        super().refresh_data(date_time_str)

    def refresh_ui(self, date_time_str):
        super().refresh_ui(date_time_str)
        super().refresh_ui_end(date_time_str)

    def update_data(self, data=None):
        """
        更新持久数据事件
        """
        if self.data == data:
            return
        # 重新初始化配置
        self.data = data
        # 理论上更新时，更新的是其他主机的设置数据，不需要更改此主机的设置数据，不过更新了也无妨，不会影响什么
        self.setting_data = self.data.setdefault(self.hardware_id, {})

    # 设置卡片排列
    def push_button_setting_card_permutation_click(self):
        # 未登录的判断
        self.main_object.show_login_tip(tip_text="海量卡片和卡片设计功能需要登录使用，要现在登录吗？")
        if self.main_object.current_user['username'] == "LocalUser":
            return
        self.toolkit.resolution_util.out_animation(self.main_object)
        QTimer.singleShot(100, self.show_card_permutation_win)

    def show_card_permutation_win(self):
        from src.card.main_card.SettingCard.setting.card_permutation import CardPermutationWindow
        user_card_list = copy.deepcopy(self.main_object.main_data["card"])
        main_config = copy.deepcopy(self.main_object.main_data)
        self.card_permutation_win = CardPermutationWindow(self, self.main_object, user_card_list, main_config)
        self.card_permutation_win.show()

    def save_card_data(self, card, data):
        self.setting_data["width"] = data["width"]
        self.setting_data["height"] = data["height"]
        in_data = {
            "card": card,
            "SettingCard": self.data,
            "width": data["width"],
            "height": data["height"],
        }
        self.save_data_func(trigger_type=data_save_constant.TRIGGER_TYPE_SETTING_PERMUTATION, in_data=in_data)

    def refresh_card_version(self):
        self.main_object.refresh_card_version()

    # 打开设置快捷键窗口
    def push_button_setting_system_click(self):
        from src.card.main_card.SettingCard.setting.setting_system import SettingSystemWindow
        self.toolkit.resolution_util.out_animation(self.main_object)
        self.setting_system_win = SettingSystemWindow(self, self.main_object, self.setting_data)
        self.setting_system_win.refresh_geometry(self.toolkit.resolution_util.get_screen(self.main_object))
        # self.setting_system_win.set_top()
        self.setting_system_win.show()

    # 打开设置界面窗口
    def push_button_setting_screen_click(self):
        from src.card.main_card.SettingCard.setting.setting_screen import SettingScreenWindow
        self.toolkit.resolution_util.out_animation(self.main_object)
        self.setting_screen_win = SettingScreenWindow(self, self.main_object, self.setting_data)
        self.setting_screen_win.refresh_geometry(self.toolkit.resolution_util.get_screen(self.main_object))
        # self.setting_screen_win.set_top()
        self.setting_screen_win.show()

    # 打开设置主题窗口
    def push_button_setting_theme_click(self):
        from src.card.main_card.SettingCard.setting.setting_theme import SettingThemeWindow
        self.toolkit.resolution_util.out_animation(self.main_object)
        self.setting_theme_win = SettingThemeWindow(self, self.main_object, self.setting_data)
        self.setting_theme_win.refresh_geometry(self.toolkit.resolution_util.get_screen(self.main_object))
        # self.setting_theme_win.set_top()
        self.setting_theme_win.show()

    def save_setting_to_main(self, trigger_type, in_data=None):
        self.setting_data.update(in_data)
        self.save_data_func(trigger_type=trigger_type, in_data=self.data)

    def refresh_theme(self):
        for setting_card_button in self.setting_card_button_list:
            button = setting_card_button[0]
            icon_type = setting_card_button[2]
            icon_name = setting_card_button[3]
            icon_label = setting_card_button[4]
            text_label = setting_card_button[5]
            icon_label.setPixmap(style_util.get_pixmap_by_path(icon_type + '/' + icon_name, is_dark=not self.is_light()))
            if self.is_light():
                text_label.setStyleSheet("color:rgb(0,0,0);border: 0px solid black;background: transparent;")
                button.setStyleSheet("""
                QPushButton {
                    border-radius: 10px;
                    border: 0px solid black;
                    background: transparent;
                }
                QPushButton:hover {
                    border-radius: 10px;
                    border: 0px solid black;
                    background: rgba(34, 34, 34, 20);
                }
                """)
            else:
                text_label.setStyleSheet("color:rgb(239, 240, 241);border: 0px solid black;background: transparent;")
                button.setStyleSheet("""
                QPushButton {
                    border-radius: 10px;
                    border: 0px solid black;
                    background: transparent;
                }
                QPushButton:hover {
                    border-radius: 10px;
                    border: 0px solid black;
                    background: rgba(255, 255, 255, 15);
                }""")
        if self.is_light():
            panel_style = "QWidget {" + \
                              "border-radius: 10px;" + \
                              "border: 1px solid white;" + \
                              "background-color:rgba(255, 255, 255, 200);" + \
                          "}"
        else:
            panel_style = "QWidget {" + \
                              "border-radius: 10px;" + \
                              "border: 0px solid rgba(0, 0, 0, 220);" + \
                              "background-color:rgba(0, 0, 0, 60);" + \
                          "}"
        self.parent.widget_setting_setting.setStyleSheet(panel_style)
        self.parent.widget_setting_update.setStyleSheet(panel_style)
        self.parent.widget_setting_about.setStyleSheet(panel_style)
        self.parent.widget_setting_open_source.setStyleSheet(panel_style)
        # 在按钮右上角添加/显示更新提示
        button_width = 70
        button_interval = 10
        red_dot_padding = 10
        try:
            if self.main_object.ticket_vip_sign is None:
                self.main_object.ticket_vip_sign = add_vip_sign_in_button(self.main_object.push_button_setting_ticket, self.main_object.is_dark)
                self.main_object.ticket_vip_sign.move(button_width * 3 + button_interval * 2 - red_dot_padding - 5, red_dot_padding)
            else:
                self.main_object.ticket_vip_sign.show()
        except Exception as e:
            print(f"设置界面:{e}")

    def push_button_setting_faq_click(self):
        self.toolkit.resolution_util.out_animation(self.main_object)
        browser_util.open_url(common.help_url)

    def push_button_setting_service_agreement_click(self):
        self.toolkit.resolution_util.out_animation(self.main_object)
        browser_util.open_url(common.user_agreement_url)

    def push_button_setting_privacy_agreement_click(self):
        self.toolkit.resolution_util.out_animation(self.main_object)
        browser_util.open_url(common.privacy_policy_url)

    def push_button_setting_open_source_link_click(self):
        self.toolkit.resolution_util.out_animation(self.main_object)
        browser_util.open_url(common.open_source_url)

    def push_button_setting_open_source_list_click(self):
        self.toolkit.resolution_util.out_animation(self.main_object)
        text_box_util.show_text_dialog(self.main_object, "开源许可", {
            "content": open_source_constant.open_source,
            "size": [500, 660],
            "longText": True,
            "markdown": True
        })

    def push_button_setting_about_us_click(self):
        from src.module.About.about_us import AboutUsWindow
        self.toolkit.resolution_util.out_animation(self.main_object)
        self.setting_about_us_win = AboutUsWindow(None, self.main_object)
        self.setting_about_us_win.refresh_geometry(self.toolkit.resolution_util.get_screen(self.main_object))
        # self.setting_about_us_win.set_top()
        self.setting_about_us_win.show()

    def push_button_setting_ticket_click(self):
        # 未登录的判断
        self.main_object.show_login_tip()
        if self.main_object.current_user['username'] == "LocalUser":
            return
        if not self.main_object.is_vip:
            dialog_module.box_information(self.main_object, "提示信息", "会员专属功能，请开通会员后使用哦")
            return
        self.toolkit.resolution_util.out_animation(self.main_object)
        ticket_box_util.show_ticket_list_dialog(main_object=self.main_object,
                                               current_user=self.main_object.current_user)

    def push_button_setting_feedback_opinion_click(self):
        # 未登录的判断
        self.main_object.show_login_tip()
        if self.main_object.current_user['username'] == "LocalUser":
            return
        self.toolkit.resolution_util.out_animation(self.main_object)
        feedback_box_util.show_feedback_dialog(main_object=self.main_object,
                                               title="意见反馈",
                                               current_user=self.main_object.current_user)

    def push_button_setting_version_info_click(self):
        self.toolkit.resolution_util.out_animation(self.main_object)
        text_box_util.show_text_dialog(self.main_object, "版本信息", {
            "content": version_constant.get_update_info(),
            "size": [450, 500],
            "longText": True,
            "markdown": True
        })

    def push_button_setting_version_click(self):
        """检查更新"""
        # 创建更新器实例
        self.updater = Updater(
            api_url=common.BASE_URL + "/version/public/check?type=Windows",
            app_version=self.main_object.app_version,  # 假设 main_object 有 app_version 属性,
            update_dir=self.main_object.app_data_update_path
        )

        # 连接信号
        self.updater.progress.connect(self._handle_update_progress)
        self.updater.finished.connect(self._handle_update_result)
        self.updater.message.connect(self._handle_update_message)

        # 开始检查更新
        self.updater.check_update()

    def _handle_update_progress(self, progress):
        """处理下载进度"""
        # 可以在这里显示进度条（可选）
        print(f"下载进度: {progress}%")

    def _handle_update_message(self, message):
        """处理更新消息"""
        self.toolkit.message_box_util.box_information(
            self.main_object,
            "更新消息",
            message
        )

    def _handle_update_result(self, success, update_info):
        """处理更新结果"""
        if not success:
            self.toolkit.message_box_util.box_information(
                self.main_object,
                "更新失败",
                "检查更新失败，请检查网络连接"
            )
            return

        # 判断是否需要更新
        if version_constant.compare_version(self.main_object.app_version, update_info.get("version")) >= 0:
            # 如果当前版本大于等于更新版本，隐藏检查更新右上角更新提示
            if self.main_object.update_red_dot is not None:
                self.main_object.update_red_dot.hide()
            # 提示用户当前已是最新版本
            self.toolkit.message_box_util.box_information(
                self.main_object,
                "版本信息",
                f"当前已是最新版本: {update_info['version']}"
            )
            return
        # 如果不同表示云端有更新版本，在检查更新右上角添加/显示更新提示
        button_width = 70
        button_interval = 10
        red_dot_padding = 10
        if self.main_object.update_red_dot is None:
            self.main_object.update_red_dot = add_red_dot_in_button(self.main_object.push_button_setting_version)
            self.main_object.update_red_dot.move(button_width * 2 + button_interval * 1 - red_dot_padding, red_dot_padding)
        else:
            self.main_object.update_red_dot.show()
        markdown_content = update_info["title"] + "\n" + update_info["message"]
        reply = self.toolkit.message_box_util.box_acknowledgement(self.main_object,
                                                      title="发现新版本",
                                                      markdown_content=markdown_content,
                                                      button_ok_text="确定更新", button_no_text="取消")
        if not reply:
            return

        if self.main_object.run_environment == "exe":
            # 开始下载更新包（显示进度对话框）
            self._start_update_download(update_info)
        elif self.main_object.run_environment == "msix":
            # 拉起微软应用商店
            store_url = "ms-windows-store://downloadsandupdates"
            try:
                # 在Windows上
                subprocess.Popen(f'cmd /c start "" "{store_url}"', shell=True)
            except Exception as e:
                message_box_util.box_information(self.main_object, "错误", "无法打开微软商店，请手动打开微软商店对灵卡面板进行更新")
        else:
            return

    def _start_update_download(self, update_info):
        """开始下载更新包（参考update_module.py的实现）"""
        # 创建进度对话框
        progress_dialog, progress_bar, cancel_button = self.toolkit.message_box_util.box_progress(
            self.main_object,
            "软件更新",
            "正在下载更新..."
        )

        # 保存对话框引用
        self.progress_dialog = progress_dialog
        self.progress_dialog.show()

        # 重新配置更新器（用于下载）
        self.updater = Updater(
            api_url=common.BASE_URL + "/version/public/check?type=Windows",
            app_version=self.main_object.app_version,
            update_dir=self.main_object.app_data_update_path
        )

        # 连接下载信号
        self.updater.progress.connect(progress_bar.setValue)
        self.updater.finished.connect(
            lambda success, _: self._handle_download_finished(success, update_info))

        # 取消按钮事件
        cancel_button.clicked.connect(self._handle_cancel_download)

        # 开始下载
        self.updater.download_package(update_info)

    def _handle_cancel_download(self):
        """取消下载处理"""
        if self.updater and self.updater.current_reply:
            self.updater.current_reply.abort()
        if self.progress_dialog:
            self.progress_dialog.close()
            self.progress_dialog = None

    def _handle_download_finished(self, success, update_info):
        """下载完成处理"""
        if self.progress_dialog:
            self.progress_dialog.close()
            self.progress_dialog = None

        if success:
            # 获取下载的文件路径
            download_path = self.updater.downloaded_file_path
            if update_info.get("updateTag"):
                # 大版本更新：运行安装包并退出
                self._run_installer_and_exit(download_path)
            else:
                if "exeUrl" in update_info and update_info["exeUrl"] is not None and update_info["exeUrl"] != "":
                    # 小版本更新：替换exe文件
                    self._replace_exe_and_restart(download_path, update_info)
                else:
                    # 没有小版本更新文件则默认运行安装包
                    self._run_installer_and_exit(download_path)
        else:
            self.toolkit.message_box_util.box_information(
                self.main_object,
                "更新失败",
                "下载更新包失败，请检查网络连接或稍后重试"
            )

    def _replace_exe_and_restart(self, new_exe_path, update_info):
        """替换exe文件并重启应用"""
        # 获取当前exe的路径
        current_exe_path = os.path.abspath(sys.argv[0])
        # 获取updater_helper的路径（假设在同一目录下）
        helper_path = os.path.join(os.path.dirname(current_exe_path), "patch_updater.exe")
        if not os.path.exists(helper_path):
            message_box_util.box_information(
                self.main_object,
                "错误",
                "更新失败，您可以在官网下载安装最新版本。"
            )
            self.main_object.agree_update = False
            self.main_object.update_ready.emit()
            return
        # 关闭主程序
        self.main_object.quit_before_do()
        # 运行安装包
        try:
            if sys.platform == "win32":
                os.startfile(helper_path)
            else:
                subprocess.Popen([helper_path])
        except Exception as e:
            message_box_util.box_information(
                self.main_object,
                "错误",
                f"无法启动安装程序: {str(e)}"
            )
        # 退出应用
        QApplication.quit()

    def _run_installer_and_exit(self, exe_path):
        """运行安装包并退出程序"""
        # 获取当前exe的路径
        current_exe_path = os.path.abspath(sys.argv[0])
        # 获取updater_helper的路径（假设在同一目录下）
        helper_path = os.path.join(os.path.dirname(current_exe_path), "full_updater.exe")
        if not os.path.exists(helper_path):
            message_box_util.box_information(
                self.main_object,
                "错误",
                "更新失败，您可以在官网下载安装最新版本。"
            )
            self.main_object.agree_update = False
            self.main_object.update_ready.emit()
            return
        # 关闭主程序
        self.main_object.quit_before_do()
        # 运行安装包
        try:
            if sys.platform == "win32":
                os.startfile(helper_path)
            else:
                subprocess.Popen([helper_path])
        except Exception as e:
            message_box_util.box_information(
                self.main_object,
                "错误",
                f"无法启动安装程序: {str(e)}"
            )
        # 退出应用
        QApplication.quit()
