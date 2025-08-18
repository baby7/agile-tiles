from src.card.component.AggregationCard.AggregationCard import AggregationCard
from src.card.main_card.ToolCard.bmi_calculator import bmi_calculator_util
from src.card.main_card.ToolCard.hold_grudges_gen import hold_grudges_gen_util
from src.card.main_card.ToolCard.housing_loan_rates import housing_loan_rates_util
from src.card.main_card.ToolCard.notebook_battery_graph import notebook_battery_graph_util
from src.card.main_card.ToolCard.relationship_calculator import relationship_calculator_util
from src.card.main_card.ToolCard.salary_calculator import salary_calculator_util


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
            # 趣味
            {
                "category": self.module_category_browser,
                "type": "趣味",
                "title": "这班上得值不值",
                "des": "测算版",
                "icon": "Game/handle-triangle.svg",
                "content": None,
                "link": "https://github.com/Zippland/worth-calculator/",
                "call_back_func": self.salary_calculator
            },
            {
                "category": self.module_category_browser,
                "type": "趣味",
                "title": "记仇生成器",
                "des": "这个仇我记下了",
                "icon": "Emoji/angry-face.svg",
                "content": None,
                "link": None,
                "call_back_func": self.hold_grudges_gen
            },
            {
                "category": self.module_category_browser,
                "type": "趣味",
                "title": "中国家庭称谓计算器",
                "des": "这下搞懂了",
                "icon": "png:Actor/RelationShip.png",
                "content": None,
                "link": "https://github.com/mumuy/relationship",
                "call_back_func": self.relationship_calculator
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
            # 工具
            {
                "category": self.module_category_browser,
                "type": "工具",
                "title": "笔记本电池健康曲线",
                "des": "查看你的电池健康报告",
                "icon": "Hardware/battery-storage.svg",
                "content": None,
                "link": "https://github.com/baiy/ctool",
                "call_back_func": self.notebook_battery_graph
            },
            {
                "category": self.module_category_browser,
                "type": "工具",
                "title": "中国房贷计算器",
                "des": "混合、商贷、混合贷计算",
                "icon": "Base/home.svg",
                "content": None,
                "link": None,
                "call_back_func": self.housing_loan_rates
            },
            {
                "category": self.module_category_browser,
                "type": "工具",
                "title": "BMI计算器",
                "des": "身体质量指数计算",
                "icon": "Sports/muscle.svg",
                "content": None,
                "link": None,
                "call_back_func": self.bmi_calculator
            },
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
        ]
        self.init_tab_widget()

    def salary_calculator(self):
        self.toolkit.resolution_util.out_animation(self.main_object)
        salary_calculator_util.show_salary_calculator_dialog(self.main_object, "这班上得值不值·测算版", None)

    def hold_grudges_gen(self):
        self.toolkit.resolution_util.out_animation(self.main_object)
        hold_grudges_gen_util.show_hold_grudges_gen_dialog(self.main_object, "记仇生成器", None)

    def relationship_calculator(self):
        self.toolkit.resolution_util.out_animation(self.main_object)
        relationship_calculator_util.show_relationship_calculator_dialog(self.main_object, "中国家庭称谓计算器", None)

    def notebook_battery_graph(self):
        self.toolkit.resolution_util.out_animation(self.main_object)
        notebook_battery_graph_util.show_notebook_battery_graph_dialog(self.main_object, "笔记本电池健康报告", None)

    def bmi_calculator(self):
        self.toolkit.resolution_util.out_animation(self.main_object)
        bmi_calculator_util.show_bmi_calculator_dialog(self.main_object, "BMI计算器", None)

    def housing_loan_rates(self):
        self.toolkit.resolution_util.out_animation(self.main_object)
        housing_loan_rates_util.show_housing_loan_rates_dialog(self.main_object, "中国房贷计算器", None)

    def refresh_data(self, date_time_str):
        super().refresh_data(date_time_str)

    def refresh_ui(self, date_time_str):
        super().refresh_ui(date_time_str)
        super().refresh_ui_end(date_time_str)