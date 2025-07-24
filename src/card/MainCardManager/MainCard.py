import uuid
import datetime

from PySide6.QtCore import QObject
from PySide6.QtGui import QIcon, QPixmap

from src.constant import card_constant
from src.ui import my_color
from src.util import time_util


class MainCard(QObject):

    title = "MainCard"
    name = "MainCard"
    category = "其他"
    support_size_list = []
    # 只读参数
    parent = None           # 父级
    x = None                # 坐标x
    y = None                # 坐标y
    size = None             # 大小(1_1:Point、1_2:MiniHor、2_1MiniVer、2_2Block、2_5)
    before_theme = None
    theme = None            # 主题(Light、Dark)
    left = 0                # 左边距离
    top = 0                 # 上边距离
    width = 0               # 宽度
    height = 0              # 高度
    card_width = 0
    card_height = 0
    fillet_corner = 0       # 圆角大小
    # 可使用
    card = None             # 卡片本体
    data = None             # 数据
    toolkit = None          # 工具箱，具体参考文档
    logger = None           # 日志记录工具
    # 可调用
    save_data_func = None   # 保存数据(传参为一个字典)
    uuid = None
    # 标题
    card_title_label = None
    # 卡片基础
    CARD_WIDTH = card_constant.CARD_WIDTH           # 卡片宽度
    CARD_HEIGHT = card_constant.CARD_HEIGHT         # 卡片高度
    CARD_INTERVAL = card_constant.CARD_INTERVAL     # 卡片间距

    def __init__(self, main_object=None, parent=None, theme=None, card=None, cache=None,
                 data=None, toolkit=None, logger=None, plugin_dir=None, save_data_func=None):
        super().__init__(parent)
        self.main_object = main_object
        self.hardware_id = main_object.hardware_id
        self.parent = parent
        self.theme = theme
        self.card = card
        self.cache = cache
        self.data = data
        self.toolkit = toolkit
        self.logger = logger
        self.plugin_dir = plugin_dir
        self.save_data_func = save_data_func
        self.uuid = str(uuid.uuid4())
        print(f"新增卡片，uuid:{self.uuid}")

    def __del__(self):
        self.clear()

    def init_ui(self):
        """
        初始化，只进行UI的初始化，不进行数据加载
        :return:
        """
        self.logger.card_debug(self.title, "开始初始化")

    def refresh_data(self, date_time_str):
        """
        刷新数据，在刷新完数据后再进行UI刷新
        :param date_time_str:
        :return:
        """
        self.logger.card_debug(self.title, "开始刷新数据")

    def refresh_ui(self, date_time_str):
        self.logger.card_debug(self.title, "开始刷新UI")

    def refresh_ui_end(self, date_time_str):
        self.logger.card_debug(self.title, "结束刷新UI")
        self.refresh_theme()

    def update_cache(self, cache=None):
        """
        更新缓存数据事件
        """
        pass

    def update_data(self, data=None):
        """
        更新持久数据事件
        """
        pass

    def update_all(self, cache=None, data=None):
        """
        更新缓存+持久数据事件
        """
        pass

    def enter_event(self):
        """
        鼠标移入事件
        """
        pass

    def leave_event(self):
        """
        鼠标移出事件
        """
        pass

    def show_form(self):
        """
        隐藏窗口
        """
        pass

    def hide_form(self):
        """
        隐藏窗口
        """
        pass

    def set_theme(self, is_dark=True):
        """
        修改主题
        """
        try:
            self.theme = "Dark" if is_dark else "Light"
            self.refresh_theme()
        except Exception as e:
            print(f"Card set_theme error: {str(e)}")

    def refresh_theme(self):
        """
        刷新主题
        """
        if self.before_theme is not None and self.before_theme == self.theme:
            # 重复不刷新
            return False
        try:
            print(f"{time_util.get_datetime_str(datetime.datetime.now())} - {self.name}卡片:{self.uuid}刷新主题")
            if self.card_title_label is not None:
                label_color = "rgba(255, 255, 255, 150)" if self.is_dark() else "rgba(0, 0, 0, 150)"
                self.card_title_label.setStyleSheet("QLabel{ color: " + label_color + "; border: 0px solid black; background:transparent; }")
        except Exception as e:
            print(f"Card refresh_theme error: {str(e)}")
        self.before_theme = self.theme
        return True

    def is_light(self):
        if self.theme == "Light":
            return True
        else:
            return False

    def is_dark(self):
        if self.theme == "Light":
            return False
        else:
            return True

    def get_park_path(self, icon_position):
        icon_theme_folder = "light" if self.is_dark() else "dark"
        return "./static/img/IconPark/" + icon_theme_folder + "/" + icon_position + ".png"

    def get_icon_park_path(self, icon_position):
        icon_theme_folder = "light" if self.is_dark() else "dark"
        return QIcon("./static/img/IconPark/" + icon_theme_folder + "/" + icon_position + ".png")

    def get_pixmap_park_path(self, icon_position):
        icon_theme_folder = "light" if self.is_dark() else "dark"
        return QPixmap("./static/img/IconPark/" + icon_theme_folder + "/" + icon_position + ".png")

    def get_prospect_color(self, rgb=False, rgba=False, hex=False, hexa=False, qt_type=False):
        return my_color.get_prospect_color(self.is_dark(), rgb, rgba, hex, hexa, qt_type)

    def get_background_color(self, rgb=False, rgba=False, hex=False, hexa=False, qt_type=False):
        return my_color.get_background_color(self.is_dark(), rgb, rgba, hex, hexa, qt_type)

    # 需要清理掉的时候
    def clear(self):
        # 添加通用对象清理
        if hasattr(self, 'timer') and self.timer:
            self.timer.stop()
            self.timer.deleteLater()
        self.theme = None
        self.size = None
        self.width = None
        self.height = None
        self.fillet_corner = None
        self.data = None
        self.save_data_func = None
        if self.logger is not None and self.uuid is not None:
            self.logger.card_debug(self.title, "uuid:" + self.uuid + "被删除")
        self.uuid = None
        # 最后删除自己
        try:
            self.deleteLater()
        except Exception as e:
            print(e)
