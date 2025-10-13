import datetime
import json
import time
import urllib
from src.util import my_shiboken_util
import webbrowser

from PySide6.QtCore import QCoreApplication, QRect, Qt, QUrl, Signal
from PySide6.QtGui import QFont, QCursor
from PySide6.QtWidgets import QLabel, QPushButton, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, \
    QSizePolicy, QScrollArea
from PySide6 import QtNetwork
# 获取信息
from src.card.MainCardManager.MainCard import MainCard
from src.client import common
from src.ui.style_util import scroll_bar_style
from src.util import browser_util
from src.ui import style_util
from src.my_component.LoadAnimation.LoadAnimation import LoadAnimation


# 热度标签映射
TAG_MAP = {
    "new": ("新", "#ff3852"),
    "hot": ("热", "#ff9406"),
    "boil": ("沸", "#f86400"),
    "warm": ("暖", "#ffab5a"),
    "boom": ("爆", "#bd0000"),
}


class ClickableLabel(QLabel):
    leftClicked = Signal()
    middleClicked = Signal()

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setWordWrap(True)
        self.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.leftClicked.emit()
            event.accept()  # 阻止冒泡
            return
        elif event.button() == Qt.MiddleButton:
            self.middleClicked.emit()
            event.accept()  # 阻止冒泡
            return
        super().mousePressEvent(event)  # 其它情况才交给父类


class HotSearchItem(QWidget):
    link = None
    index_label = None
    content = None
    tag_label = None
    left_click_func = None
    middle_click_func = None

    def __init__(self, parent=None, data=None, data_type=None, left_click_func=None, middle_click_func=None):
        super().__init__(parent)
        self.data = data
        if data_type == "weibo":
            self.link = "https://s.weibo.com/weibo?q=" + urllib.parse.quote("#" + str(data['t']) + "#")
        else:
            self.link = str(data['u'])
        self.left_click_func = left_click_func
        self.middle_click_func = middle_click_func

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 2, 10, 2)
        main_layout.setSpacing(0)

        # 第一行水平布局：序号 + 内容 + 标签
        first_line_layout = QHBoxLayout()
        first_line_layout.setContentsMargins(0, 0, 0, 0)
        first_line_layout.setSpacing(5)  # 增加间距避免元素过于紧凑

        # 序号 - 根据排名设置不同颜色
        self.index_label = QLabel(data["i"])
        try:
            index_num = int(data["i"])
            if index_num <= 3:
                index_color = "#f26d5f"  # 前三个红色
            else:
                index_color = "#ff8200"  # 后面橙色
        except ValueError:
            index_color = "#ff8200"  # 默认橙色
        self.index_label.setStyleSheet(f"min-width: 20px; color: {index_color}; padding: 2px 0px;")
        self.index_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        first_line_layout.addWidget(self.index_label, alignment=Qt.AlignTop)

        # 内容（可点击）- 设置蓝色
        self.content = ClickableLabel(f"{data['t']} {data['n']}")
        self.content.setStyleSheet(f"color: rgb(0, 120, 182); padding: 2px 0px;")
        self.content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.content.setMinimumWidth(0)
        first_line_layout.addWidget(self.content, stretch=1)

        # 标签
        self.tag_label = QLabel()
        if "c" in data and data["c"] in TAG_MAP:
            tag_text, tag_color = TAG_MAP[data["c"]]
            self.tag_label.setText(tag_text)
            self.tag_label.setStyleSheet(
                f"color: white; background: {tag_color};"
                f"border-radius: 6px; padding: 2px 6px;"
            )
        self.tag_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        first_line_layout.addWidget(self.tag_label, alignment=Qt.AlignRight | Qt.AlignTop)

        main_layout.addLayout(first_line_layout)
        self.setLayout(main_layout)

        # 背景默认 & hover
        self.default_color = "rgb(0, 120, 182);"
        self.hover_color = "rgb(64, 160, 182)"
        self.update_bg(self.default_color)
        self.setCursor(QCursor(Qt.PointingHandCursor))

        # 信号绑定
        self.content.leftClicked.connect(lambda: self.open_link(False))
        self.content.middleClicked.connect(lambda: self.open_link(True))

    def set_data(self, data, data_type=None):
        # 数据
        if data_type == "weibo":
            self.link = "https://s.weibo.com/weibo?q=" + urllib.parse.quote("#" + str(data['t']) + "#")
        else:
            self.link = str(data['u'])
        # 序号 - 根据排名设置不同颜色
        self.index_label.setText(data["i"])
        try:
            index_num = int(data["i"])
            if index_num <= 3:
                index_color = "#f26d5f"  # 前三个红色
            else:
                index_color = "#ff8200"  # 后面橙色
        except ValueError:
            index_color = "#ff8200"  # 默认橙色
        self.index_label.setStyleSheet(f"min-width: 20px; color: {index_color}; padding: 2px 0px;")
        # 内容（可点击）- 设置蓝色
        self.content.setText(f"{data['t']} {data['n']}")
        # 标签
        if "c" in data and data["c"] in TAG_MAP:
            tag_text, tag_color = TAG_MAP[data["c"]]
            self.tag_label.setText(tag_text)
            self.tag_label.setStyleSheet(
                f"color: white; background: {tag_color};"
                f"border-radius: 6px; padding: 2px 6px;"
            )

    def update_bg(self, color: str):
        self.content.setStyleSheet(f"color: {color}; padding: 2px 0px;")

    def enterEvent(self, event):
        self.update_bg(self.hover_color)
        return super().enterEvent(event)

    def leaveEvent(self, event):
        self.update_bg(self.default_color)
        return super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.open_link(False)
        elif event.button() == Qt.MiddleButton:
            self.open_link(True)
        return super().mousePressEvent(event)

    def open_link(self, new_tab=False):
        if new_tab:
            self.middle_click_func(self.link)
        else:
            self.left_click_func(self.link)


class HotSearchList(QWidget):
    """
    热搜列表
    """
    hot_search_item_list = []
    left_click_func = None
    middle_click_func = None
    # 布局
    main_layout = None
    main_scroll = None
    main_container = None

    def __init__(self, parent=None, left_click_func=None, middle_click_func=None):
        super().__init__(parent)
        self.left_click_func = left_click_func
        self.middle_click_func = middle_click_func
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        # 滚动区域
        self.main_scroll = QScrollArea()
        self.main_scroll.setStyleSheet("""
        QScrollArea {
            background: transparent;
            border: none;
        }
        """ + scroll_bar_style)
        self.main_scroll.setWidgetResizable(True)
        self.main_layout.addWidget(self.main_scroll)
        self.main_container = QWidget()
        self.main_container.setStyleSheet("background: transparent;")
        self.vbox = QVBoxLayout(self.main_container)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.setSpacing(4)
        self.main_scroll.setWidget(self.main_container)

    def set_data_list(self, data_list: list, data_type: str):
        if len(self.hot_search_item_list) != 0:
            for index, item in enumerate(data_list):
                self.hot_search_item_list[index].set_data(data=item, data_type=data_type)
        else:
            for item in data_list:
                widget = HotSearchItem(data=item, data_type=data_type,
                                       left_click_func=self.left_click_func, middle_click_func=self.middle_click_func)
                widget.setFont(self.font())
                self.vbox.addWidget(widget)
                self.hot_search_item_list.append(widget)
        # 滚动到顶部
        if self.main_scroll is not None:
            self.main_scroll.verticalScrollBar().setValue(0)


class TopSearchCard(MainCard):

    title = "热搜"
    name = "TopSearchCard"
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

    # tab列表
    tab_weibo = None
    tab_baidu = None
    tab_bilibili = None
    tab_zhihu = None
    tab_douyin = None
    tab_tencent = None
    tab_list = [
        [tab_weibo, "微博", "weibo"],
        [tab_baidu, "百度", "baidu"],
        [tab_bilibili, "B站", "bilibili"],
        [tab_zhihu, "知乎", "zhihu"],
        [tab_douyin, "抖音", "douyin"],
        [tab_tencent, "腾讯", "tencent"],
    ]
    tab_map = { "微博": "weibo", "百度": "baidu", "B站": "bilibili", "知乎": "zhihu", "抖音": "douyin", "腾讯": "tencent" }

    # 数据
    base_data_list = None
    base_time = None
    reply = None
    # 上次刷新时间
    last_load_time = 0
    load_interval_time = 30 * 60 * 1000                 # 加载间隔30分钟


    def __init__(self, main_object=None, parent=None, theme=None, card=None, cache=None, data=None,
                 toolkit=None, logger=None, save_data_func=None):
        super().__init__(main_object=main_object, parent=parent, theme=theme, card=card, cache=cache, data=data,
                         toolkit=toolkit, logger=logger, save_data_func=save_data_func)
        # 初始化网络管理器
        self.network_manager = QtNetwork.QNetworkAccessManager(self)

    def clear(self):
        try:
            self.network_manager.deleteLater()
            self.text_browser_top.setVisible(False)
            self.text_browser_top.deleteLater()
            self.label_top_area_number.setVisible(False)
            self.label_top_area_number.deleteLater()
            self.label_top_area_title.setVisible(False)
            self.label_top_area_title.deleteLater()
            self.label_weibo_time.setVisible(False)
            self.label_weibo_time.deleteLater()
            self.push_button_search_refresh.setVisible(False)
            self.push_button_search_refresh.deleteLater()
            self.tab_widget_toggle.setVisible(False)
            self.tab_widget_toggle.deleteLater()
            self.label_top_mask.setVisible(False)
            self.label_top_mask.deleteLater()
            self.load_animation.setVisible(False)
            self.load_animation.deleteLater()
        except Exception as e:
            print(e)
        super().clear()

    def init_ui(self):
        super().init_ui()
        # 字体
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        font3 = QFont()
        font3.setPointSize(10)
        font4 = QFont()
        font4.setPointSize(9)
        font4.setBold(False)
        tab_widget_height = 45
        self.main_layout = QVBoxLayout(self.card)
        self.main_layout.setContentsMargins(10, tab_widget_height + 1, 10, 10)
        self.main_layout.setSpacing(6)
        self.label_top_area_background_layout = QHBoxLayout()
        self.label_top_area_background_layout.setContentsMargins(5, 0, 5, 0)
        self.label_top_area_background_layout.setSpacing(5)
        # 标题背景
        self.label_top_area_background = QWidget()
        self.label_top_area_background.setObjectName(u"label_top_area_background")
        self.label_top_area_background.setFixedHeight(32)
        self.label_top_area_background.setLayout(self.label_top_area_background_layout)
        self.main_layout.addWidget(self.label_top_area_background)
        # 序号
        self.label_top_area_number = QLabel()
        self.label_top_area_number.setObjectName(u"label_top_area_number")
        self.label_top_area_number.setFont(font4)
        self.label_top_area_number.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.label_top_area_background_layout.addWidget(self.label_top_area_number)
        # 关键词
        self.label_top_area_title = QLabel()
        self.label_top_area_title.setObjectName(u"label_top_area_title")
        self.label_top_area_title.setFont(font4)
        self.label_top_area_title.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.label_top_area_background_layout.addWidget(self.label_top_area_title)
        self.label_top_area_background_layout.addStretch()
        # 时间
        self.label_weibo_time = QLabel()
        self.label_weibo_time.setObjectName(u"label_weibo_time")
        self.label_weibo_time.setFont(font4)
        self.label_weibo_time.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.label_top_area_background_layout.addWidget(self.label_weibo_time)
        # 刷新
        self.push_button_search_refresh = QPushButton()
        self.push_button_search_refresh.setObjectName(u"push_button_search_refresh")
        self.push_button_search_refresh.setFixedSize(32, 32)
        self.label_top_area_background_layout.addWidget(self.push_button_search_refresh)
        # 主要信息展示
        self.text_browser_top = HotSearchList(left_click_func=self.click_text_browser, middle_click_func=self.click_text_browser_not_active)
        self.text_browser_top.setObjectName(u"text_browser_top")
        self.text_browser_top.setFont(font3)
        self.main_layout.addWidget(self.text_browser_top)
        # 下方切换
        self.tab_widget_toggle = QTabWidget(self.card)
        self.tab_widget_toggle.setObjectName(u"tab_widget_toggle")
        self.tab_widget_toggle.setGeometry(QRect(0, 0, self.card.width(), self.card.height()))
        self.tab_widget_toggle.setFont(font1)
        self.tab_widget_toggle.setTabPosition(QTabWidget.TabPosition.North)
        self.tab_widget_toggle.setTabShape(QTabWidget.TabShape.Rounded)
        # 顶部遮罩层
        self.label_top_mask = QLabel(self.card)
        self.label_top_mask.setObjectName(u"label_top_mask")
        self.label_top_mask.setGeometry(QRect(0, 0, self.card.width(), self.card.height()))
        # 中心加载动画
        self.load_animation = LoadAnimation(self.card, self.theme)
        self.load_animation.setStyleSheet("background:transparent;border: 0px solid gray;")
        self.load_animation.setGeometry(QRect(self.card.width() / 2 - 60 / 2, self.card.height() / 2 - 60 / 2, 60, 60))
        # 样式调整
        style_util.set_tab_widget_style(self.tab_widget_toggle, self.is_dark())
        self.text_browser_top.setStyleSheet("""
        background-color: transparent;
        padding: 0px;
        margin: 0px;
        border-width: 0px;
        outline: none;
        """ + scroll_bar_style)
        # 文字
        self.label_top_area_number.setText("序号")
        self.label_top_area_title.setText("关键词")
        # 图标初始化
        self.push_button_search_refresh.setToolTip('刷新')
        # tab列表初始化
        for tab in self.tab_list:
            tab[0] = QWidget()
            tab[0].setObjectName(tab[1])
            self.tab_widget_toggle.addTab(tab[0], "")
            self.tab_widget_toggle.setTabText(self.tab_widget_toggle.indexOf(tab[0]), QCoreApplication.translate("Form", tab[1], None))
        self.tab_widget_toggle.setCurrentIndex(0)
        # 按钮事件绑定
        self.push_button_search_refresh.clicked.connect(self.push_button_search_refresh_click)
        self.tab_widget_toggle.currentChanged.connect(self.tab_widget_change)
        # 层叠
        self.tab_widget_toggle.raise_()
        self.text_browser_top.raise_()
        self.label_top_area_background.raise_()
        self.push_button_search_refresh.raise_()
        self.label_weibo_time.raise_()
        self.label_top_area_number.raise_()
        self.label_top_area_title.raise_()
        self.load_animation.raise_()
        self.label_top_mask.raise_()
        self.load_animation.hide()
        self.label_top_mask.hide()

    def refresh_data(self, date_time_str):
        super().refresh_data(date_time_str)

    def refresh_ui(self, date_time_str):
        super().refresh_ui(date_time_str)
        # 当前时间戳
        current_time = int(round(time.time() * 1000))
        # 上次时间戳
        last_time = self.last_load_time
        # 相隔x分钟内不进行重新加载
        if current_time - last_time < self.load_interval_time:
            return
        # 记录加载时间戳
        self.last_load_time = current_time
        print("热搜卡片开始刷新数据")
        self.send_network_request()
        super().refresh_ui_end(date_time_str)

    def send_network_request(self):
        """发送网络请求"""
        current_tab_title = self.tab_widget_toggle.tabText(self.tab_widget_toggle.currentIndex())
        current_tab_name = self.tab_map[current_tab_title]

        url = QUrl(common.BASE_URL + "/trending/normal/last?company=" + str(current_tab_name))
        request = QtNetwork.QNetworkRequest(url)
        # 存储token
        request.setRawHeader(b"Authorization", bytes(self.main_object.access_token, "utf-8"))

        # 显示加载动画
        self.label_top_mask.show()
        self.load_animation.show()
        self.load_animation.load()

        print("准备请求数据")
        self.reply = self.network_manager.get(request)
        self.reply.finished.connect(self.handle_network_reply)

    def handle_network_reply(self):
        """处理网络响应"""
        print("处理网络响应")
        try:
            if self.reply.error() != QtNetwork.QNetworkReply.NetworkError.NoError:
                self.logger.card_error("主程序", f"Error: {self.reply.errorString()}")
                return

            # 读取并解析数据
            data = self.reply.readAll().data()
            result = json.loads(data)

            self.base_data_list = []
            self.base_data_type = ""
            for data_entry in result["data"]:
                self.base_time = '刷新时间: ' + data_entry['updateDateStr']
                self.base_data_list = data_entry["content"]
                self.base_data_type = data_entry["company"]
            # 更新UI
            self.set_ui()
            self.logger.card_info("主程序", "数据更新成功")
        except Exception as e:
            self.logger.card_error("主程序", f"Error: {str(e)}")
        try:
            # 隐藏加载动画
            self.load_animation_end_call_back()
        except Exception as e:
            self.logger.card_error("主程序", f"Error: {str(e)}")
        # 在执行删除操作前，检查C++对象是否存活
        if self.reply is not None and my_shiboken_util.is_qobject_valid(self.reply):
            self.reply.deleteLater()
        self.reply = None

    def set_ui(self):
        try:
            self.label_weibo_time.setText(self.base_time)
            self.text_browser_top.set_data_list(self.base_data_list, self.base_data_type)
            style_util.set_font_and_right_click_style(self.main_object, self.text_browser_top)
            self.logger.card_info("主程序", "获取微博信息完成")
        except Exception as e:
            self.logger.card_error("主程序", "获取微博信息失败,错误信息:{}".format(e))

    def push_button_search_refresh_click(self):
        self.send_network_request()

    def load_animation_end_call_back(self):
        self.label_top_mask.hide()
        self.load_animation.hide()

    def click_text_browser(self, url):
        browser_util.open_url(url)

    def click_text_browser_not_active(self, url):
        # 当前时间戳
        current_time = int(round(time.time() * 1000))
        # 修改上次动画时间戳避免触发隐藏窗口动画
        self.main_object.animation_time = current_time
        # 打开浏览器
        browser_util.open_url(url)

    def tab_widget_change(self):
        self.send_network_request()

    def refresh_theme(self):
        if not super().refresh_theme():
            return False
        if self.is_light():
            text_color = "background-color: rgba(0, 0, 0, 0);color: rgba(0, 0, 0, 0.4);"
            self.label_top_area_background.setStyleSheet("background: rgb(255, 255, 255); border-radius: 10px;")
        else:
            text_color = "background-color: rgba(0, 0, 0, 0);color: rgba(255, 255, 255, 0.4);"
            self.label_top_area_background.setStyleSheet("background: rgb(0, 0, 0); border-radius: 10px;")
        style_util.set_card_button_style(self.push_button_search_refresh, "Arrows/redo", is_dark=self.main_object.is_dark)
        self.label_top_mask.setStyleSheet(u"background-color: transparent;")
        self.label_top_area_number.setStyleSheet(text_color)
        self.label_top_area_title.setStyleSheet(text_color)
        self.label_weibo_time.setStyleSheet(text_color)
        style_util.set_tab_widget_style(self.tab_widget_toggle, self.is_dark())
        self.load_animation.set_theme(self.is_light())
