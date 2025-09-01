import os, sys
import traceback
import uuid
import copy
import importlib.util

from PySide6 import QtGui, QtCore
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QLabel

from src.component.AgileTilesAcrylicWindow.AgileTilesAcrylicWindow import AgileTilesAcrylicWindow
from src.card.NormalCardManager.UiSetting import UiSetting
from src.constant import card_constant, data_save_constant


class NormalCard(QObject):

    title = "NormalCard"
    name = "NormalCard"
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
    # 外部卡片
    card_plugin = None

    def __init__(self, main_object=None, parent=None, card_name=None, theme='Light', x=None, y=None, size=None, fillet_corner=0, card=None, cache=None,
                 data=None, toolkit=None, logger=None, plugin_dir=None, save_data_func=None):
        super().__init__(parent)
        self.main_object = main_object
        self.parent = parent
        self.name = card_name
        self.theme = theme
        self.size = size
        self.x = x if x is not None else 1
        self.y = y if y is not None else 1
        self.fillet_corner = fillet_corner
        self.card = card
        self.cache = cache
        self.data = data
        self.toolkit = toolkit
        self.logger = logger
        self.plugin_dir = plugin_dir
        self.save_data_func = save_data_func
        # 卡片大小和位置调整
        self.card_width = int(self.size.split("_")[0])
        self.card_height = int(self.size.split("_")[1])
        self.width = self.card_width * self.CARD_WIDTH + (self.card_width - 1) * self.CARD_INTERVAL
        self.height = self.card_height * self.CARD_HEIGHT + (self.card_height - 1) * self.CARD_INTERVAL
        self.left = self.x * self.CARD_INTERVAL + (self.x - 1) * self.CARD_WIDTH
        self.top = self.y * self.CARD_INTERVAL + (self.y - 1) * self.CARD_HEIGHT
        self.card.setGeometry(self.left, self.top, self.width, self.height)
        # 唯一标识
        self.uuid = str(uuid.uuid4())
        # print(f"self.size:{self.size}")
        # 加载卡片设置对象
        self.card_ui_setting = UiSetting(self)
        # 加载卡片逻辑插件
        self.load_card_plugin()
        print(f"新增卡片，uuid:{self.uuid}")


    def load_card_plugin(self):
        try:
            filename = self.name + ".pyd"
            # 动态加载模块
            module_path = os.path.join(self.plugin_dir, filename)
            spec = importlib.util.spec_from_file_location(
                self.name, module_path
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            print(f'插件卡片:{module.PluginCard.title}')
            in_card_cache = copy.deepcopy(self.cache)
            in_card_data = copy.deepcopy(self.data)
            self.card_plugin = module.PluginCard(card_object=self.card, ui_setting=self.card_ui_setting,
                                                 card_cache=in_card_cache, card_data=in_card_data,
                                                 save_func=self.save_card_data_func,
                                                 toolkit=self.toolkit, logger=self.logger)
            # 对于需要引用的特殊类
            # if hasattr(self.card_plugin, 'AgileTilesFramelessWebEngineView'):
            #     self.card_plugin.AgileTilesFramelessWebEngineView = AgileTilesFramelessWebEngineView
            if hasattr(self.card_plugin, 'AgileTilesAcrylicWindow'):
                self.card_plugin.AgileTilesAcrylicWindow = AgileTilesAcrylicWindow
        except Exception as e:
            traceback.print_exc()
            print(f'load_card_plugin error:{e}')

    def __del__(self):
        try:
            self.clear()
        except Exception as e:
            print(f'__del__ error:{e}')

    def init_ui(self):
        """
        初始化，只进行UI的初始化，不进行数据加载
        :return:
        """
        self.logger.card_debug(self.title, "开始初始化")
        if self.card_plugin is not None:
            # 初始化卡片标题
            print(f"{self.name}卡片的title_show:{self.card_ui_setting.get_card_title_show()}")
            if self.card_ui_setting.get_card_title_show():
                font = QtGui.QFont()
                font.setPointSize(10)
                self.card_title_label = QLabel(self.card)
                self.card_title_label.setText(self.card_plugin.title)
                self.card_title_label.setFont(font)
                self.card_title_label.setStyleSheet("QLabel{ color: rgba(0, 0, 0, 150); border: 0px solid black; background:transparent; }")
                self.card_title_label.setGeometry(QtCore.QRect(10, 5, self.card.width(), 20))
            # 初始化卡片UI
            try:
                self.card_plugin.init_ui()
            except Exception as e:
                print(f'init_ui error:{e}')

    def save_card_data_func(self, need_upload=True, data=None, data_type=data_save_constant.DATA_TYPE_CACHE):
        self.save_data_func(trigger_type=data_save_constant.TRIGGER_TYPE_CARD_UPDATE,
                            need_upload=need_upload,
                            in_data=data,
                            data_type=data_type,
                            card_type=data_save_constant.CARD_TYPE_NORMAL,
                            card_name=self.name,
                            x=self.x,
                            y=self.y)

    def refresh_data(self, date_time_str):
        """
        刷新数据，在刷新完数据后再进行UI刷新
        :param date_time_str:
        :return:
        """
        self.logger.card_debug(self.title, "开始刷新数据")
        if self.card_plugin is not None and hasattr(self.card_plugin, 'refresh_data'):
            try:
                self.card_plugin.refresh_data(date_time_str)
            except Exception as e:
                print(f'普通卡片刷新错误:{e}')
                traceback.print_exc()

    def refresh_ui(self, date_time_str):
        """
        刷洗UI，在刷新数据后进行
        """
        self.logger.card_debug(self.title, "开始刷新UI")
        if self.card_plugin is not None and hasattr(self.card_plugin, 'refresh_ui'):
            try:
                self.card_plugin.refresh_ui(date_time_str)
            except Exception as e:
                print(f'refresh_ui error:{e}')
        self.refresh_ui_end(date_time_str)
        self.refresh_theme()

    def refresh_ui_end(self, date_time_str):
        """
        刷洗UI结束，在刷新UI后进行(如果进行了刷新的话)
        """
        self.logger.card_debug(self.title, "结束刷新UI")

    def update_cache(self, cache=None):
        """
        更新缓存数据事件
        """
        self.card_plugin.update_cache(card_cache=cache)

    def update_data(self, data=None):
        """
        更新持久数据事件
        """
        self.card_plugin.update_data(card_data=data)

    def update_all(self, cache=None, data=None):
        """
        更新缓存+持久数据事件
        """
        self.card_plugin.update_all(card_cache=cache, card_data=data)

    def enter_event(self):
        """
        鼠标移入事件
        """
        if self.card_plugin is not None and hasattr(self.card_plugin, 'enter_event'):
            self.card_plugin.enter_event()

    def leave_event(self):
        """
        鼠标移出事件
        """
        if self.card_plugin is not None and hasattr(self.card_plugin, 'leave_event'):
            self.card_plugin.leave_event()

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
        self.before_theme = self.theme
        self.card_ui_setting.card_theme = self.theme
        try:
            if self.card_title_label is not None:
                label_color = "rgba(255, 255, 255, 150)" if self.card_ui_setting.is_dark() else "rgba(0, 0, 0, 150)"
                self.card_title_label.setStyleSheet("QLabel{ color: " + label_color + "; border: 0px solid black; background:transparent; }")
        except Exception as e:
            print(f"Card refresh_theme error: {str(e)}")
        if self.card_plugin is not None and hasattr(self.card_plugin, 'refresh_theme'):
            try:
                print(f"{self.name}卡片:{self.uuid}刷新主题")
                self.card_plugin.refresh_theme()
            except Exception as e:
                print(f'refresh_theme error:{e}')
        return True

    # 需要清理掉的时候
    def clear(self):
        # 模块内容释放逻辑
        try:
            if self.card_plugin is not None and hasattr(self.card_plugin, 'clear'):
                # 时间清理
                try:
                    if getattr(self.card_plugin, 'timer') and self.card_plugin.timer:
                        self.card_plugin.timer.stop()
                        self.card_plugin.timer.deleteLater()
                except Exception as e:
                    print(f"Card clear error: {str(e)}")
                # 隐藏
                try:
                    self.card_plugin.hide()
                    self.card_plugin.setVisible(False)
                except Exception as e:
                    print(f"Card clear error: {str(e)}")
                # 释放插件对象
                try:
                    self.card_plugin.clear()
                except Exception as e:
                    print(f"Card clear error: {str(e)}")
                # 释放插件对象
                try:
                    self.card_plugin.deleteLater()
                except Exception as e:
                    print(f"Card clear error: {str(e)}")
        except Exception as e:
            print(f"释放模块资源失败: {str(e)}")
        # 新增模块释放逻辑
        try:
            # 1. 删除插件实例
            del self.card_plugin
            self.card_plugin = None
            # 2. 从sys.modules中移除模块
            if self.name in sys.modules:
                print(f"从sys.modules中移除模块: {self.name}")
                del sys.modules[self.name]
        except Exception as e:
            print(f"释放模块资源失败: {str(e)}")
        # 其他删除
        self.theme = None
        self.size = None
        self.width = None
        self.height = None
        self.fillet_corner = None
        self.data = None
        self.save_data_func = None
        try:
            if self.logger is not None and self.uuid is not None:
                self.logger.card_debug(self.title, "uuid:" + self.uuid + "被删除")
        except Exception as e:
            print(f"Card clear error: {str(e)}")
        self.uuid = None
        # 最后删除自己
        self.deleteLater()
        print("Card卡片被清理")
