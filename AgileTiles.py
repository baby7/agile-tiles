# -*- coding: utf-8 -*-
# 基础包
import copy
import json
import os, sys
import atexit
import subprocess
import time, datetime

# 忽略PyDevd的错误
os.environ['PYDEVD_DISABLE_FILE_VALIDATION'] = '1'

print("_基础包加载完成")
# 资源包
import compiled_resources
print("_资源包加载完成")
# 管理员权限(现在取消)
import ctypes
# 错误日志
import traceback
# 内存控制
import gc
# 内存跟踪 & 内存诊断
import tracemalloc
import faulthandler
print("_日志和调试分析包加载完成")
# 热键监听
from ctypes.wintypes import MSG
print("_热键监听包加载完成")
# 基础界面框架
from PySide6 import QtCore
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import QEvent, Qt, qInstallMessageHandler, QSettings, Signal, QEventLoop, Q_ARG, Slot, \
    QMetaObject, QTimer, QSharedMemory
from PySide6.QtWidgets import QApplication, QSystemTrayIcon
from PySide6.QtNetwork import QLocalServer, QLocalSocket, QNetworkDiskCache, QNetworkReply

print("_基础界面框架加载完成")
# 我的界面内容
from baby7_desktop_tool_form import Ui_Form
print("_界面加载完成")
# 卡片管理
from src.card.NormalCardManager.NormalCardManager import NormalCardManager
from src.card.MainCardManager.MainCardManager import MainCardManager
print("_卡片管理加载完成")
# 窗口工具
from src.my_component.TutorialWindow.TutorialWindow import TutorialWindow
from src.my_component.MainAcrylicWindow.MainAcrylicWindow import MainAcrylicWindow
from src.my_component.ImageCacheManager.ImageCacheManager import ImageCacheManager
from src.my_component.Neumorphism import QtWidgets, QtGui
from src.my_component.GlobalHotkeyManager import GlobalHotkeyManager
from src.my_component.TopImageAcrylicWindow import TopImageAcrylicWindow
print("_窗口工具包加载完成")
# 模块
from src.module import init_module, dialog_module
from src.module.Box import text_box_util
from src.module.Icon import icon_tool
from src.module.Theme import theme_module
from src.module.Screen import screen_module
from src.module.User import user_module
from src.module.Updater import update_module
from src.module.ColorPicker import color_converter_util
from src.module.ColorPicker.ColorPickerWidget import ScreenColorPicker
from src.module.ImageToExcel import image_to_excel_converter_util, single_image_to_excel_converter_util
from src.module.Screenshot.ScreenshotWidget import ScreenshotWidget
from src.module.UserData.Sync.data_client import DataClient
from src.module.User.user_client import UserClient
from src.module.Login.start_login import StartLoginWindow
from src.module.UserData.DataBase.DatabaseManager import DatabaseManager
from src.module.StartCard.StartCardManager import CardManager
print("_模块包加载完成")
# 线程
from src.thread_list import card_thread, main_thread
print("_线程包加载完成")
# 工具
from src.ui import style_util
from src.util.Toolkit import Toolkit
from src.util import main_data_compare, hardware_id_util, winreg_util

print("_工具包加载完成")
# 静态常量
from src.constant import data_save_constant, card_constant, version_constant
print("_静态常量加载完成")

# 捕获Qt的日志
def qt_message_handler(mode, context, message):
    if "stun" in message.lower() or "dns" in message.lower():
        print(f"[Qt Network] mode: {mode}, context: {context}, message: {message}")
qInstallMessageHandler(qt_message_handler)
print("_捕获Qt的日志完成")

# 获取当前阈值
current_thresholds = gc.get_threshold()
print(f"默认GC配置: {current_thresholds}")  # 默认通常是(700, 10, 10)
# 设置新的阈值
gc.set_threshold(2000, 30, 20) # 设置 threshold0=1000, threshold1=15, threshold2=10
# 再次获取确认设置生效
new_thresholds = gc.get_threshold()
print(f"新的GC配置: {new_thresholds}")

# # 暂停垃圾回收
# gc.disable()
# # 验证垃圾回收是否已关闭
# if not gc.isenabled():  # 检查垃圾回收机制是否被禁用
#     print("垃圾回收已关闭。")
# else:
#     print("垃圾回收仍然开启。")


def handleException(exc_type, exc_value, exc_traceback):
    '''
    使用方法在入口位置,最开始位置(sys.exit(app.exec_())之前 )加入这一行
    sys.excepthook = handle_exception
    类似：import cgitb
        cgitb.enable(format='txt')
    Args:
        exc_type:
        exc_value:
        exc_traceback:

    Returns:
    '''
    if issubclass(exc_type, KeyboardInterrupt):
        return sys.__excepthook__(exc_type, exc_value, exc_traceback)
    exception = str("".join(traceback.format_exception(
        exc_type, exc_value, exc_traceback)))
    dialog = QtWidgets.QDialog()
    # close对其进行删除操作
    dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    msg = QtWidgets.QMessageBox(dialog)
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText('程序异常,请尝试重启或联系管理员!')
    msg.setWindowTitle("系统异常提示请尝试重启")
    msg.setDetailedText(exception)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.exec()


def is_another_instance_running():
    """检查是否已有实例在运行"""
    shared_memory = QSharedMemory("AgileTiles")
    # 尝试附加到现有共享内存
    if shared_memory.attach():
        # 如果能附加，说明已有实例运行
        shared_memory.detach()
        return True
    # 尝试创建共享内存
    if not shared_memory.create(1):  # 创建1字节大小的共享内存
        # 创建失败，说明已有实例运行
        error = shared_memory.error()
        if error == QSharedMemory.AlreadyExists:
            # 共享内存已存在，尝试附加确认
            if shared_memory.attach():
                shared_memory.detach()
                return True
        return True  # 其他创建错误也认为已有实例
    # 创建成功，无其他实例
    return False


def is_running_in_msix(current_exe_path):
    """通过检查环境变量判断是否运行在 MSIX 容器中"""
    assets_dir = os.path.join(os.path.dirname(current_exe_path), "Assets")
    return os.path.exists(assets_dir)


# 主窗口
class AgileTilesForm(MainAcrylicWindow, Ui_Form):

    # 基础
    app_name = "AgileTiles"                 # 应用名称
    app_title = "灵卡面板"                    # 应用标题
    app_version = None                      # 应用版本
    tray_icon = None                        # 图标
    sys_icon = None                         # 图标文件(QIcon)
    sys_icon_pixmap = None                  # 图标文件(QPixmap)
    info_logger = None                      # 日志
    # 设备id
    hardware_id = None
    os_version = None
    run_environment = "exe"                 # 运行环境 exe/msix
    # 线程列表
    main_thread_object = None               # 主线程
    normal_card_thread_object_list = []     # 普通卡片线程列表
    main_card_thread_object_list = []       # 主卡片线程列表
    # 分辨率和动画信息
    screen_x = 0                    # 屏幕所在的屏幕位置x
    screen_y = 0                    # 屏幕所在的屏幕位置y
    taskbar_height = 0              # 任务栏高度
    desktop_width = 0               # 桌面宽度
    desktop_height = 0              # 桌面高度
    group = None                    # 执行动画的对象
    show_form = False               # 是否显示（隐藏是移动到窗口外）
    pin_form = False                # 是否钉住界面
    is_mouse_trigger = False        # 是否是鼠标触发的窗口弹出
    animation_time = 0              # 动画时间
    form_locate = "Right"           # 窗口位置 Left/Right
    dialog_fault = None
    hide_timer = None
    is_dark = None
    theme_idempotence = False       # 主题幂等控制
    is_show = False
    form_animation_time = 200
    # 控件
    widget_header = None            # 顶部导航栏
    push_button_header_info = None        # 导航栏信息
    label_menu = None               # 菜单栏
    label_current_menu = None       # 菜单指示条
    # 主题信息
    form_theme = None
    form_theme_mode = None
    form_theme_transparency = None
    # 卡片
    main_card_manager = None
    normal_card_manager = None
    main_card_list = []
    normal_card_list = []
    image_card_data = None  # 图片卡片数据
    cache_label = None  # 卡片缓存
    card_area_list = []
    card_content_list = []
    use_card_area_list = []
    CARD_WIDTH = card_constant.CARD_WIDTH           # 卡片宽度
    CARD_HEIGHT = card_constant.CARD_HEIGHT         # 卡片高度
    CARD_INTERVAL = card_constant.CARD_INTERVAL     # 卡片间距
    # 图片缓存管理器
    image_cache_manager = None
    # 设置
    card_permutation_win = None
    setting_keyboard_win = None
    # 键盘热键管理
    hotkey_manager = None
    # 用户
    current_user = None
    login_restart_data = None       # 用于登录时刷新失效重新登录的数据
    database_manager = None
    user_data_status = None
    is_login = False
    main_data = {}
    is_vip = False
    access_token = None
    refresh_token = None
    refresh_token_datetime = None
    # 上次获取用户时间
    last_get_user_info_time = 0
    get_user_info_interval_time = 10 * 60 * 1000                 # 加载间隔10分钟
    # 启动状态
    is_first = True
    start_login_view = False        # 登录窗口是否展示
    # 更新相关
    agree_update = True
    update_red_dot = None   # 更新提示红点
    # VIP相关
    ticket_vip_sign = None
    qr_code_dialog = None            # 支付窗口
    user_server_recover_win = None   # 恢复历史数据窗口
    subscription_history_dialog = None   # 会员订阅记录窗口
    # 其他
    theme_switch_button = None
    silent_updater = None
    # 窗口
    dialog_map = {}
    # 截图
    show_overlay_status = False

    update_ready = Signal()
    login_ready = Signal()
    card_ready = Signal()

    def __init__(self):
        super(AgileTilesForm, self).__init__()
        # **************** 基本初始化 ****************
        # 窗口置顶
        self.setWindowFlag(Qt.WindowType.ToolTip)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        # 设置主机id和系统版本
        self.hardware_id = hardware_id_util.get_hardware_id()
        self.os_version = hardware_id_util.get_os_version()
        # 运行环境
        current_exe_path = os.path.abspath(sys.argv[0])
        self.run_environment = "msix" if is_running_in_msix(current_exe_path) else "exe"
        print(f'运行环境:{self.run_environment}')
        # 工具包
        self.toolkit = Toolkit(self, self)
        # 软件数据路径
        self.app_data_path = self.toolkit.file_util.get_app_data_path(self.app_name)
        self.app_data_db_path = self.toolkit.file_util.get_app_data_db_path(self.app_data_path, self.app_name)
        self.app_data_everything_db_path = self.toolkit.file_util.get_app_data_everything_db_path(self.app_data_path)
        self.app_data_everything_config_path = self.toolkit.file_util.get_app_data_everything_config_path(self.app_data_path)
        self.app_data_plugin_path = self.toolkit.file_util.get_app_data_plugin_path(self.app_data_path)
        self.app_data_network_path = self.toolkit.file_util.get_app_data_network_path(self.app_data_path)
        self.app_data_image_path = self.toolkit.file_util.get_app_data_image_path(self.app_data_path)
        self.app_data_update_path = self.toolkit.file_util.get_app_data_update_path(self.app_data_path)
        self.app_data_logger_path = self.toolkit.file_util.get_app_data_logger_path(self.app_data_path)
        # 图片缓存管理器
        self.image_cache_manager = ImageCacheManager(image_path=self.app_data_image_path)
        # 网络缓存
        self.network_disk_cache = QNetworkDiskCache(self)
        self.network_disk_cache.setCacheDirectory(self.app_data_network_path)
        self.network_disk_cache.setMaximumCacheSize(100 * 1024 * 1024)    # 设置缓存大小（单位：字节） 例如 100 MB
        # ***************** 更新检测 *****************
        # 创建本地事件循环
        update_loop = QEventLoop()
        # 数据加载完成信号
        self.update_ready.connect(update_loop.quit)
        # 启动时，检测更新
        self.check_update_run(tag="Start")
        # 阻塞等待数据就绪
        update_loop.exec()
        # 判断用户是否同意更新版本
        if not self.agree_update:
            self.quit_before(is_hide_dialog=True)
            exit()
        # ***************** 登录检测 *****************
        # 创建本地事件循环
        login_loop = QEventLoop()
        # 数据加载完成信号
        self.login_ready.connect(login_loop.quit)
        # 异步加载用户数据
        self.load_data()
        # 阻塞等待数据就绪
        login_loop.exec()
        # ***************** 卡片检测 *****************
        # 创建本地事件循环
        card_loop = QEventLoop()
        # 数据加载完成信号
        self.card_ready.connect(card_loop.quit)
        # 异步加载卡片
        self.check_card_run()
        # 阻塞等待数据就绪
        card_loop.exec()
        # **************** 后续初始化 ****************
        # 同步初始化UI
        self.atomic_init()

    def init(self):
        print(f"用户状态:{self.user_data_status}")
        if self.is_first:
            # 首次启动则进行其他初始化
            self.login_ready.emit()
        else:
            # 进行重新登录的初始化
            self.do_login_again()

    def atomic_init(self):
        # 启用faulthandler（仅在stderr可用时）
        try:
            if sys.stderr is not None:
                faulthandler.enable()
        except Exception:
            pass
        # 初始化分辨率参数、位置和大小
        screen_module.init_resolution(self, out_animation_tag=False)
        # 初始化主题
        theme_module.init_theme(self)
        # 显示加载中窗口
        self.show_load_window(f"{self.app_title}启动中...")
        # 其余初始化
        init_module.init_module(self)
        # 初始化样式
        self.update_load_window("正在初始化样式...")
        init_module.init_style(self)
        # 初始化模块
        self.update_load_window("正在初始化模块...")
        user_module.init_module(self)
        # 卡片
        self.update_load_window("正在初始化卡片...")
        self.init_card()
        # 透明窗口和隐藏任务栏图标(使用QTimer延迟执行避免阻塞)
        self.update_load_window("正在初始化透明窗口...")
        self.refresh_window_show()
        # 初始化所有请求对象
        self.update_load_window("正在初始化请求...")
        self.init_all_client()
        # 线程
        self.update_load_window("正在初始化线程...")
        self.start_thread_list()
        # 初始化鼠标检测窗口
        self.update_load_window("正在初始化鼠标检测窗口...")
        screen_module.init_mouse_detect_window(self)
        # 初始化主题
        self.update_load_window("正在设置主题...")
        init_module.set_theme(self, is_main=True)
        # 初始化弹窗
        self.update_load_window("正在初始化弹窗...")
        dialog_module.set_dialog(self)
        # 首次启动时，显示引导程序
        self.update_load_window("正在初始化引导程序...")
        self.check_first_run()
        # 更新状态
        self.is_first = False
        # 启动时，先执行一次定时任务
        self.update_load_window("正在初始化定时任务...")
        self.time_task()
        # 设置字体
        self.update_load_window("正在初始化字体...")
        style_util.set_font_and_right_click_style(self, self)
        # 退出动画
        self.update_load_window("")
        self.toolkit.resolution_util.out_animation(self)
        # 隐藏加载中窗口
        self.hide_load_window(set_auto_start=True)

    def show_load_window(self, load_title=None):
        # 显示窗口
        self.show()
        # 显示加载中窗口
        font = QFont()
        font.setPointSize(16)
        self.label_background.setFont(font)
        self.label_background.setAlignment(Qt.AlignCenter)
        if self.is_dark:
            self.label_background.setStyleSheet("background-color: rgb(24, 24, 24); color: rgb(255, 255, 255)")
        else:
            self.label_background.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgb(204, 240, 255), stop:1 rgb(244, 186, 254)); color: rgb(0, 0, 0)")
        self.label_background.setText(load_title)
        self.label_background.resize(self.width(), self.height())
        self.label_background.show()
        self.label_background.raise_()
        # 刷新界面
        QApplication.processEvents()

    def update_load_window(self, load_title=None):
        print(f'__{load_title},开始时间:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}')
        self.label_background.setText(load_title)
        QApplication.processEvents()

    def hide_load_window(self, set_auto_start=False):
        self.label_background.setText("")
        self.widget_base.show()
        self.widget_base.raise_()
        # 顶部导航条显示
        self.widget_header.show()
        # 判断用户是否登录
        if self.current_user['username'] == "LocalUser":
            self.push_button_header_info.setText("未登录状态不存储数据！")
            self.push_button_area_user_login.show()
            self.push_button_area_user_vip_subscription.hide()
            self.push_button_area_user_vip_subscription_history.hide()
            self.label_area_user_vip_info.hide()
            self.push_button_area_user_message_logout.hide()
            self.label_area_user_message_logout.hide()
        else:
            self.push_button_header_info.hide()
            self.push_button_area_user_login.hide()
        # 菜单栏显示
        self.label_menu.show()
        # 小卡片管理显示
        self.normal_card_manager.show()
        # 菜单按钮指示显示
        self.label_current_menu.show()
        # 设置菜单按钮指示位置
        self.main_card_manager.change_menu_indicate_location()
        # 弹窗
        self.widget_dialog_base.raise_()
        # 用来展示一个空白窗口
        # self.label_background.hide()
        # self.widget_base.hide()
        # self.widget_header.hide()
        # self.label_menu.hide()
        # self.normal_card_manager.hide()
        # self.label_current_menu.hide()
        # self.widget_dialog_base.hide()
        # 开机自启动
        if set_auto_start:
            winreg_util.set_auto_start(True)
        # 设置主题
        init_module.set_theme(self, is_main=True)
        # 刷新进程
        QApplication.processEvents()

    def show_login_tip(self, need_tip=True, tip_text=None):
        if need_tip:
            if self.current_user['username'] != "LocalUser":
                return
            if tip_text is None:
                tip_text = "请登录后使用该功能，要现在登录吗？"
            if not dialog_module.box_acknowledgement(self, "注意", tip_text):
                return
        QTimer.singleShot(1, lambda : self.show_login_tip_do())

    def show_login_tip_do(self):
        if hasattr(self, "single_login_tip_dialog"):
            try:
                self.single_login_tip_dialog.close()
                self.single_login_tip_dialog = None
            except Exception:
                pass
        # 启动登录窗口
        if not self.is_first:
            # 设置主题到QSetting
            settings = QSettings(self.app_name, "Theme")
            settings.setValue("IsDark", self.is_dark)
        # 显示登录窗口
        self.single_login_tip_dialog = StartLoginWindow(None, self)
        self.single_login_tip_dialog.refresh_geometry(self.toolkit.resolution_util.get_screen(self))
        self.single_login_tip_dialog.show()

    ''' **********************************数据管理*************************************** '''
    def load_data(self):
        # 启动时，检测本地用户
        try:
            # 初始化数据库
            self.database_manager = DatabaseManager(db_path=self.app_data_db_path)
            # 获取本地当前用户
            self.current_user = self.database_manager.get_current_user()
            if self.current_user is None or self.current_user["username"] == "LocalUser":
                # 如果首次启动，则以本地用户身份启动
                self.access_token = "access_token"
                self.refresh_token = "refresh_token"
                self.refresh_token_datetime = datetime.datetime.now()
                self.is_vip = False
                self.current_user = {
                    "id": "0",
                    "nickName": "本地用户",
                    "username": "LocalUser",
                    "accessToken": self.access_token,
                    "refreshToken": self.refresh_token,
                    "vipStatus": self.is_vip,
                    "vipExpireTime": None,
                    "inviteCode": None,
                }
                self.save_user(self.current_user["username"], self.refresh_token)
                self.main_data = self.save_default_data(self.current_user["username"])
                print("以本地用户身份启动")
                # 如果是本地用户则直接初始化
                self.do_local_login()
                return
            else:
                # 获取本地用户数据
                main_data_str = self.database_manager.get_current_data(self.current_user["username"])
                if main_data_str is None:
                    # 如果数据为空，则保存默认数据
                    self.main_data = self.save_default_data(self.current_user["username"])
                else:
                    self.main_data = json.loads(main_data_str)
        except Exception as e:
            self.info_logger.error(f"启动失败:{traceback.format_exc()}")
            print("启动失败")
            exit()
        # 判断用户是否登录，未登录则退出程序
        if self.current_user is None:
            self.current_user = self.database_manager.get_current_user()
            if self.current_user is None:
                self.quit_before(is_hide_dialog=True)
                print("流程1:用户未登录")
                exit()
        # 执行登录后的操作
        print("准备执行登录后的操作")
        self.do_login()

    def do_login(self):
        # 获取本地用户后，准备获取云端数据
        try:
            # 先获取本地数据
            print(f"先获取本地数据, self.current_user:{self.current_user}")
            main_data_str = self.database_manager.get_current_data(self.current_user["username"])
            if main_data_str is None:
                # 如果数据为空，则保存默认数据
                self.main_data = self.save_default_data(self.current_user["username"])
            else:
                self.main_data = json.loads(main_data_str)
            username = self.current_user["username"]
            refresh_token = self.current_user["refreshToken"]
            if username is None or refresh_token is None:
                self.user_data_status = "not_login"
                print("用户未存储登录信息")
                self.init()
                return

            # 初始化用户请求
            self.start_user_info_client = UserClient()
            self.start_user_info_client.refreshFinished.connect(self.handle_do_refresh)

            # 进行登录(其实是刷新令牌获取accessToken)
            print("进行登录(其实是刷新令牌获取accessToken)")
            self.start_user_info_client.refresh(username, refresh_token, self.hardware_id, self.os_version)
        except Exception as e:
            print(f"do_login error: {str(e)}")

    def handle_do_refresh(self, result):
        json_str = json.dumps(result)  # 转换为 JSON 字符串
        print(f"登录刷新令牌结果:{json_str}")
        # 使用 QMetaObject 确保在主线程执行
        QMetaObject.invokeMethod(
            self,
            "_safe_do_refresh",
            Qt.ConnectionType.QueuedConnection,
            Q_ARG(str, json_str)
        )

    @Slot(str)
    def _safe_do_refresh(self, result_str):
        result = json.loads(result_str)  # 解析 JSON
        # 获取本地用户后，准备获取云端数据
        try:
            if result['code'] == 1:
                self.user_data_status = "login_fail"
                self.is_login = False
                print(result)
                print(f"登录失败，原因：{result['msg']}")
                self.toolkit.message_box_util.box_information(self, "错误信息", "登录失败，请重新登录")
                # 注销登录
                self.database_manager.logout_user()
                self.current_user = None
                # 打开登录窗口手动登录
                self.show_start_login_window()
                # 判断用户是否登录，未登录则退出程序
                self.current_user = self.database_manager.get_current_user()
                if self.current_user is None or self.login_restart_data is None:
                    self.quit_before(is_hide_dialog=True)
                    print("流程2:用户未登录")
                    exit()
                result = self.login_restart_data
                self.user_data_status = "login_restart"

            # 登录成功
            print("登录成功，存储用户状态")
            result_data = result["data"]
            self.user_data_status = "login_success"
            self.is_login = True
            self.access_token = "Bearer " + result_data['accessToken']
            self.refresh_token = result_data['refreshToken']
            self.refresh_token_datetime = datetime.datetime.now()
            self.is_vip = result_data['vipStatus']
            self.current_user = {
                "id": result_data["id"],
                "nickName": result_data["nickName"],
                "username": self.current_user["username"],
                "accessToken": self.access_token,
                "refreshToken": self.refresh_token,
                "vipStatus": self.is_vip,
                "vipExpireTime": result_data['vipExpireTime'],
                "inviteCode": result_data["inviteCode"],
            }
            # 更新刷新令牌到本地
            self.database_manager.update_user_refresh_token(self.current_user["username"], self.refresh_token)

            # 设置主题到QSetting
            settings = QSettings(self.app_name, "Theme")
            settings.setValue("IsDark", self.is_dark)

            # 初始化用户数据请求
            self.start_user_data_client = DataClient()
            self.start_user_data_client.pushFinished.connect(self.handle_start_push_result)
            self.start_user_data_client.pullFinished.connect(self.handle_start_pull_result)

            # 如果登录成功，则拉取数据
            self.start_user_data_client.pull_data(self.current_user["username"], self.access_token)
        except Exception as e:
            print(f"_safe_do_refresh error: {str(e)}")
        self.login_restart_data = None

    def show_start_login_window(self):
        self.start_login_view = True
        if not self.is_first:
            # 设置主题到QSetting
            settings = QSettings(self.app_name, "Theme")
            settings.setValue("IsDark", self.is_dark)
        # 显示登录窗口
        self.user_server_recover_win = StartLoginWindow(None, self)
        self.user_server_recover_win.refresh_geometry(self.toolkit.resolution_util.get_screen(self))
        self.user_server_recover_win.exec()
        self.start_login_view = False

    def save_user(self, username, refresh_token):
        register_success = self.database_manager.register_user(username, refresh_token)
        if not register_success:
            print("保存用户失败，已更新用户信息")
            self.database_manager.update_user_refresh_token(username, refresh_token)
        self.database_manager.update_last_login(username)

    def get_current_user(self):
        return self.database_manager.get_current_user()

    def set_current_user(self, user):
        print(f"设置当前用户:{user}")
        self.current_user = user

    def save_default_data(self, username):
        return self.database_manager.save_default_data(username, self.hardware_id)

    def get_local_user_data(self, username):
        return self.database_manager.get_current_data(username)

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
            self.init()
            return

        # 云端数据为空,将本地数据同步到云端
        if result["data"] is None or result["data"]["data"] is None:
            print("云端数据为空，将本地数据同步到云端")
            self.user_data_status = "server_data_none"
            self.start_user_data_client.push_data(self.current_user["username"], self.access_token, self.main_data)
            self.init()
            return

        # 获取云端数据成功
        server_main_data = json.loads(result["data"]["data"])

        # 云端数据比本地数据新
        if server_main_data["timestamp"] > self.main_data["timestamp"]:
            self.main_data = server_main_data
            self.user_data_status = "data_sync_success"
            print("云端数据比本地数据新，将云端数据同步到本地数据")
            self.init()
            return

        # 云端数据比本地数据旧
        if server_main_data["timestamp"] < self.main_data["timestamp"]:
            print("本地数据比云端数据新，将本地数据同步到云端")
            self.start_user_data_client.push_data(self.current_user["username"], self.access_token, self.main_data)
            self.init()
            return

        # 云端数据与本地数据一致
        print("云端数据与本地数据一致，无需更新本地数据")
        try:
            result = self.toolkit.time_util.get_datetime_str_by_timestamp(self.main_data["timestamp"])
            self.handle_update_backup_time(result)
        except Exception as e:
            self.info_logger.card_error("主程序", "导入数据失败,错误信息:{}".format(e))
        self.init()
        return

    def do_local_login(self):
        self.user_data_status = "login_success"
        self.is_login = True
        # 设置主题到QSetting
        settings = QSettings(self.app_name, "Theme")
        settings.setValue("IsDark", self.is_dark)
        QTimer.singleShot(1, self.init)

    def handle_update_backup_time(self, result):
        # 使用 QMetaObject 确保在主线程执行
        QMetaObject.invokeMethod(
            self,
            "_backup_time_update",
            Qt.ConnectionType.QueuedConnection,
            Q_ARG(str, result)
        )

    @Slot(str)
    def _backup_time_update(self, result):
        if hasattr(self, "label_user_last_backup_time"):
            self.label_user_last_backup_time.setText(self.toolkit.time_util.get_datetime_str_by_timestamp(self.main_data["timestamp"]))

    def handle_start_push_result(self, result):
        print(f"处理用户数据推送结果: {result}")
        if result['code'] == 1:
            self.info_logger.error(f"同步云端数据失败，原因：{result['msg']}")
            return
        if hasattr(self, "label_user_last_backup_time"):
            self.label_user_last_backup_time.setText(self.toolkit.time_util.get_datetime_str_by_timestamp(self.main_data["timestamp"]))

    def init_all_client(self):
        # 初始化用户数据请求
        self.user_data_client = DataClient()
        self.user_data_client.pushFinished.connect(self.handle_run_push_result)
        self.user_data_client.pullFinished.connect(self.handle_run_pull_result)
        # 初始化用户请求
        self.user_info_client = UserClient()
        self.user_info_client.infoFinished.connect(self.handle_user_detection_result)
        self.user_info_client.refreshFinished.connect(self.handle_refresh_token_result)
        # 初始化用户数据请求(设置处使用)
        self.user_data_client_by_setting = DataClient()
        self.user_data_client_by_setting.pushFinished.connect(self.handle_push_area_user_data_backup)
        self.user_data_client_by_setting.pullFinished.connect(self.handle_pull_area_user_data_synchronization)

    def sync_data(self):
        try:
            if self.current_user is None or self.current_user["username"] is None or self.access_token is None:
                return
            self.user_data_client.pull_data(self.current_user["username"], self.access_token)
        except Exception:
            self.info_logger.error(traceback.format_exc())

    def handle_run_pull_result(self, result):
        try:
            if result['code'] == 1:
                self.info_logger.error(f"同步云端数据失败，原因：{result['msg']}")
                return
            if result["data"] is None:
                print("云端无数据，需要上传到云端")
                try:
                    if self.current_user is not None and self.current_user["username"] is not None and self.access_token is not None:
                        self.user_data_client.push_data(self.current_user["username"], self.access_token, self.main_data)
                except Exception as e:
                    self.info_logger.error(traceback.format_exc())
                return
            server_main_data = json.loads(result["data"]["data"])
            server_timestamp = int(result["data"]["timestamp"])
            local_timestamp = int(self.main_data["timestamp"])
            if server_timestamp == local_timestamp:
                print("数据无更新")
                if self.is_vip:
                    self.label_user_last_backup_time.setText(self.toolkit.time_util.get_datetime_str_by_timestamp(self.main_data["timestamp"]))
                return
            elif server_timestamp < local_timestamp:
                print("本地数据比云端数据更新，需要上传到云端")
                try:
                    if self.current_user is not None and self.current_user["username"] is not None:
                        self.user_data_client.push_data(self.current_user["username"], self.access_token, self.main_data)
                except Exception as e:
                    self.info_logger.error(traceback.format_exc())
                return
            else:
                print("云端数据更新，需要更新到本地")
                old_data = copy.deepcopy(self.main_data)
                new_data = copy.deepcopy(server_main_data)
                self.main_data = server_main_data
                self.server_trigger_data_update(old_data=old_data, new_data=new_data)
                return
        except Exception:
            self.info_logger.error(traceback.format_exc())

    def handle_run_push_result(self, result):
        if result['code'] == 1:
            self.info_logger.error(f"保存云端数据失败，原因：{result['msg']}")
            return
        # 更新备份时间
        self.label_user_last_backup_time.setText(self.toolkit.time_util.get_datetime_str_by_timestamp(self.main_data["timestamp"]))

    ''' **********************************设置模块*************************************** '''

    # 连接信号处理
    def handle_pull_area_user_data_synchronization(self, result):
        if result['code'] == 1:
            self.toolkit.dialog_module.box_information(self, "提醒", f"同步云端数据失败，原因：{result['msg']}")
            return
        server_user_data = result
        if server_user_data['code'] == 1:
            self.toolkit.dialog_module.box_information(self, "提醒", f"同步云端数据失败，原因：{server_user_data['msg']}")
            return
        server_timestamp = int(server_user_data["data"]["timestamp"])
        local_timestamp = int(self.main_data["timestamp"])
        print(f"服务器时间戳:{server_timestamp},本地时间戳:{local_timestamp},服务器比本地多了{server_timestamp - local_timestamp}毫秒")
        if server_timestamp <= local_timestamp:
            self.toolkit.dialog_module.box_information(self, "提醒", f"云端数据与本地数据一致，无需同步")
            self.label_user_last_backup_time.setText(self.toolkit.time_util.get_datetime_str_by_timestamp(self.main_data["timestamp"]))
            return
        if server_user_data["data"]["data"] is None or server_user_data["data"]["data"] == "":
            self.toolkit.dialog_module.box_information(self, "提醒", f"云端数据为空，无需同步")
            self.label_user_last_backup_time.setText(self.toolkit.time_util.get_datetime_str_by_timestamp(self.main_data["timestamp"]))
            return
        server_main_data = json.loads(server_user_data["data"]["data"])
        old_data = copy.deepcopy(self.main_data)
        new_data = copy.deepcopy(server_main_data)
        self.main_data = server_main_data
        self.server_trigger_data_update(old_data=old_data, new_data=new_data)
        self.toolkit.dialog_module.box_information(self, "提醒", f"同步云端数据成功")
        self.label_user_last_backup_time.setText(self.toolkit.time_util.get_datetime_str_by_timestamp(self.main_data["timestamp"]))

    # 连接信号处理
    def handle_push_area_user_data_backup(self, result):
        if result['code'] == 1:
            self.toolkit.dialog_module.box_information(self, "提醒", f"保存云端数据失败，原因：{result['msg']}")
        else:
            self.toolkit.dialog_module.box_information(self, "提醒", f"保存云端数据成功")
            self.label_user_last_backup_time.setText(
                self.toolkit.time_util.get_datetime_str_by_timestamp(
                    self.main_data["timestamp"]
                )
            )

    ''' **********************************重启*************************************** '''
    def reboot(self):
        # 获取login_helper的路径（假设在同一目录下）
        current_exe_path = os.path.abspath(sys.argv[0])
        login_helper_path = os.path.join(os.path.dirname(current_exe_path), "login_helper.exe")
        # 关闭主程序
        self.quit_before_do()
        # 启动替换程序
        try:
            subprocess.Popen([login_helper_path])
        except Exception as e:
            QApplication.quit()
        # 退出应用
        QApplication.quit()


    ''' **********************************退出登录*************************************** '''
    def logout(self, need_dialog=True, dialog_content=None):
        # 显示对话框来确认
        if need_dialog:
            if dialog_content is None:
                dialog_content = "确定要退出登录吗？"
            confirm = self.toolkit.message_box_util.box_acknowledgement(self, "退出", dialog_content,
                                                                        dialog_map=self.dialog_map, dialog_key="logout")
            if not confirm:
                return
        # 获取login_helper的路径（假设在同一目录下）
        current_exe_path = os.path.abspath(sys.argv[0])
        login_helper_path = os.path.join(os.path.dirname(current_exe_path), "login_helper.exe")
        # 找不到就进行旧的更新逻辑
        if not os.path.exists(login_helper_path):
            try:
                # 隐藏窗口
                self.hide()
                # 消除登录状态
                self.user_data_status = "logout"
                self.is_login = False
                self.is_vip = None
                self.vip_expire_time = None
                self.access_token = None
                self.refresh_token = None
                self.refresh_token_datetime = None
                self.main_data = None
                self.current_user = None
                # 登出前的操作
                self.do_logout()
                # 启动登录窗口
                self.show_start_login_window()
            except Exception as e:
                self.info_logger.error(traceback.format_exc())
                exit()
            # 判断用户是否登录，未登录则退出程序
            if self.current_user is None:
                self.quit_before(is_hide_dialog=True)
                exit()
            # 展示窗口
            self.show()
            # 执行登录后的操作
            self.do_login()
        else:
            # 否则执行新的逻辑
            # 注销云端登录
            if self.current_user is not None and "id" in self.current_user:
                self.user_info_client.logout(self.current_user["id"], self.hardware_id)
                print("云端注销登录成功")
            # 注销本地登录
            self.database_manager.logout_user()
            print("本地注销登录成功")
            # 关闭主程序
            self.quit_before_do()
            # 启动替换程序
            try:
                subprocess.Popen([login_helper_path])
            except Exception as e:
                QApplication.quit()
            # 退出应用
            QApplication.quit()

    def do_logout(self):
        # 注销云端登录
        if self.current_user is not None and "id" in self.current_user:
            self.user_info_client.logout(self.current_user["id"], self.hardware_id)
            print("云端注销登录成功")
        # 注销本地登录
        self.database_manager.logout_user()
        print("本地注销登录成功")
        # 取消鼠标追踪
        self.setMouseTracking(False)
        self.form_enable_sidebar = False
        # 结束线程列表
        self.stop_thread_list()
        # 清理卡片
        self.clear_normal_card_list()
        self.clear_main_card_list()
        # 设置主题幂等控制
        self.theme_idempotence = True
        # 隐藏背景
        self.label_background.hide()
        # 删除vip角标
        if self.ticket_vip_sign is not None:
            try:
                self.ticket_vip_sign.hide()
                self.ticket_vip_sign.deleteLater()
                self.ticket_vip_sign = None
            except Exception:
                pass
        # 删除更新红点
        if self.update_red_dot is not None:
            try:
                self.update_red_dot.hide()
                self.update_red_dot.deleteLater()
                self.update_red_dot = None
            except Exception:
                pass

    def do_login_again(self):
        # 初始化分辨率参数、位置和大小
        screen_module.init_resolution(self)
        # 初始化主题
        theme_module.init_theme(self)
        # 初始化样式
        init_module.init_style(self)
        # 初始化模块
        user_module.init_module(self)
        # 卡片
        self.init_card()
        # 线程
        self.start_thread_list()
        # 透明窗口和隐藏任务栏图标
        self.refresh_window_show()
        # 初始化主题
        init_module.set_theme(self, is_main=True)
        # 重新初始化热键
        self.keyboard_re_init()
        # 切换到热搜卡片
        self.main_card_manager.push_button_weibo_click()
        # 设置字体
        style_util.set_font_and_right_click_style(self, self)

    ''' ******************************触发的数据修改*********************************** '''
    def server_trigger_data_update(self, old_data=None, new_data=None):
        """
        云端触发的数据更新
        :param old_data: 更新前的数据
        :param new_data: 更新后的数据
        """
        print("server_trigger_data_update - 云端触发的数据更新")
        # 判断需要进行哪些刷新(进行了高级别刷新就不需要进行低级别刷新)
        need_all_restart = False        # 对整体进行重载(3级别)
        need_all_card_restart = False   # 进行卡片整体重载(2级别)
        need_part_card_refresh = False  # 进行部分卡片数据刷新(1级别)
        need_keyboard_restart = False   # 对键盘进行重载(独立)

        # 如果新老数据不一致
        if old_data != new_data:
            print("server_trigger_data_update - 新老数据不一致")
            # 如果卡片数据有更新
            if main_data_compare.card_has_change(old_data, new_data):
                # 如果卡片有新增、删除、位置改变，需要对卡片进行重载
                # need_all_card_restart = True
                need_all_restart = True
            else:
                # 否则只需要进行部分卡片数据刷新
                need_part_card_refresh = True

            # 如果设置数据有更新
            if main_data_compare.setting_has_change(old_data, new_data):
                # 判断屏幕数据是否需要更新(后续使用elif因为均为对整体进行重载，有一个需要重载就不需要再判断了)
                if main_data_compare.setting_screen_has_change(old_data, new_data):
                    need_all_restart = True
                # 判断系统是否需要更新
                elif main_data_compare.setting_system_has_change(old_data, new_data):
                    need_all_restart = True
                    # 判断快捷键是否需要更新(快捷键属于系统设置)
                    if main_data_compare.setting_keyboard_has_change(old_data, new_data):
                        need_keyboard_restart = True
                # 判断主题是否需要更新
                elif main_data_compare.setting_theme_has_change(old_data, new_data):
                    need_all_restart = True

            # 对整体进行重载
            if need_all_restart:
                print("server_trigger_data_update - 对整体进行重载")
                # 初始化分辨率参数、位置和大小
                screen_module.init_resolution(self, is_first=False, out_animation_tag=False, is_show=self.show_form)
                # 重新初始化卡片
                self.restart_card(need_menu_change=False)
                # 获取有改变的大卡片列表
                normal_card_data_update_list, big_card_data_update_list, enduring_changes = (main_data_compare.
                                                                            get_card_list_by_data_change(old_data, new_data))
                # 对需要改变的卡片列表进行数据更新
                self.main_card_manager.refresh_card_list(big_card_data_update_list, enduring_changes)
                # 设置字体
                style_util.set_font_and_right_click_style(self, self)
            # 进行卡片整体重载
            elif need_all_card_restart:
                print("server_trigger_data_update - 卡片整体重载")
                # 重新初始化卡片
                self.restart_card(need_menu_change=False)
                # 设置字体
                style_util.set_font_and_right_click_style(self, self)
            # 进行部分卡片数据刷新
            elif need_part_card_refresh:
                print("server_trigger_data_update - 进行部分卡片数据刷新")
                # 如果只是部分卡片的缓存数据有改变，则获取有改变的卡片列表
                normal_card_data_update_list, big_card_data_update_list, enduring_changes = (main_data_compare.
                                                                            get_card_list_by_data_change(old_data, new_data))
                # 对需要改变的卡片列表进行数据更新
                self.main_card_manager.refresh_card_list(big_card_data_update_list, enduring_changes)
                self.normal_card_manager.refresh_card_list(normal_card_data_update_list, enduring_changes)

            # 对键盘进行重载
            if need_keyboard_restart:
                print("server_trigger_data_update - 对键盘进行重载")
                # 重新初始化热键
                self.keyboard_re_init()

        # 保存到本地数据库
        print("server_trigger_data_update - 保存到本地数据库")
        self.save_local_data(data_save_constant.TRIGGER_TYPE_DATA_SYNC)

    def local_trigger_data_update(self, trigger_type=None, need_upload=True, in_data=None, data_type=None, card_type=None, card_name=None, x=None, y=None):
        """
        本地触发的数据更新
        :param trigger_type: 触发类型
        :param need_upload: 是否需要即时上传
        :param in_data: 传入数据
        :param data_type: 数据类型
        :param card_type: 卡片类型
        :param card_name: 卡片名称
        :param x: 卡片位置横坐标
        :param y: 卡片位置纵坐标
        """
        # 首次启动不做界面修改
        if self.is_first:
            self.info_logger.info("首次启动不做界面修改")
            return
        # 如果数据无触发来源，则打印警告日志
        if trigger_type is None:
            self.info_logger.info("WARN: 数据无触发来源")
            return
        # 如果数据为空，则打印警告日志
        if in_data is None:
            self.info_logger.info("WARN: 无数据")
            return
        # 打印触发日志
        self.info_logger.info(f"触发数据保存，触发来源为：{trigger_type}")

        # 判断需要进行哪些刷新(进行了高级别刷新就不需要进行低级别刷新)
        need_all_restart = False        # 对整体进行重载(3级别)
        need_all_card_restart = False   # 进行卡片整体重载(2级别)
        need_keyboard_restart = False   # 对键盘进行重载(独立)
        need_theme_restart = False      # 对主题进行重载(独立)

        # 单个卡片触发更新
        if trigger_type == data_save_constant.TRIGGER_TYPE_CARD_UPDATE:
            self.info_logger.info(f"准备修改{card_type}卡片:{card_name}的{data_type}数据")
            if data_type == data_save_constant.DATA_TYPE_CACHE:
                if card_type == data_save_constant.CARD_TYPE_NORMAL:
                    for card in self.main_data["card"]:
                        if card["name"] == card_name and card["x"] == x and card["y"] == y:
                            card["data"] = in_data
                            self.info_logger.info(f"成功修改普通卡片:{card_name}缓存数据")
                            break
                elif card_type == data_save_constant.CARD_TYPE_Big:
                    for card in self.main_data["bigCard"]:
                        if card["name"] == card_name:
                            card["data"] = in_data
                            self.info_logger.info(f"成功修改主要卡片:{card_name}缓存数据")
                            break
                else:
                    return
            elif data_type == data_save_constant.DATA_TYPE_ENDURING:
                self.main_data["data"][card_name] = in_data
                self.info_logger.info(f"成功卡片:{card_name}持久数据")
            else:
                return
        # 卡片排列触发更新
        elif trigger_type == data_save_constant.TRIGGER_TYPE_SETTING_PERMUTATION:
            need_all_restart = True     # 这里因为安装了新的卡片，所以需要重启
            self.main_data["card"] = in_data["card"]
            self.main_data["data"]["SettingCard"] = in_data["SettingCard"]
            self.main_data["width"] = in_data["width"]
            self.main_data["height"] = in_data["height"]
        # 屏幕数据更新
        elif trigger_type == data_save_constant.TRIGGER_TYPE_SETTING_SCREEN:
            need_all_restart = True
            self.main_data["data"]["SettingCard"] = in_data
        # 系统设置更新
        elif trigger_type == data_save_constant.TRIGGER_TYPE_SETTING_SYSTEM:
            need_all_restart = True
            # 暂不判断快捷键是否需要更新，直接进行更新
            need_keyboard_restart = True
            self.main_data["data"]["SettingCard"] = in_data
        # 主题更新
        elif trigger_type == data_save_constant.TRIGGER_TYPE_SETTING_THEME:
            need_theme_restart = True
            self.main_data["data"]["SettingCard"] = in_data
        # 数据恢复
        elif trigger_type == data_save_constant.TRIGGER_TYPE_DATA_RECOVER:
            need_all_restart = True
            self.main_data = in_data
        # 数据导入
        elif trigger_type == data_save_constant.TRIGGER_TYPE_DATA_IMPORT:
            need_all_restart = True
            self.main_data = in_data

        # 对整体进行重载
        if need_all_restart:
            # 初始化分辨率参数、位置和大小
            screen_module.init_resolution(self, is_first=False)
            # 重新初始化卡片
            self.restart_card()
            # 设置字体
            style_util.set_font_and_right_click_style(self, self)
        # 进行卡片整体重载
        elif need_all_card_restart:
            # 重新初始化卡片
            self.restart_card()

        # 对键盘进行重载
        if need_keyboard_restart:
            # 重新初始化热键
            self.keyboard_re_init()

        # 对主题进行重载
        if need_theme_restart:
            old_is_dark = self.is_dark
            theme_module.init_theme(self)
            print(f"旧主题:{old_is_dark},新主题:{self.is_dark}")
            if old_is_dark != self.is_dark:
                self.is_dark = old_is_dark
                self.theme_switch_button.click()
            else:
                self.change_theme()
            # 设置主题到QSetting
            settings = QSettings(self.app_name, "Theme")
            settings.setValue("IsDark", self.is_dark)

        # 更新时间戳
        self.main_data["timestamp"] = int(time.time() * 1000)
        # 保存到本地数据库
        self.save_local_data(trigger_type)
        # 保存到云端数据
        self.save_server_data(need_upload)

    def save_local_data(self, trigger_type=None):
        # 本地同步
        try:
            self.database_manager.save_user_data(
                self.current_user["username"],
                json.dumps(self.main_data).encode('utf-8'),
                source='local',
                backup_tag=trigger_type)
            print("保存到本地sqlite数据库成功")
        except Exception as e:
            print(f"保存到本地sqlite数据库失败: {str(e)}")

    def save_server_data(self, need_upload):
        # 云端同步
        try:
            # 非VIP不进行同步
            if not self.is_vip:
                return
            # 如果不需要即时上传的就等待定时同步
            if not need_upload:
                return
            # 其他情况再进行同步
            if self.current_user is not None and self.current_user["username"] is not None:
                self.user_data_client.push_data(self.current_user["username"], self.access_token, self.main_data)
        except Exception as e:
            print(f"保存数据到云端失败: {str(e)}")

    def refresh_card_version(self):
        try:
            screen_module.init_resolution(self, is_first=False)     # 初始化分辨率参数、位置和大小
            self.restart_card()                                     # 重新加载卡片
        except Exception as e:
            print(f"refresh_card_version error: {str(e)}")

    ''' **********************************引导程序*************************************** '''
    def check_first_run(self):
        settings = QSettings(self.app_name, "TutorialProgram")
        # settings.setValue("FirstRun", True)
        if settings.value("FirstRun", True, type=bool):
            print("第一次启动，显示引导程序")
            # 延迟显示引导界面，确保主窗口布局完成
            QApplication.processEvents()
            self.show()
            self.show_tutorial()
            settings.setValue("FirstRun", False)
        else:
            print("非第一次启动，不显示引导程序")

    def show_tutorial(self):
        self.tutorial = TutorialWindow()
        # 添加引导步骤图片（替换为实际路径）
        self.tutorial.add_step(":static/img/tutorial/tutorial_1.png")
        self.tutorial.add_step(":static/img/tutorial/tutorial_2.png")
        self.tutorial.add_step(":static/img/tutorial/tutorial_3.png")
        self.tutorial.start()

    ''' **********************************更新程序*************************************** '''
    def check_update_run(self, tag=None):
        self.app_version = str(version_constant.get_current_version())
        update_module.check_update_on_start(self, tag=tag)

    ''' **********************************更新卡片*************************************** '''
    def check_card_run(self):
        self.card_manager = CardManager(self)
        self.card_manager.check_card_on_start()

    ''' **********************************定时检测*************************************** '''
    def time_task(self):
        print("主进程 - time_task")
        # 获取用户信息和更新部分
        try:
            if self.current_user is None or self.current_user["username"] is None:
                return
            # 获取用户信息(后续进行vip校验、数据同步等操作)
            self.user_info_client.get_user_info(self.current_user["username"], self.access_token)
            # 检查更新
            update_module.check_update_normal(self)
        except Exception:
            self.info_logger.error(traceback.format_exc())
        # 刷新token部分
        try:
            # 当前时间
            datetime_now = datetime.datetime.now()
            # 如果登录界面正在显示，则不进行令牌刷新避免登录界面的闪退
            if self.start_login_view:
                # 但是超过18小时就进行强制刷新
                if self.refresh_token_datetime is None or datetime_now - self.refresh_token_datetime >= datetime.timedelta(hours=18):
                    self.user_info_client.refresh(self.current_user["username"], self.refresh_token, self.hardware_id, self.os_version)
                return
            # 如果支付界面正在显示，则不进行令牌刷新避免闪退
            if self.qr_code_dialog is not None and self.qr_code_dialog.isVisible():
                # 但是超过18小时就进行强制刷新
                if self.refresh_token_datetime is None or datetime_now - self.refresh_token_datetime >= datetime.timedelta(hours=18):
                    self.user_info_client.refresh(self.current_user["username"], self.refresh_token, self.hardware_id, self.os_version)
                return
            # 判断时间，如果时间超过12个小时就更新令牌
            if self.refresh_token_datetime is None or datetime_now - self.refresh_token_datetime >= datetime.timedelta(hours=12):
                self.user_info_client.refresh(self.current_user["username"], self.refresh_token, self.hardware_id, self.os_version)
        except Exception:
            self.info_logger.error(traceback.format_exc())

    def handle_user_detection_result(self, result):
        print("主进程 - handle_user_detection_result")
        # 当前时间戳
        current_time = int(round(time.time() * 1000))
        # 上次时间戳
        last_time = self.last_get_user_info_time
        # 登录失败
        if result['code'] == 1:
            self.info_logger.error(f"获取用户信息失败，原因：{result['msg']}")
            # 相隔x分钟内不进行退出
            if current_time - last_time < self.get_user_info_interval_time:
                return
            # 超过时间直接退出登录
            self.logout(need_dialog=False)
            return
        self.info_logger.info(f"获取用户信息成功")
        # 记录加载时间戳
        self.last_get_user_info_time = current_time
        # 更新信息
        self.current_user = {
            "id": result["data"]["id"],
            "nickName": result["data"]["nickName"],
            "username": result["data"]["username"],
            "accessToken": self.access_token,
            "refreshToken": self.refresh_token,
            "vipStatus": result["data"]["vipStatus"],
            "vipExpireTime": result["data"]['vipExpireTime'],
            "inviteCode": result["data"]["inviteCode"],
        }
        # 判断是否为vip用户
        if not self.current_user['vipStatus']:
            self.is_vip = False
            return
        # vip用户需要做数据同步
        self.is_vip = True
        self.sync_data()
        # 刷新用户信息界面
        self.update_user_view()

    def update_user_view(self):
        user_module.update_user_view(self)

    def handle_refresh_token_result(self, result):
        print("主进程 - handle_refresh_token_result")
        if result['code'] == 1:
            self.info_logger.error(f"刷新令牌失败，原因：{result['msg']}")
            if result["msg"] == "无效刷新令牌" or result["msg"] == "刷新令牌过期" or result["msg"] == "用户不存在":
                # 重新登录
                self.logout(dialog_content="很抱歉，您的登录已过期，请重新登录")
            return
        self.info_logger.info(f"刷新令牌成功")
        print(f"刷新令牌结果:{result}")
        self.access_token = "Bearer " + result["data"]['accessToken']
        self.refresh_token = result["data"]['refreshToken']
        self.refresh_token_datetime = datetime.datetime.now()
        # 更新信息
        self.current_user["accessToken"] = self.access_token
        self.current_user["refreshToken"] = self.refresh_token
        # 更新刷新令牌到本地
        self.database_manager.update_user_refresh_token(self.current_user["username"], self.refresh_token)

    ''' **********************************卡片管理*************************************** '''
    def init_card(self):
        # 主卡片管理
        if self.main_card_manager is None:
            self.update_load_window("正在创建主卡片...")
            self.main_card_manager = MainCardManager(self)
        self.update_load_window("正在初始化主卡片...")
        self.main_card_manager.init(self.main_data["card"])
        # 卡片管理
        if self.normal_card_manager is None:
            self.update_load_window("正在创建小卡片...")
            self.normal_card_manager = NormalCardManager(self.widget_base, self)
        self.update_load_window("正在初始化小卡片...")
        self.normal_card_manager.set_card_map_list(self.main_data["card"], self.main_data["data"],
                                            self.toolkit, self.info_logger, self.local_trigger_data_update)

    def restart_card(self, need_menu_change=True):
        # 停止卡片线程
        self.stop_normal_card_thread_list()
        # 清空卡片
        if self.normal_card_manager is not None:
            self.normal_card_manager.clear_all()
        # 重新初始化卡片管理器
        self.normal_card_manager.set_card_map_list(self.main_data["card"], self.main_data["data"],
                                            self.toolkit, self.info_logger, self.local_trigger_data_update)
        # 主卡片位置调整
        self.main_card_manager.change_geometry(self.main_data["card"])
        # 线程
        self.start_thread_list(only_normal_card=True)
        # 透明窗口和隐藏任务栏图标
        self.refresh_window_show()
        # 主题切换
        user_module.refresh_theme(self)
        init_module.set_theme(self, is_main=True)
        # 是否需要切换卡片到默认的热搜卡片
        if need_menu_change:
            self.main_card_manager.see_card = "trending"
        # 切换卡片
        try:
            self.main_card_manager.show_change()
        except Exception as e:
            self.info_logger.card_error("主程序", "切换菜单失败,错误信息:{}".format(e))

    def set_all_card_data(self):
        pass

    def card_trigger_update(self, card_uuid):
        """卡片触发更新"""
        datetime_now_str = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        for card in self.main_card_list:
            if card.uuid != card_uuid:
                continue
            card.refresh_ui(datetime_now_str)
            break
        if self.normal_card_manager is not None:
            for card in self.normal_card_manager.get_card_list():
                if card.uuid != card_uuid:
                    continue
                card.refresh_ui(datetime_now_str)
                break

    def clear_normal_card_list(self):
        # 清空普通卡片
        try:
            if self.normal_card_manager is None:
                return
            self.normal_card_manager.clear_all()
        except Exception as e:
            self.info_logger.error(traceback.format_exc())

    def clear_main_card_list(self):
        # 清空主卡片
        try:
            if self.main_card_manager is None:
                return
            self.main_card_manager.clear_all()
        except Exception as e:
            self.info_logger.error(traceback.format_exc())

    def notify_card_show_form(self):
        """
        通知卡片窗口显示了
        """
        if self.normal_card_manager is not None:
            self.normal_card_manager.show_form()
        if self.main_card_manager is not None:
            self.main_card_manager.show_form()

    def notify_card_hide_form(self):
        """
        通知卡片窗口隐藏了
        """
        if self.normal_card_manager is not None:
            self.normal_card_manager.hide_form()
        if self.main_card_manager is not None:
            self.main_card_manager.hide_form()
        if hasattr(self, "header_more_menu"):
            self.header_more_menu.hide()

    ''' **********************************键盘监听*************************************** '''
    def keyboard_re_init(self):
        # 移除热键
        self.remove_keyboard_shortcut()
        # 获取热键
        wake_keyboard_key = None
        screenshot_keyboard_key = None
        search_keyboard_key = None
        try:
            # 判断是否设置了键盘快捷键
            if self.main_data is None or self.main_data["data"] is None:
                return
            main_data_data = self.main_data["data"]
            if main_data_data["SettingCard"] is None or main_data_data["SettingCard"][self.hardware_id] is None:
                return
            setting_data = main_data_data["SettingCard"][self.hardware_id]
            # 获取到具体唤醒热键
            if ("wakeUpByKeyboard" in setting_data and "wakeUpByKeyboardType" in setting_data
                    and setting_data["wakeUpByKeyboard"] and setting_data["wakeUpByKeyboardType"] is not None):
                wake_keyboard_key = setting_data["wakeUpByKeyboardType"]
            # 获取到具体截屏热键
            if ("screenshotByKeyboard" in setting_data and "screenshotByKeyboardType" in setting_data
                    and setting_data["screenshotByKeyboard"] and setting_data["screenshotByKeyboardType"] is not None):
                screenshot_keyboard_key = setting_data["screenshotByKeyboardType"]
            # 获取到具体本地搜索热键
            if ("searchByKeyboard" in setting_data and "searchByKeyboardType" in setting_data
                    and setting_data["searchByKeyboard"] and setting_data["searchByKeyboardType"] is not None):
                search_keyboard_key = setting_data["searchByKeyboardType"]
        except Exception:
            self.info_logger.error(traceback.format_exc())
        # 判断是否获取到热键
        if wake_keyboard_key is None and screenshot_keyboard_key is None:
            return
        # 创建热键管理器
        self.hotkey_manager = GlobalHotkeyManager.GlobalHotkeyManager(self)
        # 注册唤醒热键
        if wake_keyboard_key:
            try:
                self.hotkey_manager.register_hotkey(wake_keyboard_key, self.on_wake_hotkey_triggered)
            except Exception as e:
                print(f"热键注册失败: {e}")
        # 注册截屏热键
        if screenshot_keyboard_key:
            try:
                self.hotkey_manager.register_hotkey(screenshot_keyboard_key, self.on_screenshot_hotkey_triggered)
            except Exception as e:
                print(f"热键注册失败: {e}")
        # 注册本地搜索热键
        if search_keyboard_key:
            try:
                self.hotkey_manager.register_hotkey(search_keyboard_key, self.on_search_hotkey_triggered)
            except Exception as e:
                print(f"热键注册失败: {e}")

    def on_wake_hotkey_triggered(self):
        """快捷键进入退出动画"""
        # 如果登录窗口展示则不处理动画
        if self.start_login_view:
            return
        try:
            # 直接使用Qt方法置顶窗口
            self.raise_()
            self.activateWindow()
            self.showNormal()  # 避免使用Win32 API
        except Exception as e:
            self.info_logger.card_error("主程序", "快捷键进入退出动画失败,错误信息:{}".format(e))
        if self.show_form:
            print("快捷键,隐藏窗口")
            self.toolkit.resolution_util.out_animation(self)
        else:
            self.toolkit.resolution_util.in_animation(self)

    def on_search_hotkey_triggered(self):
        """快捷键本地搜索"""
        self.main_card_manager.push_button_search_click()
        if not self.show_form:
            self.toolkit.resolution_util.in_animation(self)

    def on_screenshot_hotkey_triggered(self):
        """快捷键截图"""
        # 未登录的判断
        self.show_login_tip()
        if self.current_user['username'] == "LocalUser":
            return
        # 截屏
        self.start_screenshot()

    def start_screenshot(self):
        self.show_login_tip()
        if self.current_user['username'] == "LocalUser":
            return
        if self.show_overlay_status:
            return
        # 隐藏主窗口
        self.hide()
        # 延迟显示遮罩层
        QTimer.singleShot(600, self._show_screenshot_overlay)
        self.show_overlay_status = True

    def _show_screenshot_overlay(self):
        self.overlay = ScreenshotWidget(self, self)
        self.overlay.show()
        self.overlay.setFocus(Qt.FocusReason.ActiveWindowFocusReason)  # 强制获取焦点

    def start_color_picker(self):
        if self.show_overlay_status:
            return
        # 隐藏主窗口
        self.hide()
        self.toolkit.resolution_util.out_animation(self)
        # 延迟显示遮罩层
        QTimer.singleShot(600, self._show_color_picker_overlay)
        self.show_overlay_status = True

    def _show_color_picker_overlay(self):
        self.color_picker_overlay = ScreenColorPicker(self, self)
        self.color_picker_overlay.show()
        self.color_picker_overlay.setFocus(Qt.FocusReason.ActiveWindowFocusReason)  # 强制获取焦点

    def color_picker_captured(self, color=None):
        """完成进行"""
        self.show_overlay_status = False
        # 显示主窗口
        self.show()
        # 隐藏遮罩层
        try:
            if hasattr(self, "color_picker_overlay"):
                self.color_picker_overlay.hide()
                self.color_picker_overlay.close()
        except Exception:
            pass
        # 显示颜色转换器
        if hasattr(self, "color_converter_dialog"):
            try:
                self.color_converter_dialog.close()
                self.color_converter_dialog = None
            except Exception:
                pass
        self.color_converter_dialog = color_converter_util.show_color_converter_dialog(self, "颜色转换器", initial_color=color)

    def cancel_color_picker(self):
        """取消屏幕取色"""
        self.show_overlay_status = False
        self.show()

    def screenshot_captured_to_translate(self, pixmap):
        """截图完成进行翻译"""
        self.show_overlay_status = False
        # 显示主窗口
        self.show()
        self.toolkit.resolution_util.in_animation(self)
        # 进行翻译
        self.main_card_manager.on_translate(pixmap)

    def screenshot_captured_to_ocr(self, pixmap):
        """截图完成进行识别"""
        self.show_overlay_status = False
        # 显示主窗口
        self.show()
        # 进行翻译
        self.main_card_manager.on_ocr(pixmap)

    def cancel_screenshot(self):
        """取消截图"""
        self.show_overlay_status = False
        self.show()

    def start_image_to_excel_converter(self):
        # 显示图片转excel转换器
        if hasattr(self, "image_to_excel_converter_dialog"):
            try:
                self.image_to_excel_converter_dialog.close()
                self.image_to_excel_converter_dialog = None
            except Exception:
                pass
        self.image_to_excel_converter_dialog = image_to_excel_converter_util.show_image_to_excel_converter_dialog(self, "图片批量转Excel")

    def start_single_image_to_excel_converter(self, pixmap):
        # 显示图片转excel转换器
        if hasattr(self, "single_image_to_excel_converter_dialog"):
            try:
                self.single_image_to_excel_converter_dialog.close()
                self.single_image_to_excel_converter_dialog = None
            except Exception:
                pass
        self.single_image_to_excel_converter_dialog = (
            single_image_to_excel_converter_util.show_single_image_to_excel_converter_dialog(self, "图片转Excel", pixmap=pixmap))

    def start_image_show(self, pixmap: QPixmap):
        # 显示图片
        if hasattr(self, "image_show_dialog"):
            try:
                self.image_show_dialog.close()
                self.image_show_dialog = None
            except Exception:
                pass
        if pixmap is None:
            return
        self.image_show_dialog = self.toolkit.image_box_util.show_image_dialog(self, "图片查看器", pixmap=pixmap)

    def start_top_image_show(self, pixmap: QPixmap):
        # 显示图片
        if hasattr(self, "top_image_show_dialog"):
            try:
                self.top_image_show_dialog.close()
                self.top_image_show_dialog = None
            except Exception:
                pass
        if pixmap is None:
            return
        self.top_image_show_dialog = TopImageAcrylicWindow.show_top_image_dialog(self, pixmap=pixmap)


    ''' **********************************其他*************************************** '''
    def nativeEvent(self, eventType, message):
        """处理 Windows 原生事件"""
        # 修复：正确处理 VoidPtr 类型
        msg = MSG.from_address(int(message))

        if msg.message == GlobalHotkeyManager.WM_HOTKEY:
            # 提取热键ID
            hotkey_id = msg.wParam
            self.hotkey_manager.handle_hotkey(hotkey_id)
            return True, 0  # 表示已处理此消息
        # 其他事件传递给基类处理
        return super().nativeEvent(eventType, message)

    def remove_keyboard_shortcut(self):
        try:
            if self.hotkey_manager is not None:
                self.hotkey_manager.unregister_all()
                del self.hotkey_manager
            self.hotkey_manager = None
        except Exception as e:
            self.info_logger.error(traceback.format_exc())


    ''' **********************************其他*************************************** '''

    def show_hide_form(self, click_button):
        """显示或隐藏窗口"""
        # 右键不处理动画
        if click_button is not None and click_button == QSystemTrayIcon.ActivationReason.Context:
            return
        # 如果登录窗口展示则不处理动画
        if self.start_login_view:
            return
        # 当前时间戳
        current_time = int(round(time.time() * 1000))
        # 上次时间戳
        last_time = self.animation_time
        # 相隔0.35秒内不进行动画
        if current_time - last_time < self.form_animation_time:
            return
        if self.is_show:
            screen_module.trigger_hide_animation(self)
        else:
            screen_module.trigger_show_animation(self)

    def refresh_window_show(self):
        try:
            # 直接使用Qt方法置顶窗口
            self.raise_()
            self.activateWindow()
            self.showNormal()  # 避免使用Win32 API
        except Exception as e:
            self.info_logger.error(f"Win32API错误: {e}")
        # 窗口置顶
        self.setWindowFlag(Qt.WindowType.ToolTip)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

    def stop_normal_card_thread_list(self):
        """结束普通卡片线程列表"""
        for card_thread_object in self.normal_card_thread_object_list:
            card_thread_object.stop()
        self.normal_card_thread_object_list = []

    def start_thread_list(self, only_normal_card=False):
        """开始线程列表"""
        self.info_logger.info("开始线程初始化")
        # 初始化普通卡片线程列表
        for card_thread_object in self.normal_card_thread_object_list:
            if card_thread_object is None:
                continue
            card_thread_object.stop()
        self.normal_card_thread_object_list = []
        if self.normal_card_manager is not None:
            for card in self.normal_card_manager.get_card_list():
                card_thread_object = card_thread.CardThread(self, card)
                self.normal_card_thread_object_list.append(card_thread_object)
                card_thread_object.refresh_trigger.connect(self.card_trigger_update)
                card_thread_object.start()
        if only_normal_card:
            return
        # 初始化主卡片线程列表
        for card_thread_object in self.main_card_thread_object_list:
            if card_thread_object is None:
                continue
            card_thread_object.stop()
        self.main_card_thread_object_list = []
        for card in self.main_card_list:
            card_thread_object = card_thread.CardThread(self, card)
            self.main_card_thread_object_list.append(card_thread_object)
            card_thread_object.refresh_trigger.connect(self.card_trigger_update)
            card_thread_object.start()
        # 主线程
        self.main_thread_object = main_thread.MainThread()
        self.main_card_thread_object_list.append(self.main_thread_object)
        self.main_thread_object.time_task_trigger.connect(self.time_task)
        self.main_thread_object.start()

    def stop_thread_list(self):
        """结束线程列表"""
        try:
            card_thread_object_list = self.normal_card_thread_object_list + self.main_card_thread_object_list
            for i, card_thread_object in enumerate(card_thread_object_list):
                # print(f"正在停止线程{i}: {card_thread_object.objectName()}")
                card_thread_object.stop()
            self.normal_card_thread_object_list = []
            self.main_card_thread_object_list = []
            # 卸载快捷键
            self.remove_keyboard_shortcut()
            # 取消主线程
            if self.main_thread_object:
                self.main_thread_object.stop()
        except Exception as e:
            self.info_logger.error(traceback.format_exc())

    def change_theme(self):
        # 修改主题
        self.show_load_window("切换主题中...")
        print(f"修改主题,当前主题:{self.is_dark}")
        if self.main_card_manager is not None:
            self.main_card_manager.set_theme()
        if self.normal_card_manager is not None:
            self.normal_card_manager.set_theme()
        user_module.refresh_theme(self)
        icon_tool.set_icon(self)
        icon_tool.set_tray_icon(self)
        self.update()
        self.hide_load_window()

    def open_update_view(self):
        """更新记录"""
        text_box_util.show_text_dialog(self, "版本信息", {
            "content": version_constant.get_update_info(),
            "size": [450, 500],
            "longText": True,
            "markdown": True
        })

    def send_message(self, title="", descript="", url=None):
        """
        发送右下角弹框提醒
        :param title: 消息标题
        :param descript: 消息内容
        :param url: 点击跳转的地址
        """
        icon = QPixmap(self.sys_icon_pixmap)
        if len(title) > 20:
            title = title[:20] + "..."
        if len(descript) > 100:
            descript = descript[:100] + "..."
        self.info_logger.info(f"发送提醒: {title}")
        self.tray_icon.showMessage(
            f"【{self.app_title}】{title}",
            descript,
            icon,
            3500  # 显示时长（毫秒）
        )

    def quit_before(self, is_hide_dialog=False):
        """退出前置处理"""
        if self.app_title is None:
            self.quit_before_do()
            self.run_exit_helper()
            QApplication.instance().quit()
            exit()
        if is_hide_dialog:
            # 如果不显示对话框，则直接退出
            self.quit_before_do()
            self.run_exit_helper()
            QApplication.instance().quit()
            exit()
        else:
            # 显示对话框来确认
            confirm = self.toolkit.message_box_util.box_acknowledgement(self, "退出", f"确定要退出{self.app_title}吗？",
                                                                        dialog_map=self.dialog_map, dialog_key="quit")
            if confirm:
                self.quit_before_do()
                self.run_exit_helper()
                QApplication.instance().quit()
                exit()

    def run_exit_helper(self):
        QTimer.singleShot(1000, self.run_exit_helper_one)
        QTimer.singleShot(2000, self.run_exit_helper_one)
        QTimer.singleShot(3000, self.run_exit_helper_one)

    def run_exit_helper_one(self):
        while True:
            QApplication.instance().quit()

    def quit_before_do(self):
        """退出前置处理"""
        # 打印信息
        if self.info_logger is not None:
            self.info_logger.info("开始退出处理程序")
        # 清理线程
        self.stop_thread_list()
        # 隐藏窗口
        self.setVisible(False)
        # 如果登录窗口存在则隐藏登录窗口并关闭
        try:
            if self.start_login_view:
                self.user_server_recover_win.hide()
                self.user_server_recover_win.close()
        except Exception as e:
            print(e)
        # 关闭托盘
        if self.tray_icon is not None:
            self.tray_icon.hide()
        # 清理卡片
        self.clear_normal_card_list()
        self.clear_main_card_list()
        # 卸载快捷键
        self.remove_keyboard_shortcut()
        # 打印信息
        if self.info_logger is not None:
            self.info_logger.info("完成退出处理程序")

    def event(self, event):
        """ 处理窗口失焦事件 """
        if type(event) == QNetworkReply:
            return super().event(event)
        if QEvent.Type.WindowDeactivate == event.type():
            # 如果窗口显示且鼠标不在边缘区域，才隐藏
            if self.show_form:
                cursor_pos = QtGui.QCursor.pos()
                x = cursor_pos.x()
                if x < self.desktop_width - 5:  # 5px边缘阈值
                    screen_module.trigger_hide_animation(self)
        if QEvent.Type.WindowDeactivate == event.type() or QEvent.Type.ActivationChange == event.type():
            if not self.show_form:
                return super().event(event)
            if QApplication.activeWindow() == self or QApplication.activeWindow() is not None:
                return super().event(event)
            self.toolkit.resolution_util.out_animation(self)
        return super().event(event)

    def enterEvent(self, event):
        """ 鼠标进入窗口时取消隐藏定时 """
        super(AgileTilesForm, self).enterEvent(event)
        if self.hide_timer is not None:
            self.hide_timer.stop()

    def leaveEvent(self, event):
        """ 鼠标离开窗口时启动延迟检测 """
        super(AgileTilesForm, self).leaveEvent(event)
        if self.show_form and self.hide_timer is not None:
            self.hide_timer.start(100)

    def closeEvent(self, event):
        """
        最终退出
        :param event: QCloseEvent
        :return:
        """
        if event.type() == QEvent.Type.Close:
            event.ignore()
        else:
            event.accept()


if __name__ == '__main__':
    # 设置工作目录为应用安装目录来修复开机自启动无法加载图片的问题(sys.frozen用来判断pyinstaller，__compiled__用来判断nuitka)
    if getattr(sys, 'frozen', False) or '__compiled__' in globals():
        os.chdir(os.path.dirname(sys.executable))
    # 跟踪100个最近内存分配
    tracemalloc.start(100)
    # 开启DPI适应
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    # 禁用系统代理(不会被Fiddler抓到)
    # QNetworkProxyFactory.setUseSystemConfiguration(False)
    # 禁用系统代理(不走vpn)
    # QNetworkProxy.setApplicationProxy(QNetworkProxy.NoProxy)
    # 启用插件调试
    # os.environ['QT_DEBUG_PLUGINS'] = '1'
    # 将警告转为崩溃
    # os.environ['QT_FATAL_WARNINGS'] = '1'
    # 其他配置
    # os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = (
    #     "--disable-ipv6"            # 禁用IPv6
    #     #" --log-level=3"            # 设置日志级别为警告及以上
    #     " --no-sandbox"             # 禁用沙箱模式（在部分系统环境下需要）
    #     # " --enable-logging --v=1"   # 启用Chromium日志
    # )
    # 检查是否已有实例运行
    if is_another_instance_running():
        print("程序已在运行中，新实例将退出")
        # 可选：激活已运行的实例窗口
        try:
            socket = QLocalSocket()
            socket.connectToServer("AgileTiles")
            if socket.waitForConnected(500):
                socket.write(b"activate")
                socket.flush()
                socket.waitForBytesWritten(1000)
                socket.close()
        except:
            pass
        sys.exit(0)
    # 程序退出时清理共享内存
    def cleanup_shared_memory():
        shared_memory = QSharedMemory("AgileTiles")
        if shared_memory.isAttached():
            shared_memory.detach()
    # 限制单机挂载数量一个
    try:
        app = QApplication(sys.argv)
        # 异常处理
        sys.excepthook = handleException
        # 创建本地服务器用于实例间通信（可选）
        localServer = QLocalServer()
        localServer.listen("AgileTiles")
        # 原始启动逻辑
        my_form = AgileTilesForm()
        my_form.show()
        # 注册清理函数
        atexit.register(cleanup_shared_memory)
        sys.exit(app.exec())
    except Exception as e:
        print("程序启动异常：{}".format(e))
        # 打印错误详细信息
        traceback.print_exc()
        atexit.register(cleanup_shared_memory)
    atexit.register(cleanup_shared_memory)
    sys.exit(0)
