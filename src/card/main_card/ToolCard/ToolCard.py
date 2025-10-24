from PySide6.QtWidgets import QVBoxLayout

from src.card.card_component.AggregationCard.AggregationCard import AggregationCard


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
            # 工具
            {
                "category": self.module_category_browser,
                "type": "工具",
                "title": "屏幕截图",
                "des": "默认快捷键Alt+2",
                "icon": "Edit/screenshot",
                "content": None,
                "link": None,
                "call_back_func": self.screenshot
            },
            {
                "category": self.module_category_browser,
                "type": "工具",
                "title": "屏幕取色",
                "des": "获取屏幕某个点的颜色",
                "icon": "Hardware/electronic-pen",
                "content": None,
                "link": None,
                "call_back_func": self.color_picker
            },
            {
                "category": self.module_category_browser,
                "type": "工具",
                "title": "图片批量转表格",
                "des": "批量图片OCR识别转表格",
                "icon": "Office/excel",
                "content": None,
                "link": None,
                "call_back_func": self.image_to_excel_converter
            },
            {
                "category": self.module_category_browser,
                "type": "工具",
                "title": "颜色转换器",
                "des": "转换各种颜色格式",
                "icon": "Components/platte",
                "content": None,
                "link": None,
                "call_back_func": self.color_converter
            },
            {
                "category": self.module_category_browser,
                "type": "工具",
                "title": "文件批量操作",
                "des": "根据规则批量重命名/删除",
                "icon": "Office/file-editing",
                "content": None,
                "link": None,
                "call_back_func": self.file_operation
            },
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
            # 程序员
            {
                "category": self.module_category_browser,
                "type": "程序员",
                "title": "时间计算器",
                "des": "时间/时区、时间戳的计算",
                "icon": "Time/stopwatch-start",
                "content": None,
                "link": None,
                "call_back_func": lambda : self.time_calculator("时间计算器")
            },
            {
                "category": self.module_category_browser,
                "type": "程序员",
                "title": "颜色转换器",
                "des": "转换各种颜色格式",
                "icon": "Components/platte",
                "content": None,
                "link": None,
                "call_back_func": self.color_converter
            },
            {
                "category": self.module_category_browser,
                "type": "程序员",
                "title": "编解码工具",
                "des": "URL Base64 ASCII 等",
                "icon": "Sports/muscle",
                "content": None,
                "link": None,
                "call_back_func": lambda : self.codec_tool("编解码工具")
            },
            {
                "category": self.module_category_browser,
                "type": "程序员",
                "title": "Base64图片编解码",
                "des": "Base64文本和图片互转",
                "icon": "Office/file-conversion",
                "content": None,
                "link": None,
                "call_back_func": lambda : self.base64_image_tool("Base64图片编解码工具")
            },
            {
                "category": self.module_category_browser,
                "type": "程序员",
                "title": "加解密工具",
                "des": "A/DES RC4 Rabbi MD5 等",
                "icon": "Safe/key",
                "content": None,
                "link": None,
                "call_back_func": lambda : self.crypto_tool("加解密工具")
            },
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
                "title": "Cron表达式生成器",
                "des": "Crontab表达式生成器",
                "icon": "Time/alarm-clock",
                "content": None,
                "link": None,
                "call_back_func": lambda : self.cron_generator("Cron表达式生成器")
            },
            {
                "category": self.module_category_browser,
                "type": "程序员",
                "title": "UUID生成器",
                "des": "批量生成UUID",
                "icon": "Edit/layers",
                "content": None,
                "link": None,
                "call_back_func": lambda : self.uuid_generator("UUID生成器")
            },
            {
                "category": self.module_category_browser,
                "type": "程序员",
                "title": "本机IP信息",
                "des": "查看本机IP详细信息",
                "icon": "Connect/network-tree",
                "content": None,
                "link": None,
                "call_back_func": lambda : self.ip_info("本机IP信息")
            },
            {
                "category": self.module_category_browser,
                "type": "程序员",
                "title": "JWT编解码工具",
                "des": "JWT头部、载荷、签名",
                "icon": "Connect/network-tree",
                "content": None,
                "link": None,
                "call_back_func": lambda : self.jwt_tool("JWT编解码工具")
            },
            {
                "category": self.module_category_browser,
                "type": "程序员",
                "title": "IP归属地",
                "des": "查询IP地址的地理位置",
                "icon": "Connect/network-tree",
                "content": None,
                "link": None,
                "call_back_func": lambda : self.ip_location_query("IP归属地")
            },
            # 生活
            {
                "category": self.module_category_browser,
                "type": "生活",
                "title": "中国房贷计算器",
                "des": "混合、商贷、混合贷计算",
                "icon": "Base/home",
                "content": None,
                "link": None,
                "call_back_func": self.housing_loan_rates
            },
            {
                "category": self.module_category_browser,
                "type": "生活",
                "title": "个人所得税计算器",
                "des": "个人所得税计算",
                "icon": "Money/paper-money",
                "content": None,
                "link": None,
                "call_back_func": lambda : self.tax_calculator("个人所得税计算器")
            },
            {
                "category": self.module_category_browser,
                "type": "生活",
                "title": "BMI计算器",
                "des": "身体质量指数计算",
                "icon": "Sports/muscle",
                "content": None,
                "link": None,
                "call_back_func": lambda : self.bmi_calculator("BMI计算器")
            },
            {
                "category": self.module_category_browser,
                "type": "生活",
                "title": "热量计算器",
                "des": "卡路里、大卡、千焦转换",
                "icon": "Foods/chicken-leg",
                "content": None,
                "link": None,
                "call_back_func": lambda : self.calorie_calculator("热量计算器")
            },
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
        ]
        self.init_tab_widget()

    def screenshot(self):
        self.main_object.on_screenshot_hotkey_triggered()

    def color_picker(self):
        self.main_object.start_color_picker()

    def image_to_excel_converter(self):
        # 未登录的判断
        self.main_object.show_login_tip()
        if self.main_object.current_user['username'] == "LocalUser":
            return
        self.main_object.start_image_to_excel_converter()

    def color_converter(self):
        self.main_object.color_picker_captured()

    def salary_calculator(self):
        from src.card.main_card.ToolCard.salary_calculator import salary_calculator_util
        self.toolkit.resolution_util.out_animation(self.main_object)
        salary_calculator_util.show_salary_calculator_dialog(self.main_object, "这班上得值不值·测算版", None)

    def file_operation(self):
        from src.card.main_card.ToolCard.file_operation import file_operation_util
        self.toolkit.resolution_util.out_animation(self.main_object)
        file_operation_util.show_file_operation_dialog(self.main_object, "文件批量操作", None)

    def hold_grudges_gen(self, title):
        from src.card.main_card.ToolCard.hold_grudges_gen.hold_grudges_gen_util import HoldGrudgesGenPopup
        # 清理展示面板
        self.clear_show_panel()
        self.util_app = HoldGrudgesGenPopup(self.card, main_object=self.main_object, is_dark=self.main_object.is_dark)
        self.show_util_in_show_panel(title=title, util_app=self.util_app)

    def relationship_calculator(self):
        from src.card.main_card.ToolCard.relationship_calculator import relationship_calculator_util
        self.toolkit.resolution_util.out_animation(self.main_object)
        relationship_calculator_util.show_relationship_calculator_dialog(self.main_object, "中国家庭称谓计算器", None)

    def progress_bar_generator(self):
        from src.card.main_card.ToolCard.progress_bar_generator import progress_bar_generator_util
        self.toolkit.resolution_util.out_animation(self.main_object)
        progress_bar_generator_util.show_progress_bar_generator_dialog(self.main_object, "视频进度条生成器", None)

    def notebook_battery_graph(self):
        from src.card.main_card.ToolCard.notebook_battery_graph import notebook_battery_graph_util
        self.toolkit.resolution_util.out_animation(self.main_object)
        notebook_battery_graph_util.show_notebook_battery_graph_dialog(self.main_object, "笔记本电池健康报告", None)

    def tax_calculator(self, title):
        from src.card.main_card.ToolCard.tax_calculator.tax_calculator_util import TaxCalculatorPopup
        # 清理展示面板
        self.clear_show_panel()
        self.util_app = TaxCalculatorPopup(self.card, main_object=self.main_object, is_dark=self.main_object.is_dark)
        self.show_util_in_show_panel(title=title, util_app=self.util_app)

    def bmi_calculator(self, title):
        from src.card.main_card.ToolCard.bmi_calculator.bmi_calculator_util import BMICalculatorPopup
        # 清理展示面板
        self.clear_show_panel()
        self.util_app = BMICalculatorPopup(self.card, main_object=self.main_object, is_dark=self.main_object.is_dark)
        self.show_util_in_show_panel(title=title, util_app=self.util_app)

    def calorie_calculator(self, title):
        from src.card.main_card.ToolCard.calorie_calculator.calorie_calculator_util import CalorieCalculatorPopup
        # 清理展示面板
        self.clear_show_panel()
        self.util_app = CalorieCalculatorPopup(self.card, main_object=self.main_object, is_dark=self.main_object.is_dark)
        self.show_util_in_show_panel(title=title, util_app=self.util_app)

    def cron_generator(self, title):
        from src.card.main_card.ToolCard.cron_generator.cron_generator_util import CronGeneratorPopup
        # 清理展示面板
        self.clear_show_panel()
        self.util_app = CronGeneratorPopup(self.card, main_object=self.main_object, is_dark=self.main_object.is_dark)
        self.show_util_in_show_panel(title=title, util_app=self.util_app)

    def uuid_generator(self, title):
        from src.card.main_card.ToolCard.uuid_generator.uuid_generator_util import UUIDGeneratorPopup
        # 清理展示面板
        self.clear_show_panel()
        self.util_app = UUIDGeneratorPopup(self.card, main_object=self.main_object, is_dark=self.main_object.is_dark)
        self.show_util_in_show_panel(title=title, util_app=self.util_app)

    def jwt_tool(self, title):
        from src.card.main_card.ToolCard.jwt_tool.jwt_tool_util import JWTEncoderDecoderPopup
        # 清理展示面板
        self.clear_show_panel()
        self.util_app = JWTEncoderDecoderPopup(self.card, main_object=self.main_object, is_dark=self.main_object.is_dark)
        self.show_util_in_show_panel(title=title, util_app=self.util_app)

    def ip_location_query(self, title):
        from src.card.main_card.ToolCard.ip_location_query.ip_location_query_util import IPLocationQueryPopup
        # 清理展示面板
        self.clear_show_panel()
        self.util_app = IPLocationQueryPopup(self.card, main_object=self.main_object, is_dark=self.main_object.is_dark)
        self.show_util_in_show_panel(title=title, util_app=self.util_app)

    def ip_info(self, title):
        from src.card.main_card.ToolCard.ip_info.ip_info_util import IPInfoPopup
        # 清理展示面板
        self.clear_show_panel()
        self.util_app = IPInfoPopup(self.card, main_object=self.main_object, is_dark=self.main_object.is_dark)
        self.show_util_in_show_panel(title=title, util_app=self.util_app)

    def codec_tool(self, title):
        from src.card.main_card.ToolCard.codec_tool.codec_tool_util import CodecTool
        # 清理展示面板
        self.clear_show_panel()
        self.util_app = CodecTool(self.card, main_object=self.main_object, is_dark=self.main_object.is_dark)
        self.show_util_in_show_panel(title=title, util_app=self.util_app)

    def base64_image_tool(self, title):
        from src.card.main_card.ToolCard.base64_image_tool.base64_image_tool_util import Base64ImageTool
        # 清理展示面板
        self.clear_show_panel()
        self.util_app = Base64ImageTool(self.card, main_object=self.main_object, is_dark=self.main_object.is_dark)
        self.show_util_in_show_panel(title=title, util_app=self.util_app)

    def crypto_tool(self, title):
        from src.card.main_card.ToolCard.crypto_too.crypto_tool_util import CryptoTool
        # 清理展示面板
        self.clear_show_panel()
        self.util_app = CryptoTool(self.card, main_object=self.main_object, is_dark=self.main_object.is_dark)
        self.show_util_in_show_panel(title=title, util_app=self.util_app)

    def json_formatter(self):
        from src.card.main_card.ToolCard.json_formatter import json_formatter_util
        self.toolkit.resolution_util.out_animation(self.main_object)
        json_formatter_util.show_json_formatter_dialog(self.main_object, "Json格式化工具", None)

    def time_calculator(self, title):
        from src.card.main_card.ToolCard.time_calculator.time_calculator_util import TimeCalculatorApp
        # 清理展示面板
        self.clear_show_panel()
        self.util_app = TimeCalculatorApp(self.card, main_object=self.main_object, is_dark=self.main_object.is_dark)
        self.show_util_in_show_panel(title=title, util_app=self.util_app)

    def housing_loan_rates(self):
        from src.card.main_card.ToolCard.housing_loan_rates import housing_loan_rates_util
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