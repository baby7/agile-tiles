from src.card.component.AggregationCard.AggregationCard import AggregationCard


class GameCard(AggregationCard):

    title = "游戏"
    name = "GameCard"
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

    def init_ui(self):
        super().init_ui()
        self.aggregation_module_list = [
            # 文字游戏
            {
                "category": self.module_category_browser,
                "type": "文字游戏",
                "title": "小黑屋",
                "des": "纯文字的冒险游戏",
                "icon": "png:Actor/ADR.png",
                "content": {
                    "url": "https://adarkroom.doublespeakgames.com/?lang=zh_cn",
                    "size": [1200, 800]
                },
                "link": "https://github.com/doublespeakgames/adarkroom",
                "call_back_func": None
            },
            {
                "category": self.module_category_browser,
                "type": "文字游戏",
                "title": "我的文字修仙全靠刷",
                "des": "刷！刷！刷！",
                "icon": "png:Actor/XiuXian.png",
                "content": {
                    "url": "https://xiuxian.wenzi.games/",
                    "size": [800, 950]
                },
                "link": "https://github.com/setube/vue-XiuXianGame",
                "call_back_func": None
            },
            {
                "category": self.module_category_browser,
                "type": "文字游戏",
                "title": "人生重开模拟器",
                "des": "这垃圾人生一秒也不想呆了",
                "icon": "png:Actor/LR.png",
                "content": {
                    "url": "https://liferestart.syaro.io/public/index.html",
                    "size": [600, 800]
                },
                "link": "https://github.com/VickScarlet/lifeRestart",
                "call_back_func": None
            },
            # {
            #     "category": self.module_category_browser,
            #     "type": "文字游戏",
            #     "title": "进化",
            #     "des": "进化",
            #     "icon": "Edit/calendar.svg",
            #     "content": {
            #         "url": "https://pmotschmann.github.io/Evolve/",
            #         "size": [1200, 800]
            #     },
            #    "link": "https://github.com/pmotschmann/Evolve",
            #     "call_back_func": None
            # },
            {
                "category": self.module_category_browser,
                "type": "文字游戏",
                "title": "信任的进化",
                "des": "THE EVOLUTION OF TRUST",
                "icon": "png:Actor/Trust.png",
                "content": {
                    "url": "https://dccxi.com/trust/",
                    "size": [1200, 800]
                },
                "link": "https://github.com/ncase/trust",
                "call_back_func": None
            },
            {
                "category": self.module_category_browser,
                "type": "文字游戏",
                "title": "超苦逼冒险者",
                "des": "超苦逼冒险者",
                "icon": "png:Actor/KuBitionAdvanture.png",
                "content": {
                    "url": "https://kubitionadvanture.sinaapp.com/",
                    "size": [1000, 610]
                },
                "link": "https://maou.sinaapp.com/?page_id=47",
                "call_back_func": None
            },
            {
                "category": self.module_category_browser,
                "type": "文字游戏",
                "title": "太空公司",
                "des": "太空公司",
                "icon": "png:Actor/SpaceCompany.png",
                "content": {
                    "url": "https://sparticle999.github.io/SpaceCompany/",
                    "size": [1200, 800]
                },
                "link": "https://github.com/sparticle999/SpaceCompany",
                "call_back_func": None
            },
            # RGB类
            {
                "category": self.module_category_browser,
                "type": "RGB类",
                "title": "Idle",
                "des": "挂机放置类小游戏",
                "icon": "png:Actor/Idle.png",
                "content": {
                    "url": "http://couy.xyz/#/",
                    "size": [1200, 700]
                },
                "link": "https://github.com/Couy69/vue-idle-game",
                "call_back_func": None
            },
            # 经典
            {
                "category": self.module_category_browser,
                "type": "经典",
                "title": "2048",
                "des": "合并出2048吧！",
                "icon": "png:Actor/2048.png",
                "content": {
                    "url": "https://play2048.co/",
                    "size": [400, 600]
                },
                "link": "https://github.com/gabrielecirulli/2048",
                "call_back_func": None
            },
            {
                "category": self.module_category_browser,
                "type": "经典",
                "title": "圈小猫",
                "des": "点击小圆点，圈住小猫猫",
                "icon": "png:Actor/CorralCat.png",
                "content": {
                    "url": "https://ganlvtech.github.io/phaser-catch-the-cat/",
                    "size": [400, 550]
                },
                "link": "https://github.com/ganlvtech/phaser-catch-the-cat",
                "call_back_func": None
            },
            # {
            #     "category": self.module_category_browser,
            #     "type": "经典",
            #     "title": "数独",
            #     "des": "填数趣味游戏",
            #     "icon": "Hardware/nine-key.svg",
            #     "content": {
            #         "url": "/static/html/Game/Sudoku/index.html",
            #         "size": [400, 450]
            #     },
            #     "call_back_func": None
            # },
            # {
            #     "category": self.module_category_browser,
            #     "type": "经典",
            #     "title": "俄罗斯方块",
            #     "des": "经典的俄罗斯方块",
            #     "icon": "Game/block-nine.svg",
            #     "content": {
            #         "url": "/static/html/Game/Tetris/index.html",
            #         "size": [300, 550]
            #     },
            #     "call_back_func": None
            # },
        ]
        self.init_tab_widget()

    def refresh_data(self, date_time_str):
        super().refresh_data(date_time_str)

    def refresh_ui(self, date_time_str):
        super().refresh_ui(date_time_str)
        super().refresh_ui_end(date_time_str)