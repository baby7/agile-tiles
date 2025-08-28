import datetime
import json

from PySide6.QtCore import QUrl, Slot
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QApplication

from src.card.component.AggregationCard.AggregationCard import AggregationCard
from src.client import common
from src.ui import style_util


class InformationCard(AggregationCard):

    title = "信息聚合"
    name = "InformationCard"
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
    # 模块列表
    aggregation_module_list = []
    base_url = common.BASE_URL + "/textContent/normal/random"
    # 新增：记录已加载的分类
    loaded_tabs = set()


    def __init__(self, main_object=None, parent=None, theme=None, card=None, cache=None, data=None,
                 toolkit=None, logger=None, save_data_func=None):
        super().__init__(main_object=main_object, parent=parent, theme=theme, card=card, cache=cache, data=data,
                         toolkit=toolkit, logger=logger, save_data_func=save_data_func)
        # 添加网络管理器
        self.network_manager = QNetworkAccessManager(self)

    def init_ui(self):
        super().init_ui()
        self.aggregation_module_list = [
            # 图片类
            {
                "category": self.module_category_image,
                "type": "瞅瞅图",
                "title": "摸鱼人日历",
                "des": "摸鱼摸得好,上班没烦恼",
                "icon": "png:Actor/MoYu.png",
                "content": None,
                "link": "https://moyu.games/",
                "call_back_func": lambda : self.push_button_moyu_image_click()
            },
            { "category": self.module_category_image,
                "type": "瞅瞅图",
                "title": "随机Kfc星期四图片",
                "des": "Kfc疯狂星期四梗图表情包",
                "icon": "png:Actor/Kfc.png",
                "content": None,
                "link": None,
                "call_back_func": lambda : self.push_button_random_image_click("kfc", "随机Kfc星期四图片")
            },
            { "category": self.module_category_image,
                "type": "瞅瞅图",
                "title": "随机猫咪图片",
                "des": "猫咪的治愈魔法",
                "icon": "png:Actor/Cat.png",
                "content": None,
                "link": "https://api.pexels.com",
                "call_back_func": lambda : self.push_button_random_image_click("cat", "随机猫咪图片")
            },
            { "category": self.module_category_image,
                "type": "瞅瞅图",
                "title": "随机小狗图片",
                "des": "总有一张能治愈你的心",
                "icon": "png:Actor/Dog.png",
                "content": None,
                "link": "https://api.pexels.com",
                "call_back_func": lambda : self.push_button_random_image_click("dog", "随机小狗图片")
            },
            { "category": self.module_category_image,
                "type": "瞅瞅图",
                "title": "随机风景图片",
                "des": "来一场说走就走的旅行",
                "icon": "png:Actor/LvYou.png",
                "content": None,
                "link": "https://api.pexels.com",
                "call_back_func": lambda : self.push_button_random_image_click("scenery", "随机风景图片")
            },
            { "category": self.module_category_image,
                "type": "瞅瞅图",
                "title": "随机美食图片",
                "des": "深夜食堂最是馋人",
                "icon": "png:Actor/Food.png",
                "content": None,
                "link": "https://api.pexels.com",
                "call_back_func": lambda : self.push_button_random_image_click("delicious", "随机美食图片")
            },
            {
                "category": self.module_category_image,
                "type": "瞅瞅图",
                "title": "显卡天梯图",
                "des": "桌面端显卡性能天梯图",
                "icon": "Hardware/chip.svg",
                "content": "https://server.agiletiles.com/file_cdn/gpu_top_qiudaoyu/Gpu-2025-08.jpg",
                "link": "https://tieba.baidu.com/p/6133450546?pn=1",
                "call_back_func": None
            },
            {
                "category": self.module_category_image,
                "type": "瞅瞅图",
                "title": "处理器天梯图",
                "des": "桌面端处理器性能天梯图",
                "icon": "Hardware/cpu.svg",
                "content": "https://server.agiletiles.com/file_cdn/gpu_top_qiudaoyu/Cpu-2025-08.jpg",
                "link": "https://tieba.baidu.com/p/5005825360?pn=1",
                "call_back_func": None
            },
            # 文字类
            {
                "category": self.module_category_text,
                "type": "看看字",
                "title": "历史上的今天",
                "des": "看看历史上的今天有啥事",
                "icon": "Edit/calendar.svg",
                "content": None,
                "call_back_func": self.push_button_reading_history_click
            },
            {
                "category": self.module_category_text,
                "type": "看看字",
                "title": "随机KFC星期四文案",
                "des": "肯德基疯狂星期四文案",
                "icon": "Foods/chicken-leg.svg",
                "content": None,
                "call_back_func": self.push_button_reading_kfc_click
            },
            {
                "category": self.module_category_text,
                "type": "看看字",
                "title": "随机生活小妙招",
                "des": "简单又实用,送给大家",
                "icon": "Life/hanger.svg",
                "content": None,
                "call_back_func": self.push_button_reading_life_click
            },
            # {
            #     "category": self.module_category_text,
            #     "type": "看看字",
            #     "title": "脑筋急转弯",
            #     "des": "打什么东西,不必花力气?",
            #     "icon": "Health/brain.svg",
            #     "content": None,
            #     "call_back_func": self.push_button_reading_riddle_click
            # },
            {
                "category": self.module_category_text,
                "type": "看看字",
                "title": "随机彩虹屁",
                "des": "这是什么绝世小可爱",
                "icon": "Life/beach-umbrella.svg",
                "content": None,
                "call_back_func": self.push_button_reading_rainbow_click
            },
            {
                "category": self.module_category_text,
                "type": "看看字",
                "title": "随机早安心语",
                "des": "早上好!祝你有个好心情",
                "icon": "Weather/sun-one.svg",
                "content": None,
                "call_back_func": self.push_button_reading_morning_click
            },
            {
                "category": self.module_category_text,
                "type": "看看字",
                "title": "随机晚安心语",
                "des": "晚安,愿你今晚有个好梦",
                "icon": "Weather/moon.svg",
                "content": None,
                "call_back_func": self.push_button_reading_night_click
            },
            {
                "category": self.module_category_text,
                "type": "看看字",
                "title": "随机毒鸡汤",
                "des": "猛士,干了碗毒鸡汤",
                "icon": "Animals/chicken-zodiac.svg",
                "content": None,
                "call_back_func": self.push_button_reading_chicken_1_click
            },
            {
                "category": self.module_category_text,
                "type": "看看字",
                "title": "随机土味情话",
                "des": "我有超能力,超喜欢你",
                "icon": "Base/like.svg",
                "content": None,
                "call_back_func": self.push_button_reading_cheesy_love_click
            },
        ]
        self.init_tab_widget()

    def refresh_data(self, date_time_str):
        super().refresh_data(date_time_str)

    def refresh_ui(self, date_time_str):
        super().refresh_ui(date_time_str)
        super().refresh_ui_end(date_time_str)

    def show_text_in_show_panel(self, title, text, set_type=True, call_back=None):
        if set_type:
            self.current_show_panel_type = "Text"
        # 设置标题
        self.show_panel_label_title.setText(title)
        # 设置右上角按钮内容
        self.show_panel_hide_button.show()
        self.show_panel_hide_button.setText("随机一条")
        if call_back is not None:
            self.show_panel_hide_button.clicked.connect(call_back)
        # 设置右上角2按钮内容
        self.show_panel_hide_button_2.show()
        self.show_panel_hide_button_2.setText("复制")
        self.show_panel_hide_button_2.clicked.connect(lambda : self.copy_text(text, label_info))
        # 面板增加布局
        layout = QVBoxLayout(self.show_panel_content_panel)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        # 增加展示文字
        label_content = QLabel()
        label_content.setWordWrap(True)
        label_content.setText(text)
        layout.addWidget(label_content)
        # 增加一个展示信息的状态
        label_info = QLabel()
        label_info.hide()
        layout.addWidget(label_info)
        # 伸缩条
        layout.addStretch()
        # 切换到展示面板
        self.stacked_widget.setCurrentIndex(1)

    def copy_text(self, text, info_label):
        QApplication.clipboard().setText(text)
        info_label.show()
        info_label.setText("复制内容成功，您现在可以粘贴了~")

    def show_image_in_show_panel(self, title, image_url, call_back=None):
        self.current_show_panel_type = "Image"
        # 创建网络请求
        request = QNetworkRequest(QUrl(image_url))
        request.setMaximumRedirectsAllowed(5)  # 设置最大重定向次数
        reply = self.network_manager.get(request)
        reply.finished.connect(lambda : self.on_request_finished(reply, title, call_back=call_back))

    def on_request_finished(self, reply, title, call_back=None):
        if reply.error() == QNetworkReply.NoError:
            data = reply.readAll()
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            self.show_image_in_show_panel_end(title, pixmap, call_back=call_back)
        else:
            print(f"Request failed: {reply.errorString()}")
            self.show_text_in_show_panel("请求失败", "请检查网络连接", set_type=False)
        reply.deleteLater()

    def show_image_in_show_panel_end(self, title, image, call_back=None):
        # 设置标题
        self.show_panel_label_title.setText(title)
        # 设置右上角按钮内容
        self.show_panel_hide_button.show()
        self.show_panel_hide_button.setText("显示大图")
        if call_back is not None:
            self.show_panel_hide_button.clicked.connect(call_back)
        self.show_panel_hide_button_2.hide()
        # 面板增加布局
        layout = QVBoxLayout(self.show_panel_content_panel)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        # 增加展示文字
        label_content = QLabel()
        # 图片自适应
        max_width = self.card.width() - 40
        max_height = self.card.height() - 70
        image_width = image.width()
        image_height = image.height()
        # 判断图片是否需要缩放
        if image_width > max_width or image_height > max_height:
            if image_width > image_height:
                new_width = max_width
                new_height = int(round(image_height * max_width / image_width))
            else:
                new_width = int(round(image_width * max_height / image_height))
                new_height = max_height
        else:
            new_width = image_width
            new_height = image_height
        # 缩放后是否还大于显示区域
        if new_width > max_width:
            new_width = max_width
            new_height = int(round(image_height * max_width / image_width))
        # 创建高质量缩放图片
        scaled_pixmap = image.scaled(
            new_width,
            new_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        # 设置图片
        label_content.setPixmap(scaled_pixmap)
        layout.addWidget(label_content)
        # 切换到展示面板
        self.stacked_widget.setCurrentIndex(1)

    def push_button_reading_history_click(self):
        # 清理展示面板
        self.clear_show_panel()
        # 创建网络请求
        url = QUrl(common.BASE_URL + '/historyToday/normal/today')
        request = QNetworkRequest(url)
        request.setRawHeader(b"Authorization", self.main_object.access_token.encode())
        # 设置请求属性（可选）
        reply = self.network_manager.get(request)
        # 存储上下文信息
        reply.finished.connect(lambda : self.process_history_data(reply))

    # 历史数据处理函数
    def process_history_data(self, reply):
        try:
            # 解析数据
            data = reply.readAll().data().decode()
            result = json.loads(data)
            history_list = result["data"]
            history_str = ""
            # 遍历数据
            for i in range(len(history_list)):
                history = history_list[len(history_list) - i - 1]
                history_str += ("【" + history['date'] + "】" + str(history["title"]).replace("&nbsp;", " ") + "\r\n")
            # 显示内容
            self.show_text_in_show_panel("历史上的今天", history_str)
            self.show_panel_hide_button.hide()
        except Exception as e:
            self.main_object.toolkit.dialog_module.box_information(
                self.main_object, "错误信息",
                f"获取历史上的今天失败: {str(e)}"
            )

    def push_button_reading_kfc_click(self):
        try:
            self.push_button_random_text_click("KFC星期四文案", "?category=KFCThursday", self.push_button_reading_kfc_click)
        except Exception as e:
            self.main_object.toolkit.dialog_module.box_information(self.main_object, "错误信息", "获取{}失败,请稍后重试".format("随机KFC星期四文案"))

    def push_button_reading_life_click(self):
        try:
            self.push_button_random_text_click("生活小妙招", "?category=GoodMorning", self.push_button_reading_life_click)
        except Exception as e:
            self.main_object.toolkit.dialog_module.box_information(self.main_object, "错误信息", "获取{}失败,请稍后重试".format("随机生活小妙招"))

    def push_button_reading_rainbow_click(self):
        try:
            self.push_button_random_text_click("彩虹屁", "?category=RainbowFart", self.push_button_reading_rainbow_click)
        except Exception as e:
            self.main_object.toolkit.dialog_module.box_information(self.main_object, "错误信息", "获取{}失败,请稍后重试".format("随机彩虹屁"))

    def push_button_reading_morning_click(self):
        try:
            self.push_button_random_text_click("早安啦", "?category=GoodMorning", self.push_button_reading_morning_click)
        except Exception as e:
            self.main_object.toolkit.dialog_module.box_information(self.main_object, "错误信息", "获取{}失败,请稍后重试".format("随机早安心语"))

    def push_button_reading_night_click(self):
        try:
            self.push_button_random_text_click("晚安啦", "?category=GoodNight", self.push_button_reading_night_click)
        except Exception as e:
            self.main_object.toolkit.dialog_module.box_information(self.main_object, "错误信息", "获取{}失败,请稍后重试".format("随机晚安心语"))

    def push_button_reading_chicken_1_click(self):
        try:
            self.push_button_random_text_click("毒鸡汤", "?category=PoisonChickenSoup2", self.push_button_reading_chicken_1_click)
        except Exception as e:
            self.main_object.toolkit.dialog_module.box_information(self.main_object, "错误信息", "获取{}失败,请稍后重试".format("随机毒鸡汤"))

    def push_button_reading_cheesy_love_click(self):
        try:
            self.push_button_random_text_click("土味情话", "?category=LostInLove", self.push_button_reading_cheesy_love_click)
        except Exception as e:
            self.main_object.toolkit.dialog_module.box_information(self.main_object, "错误信息", "获取{}失败,请稍后重试".format("随机土味情话"))

    def push_button_random_text_click(self, title, url_suffix, call_back=None):
        # 清理展示面板
        self.clear_show_panel()
        # 创建网络请求
        url = QUrl(self.base_url + url_suffix)
        request = QNetworkRequest(url)
        request.setRawHeader(b"Authorization", self.main_object.access_token.encode())
        # 设置请求属性（可选）
        reply = self.network_manager.get(request)
        # 存储上下文信息
        reply.finished.connect(lambda : self.process_random_text_data(reply, title, call_back=call_back))

    def process_random_text_data(self, reply, title, call_back):
        try:
            # 解析数据
            data = reply.readAll().data().decode()
            result = json.loads(data)
            data = result.get('data', {})
            content = data.get('content', '')
            # 显示内容
            self.show_text_in_show_panel(title, content, call_back=call_back)
        except Exception as e:
            self.main_object.toolkit.dialog_module.box_information(
                self.main_object, "错误信息",
                f"获取{title}失败: {str(e)}"
            )

    def push_button_moyu_image_click(self):
        url = QUrl(f'{common.BASE_URL}/imageContent/normal/moyu/today')
        request = QNetworkRequest(url)
        request.setRawHeader(b"Authorization", self.main_object.access_token.encode())

        reply = self.network_manager.get(request)
        reply.finished.connect(lambda : self.process_moyu_image(reply))

    # 每日一图处理函数
    def process_moyu_image(self, reply):
        try:
            data = reply.readAll().data().decode()
            result = json.loads(data)
            image_url = result['data']['result']
            call_back = lambda : self.toolkit.image_box_util.show_image_dialog(
                self.main_object, "摸鱼人日历", image_url, "https://moyu.games/"
            )
            self.show_image_in_show_panel("摸鱼人日历", image_url, call_back=call_back)
        except Exception as e:
            self.main_object.toolkit.dialog_module.box_information(
                self.main_object, "错误信息",
                f"获取摸鱼人日历失败: {str(e)}"
            )

    def push_button_random_image_click(self, image_type, title):
        url = QUrl(f'{common.BASE_URL}/imageContent/normal/random?type={image_type}')
        request = QNetworkRequest(url)
        request.setRawHeader(b"Authorization", self.main_object.access_token.encode())

        reply = self.network_manager.get(request)
        reply.finished.connect(lambda : self.process_random_image(reply, image_type, title))


    def process_random_image(self, reply, image_type, title):
        try:
            data = reply.readAll().data().decode()
            result = json.loads(data)
            image_url = result['data']['result']
            if image_type == "kfc":
                call_back = lambda : self.toolkit.image_box_util.show_image_dialog(
                    self.main_object, title, image_url, None
                )
            else:
                call_back = lambda : self.toolkit.image_box_util.show_image_dialog(
                    self.main_object, title, image_url, "https://api.pexels.com"
                )
            self.show_image_in_show_panel(title, image_url, call_back=call_back)
        except Exception as e:
            self.main_object.toolkit.dialog_module.box_information(
                self.main_object, "错误信息",
                f"获取{title}失败: {str(e)}"
            )