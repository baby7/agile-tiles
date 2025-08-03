import datetime
import json

from PySide6.QtCore import QUrl
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest

from src.card.component.AggregationCard.AggregationCard import AggregationCard
from src.client import common


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


    def __init__(self, main_object=None, parent=None, theme=None, card=None, cache=None, data=None,
                 toolkit=None, logger=None, save_data_func=None):
        super().__init__(main_object=main_object, parent=parent, theme=theme, card=card, cache=cache, data=data,
                         toolkit=toolkit, logger=logger, save_data_func=save_data_func)
        # 添加网络管理器
        self.network_manager = QNetworkAccessManager(self)
        self.network_manager.finished.connect(self.handle_network_reply)

    # 统一的网络响应处理函数
    def handle_network_reply(self, reply):
        try:
            if reply.error() == QNetworkReply.NoError:
                data = reply.readAll().data()
                callback = reply.property("callback")
                if callback:
                    callback(data, reply)
            else:
                self.logger.error(f"Network error: {reply.errorString()}")
        finally:
            reply.deleteLater()

    def init_ui(self):
        super().init_ui()
        self.aggregation_module_list = [
            # 图片类
            {
                "category": self.module_category_image,
                "type": "瞅瞅图",
                "title": "摸鱼人日历",
                "des": "摸鱼摸得好,上班没烦恼",
                "icon": "Animals/fish-one.svg",
                "content": "https://api.vvhan.com/api/moyu",
                "link": "https://moyu.games/",
                "call_back_func": None
            },
            { "category": self.module_category_image,
                "type": "瞅瞅图",
                "title": "随机猫咪图片",
                "des": "猫咪的治愈魔法",
                "icon": "Animals/cat.svg",
                "content": None,
                "link": "https://api.pexels.com",
                "call_back_func": lambda : self.push_button_random_image_click("cat")
            },
            { "category": self.module_category_image,
                "type": "瞅瞅图",
                "title": "随机小狗图片",
                "des": "总有一张能治愈你的心",
                "icon": "Animals/dog.svg",
                "content": None,
                "link": "https://api.pexels.com",
                "call_back_func": lambda : self.push_button_random_image_click("dog")
            },
            { "category": self.module_category_image,
                "type": "瞅瞅图",
                "title": "随机风景图片",
                "des": "来一场说走就走的旅行",
                "icon": "Travel/landscape.svg",
                "content": None,
                "link": "https://api.pexels.com",
                "call_back_func": lambda : self.push_button_random_image_click("scenery")
            },
            { "category": self.module_category_image,
                "type": "瞅瞅图",
                "title": "随机美食图片",
                "des": "深夜食堂最是馋人",
                "icon": "Foods/knife-fork.svg",
                "content": None,
                "link": "https://api.pexels.com",
                "call_back_func": lambda : self.push_button_random_image_click("delicious")
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
                "title": "生活小妙招",
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
                "title": "彩虹屁",
                "des": "这是什么绝世小可爱",
                "icon": "Life/beach-umbrella.svg",
                "content": None,
                "call_back_func": self.push_button_reading_rainbow_click
            },
            {
                "category": self.module_category_text,
                "type": "看看字",
                "title": "早安啦",
                "des": "早上好!祝你有个好心情",
                "icon": "Weather/sun-one.svg",
                "content": None,
                "call_back_func": self.push_button_reading_morning_click
            },
            {
                "category": self.module_category_text,
                "type": "看看字",
                "title": "晚安啦",
                "des": "晚安,愿你今晚有个好梦",
                "icon": "Weather/moon.svg",
                "content": None,
                "call_back_func": self.push_button_reading_night_click
            },
            {
                "category": self.module_category_text,
                "type": "看看字",
                "title": "毒鸡汤",
                "des": "猛士,干了碗毒鸡汤",
                "icon": "Animals/chicken-zodiac.svg",
                "content": None,
                "call_back_func": self.push_button_reading_chicken_1_click
            },
            {
                "category": self.module_category_text,
                "type": "看看字",
                "title": "土味情话",
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

    def push_button_reading_history_click(self):
        url = QUrl(common.BASE_URL + '/historyToday/normal/today')
        request = QNetworkRequest(url)
        request.setRawHeader(b"Authorization", self.main_object.access_token.encode())
        # 设置请求属性（可选）
        reply = self.network_manager.get(request)
        # 存储上下文信息
        reply.setProperty("callback", self.process_history_data)

    # 历史数据处理函数
    def process_history_data(self, data, reply):
        try:
            result = json.loads(data)
            history_list = result["data"]
            history_str = ""

            for i in range(len(history_list)):
                history = history_list[len(history_list) - i - 1]
                history_str += ("【" + history['date'] + "】" + str(history["title"]).replace("&nbsp;", " ") + "\r\n")

            self.toolkit.text_box_util.show_text_dialog(
                self.main_object, "历史上的今天",
                {"content": history_str, "size": [500, 400]}
            )
        except Exception as e:
            self.main_object.toolkit.message_box_util.box_information(
                self.main_object, "错误信息",
                f"获取历史上的今天失败: {str(e)}"
            )

    def push_button_reading_life_click(self):
        try:
            self.toolkit.text_box_util.show_text_dialog(self.main_object, "生活小窍门", {
                "url": self.base_url + "?category=GoodMorning",
                "size": [300, 200]
            })
        except Exception as e:
            self.main_object.toolkit.message_box_util.box_information(self.main_object, "错误信息", "获取{}失败,请稍后重试".format("生活小窍门"))

    def push_button_reading_rainbow_click(self):
        try:
            self.toolkit.text_box_util.show_text_dialog(self.main_object, "彩虹屁", {
                "url": self.base_url + "?category=RainbowFart",
                "size": [300, 200]
            })
        except Exception as e:
            self.main_object.toolkit.message_box_util.box_information(self.main_object, "错误信息", "获取{}失败,请稍后重试".format("彩虹屁"))

    def push_button_reading_morning_click(self):
        try:
            self.toolkit.text_box_util.show_text_dialog(self.main_object, "早安心语", {
                "url": self.base_url + "?category=GoodMorning",
                "size": [300, 200]
            })
        except Exception as e:
            self.main_object.toolkit.message_box_util.box_information(self.main_object, "错误信息", "获取{}失败,请稍后重试".format("早安心语"))

    def push_button_reading_night_click(self):
        try:
            self.toolkit.text_box_util.show_text_dialog(self.main_object, "晚安心语", {
                "url": self.base_url + "?category=GoodNight",
                "size": [300, 200]
            })
        except Exception as e:
            self.main_object.toolkit.message_box_util.box_information(self.main_object, "错误信息", "获取{}失败,请稍后重试".format("晚安心语"))

    def push_button_reading_chicken_1_click(self):
        try:
            self.toolkit.text_box_util.show_text_dialog(self.main_object, "毒鸡汤", {
                "url": self.base_url + "?category=PoisonChickenSoup2",
                "size": [300, 200]
            })
        except Exception as e:
            self.main_object.toolkit.message_box_util.box_information(self.main_object, "错误信息", "获取{}失败,请稍后重试".format("毒鸡汤"))

    def push_button_reading_cheesy_love_click(self):
        try:
            self.toolkit.text_box_util.show_text_dialog(self.main_object, "土味情话", {
                "url": self.base_url + "?category=LostInLove",
                "size": [300, 200]
            })
        except Exception as e:
            self.main_object.toolkit.message_box_util.box_information(self.main_object, "错误信息", "获取{}失败,请稍后重试".format("土味情话"))

    def push_button_random_image_click(self, image_type):
        url = QUrl(f'{common.BASE_URL}/imageContent/normal/random?type={image_type}')
        request = QNetworkRequest(url)
        request.setRawHeader(b"Authorization", self.main_object.access_token.encode())

        reply = self.network_manager.get(request)
        reply.setProperty("callback", self.process_bing_image)

    # 每日一图处理函数
    def process_bing_image(self, data, reply):
        try:
            result = json.loads(data)
            image_url = result['data']['result']
            self.toolkit.image_box_util.show_image_dialog(
                self.main_object, "随机图片", image_url, "https://api.pexels.com"
            )
        except Exception as e:
            self.main_object.toolkit.message_box_util.box_information(
                self.main_object, "错误信息",
                f"获取随机图片失败: {str(e)}"
            )