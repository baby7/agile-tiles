from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import QCoreApplication, QRect, QSize
from PySide6.QtWidgets import QTabWidget, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout
# 获取信息
from src.card.MainCardManager.MainCard import MainCard
from src.ui import style_util
from src.module.Box import message_box_util


class AggregationCard(MainCard):

    title = "聚合"
    name = "AggregationCard"
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


    def __init__(self, main_object=None, parent=None, theme=None, card=None, cache=None, data=None,
                 toolkit=None, logger=None, save_data_func=None):
        super().__init__(main_object=main_object, parent=parent, theme=theme, card=card, cache=cache, data=data,
                         toolkit=toolkit, logger=logger, save_data_func=save_data_func)

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
        font1.setFamilies(["思源黑体"])
        font1.setPointSize(10)
        font1.setBold(False)
        # 下方切换
        self.aggregation_tab_widget = QTabWidget(self.card)
        self.aggregation_tab_widget.setObjectName(u"aggregation_tab_widget")
        self.aggregation_tab_widget.setGeometry(QRect(0, 0, self.card.width(), self.card.height()))
        self.aggregation_tab_widget.setFont(font1)
        self.aggregation_tab_widget.setTabPosition(QTabWidget.North)
        self.aggregation_tab_widget.setTabShape(QTabWidget.Rounded)

    def init_tab_widget(self):
        # 初始化tab组信息
        self.init_module_tab_map()
        # tab列表初始化
        for tab_type, tab in self.module_tab_map.items():
            tab.setObjectName(self.name + "_" + tab_type)
            self.aggregation_tab_widget.addTab(tab, "")
            self.aggregation_tab_widget.setTabText(self.aggregation_tab_widget.indexOf(tab),
                                                   QCoreApplication.translate("Form", " " + tab_type + " ", None))
        self.aggregation_tab_widget.setCurrentIndex(0)
        # 模块字典index
        self.model_index_map = {}
        for key in self.module_tab_map:
            self.model_index_map[key] = 0
        # 模块加载
        for aggregation_module in self.aggregation_module_list:
            button_index, button, image_label, label_title, label_des = self.gen_button(aggregation_module)
            aggregation_module["button_index"] = button_index
            aggregation_module["button"] = button
            aggregation_module["image_label"] = image_label
            aggregation_module["label_title"] = label_title
            aggregation_module["label_des"] = label_des

    def init_module_tab_map(self):
        self.module_tab_map = {}
        for aggregation_module in self.aggregation_module_list:
            if aggregation_module["type"] in self.module_tab_map:
                continue
            self.module_tab_map[aggregation_module["type"]] = QWidget()

    def gen_button(self, aggregation_module):
        interval = 10       # 间隔
        interval_size = 5   # 左边两个，中间一个，右边两个，总计5个间隔
        width = int((self.card.width() - interval * interval_size) / 2)
        height = 63
        # 首先生成按钮本体
        button = QPushButton(self.module_tab_map[aggregation_module["type"]])
        self.model_index_map[aggregation_module["type"]] += 1
        index = self.model_index_map[aggregation_module["type"]]
        # 按钮初始化
        button.setObjectName(u"push_button_aggregation_" + str(index))
        button.setMinimumSize(QSize(width, height))
        # 两列，根据index生成坐标
        button.setGeometry(QRect(int((index - 1) % 2) * (width + 10) + 10, int((index - 1) / 2) * (height + 10) + 10, width, height))
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
        if ".svg" in aggregation_module["icon"]:
            image_path = "static/img/IconPark/svg/" + aggregation_module["icon"]
            try:
                label_image.setPixmap(self.toolkit.image_util.load_light_svg(image_path))
            except Exception as e:
                print("加载svg报错:{}".format(e))
                pass
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
        button_right_layout.addWidget(label_des)
        button_layout.addLayout(button_right_layout)
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
            message_box_util.box_information(self.main_object, "错误信息", f"获取{str(aggregation_module)}失败,请稍后重试")

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
            message_box_util.box_information(self.main_object, "错误信息", f"获取{str(aggregation_module)}失败,请稍后重试")

    def push_button_browser_click(self, aggregation_module):
        try:
            title = aggregation_module["title"]
            content = aggregation_module["content"]
            link = None
            if "link" in aggregation_module:
                link = aggregation_module["link"]
            dialog = self.toolkit.browser_box_util.show_browser_dialog(self.main_object, title, content, link)
            self.dialog_list.append(dialog)
        except Exception as e:
            print(e)
            self.main_object.logger.card_error("聚合卡片", f"获取{str(aggregation_module)}失败,请稍后重试")
            message_box_util.box_information(self.main_object, "错误信息", f"获取{str(aggregation_module)}失败,请稍后重试")

    def refresh_theme(self):
        for aggregation_module in self.aggregation_module_list:
            if "button_index" not in aggregation_module:
                break
            button_index = aggregation_module["button_index"]
            button = aggregation_module["button"]
            image_label = aggregation_module["image_label"]
            label_title = aggregation_module["label_title"]
            label_title.setStyleSheet("background: transparent; color: {};".format(self.get_prospect_color(rgb=True)))
            label_des = aggregation_module["label_des"]
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
                .replace("{hover-background-color}", self.toolkit.color.get_rgba_color(button_index, 20)))
                label_des.setStyleSheet("background: transparent; color: rgba(239, 240, 241, 150);")
            else:
                button.setStyleSheet(button_style
                .replace("{background-color}", self.toolkit.color.get_rgba_color(button_index, 50))
                .replace("{hover-background-color}", self.toolkit.color.get_rgba_color(button_index, 20)))
                label_des.setStyleSheet("background: transparent; color: rgba(24, 24, 24, 150);")
            style_util.set_tab_widget_style(self.aggregation_tab_widget, self.is_dark())
            # 图标
            if "png:" in aggregation_module["icon"]:
                image_end_path = aggregation_module["icon"].replace("png:", "")
                image_label.setPixmap(QPixmap("static/img/IconPark/png/" + image_end_path))
            else:
                image_path = "static/img/IconPark/svg/" + aggregation_module["icon"]
                if self.is_dark():
                    image_label.setPixmap(self.toolkit.image_util.load_light_svg(image_path))
                else:
                    image_label.setPixmap(self.toolkit.image_util.load_dark_svg(image_path))
