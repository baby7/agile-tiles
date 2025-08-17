from src.card.component.AggregationCard.AggregationCard import AggregationCard
from src.card.main_card.ToolCard.hold_grudges_gen import hold_grudges_gen_util


class ToolCard(AggregationCard):

    title = "工具箱"
    name = "ToolCard"
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
            # 程序员
            {
                "category": self.module_category_browser,
                "type": "程序员",
                "title": "Ctool",
                "des": "程序员工具箱",
                "icon": "png:Actor/Ctool.png",
                "content":{
                    "url": "https://ctool.dev/tool.html#/tool/json?category=conversion",
                    "size": [1000, 600]
                },
                "link": "https://github.com/baiy/ctool",
                "call_back_func": None
            },
            {
                "category": self.module_category_browser,
                "type": "程序员",
                "title": "Quick Reference",
                "des": "程序员速查表",
                "icon": "png:Actor/QuickReference.png",
                "content":{
                    "url": "https://wangchujiang.com/reference/",
                    "size": [1200, 950]
                },
                "link": "https://github.com/jaywcjlove/reference",
                "call_back_func": None
            },
            {
                "category": self.module_category_browser,
                "type": "程序员",
                "title": "Hoppscotch",
                "des": "API调试工具",
                "icon": "png:Actor/Hoppscotch.png",
                "content":{
                    "url": "https://hoppscotch.io/",
                    "size": [1200, 950]
                },
                "link": "https://github.com/hoppscotch/hoppscotch",
                "call_back_func": None
            },
            # 作图
            {
                "category": self.module_category_browser,
                "type": "作图",
                "title": "Excalidraw",
                "des": "手绘风格的绘图工具",
                "icon": "png:Actor/Excalidraw.png",
                "content":{
                    "url": "https://excalidraw.com/",
                    "size": [1000, 800]
                },
                "link": "https://github.com/excalidraw/excalidraw",
                "call_back_func": None
            },
            {
                "category": self.module_category_browser,
                "type": "作图",
                "title": "Draw.io",
                "des": "经典作图工具",
                "icon": "png:Actor/DrawIO.png",
                "content":{
                    "url": "https://app.diagrams.net/index.html",
                    "size": [1000, 800]
                },
                "link": "https://github.com/jgraph/drawio",
                "call_back_func": None
            },
            {
                "category": self.module_category_browser,
                "type": "作图",
                "title": "piskel",
                "des": "像素绘图工具",
                "icon": "png:Actor/Piskel.png",
                "content":{
                    "url": "https://www.piskelapp.com/p/create/sprite",
                    "size": [1000, 800]
                },
                "link": "https://github.com/piskelapp/piskel",
                "call_back_func": None
            },
            {
                "category": self.module_category_browser,
                "type": "作图",
                "title": "SvgPathEditor",
                "des": "Svg编辑工具",
                "icon": "png:Actor/SvgPathEditor.png",
                "content":{
                    "url": "https://yqnn.github.io/svg-path-editor/",
                    "size": [1000, 800]
                },
                "link": "https://github.com/Yqnn/svg-path-editor",
                "call_back_func": None
            },
            {
                "category": self.module_category_browser,
                "type": "作图",
                "title": "ASCIIFlow",
                "des": "Ascii作图工具",
                "icon": "png:Actor/AsciiFlow.png",
                "content":{
                    "url": "https://asciiflow.com/#/",
                    "size": [1200, 950]
                },
                "link": "https://github.com/lewish/asciiflow",
                "call_back_func": None
            },
            # 趣味
            {
                "category": self.module_category_browser,
                "type": "趣味",
                "title": "记仇生成器",
                "des": "这个仇我记下了",
                "icon": "Emoji/angry-face.svg",
                "content": None,
                "link": None,
                "call_back_func": lambda : self.hold_grudges_gen()
            },
            {
                "category": self.module_category_browser,
                "type": "趣味",
                "title": "中国家庭称谓计算器",
                "des": "这下搞懂了",
                "icon": "png:Actor/RelationShip.png",
                "content":{
                    "url": "https://passer-by.com/relationship/vue/#/",
                    "size": [600, 800]
                },
                "link": "https://github.com/mumuy/relationship",
                "call_back_func": None
            },
            {
                "category": self.module_category_browser,
                "type": "趣味",
                "title": "中国制霸生成器",
                "des": "看看你都去过哪些省",
                "icon": "png:Actor/ChinaWorldEX.png",
                "content":{
                    "url": "https://lab.magiconch.com/china-ex/",
                    "size": [600, 800]
                },
                "link": "https://github.com/itorr/china-ex",
                "call_back_func": None
            },
            {
                "category": self.module_category_browser,
                "type": "趣味",
                "title": "全球制霸生成器",
                "des": "看看你都去过哪些国家",
                "icon": "png:Actor/ChinaWorldEX.png",
                "content":{
                    "url": "https://lab.magiconch.com/world-ex/",
                    "size": [600, 800]
                },
                "link": "https://github.com/itorr/world-ex",
                "call_back_func": None
            },
            # 计算器
            {
                "category": self.module_category_browser,
                "type": "计算器",
                "title": "Calcium Calculator",
                "des": "科学计算器",
                "icon": "png:Actor/Calcium.png",
                "content": {
                    "url": "https://calcium.js.org/",
                    "size": [1000, 600]
                },
                "link": "https://github.com/nocpiun/calcium",
                "call_back_func": None
            },
            {
                "category": self.module_category_browser,
                "type": "计算器",
                "title": "CL Calc",
                "des": "命令行计算器",
                "icon": "png:Actor/Clcalc.png",
                "content": {
                    "url": "https://clcalc.net/",
                    "size": [1000, 600]
                },
                "link": "https://github.com/ovk/clcalc",
                "call_back_func": None
            },
            {
                "category": self.module_category_browser,
                "type": "计算器",
                "title": "中国家庭称谓计算器",
                "des": "这下搞懂了",
                "icon": "png:Actor/RelationShip.png",
                "content":{
                    "url": "https://passer-by.com/relationship/vue/#/",
                    "size": [600, 800]
                },
                "link": "https://github.com/mumuy/relationship",
                "call_back_func": None
            },
        ]
        self.init_tab_widget()

    def hold_grudges_gen(self):
        self.toolkit.resolution_util.out_animation(self.main_object)
        hold_grudges_gen_util.show_hold_grudges_gen_dialog(self.main_object, "记仇生成器", None)

    def refresh_data(self, date_time_str):
        super().refresh_data(date_time_str)

    def refresh_ui(self, date_time_str):
        super().refresh_ui(date_time_str)
        super().refresh_ui_end(date_time_str)