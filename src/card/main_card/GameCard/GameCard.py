from src.card.card_component.AggregationCard.AggregationCard import AggregationCard
from src.card.main_card.GameCard.link import game_list, tool_list, draw_list, knowledge_list, programmer_list, interesting_list, top_list


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
    # 新增：记录已加载的分类
    loaded_tabs = set()


    def __init__(self, main_object=None, parent=None, theme=None, card=None, cache=None, data=None,
                 toolkit=None, logger=None, save_data_func=None):
        super().__init__(main_object=main_object, parent=parent, theme=theme, card=card, cache=cache, data=data,
                         toolkit=toolkit, logger=logger, save_data_func=save_data_func)

    def init_ui(self):
        super().init_ui()
        # 设置信息条样式和内容
        self.info_bar.setText("以下为第三方模块，本工具不对其内容负责(分类可滚动鼠标滑轮切换)")
        self.info_bar.setStyleSheet(
            f"background: transparent; border: none; font-weight: bold; font-size: 12px; color: rgba(255, 140, 0, 0.8);"
        )
        self.info_bar.show()
        self.aggregation_module_list = (top_list.top_list
                                        + game_list.game_list
                                        + tool_list.tool_list
                                        + programmer_list.programmer_list
                                        + draw_list.draw_list
                                        + interesting_list.interesting_list
                                        + knowledge_list.knowledge_list)
        # for aggregation_module in self.aggregation_module_list:
        #     if aggregation_module["icon"] is None:
        #         aggregation_module["icon"] = "Travel/planet.svg"
        self.init_tab_widget()

    def refresh_data(self, date_time_str):
        super().refresh_data(date_time_str)

    def refresh_ui(self, date_time_str):
        super().refresh_ui(date_time_str)
        super().refresh_ui_end(date_time_str)