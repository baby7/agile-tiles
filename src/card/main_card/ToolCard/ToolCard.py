from src.card.component.AggregationCard.AggregationCard import AggregationCard


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
            # 翻译
            {
                "category": self.module_category_browser,
                "type": "翻译",
                "title": "有道翻译",
                "des": "网易家的翻译工具",
                "icon": "Base/translate.svg",
                "content":{
                    "url": "https://fanyi.youdao.com/#/TextTranslate",
                    "size": [1500, 800]
                },
                "link": "https://fanyi.youdao.com/#/TextTranslate",
                "call_back_func": None
            },
            {
                "category": self.module_category_browser,
                "type": "翻译",
                "title": "百度翻译",
                "des": "百度家的翻译工具",
                "icon": "Base/translate.svg",
                "content":{
                    "url": "https://fanyi.baidu.com/mtpe-individual/multimodal?aldtype=16047&ext_channel=Aldtype#/auto/zh",
                    "size": [1500, 800]
                },
                "link": "https://fanyi.baidu.com/mtpe-individual/multimodal?aldtype=16047&ext_channel=Aldtype#/auto/zh",
                "call_back_func": None
            },
            {
                "category": self.module_category_browser,
                "type": "翻译",
                "title": "谷歌翻译",
                "des": "谷歌家的翻译工具",
                "icon": "Brand/google.svg",
                "content":{
                    "url": "https://translate.google.com/?hl=zh-cn&sl=auto&tl=zh-CN&op=translate",
                    "size": [1500, 800]
                },
                "link": "https://translate.google.com/?hl=zh-cn&sl=auto&tl=zh-CN&op=translate",
                "call_back_func": None
            },
            {
                "category": self.module_category_browser,
                "type": "翻译",
                "title": "必应翻译",
                "des": "微软家的翻译工具",
                "icon": "Brand/windows.svg",
                "content":{
                    "url": "https://www.bing.com/translator/",
                    "size": [1500, 800]
                },
                "link": "https://www.bing.com/translator/",
                "call_back_func": None
            },
            {
                "category": self.module_category_browser,
                "type": "翻译",
                "title": "讯飞翻译",
                "des": "科大讯飞的翻译工具",
                "icon": "Base/translate.svg",
                "content":{
                    "url": "https://fanyi.xfyun.cn/console/trans/text",
                    "size": [1500, 800]
                },
                "link": "https://fanyi.xfyun.cn/console/trans/text",
                "call_back_func": None
            },
            {
                "category": self.module_category_browser,
                "type": "翻译",
                "title": "DeepL翻译",
                "des": "DeepL 的翻译工具",
                "icon": "Base/translate.svg",
                "content":{
                    "url": "https://www.deepl.com/zh/translator",
                    "size": [1500, 800]
                },
                "link": "https://www.deepl.com/zh/translator",
                "call_back_func": None
            },
            # 程序员
            {
                "category": self.module_category_browser,
                "type": "程序员",
                "title": "Ctool",
                "des": "程序员工具箱",
                "icon": "Base/tool.svg",
                "content":{
                    "url": "/static/html/Tool/ctool_web/index.html",
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
                "icon": "Office/doc-search.svg",
                "content":{
                    "url": "/static/html/Tool/reference/index.html",
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
                "icon": "Connect/api.svg",
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
                "icon": "Components/platte.svg",
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
                "icon": "Edit/mind-mapping.svg",
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
                "icon": "Edit/grid-sixteen.svg",
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
                "icon": "Components/platte.svg",
                "content":{
                    "url": "https://yqnn.github.io/svg-path-editor/",
                    "size": [1000, 800]
                },
                "call_back_func": None
            },
            {
                "category": self.module_category_browser,
                "type": "作图",
                "title": "ASCIIFlow",
                "des": "Ascii作图工具",
                "icon": "Edit/write.svg",
                "content":{
                    "url": "/static/html/Tool/asciiflow/index.html",
                    "size": [1200, 950]
                },
                "link": "https://github.com/Yqnn/svg-path-editor",
                "call_back_func": None
            },
            # 生活
            {
                "category": self.module_category_browser,
                "type": "生活",
                "title": "中国家庭称谓计算器",
                "des": "这下搞懂了",
                "icon": "Charts/chart-graph.svg",
                "content":{
                    "url": "https://passer-by.com/relationship/vue/#/",
                    "size": [600, 800]
                },
                "link": "https://github.com/mumuy/relationship",
                "call_back_func": None
            },
            {
                "category": self.module_category_browser,
                "type": "生活",
                "title": "中国制霸生成器",
                "des": "看看你都去过哪些省",
                "icon": "Travel/map-two.svg",
                "content":{
                    "url": "https://lab.magiconch.com/china-ex/",
                    "size": [600, 800]
                },
                "link": "https://github.com/itorr/china-ex",
                "call_back_func": None
            },
            {
                "category": self.module_category_browser,
                "type": "生活",
                "title": "全球制霸生成器",
                "des": "看看你都去过哪些国家",
                "icon": "Travel/world.svg",
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
                "icon": "Charts/arithmetic-one.svg",
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
                "icon": "Others/terminal.svg",
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
                "icon": "Charts/chart-graph.svg",
                "content":{
                    "url": "https://passer-by.com/relationship/vue/#/",
                    "size": [600, 800]
                },
                "link": "https://github.com/mumuy/relationship",
                "call_back_func": None
            },
        ]
        self.init_tab_widget()

    def refresh_data(self, date_time_str):
        super().refresh_data(date_time_str)

    def refresh_ui(self, date_time_str):
        super().refresh_ui(date_time_str)
        super().refresh_ui_end(date_time_str)