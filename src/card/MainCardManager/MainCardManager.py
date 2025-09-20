import copy
from functools import partial

from PySide6 import QtGui, QtCore
from PySide6.QtCore import QObject, Qt, QSize, QRect, QTimer
from PySide6.QtGui import QIcon, QFont, QCursor, QAction
from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QScrollArea, QFrame, QMenu, \
    QToolButton

from src.card.component.ThemeSwitchButton.ThemeSwitchButton import ThemeSwitchButton
from src.card.main_card.FileSearchCard.FileSearchCard import FileSearchCard
from src.card.main_card.IpnCard.IpnCard import IpnCard
from src.card.main_card.SettingCard.setting.card_permutation import CardPermutationWindow
from src.card.main_card.ToolCard.ToolCard import ToolCard
from src.card.main_card.TodoCard.TodoCard import TodoCard
from src.card.main_card.BookCard.BookCard import BookCard
from src.card.main_card.ChatCard.ChatCard import ChatCard
from src.card.main_card.GameCard.GameCard import GameCard
from src.card.main_card.MusicCard.MusicCard import MusicCard
from src.card.main_card.SettingCard.SettingCard import SettingCard
from src.card.main_card.TopSearchCard.TopSearchCard import TopSearchCard
from src.card.main_card.TranslateCard.TranslateCard import TranslateCard
from src.card.main_card.InformationCard.InformationCard import InformationCard
from src.client import common
from src.constant import card_constant, data_save_constant
from src.module.Theme import theme_module
from src.module.UserData.DataBase import user_data_common
from src.module.About.about_us import AboutUsWindow
from src.util import browser_util
from src.ui import style_util


def get_position(control):
    # 获取按钮相对于窗口的坐标
    window = control.window()
    return control.mapTo(window, QtCore.QPoint(0, 0))


class MainCardManager(QObject):

    main_object = None
    see_card = "trending"  # 下方卡片中当前查看的是哪个卡片，默认是trending
    menu_button_map = None
    area_list = []
    # 卡片宽度和卡片高度
    HEADER_HEIGHT = card_constant.HEADER_HEIGHT             # 顶部实际高度
    HEADER_VIEW_HEIGHT = card_constant.HEADER_VIEW_HEIGHT   # 顶部显示高度
    CARD_WIDTH = card_constant.CARD_WIDTH                   # 卡片宽度
    CARD_HEIGHT = card_constant.CARD_HEIGHT                 # 卡片高度
    CARD_INTERVAL = card_constant.CARD_INTERVAL             # 卡片间距
    # 主卡片位置
    main_card_x = 1
    main_card_y = 1
    main_card_width = 6
    main_card_height = 8
    # 菜单
    menu_button_width = 34

    def __init__(self, main_object):
        super(MainCardManager, self).__init__()
        self.main_object = main_object

    def clear_all(self):
        """
        清空
        :return:
        """
        print("类MainCardManager开始:__del__函数")
        try:
            # 隐藏顶部
            self.main_object.widget_header.hide()
            # 隐藏菜单
            self.main_object.label_menu.hide()
            self.main_object.label_current_menu.hide()
            self.main_object.label_menu_background.hide()
            self.main_object.theme_switch_button.hide()
            # 删除窗口
            if self.main_object.card_permutation_win is not None:
                self.main_object.card_permutation_win.deleteLater()
            # 清理卡片
            for card in self.main_object.main_card_list:
                card.clear()
            self.main_object.main_card_list = []
            # 隐藏区域
            area_list = [
                self.main_object.user_area,
                self.main_object.setting_area,
                self.main_object.top_area,
                self.main_object.translate_area,
                self.main_object.chat_area,
                self.main_object.search_area,
                self.main_object.ipn_area,
                self.main_object.todo_area,
                self.main_object.book_area,
                self.main_object.music_area,
                self.main_object.looking_area,
                self.main_object.tool_area,
                self.main_object.game_area,
            ]
            for card_area in area_list:
                # 清理内容
                self.clear_scroll_area_1(card_area)
                self.clear_scroll_area_2(card_area)
                # 隐藏
                card_area.hide()
        except Exception as e:
            print(e)
        print("类MainCardManager结束:__del__函数")

    def clear_scroll_area_1(self, scroll_area):
        content = scroll_area.widget()
        if content is None:
            return

        # 删除所有子控件
        for child in content.findChildren(QWidget):
            child.deleteLater()

        # 删除布局（如果存在）
        if content.layout():
            # 清空布局内容
            while content.layout().count():
                item = content.layout().takeAt(0)
                if widget := item.widget():
                    widget.deleteLater()
            # 删除布局本身
            content.layout().deleteLater()

    def clear_scroll_area_2(self, scroll_area):
        # 获取当前内容部件
        old_widget = scroll_area.takeWidget()
        if old_widget is not None:
            # 异步删除旧部件及其所有子控件
            old_widget.deleteLater()
        # 创建新的空内容部件
        new_widget = QWidget()
        scroll_area.setWidget(new_widget)
        # 启用自动调整大小
        scroll_area.setWidgetResizable(True)

    def init(self, card_data):
        """
        初始化主卡片区域
        """
        self.main_object.main_card_list = []
        # 初始化区域
        # print(f'__主卡片初始化区域开始时间:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}')
        self.init_area()
        # 初始化顶部导航栏部分
        # print(f'__主卡片初始化导航栏开始时间:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}')
        self.init_header()
        # 菜单位置
        # print(f'__主卡片初始化区域开始时间:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}')
        self.menu_position = self.main_object.form_menu_locate
        # 初始化菜单部分
        # print(f'__主卡片初始化菜单开始时间:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}')
        self.init_menu_bg_and_slider()
        # 设置菜单样式
        # print(f'__主卡片初始化菜单样式开始时间:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}')
        self.menu_button_map = {
            "user": [self.main_object.push_button_user, "Peoples/people", self.main_object.user_area, "用户管理"],
            "setting": [self.main_object.push_button_setting, "Base/setting-two", self.main_object.setting_area, "设置"],
            # "exit": [self.main_object.push_button_exit, "Base/power", None],
            "trending": [self.main_object.push_button_weibo_info, "Energy/fire", self.main_object.top_area, "热搜"],
            "translate": [self.main_object.push_button_translate, "Base/translate", self.main_object.translate_area, "翻译"],
            "chat": [self.main_object.push_button_chat, "Abstract/smart-optimization", self.main_object.chat_area, "智能助手"],
            "tool": [self.main_object.push_button_tool, "Others/toolkit", self.main_object.tool_area, "工具箱"],
            "looking": [self.main_object.push_button_looking, "Base/preview-open", self.main_object.looking_area, "信息聚合"],
            "search": [self.main_object.push_button_search, "Base/search", self.main_object.search_area, "本地搜索"],
            "ipn": [self.main_object.push_button_ipn, "Arrows/transfer-data", self.main_object.ipn_area, "局域网文件传输"],
            "todo": [self.main_object.push_button_todo, "Edit/plan", self.main_object.todo_area, "待办事项"],
            "book": [self.main_object.push_button_book, "Office/book-one", self.main_object.book_area, "阅读"],
            "music": [self.main_object.push_button_music, "Music/music-one", self.main_object.music_area, "音乐"],
            "game": [self.main_object.push_button_game, "Travel/planet", self.main_object.game_area, "更多"],
        }
        # 初始化卡片位置数据
        # print(f'__主卡片初始化卡片位置开始时间:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}')
        self.init_geometry_data(card_data)
        # 初始化主题
        # print(f'__主卡片初始化主题开始时间:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}')
        self.set_theme()
        # 初始化主卡片区域中的菜单区域
        # print(f'__主卡片初始化菜单区域开始时间:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}')
        self.init_menu()
        # 初始化主卡片区域中的主区域
        # print(f'__主卡片初始化主区域开始时间:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}')
        self.init_main_card()
        # 初始化菜单
        # print(f'__主卡片初始化菜单开始时间:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}')
        self.show_change(is_init=True)

    def init_area(self):
        if not hasattr(self.main_object, "top_area"):
            self.main_object.top_area = QScrollArea(self.main_object.widget_base)
            self.main_object.translate_area = QScrollArea(self.main_object.widget_base)
            self.main_object.chat_area = QScrollArea(self.main_object.widget_base)
            self.main_object.tool_area = QScrollArea(self.main_object.widget_base)
            self.main_object.looking_area = QScrollArea(self.main_object.widget_base)
            self.main_object.search_area = QScrollArea(self.main_object.widget_base)
            self.main_object.ipn_area = QScrollArea(self.main_object.widget_base)
            self.main_object.todo_area = QScrollArea(self.main_object.widget_base)
            self.main_object.book_area = QScrollArea(self.main_object.widget_base)
            self.main_object.music_area = QScrollArea(self.main_object.widget_base)
            self.main_object.game_area = QScrollArea(self.main_object.widget_base)
            # 初始化主卡片区域
            area_list = [
                self.main_object.top_area,
                self.main_object.translate_area,
                self.main_object.chat_area,
                self.main_object.looking_area,
                self.main_object.tool_area,
                self.main_object.search_area,
                self.main_object.ipn_area,
                self.main_object.todo_area,
                self.main_object.book_area,
                self.main_object.music_area,
                self.main_object.game_area,
            ]
            for area in area_list:
                font = QFont()
                font.setFamilies([u"\u601d\u6e90\u9ed1\u4f53"])
                font.setBold(True)
                area.setGeometry(QRect(0, 0, 81, 81))
                area.setFont(font)
                area.setStyleSheet(
                    u"border-style:solid; border-radius:10px; border:0px groove gray; color:rgb(0, 0, 0);\n"
                    "border-color:rgba(255, 255, 255, 0); background-color:rgba(255, 255, 255, 100);")
                area.setFrameShape(QFrame.StyledPanel)
                area.setLineWidth(1)
                area.setWidgetResizable(True)
                scroll_area_widget_contents = QWidget()
                scroll_area_widget_contents.setGeometry(QRect(0, 0, 100, 100))
                area.setWidget(scroll_area_widget_contents)
                area.setParent(self.main_object.widget_base)
        # 修改区域父节点
        self.area_list = [
            self.main_object.user_area,
            self.main_object.setting_area,
            self.main_object.top_area,
            self.main_object.translate_area,
            self.main_object.chat_area,
            self.main_object.tool_area,
            self.main_object.looking_area,
            self.main_object.search_area,
            self.main_object.ipn_area,
            self.main_object.todo_area,
            self.main_object.book_area,
            self.main_object.music_area,
            self.main_object.game_area,
        ]
        for area in self.area_list:
            area.setParent(self.main_object.widget_base)
            area.show()

    def init_menu(self):
        """
        初始化主卡片区域中的菜单区域
        """
        if not self.main_object.is_first:
            return
        self.main_object.push_button_user.clicked.connect(self.push_button_user_click)
        self.main_object.push_button_setting.clicked.connect(self.push_button_setting_click)
        # self.main_object.push_button_exit.clicked.connect(partial(self.main_object.quit_before,  False))
        self.main_object.push_button_weibo_info.clicked.connect(self.push_button_weibo_click)
        self.main_object.push_button_translate.clicked.connect(self.push_button_translate_click)
        self.main_object.push_button_chat.clicked.connect(self.push_button_chat_click)
        self.main_object.push_button_tool.clicked.connect(self.push_button_tool_click)
        self.main_object.push_button_looking.clicked.connect(self.push_button_looking_click)
        self.main_object.push_button_search.clicked.connect(self.push_button_search_click)
        self.main_object.push_button_ipn.clicked.connect(self.push_button_ipn_click)
        self.main_object.push_button_todo.clicked.connect(self.push_button_todo_click)
        self.main_object.push_button_book.clicked.connect(self.push_button_book_click)
        self.main_object.push_button_music.clicked.connect(self.push_button_music_click)
        self.main_object.push_button_game.clicked.connect(self.push_button_game_click)

    def init_main_card(self):
        """
        初始化主卡片区域中的主区域
        """
        width  = self.main_card_width - self.main_object.label_menu.width() - self.CARD_INTERVAL
        height = self.main_card_height
        for area in self.area_list:
            area.hide()
            area.setGeometry(QtCore.QRect(self.main_card_x, self.main_card_y, width, height))
        self.main_object.tab_widget_user.setGeometry(QtCore.QRect(0, 0, width, height))
        # 初始化卡片
        theme = "Dark" if self.main_object.is_dark else "Light"
        self.main_object.main_card_list = []
        # 判断卡片数据是否完整
        big_card_name_list = user_data_common.big_card_name_list
        for big_card_name in big_card_name_list:
            has_this_card = False
            for card_data_index in range(len(self.main_object.main_data["bigCard"])):
                card_data = self.main_object.main_data["bigCard"][card_data_index]
                card_data_name = card_data["name"]
                if big_card_name == card_data_name:
                    has_this_card = True
                    break
            if not has_this_card:
                self.main_object.main_data["bigCard"].append({
                    "name": big_card_name,
                    "size": "Big",
                    "data": {}
                })
                break
        # 获取卡片数据
        for card_data_index in range(len(self.main_object.main_data["bigCard"])):
            # 获取卡片数据
            card_data = self.main_object.main_data["bigCard"][card_data_index]
            card_area = None
            # print(f'__主卡片初始化对应主卡片 {card_data["name"]} 创建时间:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}')
            # 初始化数据
            if card_data["name"] in self.main_object.main_data["data"]:
                long_time_data = self.main_object.main_data["data"][card_data["name"]]
                if long_time_data is None:
                    self.main_object.main_data["data"][card_data["name"]] = {}
            else:
                self.main_object.main_data["data"][card_data["name"]] = {}
            long_time_data = self.main_object.main_data["data"][card_data["name"]]
            card = None
            # 卡片缓存数据(深拷贝)
            in_card_cache = copy.deepcopy(card_data["data"])
            # 卡片持久数据(深拷贝)
            in_card_data = copy.deepcopy(long_time_data)
            # 开始初始化卡片
            if card_data["name"] == "BookCard":
                card_area = self.main_object.book_area
                card = BookCard(main_object=self.main_object, parent=self.main_object, theme=theme, card=card_area,
                                cache=in_card_cache, data=in_card_data,
                                toolkit=self.main_object.toolkit, logger=self.main_object.info_logger,
                                save_data_func=self.save_card_data_func)
            elif card_data["name"] == "ToolCard":
                card_area = self.main_object.tool_area
                card = ToolCard(main_object=self.main_object, parent=self.main_object, theme=theme, card=card_area,
                                cache=in_card_cache, data=in_card_data,
                                toolkit=self.main_object.toolkit, logger=self.main_object.info_logger,
                                save_data_func=self.save_card_data_func)
            elif card_data["name"] == "TodoCard":
                card_area = self.main_object.todo_area
                card = TodoCard(main_object=self.main_object, parent=self.main_object, theme=theme, card=card_area,
                                cache=in_card_cache, data=in_card_data,
                                toolkit=self.main_object.toolkit, logger=self.main_object.info_logger,
                                save_data_func=self.save_card_data_func)
            elif card_data["name"] == "TopSearchCard":
                card_area = self.main_object.top_area
                card = TopSearchCard(main_object=self.main_object, parent=self.main_object, theme=theme, card=card_area,
                                cache=in_card_cache, data=in_card_data,
                                toolkit=self.main_object.toolkit, logger=self.main_object.info_logger,
                                save_data_func=self.save_card_data_func)
            elif card_data["name"] == "ChatCard":
                card_area = self.main_object.chat_area
                card = ChatCard(main_object=self.main_object, parent=self.main_object, theme=theme, card=card_area,
                                cache=in_card_cache, data=in_card_data,
                                toolkit=self.main_object.toolkit, logger=self.main_object.info_logger,
                                save_data_func=self.save_card_data_func)
            elif card_data["name"] == "IpnCard":
                card_area = self.main_object.ipn_area
                card = IpnCard(main_object=self.main_object, parent=self.main_object, theme=theme, card=card_area,
                                cache=in_card_cache, data=in_card_data,
                                toolkit=self.main_object.toolkit, logger=self.main_object.info_logger,
                                save_data_func=self.save_card_data_func)
            elif card_data["name"] == "FileSearchCard":
                card_area = self.main_object.search_area
                card = FileSearchCard(main_object=self.main_object, parent=self.main_object, theme=theme, card=card_area,
                                cache=in_card_cache, data=in_card_data,
                                toolkit=self.main_object.toolkit, logger=self.main_object.info_logger,
                                save_data_func=self.save_card_data_func)
            elif card_data["name"] == "GameCard":
                card_area = self.main_object.game_area
                card = GameCard(main_object=self.main_object, parent=self.main_object, theme=theme, card=card_area,
                                cache=in_card_cache, data=in_card_data,
                                toolkit=self.main_object.toolkit, logger=self.main_object.info_logger,
                                save_data_func=self.save_card_data_func)
            elif card_data["name"] == "MusicCard":
                card_area = self.main_object.music_area
                card = MusicCard(main_object=self.main_object, parent=self.main_object, theme=theme, card=card_area,
                                cache=in_card_cache, data=in_card_data,
                                toolkit=self.main_object.toolkit, logger=self.main_object.info_logger,
                                save_data_func=self.save_card_data_func)
            elif card_data["name"] == "TranslateCard":
                card_area = self.main_object.translate_area
                card = TranslateCard(main_object=self.main_object, parent=self.main_object, theme=theme, card=card_area,
                                cache=in_card_cache, data=in_card_data,
                                toolkit=self.main_object.toolkit, logger=self.main_object.info_logger,
                                save_data_func=self.save_card_data_func)
            elif card_data["name"] == "InformationCard":
                card_area = self.main_object.looking_area
                card = InformationCard(main_object=self.main_object, parent=self.main_object, theme=theme, card=card_area,
                                cache=in_card_cache, data=in_card_data,
                                toolkit=self.main_object.toolkit, logger=self.main_object.info_logger,
                                save_data_func=self.save_card_data_func)
            elif card_data["name"] == "SettingCard":
                card_area = self.main_object.setting_area
                card = SettingCard(main_object=self.main_object, parent=self.main_object, theme=theme, card=card_area,
                                cache=in_card_cache, data=in_card_data,
                                toolkit=self.main_object.toolkit, logger=self.main_object.info_logger,
                                save_data_func=self.save_card_data_func)
            else:
                print("未支持的卡片")
            if card is None:
                continue
            self.main_object.main_card_list.append(card)
            # 隐藏
            card_area.hide()
        # 卡片初始化
        for card in self.main_object.main_card_list:
            # print(f'__主卡片初始化对应主卡片 {card.name} 初始化开始时间:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}')
            card.init_ui()
            if self.main_object.is_dark:
                card.card.setStyleSheet(self.main_object.toolkit.style_util.card_dark_style)
                style_util.set_card_shadow_effect(card.card)        # 添加外部阴影效果
            else:
                card.card.setStyleSheet(self.main_object.toolkit.style_util.card_style)
                style_util.remove_card_shadow_effect(card.card)     # 移除外部阴影效果
            # print(f'__主卡片初始化对应主卡片 {card.name} 初始化结束时间:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}')

    def save_card_data_func(self, trigger_type=data_save_constant.TRIGGER_TYPE_CARD_UPDATE, need_upload=True, in_data=None,
                            data_type=data_save_constant.DATA_TYPE_ENDURING, card_name=None):
        self.main_object.local_trigger_data_update(trigger_type=trigger_type,
                            need_upload=need_upload,
                            in_data=in_data,
                            data_type=data_type,
                            card_type=data_save_constant.CARD_TYPE_Big,
                            card_name=card_name)

    # 切换卡片显示
    def show_change(self, is_init=False):
        print(f"切换卡片显示,is_init:{is_init}")
        # 菜单位置
        if self.menu_position == card_constant.MENU_POSITION_RIGHT:
            menu_x = self.main_card_x + self.main_card_width - self.main_object.label_menu.width()
            menu_y = self.main_card_y
        else:
            menu_x = self.main_card_x - self.main_object.label_menu.width() - self.CARD_INTERVAL
            menu_y = self.main_card_y
        width  = self.main_object.label_menu.width()
        height = self.main_card_height
        self.main_object.label_menu.setGeometry(QtCore.QRect(menu_x, menu_y, width, height))
        self.main_object.label_menu_background.setGeometry(QtCore.QRect(menu_x, menu_y, width, height))
        # 调整菜单按钮指示位置
        if is_init:
            button_pos = get_position(self.main_object.label_menu)
            if self.menu_position == card_constant.MENU_POSITION_RIGHT:
                button_indicate_x = button_pos.x() + int(self.CARD_INTERVAL / 3)
            else:
                button_indicate_x = button_pos.x() + self.menu_button_width - 3
            button_indicate_y = button_pos.y() + 16
            self.main_object.label_current_menu.move(button_indicate_x, button_indicate_y)
        # 初始化菜单按钮
        for key, value in self.menu_button_map.items():
            button = value[0]
            # 设置按钮样式
            self.set_menu_style(button, key == self.see_card, is_init, value[1])
            if value[2] is None:    # 退出按钮没有区域
                continue
            # 隐藏或显示区域
            if key == self.see_card:
                value[2].show()
            else:
                value[2].hide()
            button.setToolTip(value[3])
            button.setCursor(QCursor(Qt.PointingHandCursor))     # 鼠标手形
        return 0, 0, width, height

    def change_menu_indicate_location(self):
        for button_name, value in self.menu_button_map.items():
            if button_name != self.see_card:
                continue
            button = value[0]
            self.main_object.toolkit.animation_util.start_line_y_animation(
                self.main_object.label_current_menu, self.main_object.label_current_menu.y(), get_position(button).y() + 6)
            print("设置菜单按钮指示位置")

    def theme_switch_button_click(self):
        theme_module.change_theme_data(self.main_object)
        self.main_object.change_theme()

    def set_menu_style(self, button, state, is_init, icon_path):
        """设置菜单按钮样式"""
        font = QtGui.QFont()
        if state:
            font.setPointSize(11)
            if not is_init:
                self.main_object.toolkit.animation_util.start_line_y_animation(
                    self.main_object.label_current_menu, self.main_object.label_current_menu.y(), get_position(button).y() + 6)
        else:
            font.setPointSize(10)
        font.setBold(state)
        font.setKerning(state)
        button.setStyleSheet(self.main_object.toolkit.style_util.get_menu_button_style(state))
        style_util.set_card_button_style(button, icon_path, is_dark=self.main_object.is_dark, style_change=False)
        button.setFont(font)
        button.setFocusPolicy(Qt.FocusPolicy.NoFocus)


    '''
    **********************************按钮列表 · 开始***************************************
    ↓                                                                                 ↓
    '''

    def push_button_weibo_click(self):
        print("点击热搜按钮")
        try:
            self.main_object.info_logger.card_info("主程序", "切换热搜完成")
            self.see_card = "trending"
            self.show_change()
        except Exception as e:
            self.main_object.info_logger.card_error("主程序", "切换热搜失败,错误信息:{}".format(e))
            self.main_object.toolkit.dialog_module.box_information(self.main_object, "错误信息", "切换热搜失败,请稍后重试")

    def push_button_looking_click(self):
        print("点击Looking按钮")
        try:
            self.main_object.info_logger.card_info("主程序", "切换Looking完成")
            self.see_card = "looking"
            self.show_change()
        except Exception as e:
            self.main_object.info_logger.card_error("主程序", "切换Looking失败,错误信息:{}".format(e))
            self.main_object.toolkit.dialog_module.box_information(self.main_object, "错误信息", "切换Looking失败,请稍后重试")

    def push_button_tool_click(self):
        print("点击Tool按钮")
        try:
            self.main_object.info_logger.card_info("主程序", "切换工具完成")
            self.see_card = "tool"
            self.show_change()
        except Exception as e:
            self.main_object.info_logger.card_error("主程序", "切换工具失败,错误信息:{}".format(e))
            self.main_object.toolkit.dialog_module.box_information(self.main_object, "错误信息", "切换工具失败,请稍后重试")

    def push_button_todo_click(self):
        print("点击Todo按钮")
        try:
            self.main_object.info_logger.card_info("主程序", "切换待办事项完成")
            self.see_card = "todo"
            self.show_change()
        except Exception as e:
            self.main_object.info_logger.card_error("主程序", "切换待办事项失败,错误信息:{}".format(e))
            self.main_object.toolkit.dialog_module.box_information(self.main_object, "错误信息", "切换待办事项失败,请稍后重试")

    def push_button_book_click(self):
        print("点击Book按钮")
        try:
            self.main_object.info_logger.card_info("主程序", "切换小说完成")
            self.see_card = "book"
            self.show_change()
        except Exception as e:
            self.main_object.info_logger.card_error("主程序", "切换小说失败,错误信息:{}".format(e))
            self.main_object.toolkit.dialog_module.box_information(self.main_object, "错误信息", "切换小说失败,请稍后重试")
            
    def push_button_music_click(self):
        print("点击Music按钮")
        try:
            self.main_object.info_logger.card_info("主程序", "切换音乐完成")
            self.see_card = "music"
            self.show_change()
        except Exception as e:
            self.main_object.info_logger.card_error("主程序", "切换音乐失败,错误信息:{}".format(e))
            self.main_object.toolkit.dialog_module.box_information(self.main_object, "错误信息", "切换音乐失败,请稍后重试")

    def push_button_translate_click(self):
        print("点击Translate按钮")
        try:
            self.main_object.info_logger.card_info("主程序", "切换翻译完成")
            self.see_card = "translate"
            self.show_change()
        except Exception as e:
            self.main_object.info_logger.card_error("主程序", "切换翻译失败,错误信息:{}".format(e))
            self.main_object.toolkit.dialog_module.box_information(self.main_object, "错误信息", "切换翻译失败,请稍后重试")

    def push_button_game_click(self):
        print("点击Game按钮")
        try:
            self.main_object.info_logger.card_info("主程序", "切换游戏完成")
            self.see_card = "game"
            self.show_change()
        except Exception as e:
            self.main_object.info_logger.card_error("主程序", "切换游戏失败,错误信息:{}".format(e))
            self.main_object.toolkit.dialog_module.box_information(self.main_object, "错误信息", "切换游戏失败,请稍后重试")

    def push_button_user_click(self):
        print("点击User按钮")
        try:
            self.main_object.info_logger.card_info("主程序", "切换用户完成")
            self.main_object.tab_widget_user.show()
            self.main_object.tab_widget_user.raise_()
            self.see_card = "user"
            self.show_change()
        except Exception as e:
            self.main_object.info_logger.card_error("主程序", "切换用户失败,错误信息:{}".format(e))
            self.main_object.toolkit.dialog_module.box_information(self.main_object, "错误信息", "切换用户失败,请稍后重试")

    def push_button_chat_click(self):
        print("点击Chat按钮")
        try:
            self.main_object.info_logger.card_info("主程序", "切换聊天完成")
            self.see_card = "chat"
            self.show_change()
        except Exception as e:
            self.main_object.info_logger.card_error("主程序", "切换聊天失败,错误信息:{}".format(e))
            self.main_object.toolkit.dialog_module.box_information(self.main_object, "错误信息", "切换聊天失败,请稍后重试")

    def push_button_search_click(self):
        print("点击Search按钮")
        try:
            self.main_object.info_logger.card_info("主程序", "切换搜索完成")
            self.see_card = "search"
            self.show_change()
            try:
                for card in self.main_object.main_card_list:
                    if card.name == "FileSearchCard":
                        card.show_form()
            except Exception as e:
                print(e)
        except Exception as e:
            self.main_object.info_logger.card_error("主程序", "切换搜索失败,错误信息:{}".format(e))
            self.main_object.toolkit.dialog_module.box_information(self.main_object, "错误信息", "切换搜索失败,请稍后重试")

    def push_button_ipn_click(self):
        print("点击IPN按钮")
        try:
            self.main_object.info_logger.card_info("主程序", "切换局域网文件传输完成")
            self.see_card = "ipn"
            self.show_change()
        except Exception as e:
            self.main_object.info_logger.card_error("主程序", "切换局域网文件传输失败,错误信息:{}".format(e))
            self.main_object.toolkit.dialog_module.box_information(self.main_object, "错误信息", "切换局域网文件传输失败,请稍后重试")

    def push_button_setting_click(self):
        print("点击Setting按钮")
        try:
            self.main_object.info_logger.card_info("主程序", "切换设置完成")
            self.see_card = "setting"
            self.show_change()
        except Exception as e:
            self.main_object.info_logger.card_error("主程序", "切换设置失败,错误信息:{}".format(e))
            self.main_object.toolkit.dialog_module.box_information(self.main_object, "错误信息", "切换设置失败,请稍后重试")

    def init_geometry_data(self, card_data):
        card_map = None
        print(f"card_data:{card_data}")
        for user_card_map in card_data:
            card_name = user_card_map["name"]
            if card_name == "MainCard":
                card_map = user_card_map
                break
        if card_map is None:
            return
        all_card_x = int(int(card_map["x"]) - 1) * self.CARD_WIDTH + int(card_map["x"]) * self.CARD_INTERVAL
        all_card_y = int(int(card_map["y"]) - 1) * self.CARD_HEIGHT + int(card_map["y"]) * self.CARD_INTERVAL + self.HEADER_HEIGHT
        # 位置
        if self.menu_position == card_constant.MENU_POSITION_RIGHT:
            self.main_card_x = all_card_x
            self.main_card_y = all_card_y
        else:
            self.main_card_x = all_card_x + self.main_object.label_menu.width() + self.CARD_INTERVAL
            self.main_card_y = all_card_y
        width = int(card_map["size"].split("_")[0])
        height = int(card_map["size"].split("_")[1])
        self.main_card_width = self.CARD_INTERVAL * (width - 1) + self.CARD_WIDTH * width
        self.main_card_height = self.CARD_INTERVAL * (height - 1) + self.CARD_HEIGHT * height

    def change_geometry(self, card_data):
        # 重新设置位置和尺寸数据
        self.menu_position = self.main_object.form_menu_locate
        self.init_geometry_data(card_data)
        # 重新设置主卡片区域位置
        width  = self.main_card_width - self.main_object.label_menu.width() - self.CARD_INTERVAL
        height = self.main_card_height
        for area in self.area_list:
            area.setGeometry(QtCore.QRect(self.main_card_x, self.main_card_y, width, height))
        self.main_object.tab_widget_user.setGeometry(QtCore.QRect(0, 0, width, height))
        # 初始化菜单
        self.show_change(is_init=True)
        # 设置标题栏样式
        self.set_header_button_theme()

    def init_header(self):
        if hasattr(self.main_object, "widget_header") and self.main_object.widget_header is not None:
            self.main_object.widget_header.show()
            return
        # 导航栏
        self.main_object.widget_header = QWidget(self.main_object.widget_base)
        self.main_object.widget_header.setObjectName(u"widget_header")
        self.main_object.widget_header.setGeometry(QRect(0, 0, self.main_object.width(), self.HEADER_VIEW_HEIGHT))
        self.main_object.widget_header.setStyleSheet("QWidget { border: none; background-color: transparent; }")
        # 导航栏布局
        self.main_object.layout_base_header = QVBoxLayout()
        self.main_object.layout_base_header.setSpacing(0)
        self.main_object.layout_base_header.setContentsMargins(0, 0, 0, 0)
        self.main_object.layout_base_header.setObjectName(u"layout_base_header")
        self.main_object.widget_header.setLayout(self.main_object.layout_base_header)
        # 导航栏布局
        self.main_object.layout_header = QHBoxLayout()
        self.main_object.layout_header.setSpacing(self.CARD_INTERVAL)
        self.main_object.layout_header.setContentsMargins(self.CARD_INTERVAL, 5, self.CARD_INTERVAL, 0)
        self.main_object.layout_header.setObjectName(u"layout_header")
        self.main_object.layout_base_header.addStretch()
        self.main_object.layout_base_header.addLayout(self.main_object.layout_header)
        # 导航栏左边是标题
        self.main_object.push_button_header_title = QPushButton()
        self.main_object.push_button_header_title.setObjectName(u"push_button_header_title")
        self.main_object.push_button_header_title.setText("灵卡面板")
        self.main_object.push_button_header_title.setMinimumHeight(26)
        self.main_object.push_button_header_title.setMinimumWidth(80)
        self.main_object.push_button_header_title.setIconSize(QSize(20, 20))
        self.main_object.push_button_header_title.setCursor(QCursor(Qt.PointingHandCursor))     # 鼠标手形
        self.main_object.layout_header.addWidget(self.main_object.push_button_header_title)
        self.main_object.layout_header.addStretch()
        # 右侧第一个是退出按钮
        # self.main_object.push_button_header_exit = QPushButton()
        # self.main_object.push_button_header_exit.setObjectName(u"push_button_header_exit")
        # self.main_object.push_button_header_exit.setText("")
        # self.main_object.push_button_header_exit.setMinimumHeight(26)
        # self.main_object.push_button_header_exit.setMinimumWidth(26)
        # self.main_object.push_button_header_exit.setIconSize(QSize(22, 22))
        # self.main_object.push_button_header_exit.setCursor(QCursor(Qt.PointingHandCursor))     # 鼠标手形
        # 右侧第二个是截屏按钮
        # self.main_object.push_button_screenshot = QPushButton()
        # self.main_object.push_button_screenshot.setObjectName(u"push_button_screenshot")
        # self.main_object.push_button_screenshot.setText("")
        # self.main_object.push_button_screenshot.setMinimumHeight(26)
        # self.main_object.push_button_screenshot.setMinimumWidth(26)
        # self.main_object.push_button_screenshot.setIconSize(QSize(22, 22))
        # self.main_object.push_button_screenshot.setCursor(QCursor(Qt.PointingHandCursor))     # 鼠标手形
        # 右侧第三个是钉住按钮
        self.main_object.push_button_pin = QPushButton()
        self.main_object.push_button_pin.setObjectName(u"push_button_pin")
        self.main_object.push_button_pin.setText("")
        self.main_object.push_button_pin.setMinimumHeight(26)
        self.main_object.push_button_pin.setMinimumWidth(26)
        self.main_object.push_button_pin.setIconSize(QSize(22, 22))
        self.main_object.push_button_pin.setCursor(QCursor(Qt.PointingHandCursor))              # 鼠标手形
        # 右侧第四个是更多按钮
        self.main_object.push_button_more = QToolButton()
        self.main_object.push_button_more.setObjectName(u"push_button_more")
        self.main_object.push_button_more.setText("")
        self.main_object.push_button_more.setMinimumHeight(26)
        self.main_object.push_button_more.setMinimumWidth(26)
        self.main_object.push_button_more.setIconSize(QSize(22, 22))
        self.main_object.push_button_more.setCursor(QCursor(Qt.PointingHandCursor))              # 鼠标手形
        self.main_object.push_button_more.setPopupMode(QToolButton.InstantPopup)
        # # 右侧第四个是截图按钮
        # self.main_object.push_button_screenshot = QPushButton()
        # self.main_object.push_button_screenshot.setObjectName(u"push_button_screenshot")
        # self.main_object.push_button_screenshot.setText("")
        # self.main_object.push_button_screenshot.setMinimumHeight(26)
        # self.main_object.push_button_screenshot.setMinimumWidth(26)
        # self.main_object.push_button_screenshot.setIconSize(QSize(22, 22))
        # self.main_object.push_button_screenshot.setCursor(QCursor(Qt.PointingHandCursor))              # 鼠标手形
        # # 右侧第五个是卡片设计按钮
        # self.main_object.push_button_card_design = QPushButton()
        # self.main_object.push_button_card_design.setObjectName(u"push_button_card_design")
        # self.main_object.push_button_card_design.setText("")
        # self.main_object.push_button_card_design.setMinimumHeight(26)
        # self.main_object.push_button_card_design.setMinimumWidth(26)
        # self.main_object.push_button_card_design.setIconSize(QSize(22, 22))
        # self.main_object.push_button_card_design.setCursor(QCursor(Qt.PointingHandCursor))     # 鼠标手形
        # 最右侧是隐藏按钮
        self.main_object.push_button_hide_window = QPushButton()
        self.main_object.push_button_hide_window.setObjectName(u"push_button_hide_window")
        self.main_object.push_button_hide_window.setText("")
        self.main_object.push_button_hide_window.setMinimumHeight(26)
        self.main_object.push_button_hide_window.setMinimumWidth(26)
        self.main_object.push_button_hide_window.setIconSize(QSize(22, 22))
        self.main_object.push_button_hide_window.setCursor(QCursor(Qt.PointingHandCursor))     # 鼠标手形
        # 添加到布局
        # self.main_object.layout_header.addWidget(self.main_object.push_button_header_exit)
        # self.main_object.layout_header.addWidget(self.main_object.push_button_screenshot)
        self.main_object.layout_header.addWidget(self.main_object.push_button_more)
        self.main_object.layout_header.addWidget(self.main_object.push_button_pin)
        # self.main_object.layout_header.addWidget(self.main_object.push_button_screenshot)
        # self.main_object.layout_header.addWidget(self.main_object.push_button_card_design)
        self.main_object.layout_header.addWidget(self.main_object.push_button_hide_window)
        # 点击事件
        self.main_object.push_button_header_title.clicked.connect(partial(self.click_header_title_button))
        # self.main_object.push_button_header_exit.clicked.connect(partial(self.main_object.quit_before,  False))
        # self.main_object.push_button_screenshot.clicked.connect(
        #     partial(self.main_object.toolkit.image_util.screenshot, self.main_object))
        self.main_object.push_button_pin.clicked.connect(partial(self.push_button_pin_click))
        # self.main_object.push_button_screenshot.clicked.connect(partial(self.push_button_screenshot_click))
        # self.main_object.push_button_card_design.clicked.connect(partial(self.push_button_setting_card_permutation_click))
        self.main_object.push_button_hide_window.clicked.connect(partial(self.push_button_hide_window_click))
        # 创建更多的下拉菜单
        self.main_object.header_more_menu = QMenu(self.main_object.push_button_more)
        self.main_object.header_more_menu.setObjectName(u"header_more_menu")
        # 卡片设计选项
        self.main_object.card_permutation_action = QAction("卡片设计", self.main_object.push_button_more)
        self.main_object.card_permutation_action.triggered.connect(lambda: self.push_button_setting_card_permutation_click())
        self.main_object.header_more_menu.addAction(self.main_object.card_permutation_action)
        # 截图选项
        self.main_object.screenshot_action = QAction("屏幕截图", self.main_object.push_button_more)
        self.main_object.screenshot_action.triggered.connect(lambda: self.push_button_screenshot_click())
        self.main_object.header_more_menu.addAction(self.main_object.screenshot_action)
        # 取色选项
        self.main_object.color_picker_action = QAction("屏幕取色", self.main_object.push_button_more)
        self.main_object.color_picker_action.triggered.connect(lambda: self.push_button_color_picker_click())
        self.main_object.header_more_menu.addAction(self.main_object.color_picker_action)
        # 官网选项
        self.main_object.official_website_action = QAction("打开官网", self.main_object.push_button_more)
        self.main_object.official_website_action.triggered.connect(lambda: self.open_index_url())
        self.main_object.header_more_menu.addAction(self.main_object.official_website_action)
        # 关于我们选项
        self.main_object.about_us_action = QAction("关于我们", self.main_object.push_button_more)
        self.main_object.about_us_action.triggered.connect(lambda: self.open_about_us_url())
        self.main_object.header_more_menu.addAction(self.main_object.about_us_action)
        # 绑定菜单项点击事件
        self.main_object.push_button_more.setMenu(self.main_object.header_more_menu)
        # 设置按钮样式
        self.set_header_button_theme()

    def apply_menu_style(self, is_dark):
        """应用菜单样式"""
        self.main_object.card_permutation_action.setIcon(style_util.get_icon_by_path("Build/application", is_dark=is_dark))
        self.main_object.screenshot_action.setIcon(style_util.get_icon_by_path("Edit/screenshot", is_dark=is_dark))
        self.main_object.color_picker_action.setIcon(style_util.get_icon_by_path("Hardware/electronic-pen", is_dark=is_dark))
        self.main_object.official_website_action.setIcon(style_util.get_icon_by_path("Travel/planet", is_dark=is_dark))
        self.main_object.about_us_action.setIcon(style_util.get_icon_by_path("Character/info", is_dark=is_dark))
        if is_dark:
            menu_style = """
                QMenu {
                    background-color: #333333;
                    border: 1px solid #555555;
                    border-radius: 5px;
                    padding: 5px;
                }
                QMenu::item {
                    background-color: transparent;
                    color: #ffffff;
                    padding: 5px 15px 5px 15px;
                    border-radius: 3px;
                }
                QMenu::item:selected {
                    background-color: #555555;
                }
                QMenu::item:disabled {
                    color: #888888;
                }
                QMenu::separator {
                    height: 1px;
                    background-color: #555555;
                    margin: 5px 0px 5px 0px;
                }
            """
        else:
            menu_style = """
                QMenu {
                    background-color: #ffffff;
                    border: 1px solid #cccccc;
                    border-radius: 5px;
                    padding: 5px;
                }
                QMenu::item {
                    background-color: transparent;
                    color: #333333;
                    padding: 5px 15px 5px 15px;
                    border-radius: 3px;
                }
                QMenu::item:selected {
                    background-color: #e6e6e6;
                }
                QMenu::item:disabled {
                    color: #888888;
                }
                QMenu::separator {
                    height: 1px;
                    background-color: #cccccc;
                    margin: 5px 0px 5px 0px;
                }
            """
        if hasattr(self.main_object, "header_more_menu"):
            self.main_object.header_more_menu.setStyleSheet(menu_style)

    # 设置
    def push_button_screenshot_click(self):
        self.main_object.on_screenshot_hotkey_triggered()

    # 设置
    def push_button_color_picker_click(self):
        self.main_object.start_color_picker()

    # 设置钉住
    def push_button_pin_click(self):
        if self.main_object.pin_form:
            self.main_object.pin_form = False
        else:
            self.main_object.pin_form = True
        card_pin_icon_path = "Edit/pin"
        if self.main_object.pin_form:
            card_pin_icon = style_util.get_icon_by_path(card_pin_icon_path, custom_color="#6496F3")
        else:
            card_pin_icon = style_util.get_icon_by_path(card_pin_icon_path, is_dark=self.main_object.is_dark)
        self.main_object.push_button_pin.setIcon(card_pin_icon)

    # 退出
    def push_button_hide_window_click(self):
        if self.main_object.pin_form:
            self.push_button_pin_click()
        self.main_object.toolkit.resolution_util.out_animation(self.main_object)

    # 设置卡片排列
    def push_button_setting_card_permutation_click(self):
        self.main_object.toolkit.resolution_util.out_animation(self.main_object)
        QTimer.singleShot(100, self.show_card_permutation_win)

    def show_card_permutation_win(self):
        setting_card = None
        for card in self.main_object.main_card_list:
            if card.name == "SettingCard":
                setting_card = card
        user_card_list = copy.deepcopy(self.main_object.main_data["card"])
        main_config = copy.deepcopy(self.main_object.main_data)
        self.main_object.card_permutation_win = CardPermutationWindow(setting_card, self.main_object, user_card_list, main_config)
        self.main_object.card_permutation_win.show()

    def click_header_title_button(self):
        browser_util.open_url(common.index_url)

    def init_menu_bg_and_slider(self):
        if hasattr(self.main_object, "label_menu") and self.main_object.label_menu is not None:
            self.main_object.label_menu.show()
            self.main_object.label_current_menu.show()
            self.main_object.label_menu_background.show()
            self.main_object.theme_switch_button.show()
            return
        # 菜单栏
        self.main_object.label_menu = QWidget(self.main_object.widget_base)
        self.main_object.label_menu.setObjectName(u"label_menu")
        self.main_object.label_menu.setGeometry(QRect(0, 0, 38, 590))
        self.main_object.label_menu.setStyleSheet("""
        QWidget {
            border-style: solid;
            border-radius: 15px;
            border: none;
            background-color: rgba(255, 255, 255, 160);
        }""")
        # 菜单栏底部的背景专用层(为了防止加了阴影效果导致主题切换按钮的图标显示不出来)
        self.main_object.label_menu_background = QWidget(self.main_object.widget_base)
        self.main_object.label_menu_background.setObjectName(u"label_menu_background")
        self.main_object.label_menu_background.setGeometry(QRect(0, 0, 38, 590))
        self.main_object.label_menu_background.setStyleSheet("""
        QWidget {
            border-style: solid;
            border-radius: 15px;
            border: none;
            background-color: transparent;
        }""")
        # 菜单栏布局
        self.main_object.layout_menu_background = QVBoxLayout(self.main_object.label_menu)
        self.main_object.layout_menu_background.setContentsMargins(2, 10, 4, 10)
        self.main_object.layout_menu_background.setSpacing(2)
        # 菜单栏指示按钮位置的指示条
        self.main_object.label_menu.lower()
        self.main_object.label_menu_background.lower()
        self.main_object.label_current_menu = QLabel(self.main_object.widget_base)
        self.main_object.label_current_menu.setObjectName(u"label_current_menu")
        self.main_object.label_current_menu.setGeometry(QRect(0, 0, 4, 21))
        # 菜单栏按钮列表
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setKerning(True)
        button_names = [
            'user', 'setting',
            'weibo_info', 'translate', 'chat', 'tool', 'looking', 'search', 'ipn', 'todo', 'book', 'music', 'game'
        ]
        for name in button_names:
            # 创建按钮
            menu_button = QPushButton(self.main_object.label_menu)
            setattr(self.main_object, f'push_button_{name}', menu_button)
            # 设置按钮属性
            menu_button.setFixedSize(self.menu_button_width, self.menu_button_width)
            menu_button.setObjectName(f'push_button_{name}')
            menu_button.setStyleSheet("""
            QPushButton {
                color: #FFFFFF;
                border: 10px solid #000000;
                background-color: rgba(0, 0, 0, 0);
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 160);
                color: rgb(0, 0, 0);
            }""")
            menu_button.setFont(font)
            menu_button.setIconSize(QSize(22, 22))
            self.main_object.layout_menu_background.addWidget(menu_button)
            # 上下半部分需要增加伸缩条和主题切换按钮
            if name == 'setting':
                # 主题切换按钮
                print(f"self.main_object.is_dark:{self.main_object.is_dark}")
                self.main_object.theme_switch_button = ThemeSwitchButton(default_theme=not self.main_object.is_dark)
                self.main_object.theme_switch_button.clicked.connect(self.theme_switch_button_click)
                self.main_object.theme_switch_button.setFixedSize(QSize(self.main_object.label_menu.width() - self.CARD_INTERVAL + 5, 58))
                self.main_object.theme_switch_button.resize(self.main_object.theme_switch_button.size())
                self.main_object.theme_switch_button.setCursor(QCursor(Qt.PointingHandCursor))     # 鼠标手形
                self.main_object.layout_menu_background.addWidget(self.main_object.theme_switch_button)
                # 伸缩条
                self.main_object.layout_menu_background.addStretch()
            # 底部伸缩条
            if name == button_names[-1]:
                self.main_object.layout_menu_background.addStretch()
        # 强制刷新
        self.main_object.label_menu.update()

    def set_theme(self):
        # 菜单样式
        if self.main_object.is_dark:
            self.main_object.label_menu.setStyleSheet("border-radius: 15px; border: 1px solid #2C2E39; background-color: transparent;")
            self.main_object.label_menu_background.setStyleSheet("border-radius: 15px; border: none; background-color: rgba(34, 34, 34, 255);")
            self.main_object.label_current_menu.setStyleSheet("border-radius: 2px; border: 0px solid white; background-color: white;")
            style_util.set_card_shadow_effect(self.main_object.label_menu_background)       # 添加外部阴影效果
        else:
            self.main_object.label_menu.setStyleSheet("border-radius: 15px; border: none; background-color:rgba(255, 255, 255, 160);")
            self.main_object.label_menu_background.setStyleSheet("border-radius: 15px; border: 1px solid rgba(255, 255, 255, 170); background-color: transparent;")
            self.main_object.label_current_menu.setStyleSheet("border-radius: 2px; border: 0px solid black; background-color: black;")
            style_util.remove_card_shadow_effect(self.main_object.label_menu_background)    # 移除外部阴影效果
        self.set_menu_theme()
        # 卡片样式
        for card in self.main_object.main_card_list:
            if self.main_object.is_dark:
                card.card.setStyleSheet(self.main_object.toolkit.style_util.card_dark_style)
                style_util.set_card_shadow_effect(card.card)        # 添加外部阴影效果
            else:
                card.card.setStyleSheet(self.main_object.toolkit.style_util.card_style)
                style_util.remove_card_shadow_effect(card.card)     # 移除外部阴影效果
            card.set_theme(self.main_object.is_dark)
        if self.main_object.is_dark:
            self.main_object.user_area.setStyleSheet(self.main_object.toolkit.style_util.card_dark_style)
            style_util.set_card_shadow_effect(self.main_object.user_area)        # 添加外部阴影效果
        else:
            self.main_object.user_area.setStyleSheet(self.main_object.toolkit.style_util.card_style)
            style_util.remove_card_shadow_effect(self.main_object.user_area)     # 移除外部阴影效果
        # 设置标题栏按钮样式
        self.set_header_button_theme()

    def set_header_button_theme(self):
        self.main_object.widget_header.resize(QSize(self.main_object.width(), self.HEADER_VIEW_HEIGHT))
        print(f"界面宽度和高度：{self.main_object.width()} x {self.main_object.height()}")
        # 标题栏按钮
        header_title_icon = QIcon()
        header_title_icon.addFile(":static/img/icon/icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.main_object.push_button_header_title.setIcon(header_title_icon)
        # # 退出按钮
        # style_util.set_card_button_style(self.main_object.push_button_header_exit, "Base/power",
        #                                  is_dark=self.main_object.is_dark, style_change=False)
        # # 截图按钮
        # style_util.set_card_button_style(self.main_object.push_button_screenshot, "Edit/screenshot",
        #                                  is_dark=self.main_object.is_dark, style_change=False)
        # # 卡片设计按钮
        # style_util.set_card_button_style(self.main_object.push_button_card_design, "Build/application",
        #                                  is_dark=self.main_object.is_dark, style_change=False)
        # 更多按钮
        style_util.set_card_button_style(self.main_object.push_button_more, "Base/hamburger-button",
                                         is_dark=self.main_object.is_dark, style_change=False)
        # 隐藏窗口按钮
        if self.main_object.form_locate == card_constant.MENU_POSITION_RIGHT:
            hide_window_icon_path = "Arrows/to-right"
        else:
            hide_window_icon_path = "Arrows/to-left"
        style_util.set_card_button_style(self.main_object.push_button_hide_window, hide_window_icon_path,
                                         is_dark=self.main_object.is_dark, style_change=False)
        # 钉住按钮
        card_pin_icon_path = "Edit/pin"
        if self.main_object.pin_form:
            card_pin_icon = style_util.get_icon_by_path(card_pin_icon_path, custom_color="#6496F3")
        else:
            card_pin_icon = style_util.get_icon_by_path(card_pin_icon_path, is_dark=self.main_object.is_dark)
        self.main_object.push_button_pin.setIcon(card_pin_icon)
        if self.main_object.is_dark:
            self.main_object.push_button_header_title.setStyleSheet(self.main_object.toolkit.style_util.header_button_dark_style)
            self.main_object.push_button_pin.setStyleSheet(self.main_object.toolkit.style_util.header_button_dark_style)
            self.main_object.push_button_hide_window.setStyleSheet(self.main_object.toolkit.style_util.header_button_dark_style)
            self.main_object.push_button_more.setStyleSheet(
                self.main_object.toolkit.style_util.header_button_dark_style
                .replace("QPushButton", "QToolButton") + "QToolButton::menu-indicator {image: none;}"
            )
        else:
            self.main_object.push_button_header_title.setStyleSheet(self.main_object.toolkit.style_util.header_button_style)
            self.main_object.push_button_pin.setStyleSheet(self.main_object.toolkit.style_util.header_button_style)
            self.main_object.push_button_hide_window.setStyleSheet(self.main_object.toolkit.style_util.header_button_style)
            self.main_object.push_button_more.setStyleSheet(
                self.main_object.toolkit.style_util.header_button_style
                .replace("QPushButton", "QToolButton") + "QToolButton::menu-indicator {image: none;}"
            )
        # 应用顶部更多按钮的菜单样式
        self.apply_menu_style(self.main_object.is_dark)

    # 切换卡片显示
    def set_menu_theme(self):
        for key, value in self.menu_button_map.items():
            button = value[0]
            # 设置按钮样式
            self.set_menu_style(button, key == self.see_card, True, value[1])
            if value[2] is None:    # 退出按钮没有区域
                continue
            # 隐藏或显示区域
            if key == self.see_card:
                value[2].show()
            else:
                value[2].hide()
            button.setToolTip(value[3])

    def show_form(self):
        for card in self.main_object.main_card_list:
            try:
                card.show_form()
            except Exception as e:
                print(e)

    def hide_form(self):
        for card in self.main_object.main_card_list:
            try:
                card.hide_form()
            except Exception as e:
                print(e)

    def refresh_card_list(self, main_card_data_update_list, enduring_changes):
        """
        对需要改变的卡片列表进行数据更新
        """
        for main_card in self.main_object.main_card_list:
            name = main_card.name
            need_update_cache = False
            need_update_data = False
            cache_data = None
            enduring_real_data = None
            # 判断是否需要更新缓存
            for card in main_card_data_update_list:
                if card["name"] == name:
                    need_update_cache = True
                    cache_data = card["data"]
                    break
            # 判断是否需要更新数据
            if name in enduring_changes:
                need_update_data = True
                enduring_data = enduring_changes[name]
                enduring_data_type = enduring_data["type"]
                if enduring_data_type == "added" or enduring_data_type == "removed":
                    enduring_real_data = enduring_data["data"]
                else:
                    enduring_real_data = enduring_data["new_data"]
            # 如果两个都不需更新，则跳过
            if not need_update_cache and not need_update_data:
                continue
            is_hide = main_card.card.isHidden()
            if not is_hide:
                main_card.card.hide()
            # 如果仅需更新缓存，则更新缓存
            if need_update_cache and not need_update_data:
                main_card.update_cache(cache=cache_data)
            # 如果仅需更新数据，则更新数据
            if need_update_data and not need_update_cache:
                main_card.update_data(data=enduring_real_data)
            # 如果需更新缓存和数据，则更新所有
            if need_update_cache and need_update_data:
                main_card.update_all(cache=cache_data, data=enduring_real_data)
            if not is_hide:
                main_card.card.show()

    def on_translate(self, pixmap):
        """
        ocr翻译
        """
        for card in self.main_object.main_card_list:
            if hasattr(card, 'screenshot_captured'):
                self.push_button_translate_click()
                card.screenshot_captured(pixmap, do_job="translate")

    def on_ocr(self, pixmap):
        """
        ocr
        """
        for card in self.main_object.main_card_list:
            if hasattr(card, 'screenshot_captured'):
                card.screenshot_captured(pixmap, do_job="ocr")

    def open_index_url(self):
        browser_util.open_url(common.index_url)

    def open_about_us_url(self):
        self.main_object.setting_about_us_win = AboutUsWindow(None, self.main_object)
        self.main_object.setting_about_us_win.refresh_geometry(self.main_object.toolkit.resolution_util.get_screen(self.main_object))
        self.main_object.setting_about_us_win.show()
