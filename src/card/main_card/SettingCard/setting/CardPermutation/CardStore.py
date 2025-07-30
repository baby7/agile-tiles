# coding:utf-8
import json
import os

from PySide6 import QtCore, QtWidgets, QtGui, QtNetwork
from PySide6.QtCore import Signal, Qt, QSize
from PySide6.QtGui import QIcon, QCursor

from src.card.main_card.SettingCard.setting.CardPermutation.CardDetailWidget import CardDetailWidget
from src.ui import style_util
from src.client import card_store_client


class CardStore(QtWidgets.QWidget):
    cardAdded = Signal(dict)  # 新增信号用于传递卡片数据
    storeClose = Signal(dict)  # 新增信号用于传递卡片数据
    before_plugin_map = []
    card_store_client = None

    def __init__(self, parent=None, use_parent=None, is_dark=False):
        super().__init__(parent)
        self.card_permutation = parent
        self.use_parent = use_parent
        self.card_widgets = {}  # 新增：用字典存储所有卡片widget {card_name: [widget1, widget2]}
        self.before_plugin_map = get_plugin_folder_map()
        self.is_dark = is_dark
        self.card_store_data = []
        self.network_manager = QtNetwork.QNetworkAccessManager(self)  # 新增网络管理器
        self.init_ui()
        # 加载卡片列表
        self.card_store_client = card_store_client.CardStoreClient(self.use_parent)
        self.card_store_client.card_list_received.connect(self.load_store_card_finished)
        self.card_store_client.fetch_card_store_list()
        # 图片缓存
        self.image_cache = {}  # 图片缓存字典
        self.pending_images = []  # 待加载图片队列
        self.image_loading_timer = QtCore.QTimer(self)
        self.image_loading_timer.setInterval(100)  # 每100ms处理一个图片
        self.image_loading_timer.timeout.connect(self.load_next_image)
        # 详情窗口
        self.view_card_detail_widget = None

    def init_ui(self):
        # 基础样式设置
        self.setGeometry(QtCore.QRect(0, 0, self.parent().width(), self.parent().height()))
        # 主容器
        main_widget = QtWidgets.QWidget(self)
        main_widget.setGeometry(QtCore.QRect(
            int(self.width() * 0.1),
            int(self.height() * 0.05),
            int(self.width() * 0.8),
            int(self.height() * 0.9)
        ))
        main_widget.setStyleSheet(f"""
            background-color: {'rgba(34, 34, 34, 255)' if self.is_dark else 'rgba(255, 255, 255, 160)'};
            border-radius: 15px;
            color: {'rgba(255, 255, 255, 160)' if self.is_dark else 'rgba(34, 34, 34, 255)'};
        """)

        # 主布局
        main_layout = QtWidgets.QVBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # 顶部工具栏
        top_layout = QtWidgets.QHBoxLayout()
        close_btn = self.create_close_button()
        top_layout.addItem(
            QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        top_layout.addWidget(close_btn)
        main_layout.addLayout(top_layout)

        # Tab组件
        self.tab_widget = QtWidgets.QTabWidget()
        style_util.set_tab_widget_style(self.tab_widget, self.is_dark)
        # self.init_store_card_list()
        main_layout.addWidget(self.tab_widget)

    def load_store_card_finished(self, response):
        print(f"response:{response}")
        self.card_store_data = response
        self.init_store_card_list()

    def create_close_button(self):
        btn = QtWidgets.QPushButton()
        btn.setIcon(self.get_icon(icon_path="Character/close-one", custom_theme="red"))
        btn.setIconSize(QSize(20, 20))
        btn.setStyleSheet("background: transparent;")
        btn.clicked.connect(self.close_store)
        btn.setCursor(QCursor(Qt.PointingHandCursor))     # 鼠标手形
        return btn

    def close_store(self):
        self.card_widgets.clear()
        self.storeClose.emit("")
        self.hide()

    def get_icon(self, icon_path, custom_theme=None):
        if custom_theme is not None:
            theme = custom_theme
        else:
            theme = "light" if self.is_dark else "dark"
        return QtGui.QIcon(f"./static/img/IconPark/{theme}/{icon_path}.png")

    def init_store_card_list(self):
        # 收集所有分类（排除"全部"）
        categories = set()
        for card in self.card_store_data:
            category_list = card.get("categoryList", [])
            categories.update(cat["title"] for cat in category_list if cat["title"] != "全部")

        # 构建分类顺序：全部 -> 待更新 -> 其他分类（字母序）
        categories_list = ["全部", "待更新"] + sorted(categories)

        # 清空旧标签页
        while self.tab_widget.count() > 0:
            self.tab_widget.removeTab(0)

        # 创建新标签页
        for tab_name in categories_list:
            scroll_area = self.create_scroll_area(tab_name)
            self.tab_widget.addTab(scroll_area, tab_name)

    def create_scroll_area(self, tab_name):
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet(style_util.scroll_bar_style)
        content_widget = QtWidgets.QWidget()
        content_widget.setStyleSheet("background: transparent;")
        content_layout = QtWidgets.QGridLayout(content_widget)
        content_layout.setContentsMargins(15, 15, 15, 15)
        content_layout.setHorizontalSpacing(20)  # 水平间距
        content_layout.setVerticalSpacing(20)    # 垂直间距
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # 关键设置
        # 分类过滤逻辑
        if tab_name == "全部":
            filtered_cards = self.card_store_data
        elif tab_name == "待更新":
            filtered_cards = [c for c in self.card_store_data if self.is_card_need_update(c)]
        else:
            filtered_cards = [c for c in self.card_store_data
                              if any(cat["title"] == tab_name for cat in c.get("categoryList", []))]
        # 空状态提示（新增统一处理）
        if not filtered_cards:
            empty_label = QtWidgets.QLabel("该分类暂时没有可用卡片" if tab_name != "待更新" else "没有卡片需要更新")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_label.setStyleSheet("font-size: 16px; color: gray;")
            content_layout.addWidget(empty_label, 0, 0, 1, 3)
        else:
            # 三列布局
            MAX_COLUMNS = 3
            row, col = 0, 0
            for card_data in filtered_cards:
                card_widget = self.create_card_widget(card_data)
                content_layout.addWidget(card_widget, row, col)
                col += 1
                if col >= MAX_COLUMNS:
                    col = 0
                    row += 1
            if col != 0 and col < MAX_COLUMNS:
                for c in range(col, MAX_COLUMNS):
                    content_layout.addWidget(QtWidgets.QWidget(), row, c)

        scroll_area.setWidget(content_widget)
        return scroll_area

    def is_card_need_update(self, card_data):
        installed_plugin = self.before_plugin_map.get(card_data["name"])
        if not installed_plugin:
            return False
        current_version = card_data["currentVersion"]["version"]
        installed_version = installed_plugin.get("version", "v0.0.0")
        return current_version != installed_version

    def create_card_widget(self, card_data):
        widget = QtWidgets.QWidget()
        color = "white" if self.is_dark else "black"
        # 注册到字典中
        if card_data["name"] not in self.card_widgets:
            self.card_widgets[card_data["name"]] = []
        self.card_widgets[card_data["name"]].append(widget)
        widget.setStyleSheet(f"""
            background-color: rgba({'255, 255, 255, 20' if self.is_dark else '255, 255, 255, 160'});
            border: 1px solid rgba({'255, 255, 255, 50' if self.is_dark else '0, 0, 0, 50'});
            border-radius: 10px;
        """)
        widget.card_data = card_data

        # === 修改开始：优先选择2_2大小 ===
        # 获取支持的大小列表
        sizes = card_data["currentVersion"]["supportSizeList"]
        # 查找2_2在列表中的位置
        if "2_2" in sizes:
            widget.current_size_index = sizes.index("2_2")
        else:
            widget.current_size_index = 0  # 默认选择第一个大小
        # === 修改结束 ===

        layout = QtWidgets.QVBoxLayout(widget)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(5)
        # 标题区域
        title_container = QtWidgets.QWidget()
        title_container.setStyleSheet("background: transparent; border: none;")
        title_layout = QtWidgets.QHBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(0)
        title_placeholder = QtWidgets.QLabel()              # 占位符(为了平衡右侧详情按钮)
        title_placeholder.setStyleSheet("background: transparent; border: none;")
        title_placeholder.setMaximumHeight(25)
        title_placeholder.setMaximumWidth(25)
        title_layout.addWidget(title_placeholder)
        title_layout.addStretch()
        title = QtWidgets.QLabel(card_data["title"])        # 标题
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("background: transparent; font-size: 14px; font-weight: bold; color: {}; border: none;".format(color))
        title.setMaximumHeight(25)
        title_layout.addWidget(title)
        title_layout.addStretch()
        card_details = QtWidgets.QPushButton()              # 右侧详情按钮
        button_light_style = """
        QPushButton { border-radius: 10px; border: none; background-color: transparent; }
        QPushButton:hover { background: rgba(0, 0, 0, 0.3); }"""
        button_dark_style = """
        QPushButton { border-radius: 10px; border: none; background-color: transparent; }
        QPushButton:hover { background: rgba(255, 255, 255, 0.3); }"""
        card_details.setStyleSheet(button_dark_style if self.is_dark else button_light_style)
        card_details.setMaximumHeight(25)
        card_details.setMaximumWidth(25)
        card_details.setIcon(QIcon(f"./static/img/IconPark/{'light' if self.is_dark else 'dark'}/Base/search.png"))
        card_details.setIconSize(QSize(20, 20))
        card_details.setCursor(QCursor(Qt.PointingHandCursor))     # 鼠标手形
        card_details.clicked.connect(lambda : self.open_view_card_detail(card_data["id"]))
        title_layout.addWidget(card_details)
        layout.addWidget(title_container)
        # 描述
        description = QtWidgets.QLabel(card_data["description"])
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_color = "#AAAAAA" if self.is_dark else "#666666"
        description.setStyleSheet("background: transparent; font-size: 12px; color: {}; border: none;".format(description_color))
        description.setWordWrap(True)
        description.setMaximumHeight(20)
        layout.addWidget(description)
        layout.addStretch()
        # 图片区域
        image_height = 200
        image_container = QtWidgets.QWidget()
        image_container.setStyleSheet("background: transparent; border: none;")
        image_container.setMinimumHeight(image_height)
        image_container.setMaximumHeight(image_height)
        image_layout = QtWidgets.QHBoxLayout(image_container)
        image_layout.setContentsMargins(40, 0, 40, 0)
        image_layout.setSpacing(5)
        # 左切换按钮
        btn_icon_size = 30
        self.left_btn = QtWidgets.QPushButton()             # 左切换按钮
        self.left_btn.setIcon(self.get_icon("Arrows/left-c"))
        self.left_btn.setFlat(True)
        self.left_btn.setFixedSize(btn_icon_size, btn_icon_size)
        self.left_btn.setIconSize(QSize(btn_icon_size, btn_icon_size))
        self.left_btn.setStyleSheet(button_dark_style if self.is_dark else button_light_style)
        self.left_btn.clicked.connect(lambda: self.change_size(widget, -1))
        image_layout.addWidget(self.left_btn)
        image_layout.addStretch()
        # 图片标签
        widget.img_label = QtWidgets.QLabel()               # 中间的卡片图片
        widget.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        widget.img_label.setFixedSize(image_height, image_height)
        widget.img_label.setStyleSheet(f"background: transparent; border: 1px solid rgba({'255, 255, 255, 50' if self.is_dark else '0, 0, 0, 50'});")
        widget.img_label.setScaledContents(True)
        image_layout.addWidget(widget.img_label)
        image_layout.addStretch()
        # 右切换按钮
        self.right_btn = QtWidgets.QPushButton()            # 右切换按钮
        self.right_btn.setIcon(self.get_icon("Arrows/right-c"))
        self.right_btn.setFlat(True)
        self.right_btn.setFixedSize(btn_icon_size, btn_icon_size)
        self.right_btn.setIconSize(QSize(btn_icon_size, btn_icon_size))
        self.right_btn.setStyleSheet(button_dark_style if self.is_dark else button_light_style)
        self.right_btn.clicked.connect(lambda: self.change_size(widget, +1))
        image_layout.addWidget(self.right_btn)
        layout.addWidget(image_container)
        layout.addStretch()
        # 尺寸提示
        size_widget = QtWidgets.QWidget()
        size_widget.setStyleSheet("background: transparent; border: none;")
        size_layout = QtWidgets.QHBoxLayout(size_widget)
        size_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        size_layout.setSpacing(0)
        widget.size_indicate = QtWidgets.QLabel()
        indicate_color = "#AAAAAA" if self.is_dark else "#666666"
        widget.size_indicate.setStyleSheet("background: transparent; font-size: 12px; color: {}; border: none;".format(indicate_color))
        widget.size_indicate.setWordWrap(True)
        widget.size_indicate.setMaximumHeight(20)
        size_layout.addWidget(widget.size_indicate)
        layout.addWidget(size_widget)
        # 状态指示器
        dots_widget = QtWidgets.QWidget()
        dots_widget.setStyleSheet("background: transparent; border: none;")
        dots_layout = QtWidgets.QHBoxLayout(dots_widget)
        dots_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dots_layout.setSpacing(5)
        widget.dots = []
        size_count = len(card_data["currentVersion"]["supportSizeList"])
        for i in range(size_count):
            dot = QtWidgets.QLabel()
            dot.setFixedSize(8, 8)
            dot.setStyleSheet("background-color: gray; border-radius: 4px;")
            dots_layout.addWidget(dot)
            widget.dots.append(dot)
        layout.addWidget(dots_widget)
        if size_count == 1:
            self.left_btn.hide()
            self.right_btn.hide()
        # 操作按钮
        btn_container = QtWidgets.QWidget()
        btn_container.setStyleSheet("background: transparent; border: none;")
        btn_layout = QtWidgets.QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.addStretch()
        widget.action_btn = QtWidgets.QPushButton()
        widget.action_btn.setFixedSize(80, 25)
        widget.action_btn.setStyleSheet(f"background: transparent; border: 1px solid rgba({'255, 255, 255, 50' if self.is_dark else '0, 0, 0, 50'});")
        widget.action_btn.setCursor(QCursor(Qt.PointingHandCursor))     # 鼠标手形
        self.update_action_btn(widget)
        btn_layout.addWidget(widget.action_btn)
        btn_layout.addStretch()
        layout.addWidget(btn_container)
        # 初始加载图片
        self.update_image(widget)
        self.update_dots(widget)
        self.update_indicate(widget)

        widget.setMinimumHeight(350)
        widget.setMaximumHeight(350)
        widget.setMaximumWidth(500)
        return widget

    def change_size(self, widget, delta):
        current = widget.current_size_index
        new_index = current + delta
        sizes = widget.card_data["currentVersion"]["supportSizeList"]
        if 0 <= new_index < len(sizes):
            widget.current_size_index = new_index
            self.update_image(widget)
            self.update_dots(widget)
            self.update_indicate(widget)
            self.update_action_btn(widget)

    def update_action_btn(self, widget):
        btn = widget.action_btn
        card_data = widget.card_data
        try:
            btn.clicked.disconnect()
        except RuntimeError:
            pass
        current_size = card_data["currentVersion"]["supportSizeList"][widget.current_size_index]
        border_style = "border: 1px solid rgba(255, 255, 255, 50);" if self.is_dark else "border: 1px solid rgba(0, 0, 0, 50);"
        # 对MainCard特殊处理
        if card_data["name"] == "MainCard":
            btn.setText("添加")
            btn.setStyleSheet(f"background-color: rgba({'64, 158, 255, 50' if self.is_dark else '64, 158, 255, 50'});" + border_style)
            btn.clicked.connect(lambda: self.emit_card_data(card_data, current_size))
            return
        # 已安装的卡片
        if card_data["name"] in self.before_plugin_map:
            installed_version = self.before_plugin_map[card_data["name"]]["version"]
            current_version = card_data["currentVersion"]["version"]
            if installed_version == current_version:
                btn.setText("添加")
                btn.setStyleSheet(f"background-color: rgba({'64, 158, 255, 50' if self.is_dark else '64, 158, 255, 50'});" + border_style)
                btn.clicked.connect(lambda: self.emit_card_data(card_data, current_size))
            else:
                btn.setText("更新")
                btn.setStyleSheet(f"background-color: rgba({'230, 162, 60, 50' if self.is_dark else '230, 162, 60, 50'});" + border_style)
                btn.clicked.connect(lambda: self.install_or_update_card(card_data, widget))
        else:
            # 未安装的卡片
            btn.setText("安装")
            btn.setStyleSheet(f"background-color: rgba({'230, 162, 60, 50' if self.is_dark else '230, 162, 60, 50'});" + border_style)
            btn.clicked.connect(lambda: self.install_or_update_card(card_data, widget))

    def update_image(self, widget):
        current_size = widget.card_data["currentVersion"]["supportSizeList"][widget.current_size_index]
        card_width = int(current_size.split("_")[0])
        card_height = int(current_size.split("_")[1])
        card_real_width, card_real_height = scale_size(card_width, card_height)
        widget.img_label.setFixedSize(card_real_width, card_real_height)
        network_img_path = None
        for img in widget.card_data["currentVersion"]["cardImages"]:
            if img["cardSize"] == current_size:
                network_img_path = img["darkUrl" if self.is_dark else "lightUrl"]
                break
        if network_img_path:
            # 检查缓存
            if network_img_path in self.image_cache:
                pixmap = self.image_cache[network_img_path]
                widget.img_label.setPixmap(pixmap)
            else:
                # 加入队列并启动定时器
                self.pending_images.append((network_img_path, widget.img_label))
                if not self.image_loading_timer.isActive():
                    self.image_loading_timer.start()

    def load_next_image(self):
        if self.pending_images:
            url, img_label = self.pending_images.pop(0)
            if url in self.image_cache:
                img_label.setPixmap(self.image_cache[url])
                self.load_next_image()
            else:
                pixmap = self.use_parent.image_cache_manager.get_pixmap_by_url(url)
                if pixmap is not None:
                    img_label.setPixmap(pixmap)
                    self.load_next_image()
                else:
                    # 发起网络请求
                    print(f"从网络加载图片:{url}")
                    request = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
                    request.setRawHeader(b"Authorization", self.use_parent.access_token.encode())
                    reply = self.network_manager.get(request)
                    reply.finished.connect(lambda: self.handle_image_reply(reply, url, img_label))

    def handle_image_reply(self, reply, url, img_label):
        if reply.error() == QtNetwork.QNetworkReply.NoError:
            data = reply.readAll()
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(data)
            if not pixmap.isNull():
                # 缓存图片并更新所有使用该URL的标签
                self.image_cache[url] = pixmap
                img_label.setPixmap(pixmap)
                # 缓存图片
                self.use_parent.image_cache_manager.save_pixmap_by_url(url, pixmap)
        reply.deleteLater()

    def update_dots(self, widget):
        current = widget.current_size_index
        for i, dot in enumerate(widget.dots):
            if i == current:
                dot.setStyleSheet(f"background-color: {'white' if self.is_dark else 'black'}; border-radius: 4px; width: 12px; height: 12px;")
            else:
                dot.setStyleSheet("background-color: gray; border-radius: 4px; width: 8px; height: 8px;")

    def update_indicate(self, widget):
        current = widget.current_size_index
        sizes = widget.card_data["currentVersion"]["supportSizeList"]
        size = sizes[current]
        cols, rows = map(int, size.split("_"))
        indicate = f"宽度:{cols} × 高度:{rows}"
        widget.size_indicate.setText(indicate)

    def emit_card_data(self, card_data, size):
        # 添加卡片
        self.cardAdded.emit({
            "name": card_data["name"],
            "data": {},
            "size": size
        })
        self.storeClose.emit("")
        self.hide()

    def install_or_update_card(self, card_data, widget):
        url = card_data['currentVersion']['url']
        plugin_dir = os.path.join(str(os.getcwd()), "plugin")
        zip_path = os.path.join(plugin_dir, f"{card_data['name']}.zip")  # 直接保存为插件名.zip
        btn = widget.action_btn
        btn.setEnabled(False)
        btn.setText("下载中...")

        request = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
        request.setRawHeader(b"Authorization", self.use_parent.access_token.encode())
        reply = self.network_manager.get(request)

        def on_download_finished():
            card_name = card_data["name"]
            if reply.error() == QtNetwork.QNetworkReply.NetworkError.NoError:
                with open(zip_path, 'wb') as f:
                    f.write(reply.readAll().data())
                btn.setText("添加")
                print(f"插件 {card_name} 下载完成")
                self.before_plugin_map = get_plugin_folder_map()  # 仍需要刷新插件列表
                # 对于新增的插件，需要新增到插件列表中，对于更新的插件，需要更新插件列表中该插件的版本
                if card_name in self.before_plugin_map:
                    self.before_plugin_map[card_name]["version"] = card_data["currentVersion"]["version"]
                else:
                    self.before_plugin_map[card_name] = card_data
                    self.before_plugin_map[card_name]["version"] = card_data["currentVersion"]["version"]
                self.update_action_btn(widget)
                # 关闭卡片设计器时需要重新加载插件列表
                self.parent().is_install_or_update = True
            else:
                btn.setText(f"失败: {reply.errorString()}")
                print(f"插件 {card_name} 下载失败: {reply.errorString()}")
            btn.setEnabled(True)
            reply.deleteLater()
            # 新增：更新所有同卡片的widget状态
            if card_name in self.card_widgets:
                for w in self.card_widgets[card_name]:
                    self.update_action_btn(w)

        reply.finished.connect(on_download_finished)

    def open_view_card_detail(self, card_id):
        if self.view_card_detail_widget is None:
            self.view_card_detail_widget = CardDetailWidget(self.card_permutation, use_parent=self.use_parent, card_id=card_id, is_dark=self.is_dark)
            # 连接关闭信号
            self.view_card_detail_widget.detailClose.connect(lambda: self.set_main_visible(True))
            # 隐藏主界面
            self.set_main_visible(False)
            self.view_card_detail_widget.show()
        else:
            # 隐藏主界面
            self.set_main_visible(False)
            self.view_card_detail_widget.show()
            self.view_card_detail_widget.re_init(card_id=card_id)

    def set_main_visible(self, visible: bool):
        """设置主界面可见性"""
        self.setVisible(visible)

def get_plugin_folder_map():
    """获取插件目录中每个插件的json内容组合成字典"""
    plugin_map = {}
    plugin_dir = os.path.join(str(os.getcwd()), "plugin")
    # 遍历plugin目录下的所有子目录
    for plugin_folder_name in os.listdir(plugin_dir):
        plugin_path = os.path.join(plugin_dir, plugin_folder_name)
        if os.path.isdir(plugin_path):
            config_path = os.path.join(plugin_path, "config.json")
            if os.path.exists(config_path):
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                        plugin_name = config["name"]
                        plugin_map[plugin_name] = config
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Error loading {config_path}: {str(e)}")
    return plugin_map


def scale_size(width: int, height: int):
    # 处理无效输入
    if width <= 0 or height <= 0:
        return 0, 0
    image_width = 200
    max_dim = max(width, height)
    # 新规则：最大值小于300时放大到300
    if max_dim < image_width:
        if width > height:
            new_height = int(round(height * image_width / width))
            return image_width, new_height
        else:
            new_width = int(round(width * image_width / height))
            return new_width, image_width
    # 原缩放规则：超过300时保持比例缩小
    ratio = width / height
    if width > height:
        return image_width, int(round(image_width / ratio))
    else:
        return int(round(image_width * ratio)), image_width
