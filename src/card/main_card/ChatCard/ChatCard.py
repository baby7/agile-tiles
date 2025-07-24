from src.card.component.AggregationCard.AggregationCard import AggregationCard
from src.card.main_card.ChatCard.component.chat import ChatWindow


class ChatCard(AggregationCard):

    title = "AI大模型"
    name = "ChatCard"
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


    def __init__(self, main_object=None, parent=None, theme=None, card=None, cache=None, data=None,
                 toolkit=None, logger=None, save_data_func=None):
        super().__init__(main_object=main_object, parent=parent, theme=theme, card=card, cache=cache, data=data,
                         toolkit=toolkit, logger=logger, save_data_func=save_data_func)
        self.chat_win = None

    def init_ui(self):
        super().init_ui()
        self.aggregation_module_list = [
            # 对话
            {
                "category": self.module_category_qt,
                "type": "对话",
                "title": "DeepSeek",
                "des": "近期最火的大模型",
                "icon": "Custom/deepseek.svg",
                "content": None,
                "call_back_func": lambda: self.push_button_chat_click("DeepSeek")
            },
            # {
            #     "category": self.module_category_qt,
            #     "type": "对话",
            #     "title": "ChatGPT",
            #     "des": "OpenAI的大模型",
            #     "icon": "Custom/openai.svg",
            #     "content": None,
            #     "call_back_func": self.push_button_chat_click
            # },
            {
                "category": self.module_category_qt,
                "type": "对话",
                "title": "通义千问",
                "des": "阿里的大模型",
                "icon": "Custom/qwen.svg",
                "content": None,
                "call_back_func": lambda: self.push_button_chat_click("通义千问")
            },
            {
                "category": self.module_category_qt,
                "type": "对话",
                "title": "文心一言",
                "des": "百度的大模型",
                "icon": "Custom/ernie.svg",
                "content": None,
                "call_back_func": lambda: self.push_button_chat_click("文心一言")
            },
            {
                "category": self.module_category_qt,
                "type": "对话",
                "title": "混元",
                "des": "腾讯的大模型",
                "icon": "Custom/hunyuan.svg",
                "content": None,
                "call_back_func": lambda: self.push_button_chat_click("混元")
            },
            {
                "category": self.module_category_qt,
                "type": "对话",
                "title": "讯飞星火",
                "des": "讯飞的大模型",
                "icon": "Custom/spark.svg",
                "content": None,
                "call_back_func": lambda: self.push_button_chat_click("讯飞星火")
            },
            {
                "category": self.module_category_qt,
                "type": "对话",
                "title": "豆包",
                "des": "字节跳动的大模型",
                "icon": "Custom/doubao.svg",
                "content": None,
                "call_back_func": lambda: self.push_button_chat_click("豆包")
            },
            # {
            #     "category": self.module_category_qt,
            #     "type": "对话",
            #     "title": "硅基流动",
            #     "des": "大模型集合平台",
            #     "icon": "Custom/siliconflow.svg",
            #     "content": None,
            #     "call_back_func": self.push_button_chat_click
            # },
            # {
            #     "category": self.module_category_qt,
            #     "type": "对话",
            #     "title": "秘塔AI搜索",
            #     "des": "没有广告，直达结果",
            #     "icon": "Custom/metaso.svg",
            #     "content": None,
            #     "call_back_func": self.push_button_chat_click
            # }
        ]
        self.init_tab_widget()

    def push_button_chat_click(self, title):
        self.toolkit.resolution_util.out_animation(self.main_object)
        # 窗口仅能存在一个
        if self.chat_win is not None and self.chat_win.isVisible():
            self.toolkit.message_box_util.box_information(self.main_object, "提示", "智能对话窗口仅能存在一个哦~")
            return
        self.chat_win = ChatWindow(None, self.main_object, title)
        self.chat_win.refresh_geometry(self.toolkit.resolution_util.get_screen(self.main_object))
        self.chat_win.show()

    def refresh_data(self, date_time_str):
        super().refresh_data(date_time_str)

    def refresh_ui(self, date_time_str):
        super().refresh_ui(date_time_str)
        super().refresh_ui_end(date_time_str)