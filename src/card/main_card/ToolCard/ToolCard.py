from PySide6.QtWidgets import QVBoxLayout

from src.card.component.AggregationCard.AggregationCard import AggregationCard
from src.card.main_card.ToolCard.bmi_calculator.bmi_calculator_util import BMICalculatorPopup
from src.card.main_card.ToolCard.hold_grudges_gen.hold_grudges_gen_util import HoldGrudgesGenPopup
from src.card.main_card.ToolCard.housing_loan_rates import housing_loan_rates_util
from src.card.main_card.ToolCard.json_formatter import json_formatter_util
from src.card.main_card.ToolCard.notebook_battery_graph import notebook_battery_graph_util
from src.card.main_card.ToolCard.progress_bar_generator import progress_bar_generator_util
from src.card.main_card.ToolCard.relationship_calculator import relationship_calculator_util
from src.card.main_card.ToolCard.salary_calculator import salary_calculator_util
from src.card.main_card.ToolCard.time_calculator.time_calculator_util import TimeCalculatorApp


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
    # 新增：记录已加载的分类
    loaded_tabs = set()


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
                "icon": "Game/handle-triangle",
                "content": None,
                "link": "https://github.com/Zippland/worth-calculator/",
                "call_back_func": self.salary_calculator
            },
            {
                "category": self.module_category_browser,
                "type": "趣味",
                "title": "记仇生成器",
                "des": "这个仇我记下了",
                "icon": "Emoji/angry-face",
                "content": None,
                "link": None,
                "call_back_func": lambda : self.hold_grudges_gen("记仇生成器")
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
            # 工具
            {
                "category": self.module_category_browser,
                "type": "工具",
                "title": "视频进度条生成器",
                "des": "为视频底部增加进度条",
                "icon": "Music/playback-progress",
                "content": None,
                "link": None,
                "call_back_func": self.progress_bar_generator
            },
            {
                "category": self.module_category_browser,
                "type": "工具",
                "title": "笔记本电池健康曲线",
                "des": "查看你的电池健康报告",
                "icon": "Hardware/battery-storage",
                "content": None,
                "link": None,
                "call_back_func": self.notebook_battery_graph
            },
            {
                "category": self.module_category_browser,
                "type": "工具",
                "title": "中国房贷计算器",
                "des": "混合、商贷、混合贷计算",
                "icon": "Base/home",
                "content": None,
                "link": None,
                "call_back_func": self.housing_loan_rates
            },
            {
                "category": self.module_category_browser,
                "type": "工具",
                "title": "BMI计算器",
                "des": "身体质量指数计算",
                "icon": "Sports/muscle",
                "content": None,
                "link": None,
                "call_back_func": lambda : self.bmi_calculator("BMI计算器")
            },
            # 程序员
            {
                "category": self.module_category_browser,
                "type": "程序员",
                "title": "Json格式化工具",
                "des": "经典Json格式化工具",
                "icon": "Edit/code-brackets",
                "content": None,
                "link": None,
                "call_back_func": self.json_formatter
            },
            {
                "category": self.module_category_browser,
                "type": "程序员",
                "title": "时间计算器",
                "des": "时间、时区、时间戳的计算器",
                "icon": "Time/stopwatch-start",
                "content": None,
                "link": None,
                "call_back_func": lambda : self.time_calculator("时间计算器")
            },
        ]
        self.init_tab_widget()

    def salary_calculator(self):
        self.toolkit.resolution_util.out_animation(self.main_object)
        salary_calculator_util.show_salary_calculator_dialog(self.main_object, "这班上得值不值·测算版", None)

    def hold_grudges_gen(self, title):
        # 清理展示面板
        self.clear_show_panel()
        self.util_app = HoldGrudgesGenPopup(self.card, main_object=self.main_object, is_dark=self.main_object.is_dark)
        self.show_util_in_show_panel(title=title, util_app=self.util_app)

    def relationship_calculator(self):
        self.toolkit.resolution_util.out_animation(self.main_object)
        relationship_calculator_util.show_relationship_calculator_dialog(self.main_object, "中国家庭称谓计算器", None)

    def progress_bar_generator(self):
        self.toolkit.resolution_util.out_animation(self.main_object)
        progress_bar_generator_util.show_progress_bar_generator_dialog(self.main_object, "视频进度条生成器", None)

    def notebook_battery_graph(self):
        self.toolkit.resolution_util.out_animation(self.main_object)
        notebook_battery_graph_util.show_notebook_battery_graph_dialog(self.main_object, "笔记本电池健康报告", None)

    def bmi_calculator(self, title):
        # 清理展示面板
        self.clear_show_panel()
        self.util_app = BMICalculatorPopup(self.card, main_object=self.main_object, is_dark=self.main_object.is_dark)
        self.show_util_in_show_panel(title=title, util_app=self.util_app)

    def json_formatter(self):
        self.toolkit.resolution_util.out_animation(self.main_object)
        json_formatter_util.show_json_formatter_dialog(self.main_object, "Json格式化工具", None)

    def time_calculator(self, title):
        # 清理展示面板
        self.clear_show_panel()
        self.util_app = TimeCalculatorApp(self.card, main_object=self.main_object, is_dark=self.main_object.is_dark)
        self.show_util_in_show_panel(title=title, util_app=self.util_app)

    def housing_loan_rates(self):
        self.toolkit.resolution_util.out_animation(self.main_object)
        housing_loan_rates_util.show_housing_loan_rates_dialog(self.main_object, "中国房贷计算器", None)

    def show_util_in_show_panel(self, title, util_app):
        # 设置标题
        self.show_panel_label_title.setText(title)
        # 设置右上角按钮内容
        self.show_panel_hide_button.hide()
        # 设置右上角2按钮内容
        self.show_panel_hide_button_2.hide()
        # 面板增加布局
        layout = QVBoxLayout(self.show_panel_content_panel)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        # 加入工具
        layout.addWidget(util_app)
        # 切换到展示面板
        self.stacked_widget.setCurrentIndex(1)

    def refresh_data(self, date_time_str):
        super().refresh_data(date_time_str)

    def refresh_ui(self, date_time_str):
        super().refresh_ui(date_time_str)
        super().refresh_ui_end(date_time_str)

    def refresh_theme(self):
        super().refresh_theme()
        if self.util_app is not None:
            self.util_app.refresh_theme(self.main_object)