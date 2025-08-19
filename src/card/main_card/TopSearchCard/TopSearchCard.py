import json

from PySide6.QtCore import QCoreApplication, QRect, Qt, QUrl
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel, QPushButton, QTabWidget, QTextBrowser, QWidget
from PySide6 import QtNetwork
# 获取信息
from src.card.MainCardManager.MainCard import MainCard
from src.client import common
from src.get_info import get_tophub_blog_info, get_micro_blog_info
from src.util import browser_util
from src.ui import style_util
from src.component.LoadAnimation.LoadAnimation import LoadAnimation


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
    base_html = None
    base_time = None


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
        # 主要信息展示
        self.text_browser_top = QTextBrowser(self.card)
        self.text_browser_top.setObjectName(u"text_browser_top")
        self.text_browser_top.setGeometry(QRect(20, 30 + tab_widget_height, self.card.width() - 40, self.card.height() - tab_widget_height - 50))
        self.text_browser_top.setFont(font3)
        # 序号
        self.label_top_area_number = QLabel(self.card)
        self.label_top_area_number.setObjectName(u"label_top_area_number")
        self.label_top_area_number.setGeometry(QRect(0, tab_widget_height, 41, 32))
        self.label_top_area_number.setFont(font4)
        self.label_top_area_number.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        # 关键词
        self.label_top_area_title = QLabel(self.card)
        self.label_top_area_title.setObjectName(u"label_top_area_title")
        self.label_top_area_title.setGeometry(QRect(40, tab_widget_height, 51, 32))
        self.label_top_area_title.setFont(font4)
        self.label_top_area_title.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        # 时间
        self.label_weibo_time = QLabel(self.card)
        self.label_weibo_time.setObjectName(u"label_weibo_time")
        self.label_weibo_time.setGeometry(QRect(self.card.width() - 270, tab_widget_height, 221, 32))
        self.label_weibo_time.setFont(font4)
        self.label_weibo_time.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        # 刷新
        self.push_button_search_refresh = QPushButton(self.card)
        self.push_button_search_refresh.setObjectName(u"push_button_search_refresh")
        self.push_button_search_refresh.setGeometry(QRect(self.card.width() - 44, tab_widget_height, 32, 32))
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
        QTextBrowser {
            background-color: transparent;
            padding: 0px;
            margin: 0px;
            border-width: 0px;
            outline: none;
        }
        """ + style_util.scroll_bar_style)
        # 设置浏览器不打开链接和没有滚动条
        # 关键步骤：设置文档的CSS，去除焦点时的虚线边框
        self.text_browser_top.setFocusPolicy(Qt.TabFocus)
        self.text_browser_top.setReadOnly(True)
        self.text_browser_top.setOpenLinks(False)
        self.text_browser_top.setOpenExternalLinks(False)
        self.text_browser_top.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)   # 禁止水平滚动
        # self.text_browser_top.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)   # 禁止垂直滚动
        self.text_browser_top.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
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
        self.text_browser_top.anchorClicked.connect(self.click_textbrowser)
        # 层叠
        self.tab_widget_toggle.raise_()
        self.text_browser_top.raise_()
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
        reply = self.network_manager.get(request)
        reply.finished.connect(lambda: self.handle_network_reply(reply))

    def handle_network_reply(self, reply):
        """处理网络响应"""
        print("处理网络响应")
        try:
            # 隐藏加载动画
            self.load_animation_end_call_back()

            if reply.error() != QtNetwork.QNetworkReply.NetworkError.NoError:
                self.logger.card_error("主程序", f"Error: {reply.errorString()}")
                return

            # 读取并解析数据
            data = reply.readAll().data()
            result = json.loads(data)

            # 处理数据
            self.base_html = ""
            for data_entry in result["data"]:
                self.base_time = '刷新时间: ' + data_entry['updateDateStr']
                self.base_html = get_tophub_blog_info.get_html(
                    data_entry["content"],
                    data_entry["company"],
                    self.logger
                )
                self.base_html = get_micro_blog_info.change_css(self.base_html)

            # 更新UI
            self.set_ui()
            self.logger.card_info("主程序", "数据更新成功")

        except Exception as e:
            self.logger.card_error("主程序", f"Error: {str(e)}")
        finally:
            reply.deleteLater()

    def set_ui(self):
        try:
            self.label_weibo_time.setText(self.base_time)
            self.text_browser_top.setHtml(self.base_html)
            self.text_browser_top.document().setDefaultStyleSheet("a:focus { outline: none; }")
            self.logger.card_info("主程序", "获取微博信息完成")
        except Exception as e:
            self.logger.card_error("主程序", "获取微博信息失败,错误信息:{}".format(e))

    def push_button_search_refresh_click(self):
        self.send_network_request()

    def load_animation_end_call_back(self):
        self.label_top_mask.hide()
        self.load_animation.hide()

    def click_textbrowser(self, url):
        browser_util.open_url(url.toString())

    def tab_widget_change(self):
        self.send_network_request()

    def refresh_theme(self):
        if not super().refresh_theme():
            return False
        if self.is_light():
            self.push_button_search_refresh.setStyleSheet(
                style_util.card_button_style.replace("{image}", "Arrows/redo"))
            # self.label_top_mask.setStyleSheet(u"background-color: rgba(255, 255, 255, 160);")
            text_color = "background-color: rgba(0, 0, 0, 0);color: rgba(0, 0, 0, 0.4);"
        else:
            self.push_button_search_refresh.setStyleSheet(
                style_util.card_button_dark_style.replace("{image}", "Arrows/redo"))
            # self.label_top_mask.setStyleSheet(u"background-color: rgba(0, 0, 0, 160);")
            text_color = "background-color: rgba(0, 0, 0, 0);color: rgba(255, 255, 255, 0.4);"
        self.label_top_mask.setStyleSheet(u"background-color: transparent;")
        self.label_top_area_number.setStyleSheet(text_color)
        self.label_top_area_title.setStyleSheet(text_color)
        self.label_weibo_time.setStyleSheet(text_color)
        style_util.set_tab_widget_style(self.tab_widget_toggle, self.is_dark())
        self.load_animation.set_theme(self.is_light())
