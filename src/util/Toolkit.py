from PySide6.QtCore import QObject

from src.network_manager.FileUploadDownloadManager.FileUploadDownloadManager import FileUploadDownloadManager
from src.network_manager.HolidayManager.HolidayManager import HolidayManager
from src.network_manager.PermissionRequestManager.PermissionRequestManager import PermissionRequestManager
from src.network_manager.WeatherManager.WeatherManager import WeatherManager
from src.network_manager.TextContentManager.TextContentManager import TextContentManager
from src.util import file_util, browser_util, time_util, version_util
from src.ui import style_util, animation_util, image_util
from src.module.Screen import screen_module
import src.ui.my_color as my_color
from src.module.Box import image_box_util, text_box_util, message_box_util
from src.module import dialog_module
from src.module.Pay import qr_code_box_util
import psutil, calendar, webbrowser, lunardate
from lxml import html


class Toolkit(QObject):
    resolution_util = screen_module
    browser_util = browser_util
    version_util = version_util
    time_util = time_util
    file_util = file_util
    animation_util = animation_util
    image_util = image_util
    style_util = style_util
    color = my_color
    # 下面主要是弹窗工具
    message_box_util = message_box_util
    dialog_module = dialog_module
    image_box_util = image_box_util
    qr_code_box_util = qr_code_box_util
    text_box_util = text_box_util
    # 下面主要是为了第三方卡片使用
    psutil = psutil
    calendar = calendar
    webbrowser = webbrowser
    lunardate = lunardate
    html = html

    def __init__(self, parent=None, use_parent=None):
        super().__init__(parent)
        self.use_parent = use_parent

    def get_permission_manager(self):
        # 权限请求类，暂时只用于权限请求
        return PermissionRequestManager(parent=self, use_parent=self.use_parent)

    def get_file_upload_download_manager(self):
        # 文件下载类，暂时只用于图片卡片下载图片
        return FileUploadDownloadManager(parent=self, use_parent=self.use_parent)

    def get_holiday_manager(self):
        # 节假日获取类，暂时只用于节假日获取
        return HolidayManager(parent=self, use_parent=self.use_parent)

    def get_weather_manager(self):
        # 天气获取类，暂时只用于天气预报获取
        return WeatherManager(parent=self, use_parent=self.use_parent)

    def get_text_content_manager(self):
        # 文字信息获取类，暂时只用于文字信息获取
        return TextContentManager(parent=self, use_parent=self.use_parent)
