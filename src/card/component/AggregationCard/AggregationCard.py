import re
from PySide6 import QtWidgets, QtCore, QtGui, QtNetwork
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import QCoreApplication, QRect, QSize, Qt
from PySide6.QtWidgets import QTabWidget, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QScrollArea
# 获取信息
from src.card.MainCardManager.MainCard import MainCard
from src.module import dialog_module
from src.ui import style_util


class AggregationCard(MainCard):
    title = "聚合"
    name = "AggregationCard"
    support_size_list = ["Big"]
    # 只读参数
    x = None  # 坐标x
    y = None  # 坐标y
    size = None  # 大小(1_1:Point、1_2:MiniHor、2_1MiniVer、2_2Block、2_5)
    theme = None  # 主题(Light、Dark)
    width = 0  # 宽度
    height = 0  # 高度
    fillet_corner = 0  # 圆角大小
    # 可使用
    card = None  # 卡片本体
    data = None  # 数据
    toolkit = None  # 工具箱，具体参考文档
    logger = None  # 日志记录工具
    # 可调用
    save_data_func = None  # 保存数据(传参为一个字典)
    #
    is_first = True
    need_refresh_ui = False
    # 模块种类
    module_category_text = "Text"
    module_category_image = "Image"
    module_category_browser = "Browser"
    module_category_qt = "Qt"
    # 模块列表
    aggregation_module_list = [
        {
            "category": module_category_text,
            "type": "类型",
            "title": "标题",
            "des": "解释",
            "content": "内容",
            "icon": "图标",
            "call_back_func": None
        },
    ]
    module_tab_map = {
        "类型": None
    }
    model_index_map = {}
    # 对话框列表
    dialog_list = []
    # 新增：记录已加载的分类
    loaded_tabs = set()

    def __init__(self, main_object=None, parent=None, theme=None, card=None, cache=None, data=None,
                 toolkit=None, logger=None, save_data_func=None):
        super().__init__(main_object=main_object, parent=parent, theme=theme, card=card, cache=cache, data=data,
                         toolkit=toolkit, logger=logger, save_data_func=save_data_func)
        self.current_show_panel_type = None
        self.util_app = None

    def clear(self):
        try:
            self.aggregation_tab_widget.setVisible(False)
            self.aggregation_tab_widget.deleteLater()
        except Exception as e:
            print(e)
        super().clear()

    def init_ui(self):
        super().init_ui()
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        # 创建堆栈窗口
        self.stacked_widget = QtWidgets.QStackedWidget(self.card)
        self.stacked_widget.setGeometry(QtCore.QRect(0, 0, self.card.width(), self.card.height()))
        # 分类面板
        self.aggregation_tab = QWidget(self.card)
        # 分类面板面板增加竖向布局
        self.aggregation_tab_layout = QVBoxLayout(self.card)
        self.aggregation_tab_layout.setSpacing(0)
        self.aggregation_tab_layout.setContentsMargins(0, 0, 0, 0)
        self.aggregation_tab.setLayout(self.aggregation_tab_layout)
        # 顶部信息条
        self.info_bar = QLabel()
        self.info_bar.setAlignment(Qt.AlignCenter)
        self.info_bar.setFixedHeight(25)
        self.info_bar.setStyleSheet("background: transparent; border: none; font-weight: bold; font-size: 12px;")
        self.aggregation_tab_layout.addWidget(self.info_bar)
        self.info_bar.hide()
        # 下方切换
        self.aggregation_tab_widget = QTabWidget(self.card)
        self.aggregation_tab_widget.setObjectName(u"aggregation_tab_widget")
        self.aggregation_tab_widget.setGeometry(QRect(0, 0, self.card.width(), self.card.height()))
        self.aggregation_tab_widget.setFont(font1)
        self.aggregation_tab_widget.setTabPosition(QTabWidget.North)
        self.aggregation_tab_widget.setTabShape(QTabWidget.Rounded)
        self.aggregation_tab_layout.addWidget(self.aggregation_tab_widget)
        # 点击进入的面板
        self.show_panel = QWidget(self.card)
        self.show_panel.setObjectName(u"show_panel")
        self.show_panel.setGeometry(QRect(0, 0, self.card.width(), self.card.height()))
        self.show_panel.setStyleSheet("background: transparent; border: none;")
        # 面板增加竖向布局
        self.show_panel_layout = QVBoxLayout(self.show_panel)
        self.show_panel_layout.setSpacing(10)
        self.show_panel_layout.setContentsMargins(10, 10, 10, 10)
        # 顶部左侧返回按钮
        button_style = """
        QPushButton { border-radius: 10px; background-color: transparent; border: 1px solid #888888; padding-left: 2px; padding-right: 2px;}
        QPushButton:hover { background-color: rgba(0, 0, 0, 0.1); }
        QPushButton:pressed { background-color: rgba(0, 0, 0, 0.2); }
        """
        self.show_panel_back_button = QtWidgets.QPushButton()
        self.show_panel_back_button.setMinimumHeight(20)
        self.show_panel_back_button.setMinimumHeight(20)
        self.show_panel_back_button.setObjectName("show_panel_back_button")
        self.show_panel_back_button.setText("返回")
        self.show_panel_back_button.setStyleSheet(button_style)
        # 顶部标题栏
        self.show_panel_head = QWidget()
        self.show_panel_head.setObjectName("show_panel_content_panel")
        self.show_panel_head.setStyleSheet(f"background: transparent; border: none;")
        self.show_panel_head.setMaximumHeight(30)
        # 顶部标题布局
        font = QtGui.QFont()
        font.setPointSize(10)
        self.show_panel_label_title = QLabel()
        self.show_panel_label_title.setText("暂无标题")
        self.show_panel_label_title.setFont(font)
        self.show_panel_label_title.setStyleSheet("background: transparent; border: none;")
        # 顶部右侧隐藏按钮
        self.show_panel_hide_button = QtWidgets.QPushButton()
        self.show_panel_hide_button.setMinimumHeight(20)
        self.show_panel_hide_button.setMinimumHeight(20)
        self.show_panel_hide_button.setObjectName("show_panel_hide_button")
        self.show_panel_hide_button.setStyleSheet(button_style)
        # 顶部右侧隐藏按钮
        self.show_panel_hide_button_2 = QtWidgets.QPushButton()
        self.show_panel_hide_button_2.setMinimumHeight(20)
        self.show_panel_hide_button_2.setMinimumHeight(20)
        self.show_panel_hide_button_2.setObjectName("show_panel_hide_button_2")
        self.show_panel_hide_button_2.setStyleSheet(button_style)
        # 顶部布局
        self.show_panel_head_layout = QHBoxLayout()
        self.show_panel_head_layout.setSpacing(5)
        self.show_panel_head_layout.setContentsMargins(5, 5, 5, 5)
        self.show_panel_head_layout.addWidget(self.show_panel_back_button)
        self.show_panel_head_layout.addStretch()
        self.show_panel_head_layout.addWidget(self.show_panel_label_title)
        self.show_panel_head_layout.addStretch()
        self.show_panel_head_layout.addWidget(self.show_panel_hide_button)
        self.show_panel_head_layout.addWidget(self.show_panel_hide_button_2)
        self.show_panel_head.setLayout(self.show_panel_head_layout)
        self.show_panel_layout.addWidget(self.show_panel_head)
        # 下面增加一个内容面板
        self.show_panel_content_panel = QWidget()
        self.show_panel_content_panel.setObjectName("show_panel_content_panel")
        self.show_panel_layout.addWidget(self.show_panel_content_panel, 1)
        # 将现有的分类列表和展示面板添加到堆栈中
        self.stacked_widget.addWidget(self.aggregation_tab)  # 索引0 - 分类列表
        self.stacked_widget.addWidget(self.show_panel)  # 索引1 - 展示面板
        # 默认显示分类列表
        self.stacked_widget.setCurrentIndex(0)
        # 事件
        self.show_panel_back_button.clicked.connect(self.back_to_aggregation_tab)
        # 新增：监听tab切换事件
        self.aggregation_tab_widget.currentChanged.connect(self.on_tab_changed)

    def on_tab_changed(self, index):
        """切换tab时加载对应分类的按钮"""
        if index < 0 or index >= self.aggregation_tab_widget.count():
            return

        # 获取当前tab的类型
        tab_text = self.aggregation_tab_widget.tabText(index).strip()

        # 如果该分类尚未加载，则加载
        if tab_text not in self.loaded_tabs:
            self.load_tab_buttons(tab_text)
            self.loaded_tabs.add(tab_text)

    def back_to_aggregation_tab(self):
        # 切换到分类列表
        self.stacked_widget.setCurrentIndex(0)
        # 清空面板
        self.clear_show_panel()

    def clear_show_panel(self):
        # 解绑事件
        try:
            self.show_panel_hide_button.clicked.disconnect()
        except Exception as e:
            print(e)
        try:
            self.show_panel_hide_button_2.clicked.disconnect()
        except Exception as e:
            print(e)
        # 删除子控件
        layout = self.show_panel_content_panel.layout()
        if layout is not None:
            # 递归删除所有子控件
            self._clear_layout(layout)
            # 删除布局本身
            layout.deleteLater()
            # 从widget中移除布局引用
            self.show_panel_content_panel.setLayout(None)
        self.util_app = None

    def _clear_layout(self, layout):
        """递归清除布局中的所有控件"""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                # 删除控件
                widget.deleteLater()
            else:
                # 如果是子布局，递归清除
                child_layout = item.layout()
                if child_layout is not None:
                    self._clear_layout(child_layout)

    def init_tab_widget(self):
        # 初始化tab组信息
        self.init_module_tab_map()
        # tab列表初始化
        for tab_type, tab_info in self.module_tab_map.items():
            tab_info["scroll_area"].setObjectName(self.name + "_" + tab_type)
            self.aggregation_tab_widget.addTab(tab_info["scroll_area"], "")
            self.aggregation_tab_widget.setTabText(self.aggregation_tab_widget.indexOf(tab_info["scroll_area"]),
                                                   QCoreApplication.translate("Form", " " + tab_type + " ", None))
        self.aggregation_tab_widget.setCurrentIndex(0)
        # 模块字典index
        self.model_index_map = {}
        for key in self.module_tab_map:
            self.model_index_map[key] = 0

        # 修改：只加载第一个分类的按钮
        if self.aggregation_tab_widget.count() > 0:
            first_tab_text = self.aggregation_tab_widget.tabText(0).strip()
            self.load_tab_buttons(first_tab_text)
            self.loaded_tabs.add(first_tab_text)

    def load_tab_buttons(self, tab_type):
        """加载指定分类的按钮"""
        # 找到属于该分类的所有模块
        tab_modules = [m for m in self.aggregation_module_list if m["type"] == tab_type]

        # 为每个模块生成按钮
        for aggregation_module in tab_modules:
            button_index, button, image_label, label_title, label_des = self.gen_button(aggregation_module)
            aggregation_module["button_index"] = button_index
            aggregation_module["button"] = button
            aggregation_module["image_label"] = image_label
            aggregation_module["label_title"] = label_title
            aggregation_module["label_des"] = label_des

        # 根据模块数量调整按钮宽度(为了适配超出时出现的滚动条)
        if len(tab_modules) > 14:
            interval = 10  # 间隔
            for aggregation_module in tab_modules:
                button = aggregation_module["button"]
                width = int((self.card.width() - interval * 3) / 2) - 15  # 减去边距和间隔
                height = 63
                button.setMinimumSize(QSize(width, height))
                button.setMaximumSize(QSize(width, height))

    def init_module_tab_map(self):
        self.module_tab_map = {}
        for aggregation_module in self.aggregation_module_list:
            if aggregation_module["type"] in self.module_tab_map:
                continue

            # 创建滚动区域
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
            scroll_area.setStyleSheet(style_util.scroll_bar_style)

            # 创建内容容器
            content_widget = QWidget()
            content_layout = QVBoxLayout(content_widget)
            content_layout.setSpacing(10)
            content_layout.setContentsMargins(10, 10, 10, 10)
            content_layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)  # 设置靠左靠上对齐

            # 设置滚动区域的内容部件
            scroll_area.setWidget(content_widget)

            self.module_tab_map[aggregation_module["type"]] = {
                "scroll_area": scroll_area,
                "content_widget": content_widget,
                "content_layout": content_layout
            }

    def gen_button(self, aggregation_module):
        interval = 10  # 间隔
        width = int((self.card.width() - interval * 3) / 2) - 10  # 减去边距和间隔
        height = 63

        # 获取当前类型的tab信息
        tab_info = self.module_tab_map[aggregation_module["type"]]
        self.model_index_map[aggregation_module["type"]] += 1
        index = self.model_index_map[aggregation_module["type"]]

        # 每两个按钮需要创建一个水平布局容器
        if index % 2 == 1:
            # 创建新的水平布局容器
            button_row_widget = QWidget()
            button_row_layout = QHBoxLayout(button_row_widget)
            button_row_layout.setSpacing(10)
            button_row_layout.setContentsMargins(0, 0, 0, 0)
            button_row_layout.setAlignment(QtCore.Qt.AlignLeft)  # 设置靠左对齐
            tab_info["content_layout"].addWidget(button_row_widget)

        # 首先生成按钮本体
        button = QPushButton()
        button.setObjectName(u"push_button_aggregation_" + str(index))
        button.setMinimumSize(QSize(width, height))
        button.setMaximumSize(QSize(width, height))

        # 在按钮内创建一个布局
        button_layout = QHBoxLayout(button)
        button_layout.setContentsMargins(5, 5, 5, 5)  # 设置布局的外边距为9
        button_layout.setSpacing(3)  # 设置布局的控件间距为0

        # 布局左边是一个图标
        label_image = QLabel(button)
        label_image.setObjectName(u"label_image")
        label_image.setMinimumSize(QSize(36, 36))
        label_image.setMaximumSize(QSize(36, 36))
        label_image.setStyleSheet(u"border-style: solid;\n"
                                  "border-radius: 18px;\n"
                                  "border: 0px solid black;\n"
                                  "border-color: rgb(0, 0, 0);\n"
                                  "background: " + self.toolkit.color.get_rgba_color(index, 100) + ";\n"
                                                                                                   "padding: 5px;")
        # if ".svg" in aggregation_module["icon"]:
        #     image_path = "static/img/IconPark/svg/" + aggregation_module["icon"]
        #     try:
        #         label_image.setPixmap(self.toolkit.image_util.load_light_svg(image_path))
        #     except Exception as e:
        #         print("加载svg报错:{}".format(e))
        #         pass
        label_image.setScaledContents(True)
        button_layout.addWidget(label_image)

        # 布局的右边是一个布局，上面是标题，下面是描述
        button_right_layout = QVBoxLayout()
        button_right_layout.setContentsMargins(0, 8, 0, 8)  # 设置布局的外边距为9
        button_right_layout.setSpacing(6)  # 设置布局的控件间距为0
        font_title = QFont()
        font_title.setPointSize(10)
        label_title = QLabel(button)
        label_title.setObjectName(u"label_title")
        label_title.setFont(font_title)
        label_title.setText(aggregation_module["title"])
        label_title.setStyleSheet("background: transparent;")
        button_right_layout.addWidget(label_title)
        font_des = QFont()
        font_des.setPointSize(8)
        label_des = QLabel(button)
        label_des.setObjectName(u"label_des")
        label_des.setFont(font_des)
        label_des.setText(aggregation_module["des"])
        label_des.setStyleSheet("background: transparent;")
        button_right_layout.addWidget(label_des)
        button_layout.addLayout(button_right_layout)

        # 将按钮添加到当前行的布局中
        current_row_layout = tab_info["content_layout"].itemAt(tab_info["content_layout"].count() - 1).widget().layout()
        current_row_layout.addWidget(button)

        # 按钮绑定
        if 'call_back_func' in aggregation_module and aggregation_module["call_back_func"] is not None:
            button.clicked.connect(aggregation_module["call_back_func"])
        else:
            if aggregation_module["category"] == self.module_category_text:
                button.clicked.connect(lambda: self.push_button_text_click(aggregation_module))
            elif aggregation_module["category"] == self.module_category_image:
                button.clicked.connect(lambda: self.push_button_image_click(aggregation_module))
            elif aggregation_module["category"] == self.module_category_browser:
                button.clicked.connect(lambda: self.push_button_browser_click(aggregation_module))
            elif aggregation_module["category"] == self.module_category_qt:
                button.clicked.connect(aggregation_module["call_back_func"])

        # 设置按钮和标签样式
        self.set_button_and_des(button, label_des, index)
        # 图标
        self.set_image_icon(label_image, aggregation_module)
        return index, button, label_image, label_title, label_des

    def refresh_data(self, date_time_str):
        super().refresh_data(date_time_str)

    def refresh_ui(self, date_time_str):
        super().refresh_ui(date_time_str)
        super().refresh_ui_end(date_time_str)

    def push_button_text_click(self, aggregation_module):
        try:
            title = aggregation_module["title"]
            content = aggregation_module["content"]
            dialog = self.toolkit.text_box_util.show_text_dialog(self.main_object, title, content)
            self.dialog_list.append(dialog)
        except Exception as e:
            print(e)
            self.main_object.logger.card_error("聚合卡片", f"获取{str(aggregation_module)}失败,请稍后重试")
            dialog_module.box_information(self.main_object, "错误信息", f"获取{str(aggregation_module)}失败,请稍后重试")

    def push_button_image_click(self, aggregation_module):
        try:
            title = aggregation_module["title"]
            content = aggregation_module["content"]
            link = None
            if "link" in aggregation_module:
                link = aggregation_module["link"]
            dialog = self.toolkit.image_box_util.show_image_dialog(self.main_object, title, content, link)
            self.dialog_list.append(dialog)
        except Exception as e:
            print(e)
            self.main_object.logger.card_error("聚合卡片", f"获取{str(aggregation_module)}失败,请稍后重试")
            dialog_module.box_information(self.main_object, "错误信息", f"获取{str(aggregation_module)}失败,请稍后重试")

    def push_button_browser_click(self, aggregation_module):
        try:
            self.toolkit.browser_util.open_url(aggregation_module["content"]["url"])
        except Exception as e:
            print(e)
            self.main_object.logger.card_error("聚合卡片", f"获取{str(aggregation_module)}失败,请稍后重试")
            dialog_module.box_information(self.main_object, "错误信息", f"获取{str(aggregation_module)}失败,请稍后重试")

    def refresh_theme(self):
        if self.before_theme is not None and self.before_theme == self.theme:
            # 重复不刷新
            return False
        self.before_theme = self.theme
        self.refresh_theme_real()

    def refresh_theme_real(self):
        for aggregation_module in self.aggregation_module_list:
            if "button_index" not in aggregation_module:
                break
            button_index = aggregation_module["button_index"]
            button = aggregation_module["button"]
            image_label = aggregation_module["image_label"]
            label_title = aggregation_module["label_title"]
            label_title.setStyleSheet("background: transparent; color: {};".format(self.get_prospect_color(rgb=True)))
            label_des = aggregation_module["label_des"]
            # 设置按钮和标签样式
            self.set_button_and_des(button, label_des, button_index)
            # 图标
            self.set_image_icon(image_label, aggregation_module)
            # 样式
            style_util.set_tab_widget_style(self.aggregation_tab_widget, self.is_dark())
        # 展示面板左上角按钮图标
        style_util.set_button_style(self.show_panel_back_button, icon_path="Edit/return",
                                    is_dark=self.is_dark(), style_change=False)
        style_util.set_button_style(self.show_panel_hide_button, icon_path="Base/preview-open",
                                    is_dark=self.is_dark(), style_change=False)
        style_util.set_button_style(self.show_panel_hide_button_2, icon_path="Office/copy-one",
                                    is_dark=self.is_dark(), style_change=False)
        # 显示面板背景
        if self.is_dark():
            self.show_panel_content_panel.setStyleSheet(
                f"background: rgba(24, 24, 24, 150); border-radius: 10px; border: none; padding: 10px;")
        else:
            self.show_panel_content_panel.setStyleSheet(
                f"background: rgba(255, 255, 255, 150); border-radius: 10px; border: none; padding: 10px;")

    def set_image_icon(self, image_label, aggregation_module):
        if aggregation_module["icon"] is not None:
            # 图标路径存在
            icon_path = aggregation_module["icon"]
            if icon_path.startswith("http"):
                self.fetch_icon(icon_path, image_label)
            elif "png:" in icon_path:
                # 加载png图片
                image_end_path = icon_path.replace("png:", "")
                image_label.setPixmap(QPixmap(":static/img/IconPark/png/" + image_end_path))
            else:
                image_label.setPixmap(style_util.get_pixmap_by_path(icon_path, is_dark=self.is_dark()))
        else:
            # 图标路径不存在，首先加载默认图标
            image_label.setPixmap(style_util.get_pixmap_by_path("Travel/planet", is_dark=self.is_dark()))
            # 然后根据网页地址加载图片
            if "content" in aggregation_module and "url" in aggregation_module["content"]:
                url = aggregation_module["content"]["url"]
                # 根据网页地址加载网页图标地址
                self.load_url_icon(url, image_label)

    def set_button_and_des(self, button, label_des, button_index):
        button_style = """
            QPushButton {
                border-style: solid;
                border-radius: 10px;
                border: none;
                background-color: {background-color};
            }
            QPushButton:hover {
                background: {hover-background-color};
            }
            """
        if self.is_dark():
            button.setStyleSheet(button_style
                                 .replace("{background-color}", self.toolkit.color.get_rgba_color(button_index, 50))
                                 .replace("{hover-background-color}",
                                          self.toolkit.color.get_rgba_color(button_index, 20)))
            label_des.setStyleSheet("background: transparent; color: rgba(239, 240, 241, 150);")
        else:
            button.setStyleSheet(button_style
                                 .replace("{background-color}", self.toolkit.color.get_rgba_color(button_index, 50))
                                 .replace("{hover-background-color}",
                                          self.toolkit.color.get_rgba_color(button_index, 20)))
            label_des.setStyleSheet("background: transparent; color: rgba(24, 24, 24, 150);")

    def load_url_icon(self, url, image_label):
        # 创建网络访问管理器
        self.network_manager = QtNetwork.QNetworkAccessManager(self)
        self.network_manager.setCache(self.main_object.network_disk_cache)
        self.network_manager.finished.connect(lambda reply: self.handle_icon_response(reply, image_label, url))

        # 首先尝试从网页的HTML中获取shortcut图标链接
        request = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
        request.setAttribute(QtNetwork.QNetworkRequest.RedirectPolicyAttribute,
                             QtNetwork.QNetworkRequest.NoLessSafeRedirectPolicy)
        self.network_manager.get(request)

    def handle_icon_response(self, reply, image_label, original_url):
        try:
            if reply.error() == QtNetwork.QNetworkReply.NoError:
                # 获取网页内容
                html_content = str(reply.readAll(), 'utf-8')

                # 使用正则表达式查找图标链接
                icon_url = None

                # 查找rel属性包含icon或shortcut的link标签
                icon_patterns = [
                    r'<link[^>]*rel=("icon"|\'icon\'|"shortcut icon"|\'shortcut icon\'|"apple-touch-icon"|\'apple-touch-icon\')[^>]*href=("([^"]*)"|\'([^\']*)\')',
                    r'<link[^>]*href=("([^"]*)"|\'([^\']*)\')[^>]*rel=("icon"|\'icon\'|"shortcut icon"|\'shortcut icon\'|"apple-touch-icon"|\'apple-touch-icon\')'
                ]

                for pattern in icon_patterns:
                    match = re.search(pattern, html_content, re.IGNORECASE)
                    if match:
                        # 获取匹配的href值
                        icon_url = match.group(2) or match.group(3) or match.group(4) or match.group(5)
                        if icon_url:
                            break

                if icon_url:
                    # 去除引号
                    icon_url = icon_url.strip("'\"")
                    # 将相对URL转换为绝对URL
                    base_url = QtCore.QUrl(original_url)
                    absolute_icon_url = base_url.resolved(QtCore.QUrl(icon_url))
                    print("加载图标地址: " + absolute_icon_url.toString())
                    self.fetch_icon(absolute_icon_url.toString(), image_label)
                else:
                    # 如果没有找到图标链接，尝试访问网站首页
                    base_url = QtCore.QUrl(original_url)
                    home_url = f"{base_url.scheme()}://{base_url.host()}"
                    if original_url != home_url:
                        self.load_url_icon(home_url, image_label)
                    else:
                        # 如果已经是首页，尝试访问默认的根目录favicon.ico
                        favicon_url = f"{home_url}/favicon.ico"
                        print("加载图标地址: " + favicon_url)
                        self.fetch_icon(favicon_url, image_label)
            else:
                print("请求失败: " + reply.errorString())
                # 如果请求失败，尝试访问默认的根目录favicon.ico
                base_url = QtCore.QUrl(original_url)
                home_url = f"{base_url.scheme()}://{base_url.host()}"
                favicon_url = f"{home_url}/favicon.ico"
                print("加载图标地址: " + favicon_url)
                self.fetch_icon(favicon_url, image_label)

        except Exception as e:
            print(f"Error parsing HTML: {e}")
            # 如果解析失败，尝试访问默认的根目录favicon.ico
            base_url = QtCore.QUrl(original_url)
            home_url = f"{base_url.scheme()}://{base_url.host()}"
            favicon_url = f"{home_url}/favicon.ico"
            print("加载图标地址: " + favicon_url)
            self.fetch_icon(favicon_url, image_label)

        finally:
            reply.deleteLater()

    def fetch_icon(self, icon_url, image_label):
        # 创建新的网络请求获取图标
        icon_network_manager = QtNetwork.QNetworkAccessManager(self)
        icon_network_manager.setCache(self.main_object.network_disk_cache)
        icon_network_manager.finished.connect(lambda reply: self.handle_icon_data(reply, image_label))

        request = QtNetwork.QNetworkRequest(QtCore.QUrl(icon_url))
        request.setAttribute(QtNetwork.QNetworkRequest.RedirectPolicyAttribute,
                             QtNetwork.QNetworkRequest.NoLessSafeRedirectPolicy)
        icon_network_manager.get(request)

    def handle_icon_data(self, reply, image_label):
        try:
            if reply.error() == QtNetwork.QNetworkReply.NoError:
                # 获取图标数据
                icon_data = reply.readAll()

                # 将图标数据转换为QPixmap
                pixmap = QtGui.QPixmap()
                if pixmap.loadFromData(icon_data):
                    # 缩放图标到合适大小
                    scaled_pixmap = pixmap.scaled(36, 36, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                    image_label.setPixmap(scaled_pixmap)
                else:
                    # 如果加载失败，设置默认图标
                    self.set_default_icon(image_label)
            else:
                # 如果请求失败，设置默认图标
                self.set_default_icon(image_label)

        except Exception as e:
            print(f"Error loading icon: {e}")
            self.set_default_icon(image_label)

        finally:
            reply.deleteLater()

    def set_default_icon(self, image_label):
        # 设置默认图标
        image_label.setPixmap(style_util.get_pixmap_by_path("Travel/planet", is_dark=self.is_dark()))