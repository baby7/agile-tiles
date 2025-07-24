# -*- coding: utf-8 -*-
import uuid
from functools import cmp_to_key

from PySide6 import QtWidgets
from PySide6.QtWidgets import QWidget
from src.card.NormalCardManager.NormalCard import NormalCard
from src.util import version_util
from src.ui import style_util


class NormalCardItem(QWidget):

    id = None
    card = None
    plugin_info_map = {}

    def __init__(self, main_object=None, parent=None, plugin_info_map=None, is_dark=False, size=None, card_data=None, long_time_data=None,
                 toolkit=None, info_logger=None, save_data_func=None):
        super(NormalCardItem, self).__init__(parent)
        self.plugin_info_map = plugin_info_map
        # 信息
        self.data_name = card_data["name"]
        self.data_size = card_data["size"]
        self.data_x = card_data["x"]
        self.data_y = card_data["y"]
        # 主背景
        self.label = QWidget(parent)  # 自定义控件
        self.label.resize(size)
        # 填充内容
        theme = "Dark" if is_dark else "Light"
        card_name = card_data["name"]
        # 获取插件信息
        plugin_info = self.plugin_info_map[card_name]
        if len(plugin_info) <= 1:
            plugin_dir = plugin_info[list(plugin_info.keys())[0]]
        else:
            # 获取所有版本列表
            version_list = list(plugin_info.keys())
            # 使用cmp_to_key进行排序
            version_list.sort(
                key=cmp_to_key(version_util.compare_versions),
                reverse=True  # 降序排列（最新版本在前）
            )
            # 保留最新版本
            latest_version = version_list[0]
            plugin_dir = plugin_info[latest_version]
        self.card = NormalCard(main_object=main_object, parent=self, card_name=card_name, theme=theme, x=card_data["x"], y=card_data["y"],
                         size=card_data["size"], card=self.label,
                         cache=card_data["data"], data=long_time_data,
                         toolkit=toolkit, logger=info_logger,
                         plugin_dir=plugin_dir, save_data_func=save_data_func)
        # 调整位置
        self.label.raise_()
        self.layout = QtWidgets.QStackedLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.id = str(uuid.uuid4())

    def set_theme(self, is_dark):
        if is_dark:
            style_util.set_card_shadow_effect(self)        # 添加外部阴影效果
            # 纯紫色: background-color: rgba(40, 42, 54, 255);
            # 紫色渐变: background-color: qlineargradient(x1:0, y1:1, x2:0, y2:0,stop:0 rgba(34, 36, 48, 255), stop:1 rgba(40, 42, 54, 255));
            # 蓝色渐变: background-color: qlineargradient(x1:0, y1:1, x2:0, y2:0,stop:0 rgba(36, 41, 52, 255), stop:1 rgba(26, 32, 50, 255));
            style = """
                border-radius: 12px;
                border: 1px solid #262934;
                background-color: rgba(34, 34, 34, 255);
            """
        else:
            style_util.remove_card_shadow_effect(self)     # 移除外部阴影效果
            style = """
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 170);
                background-color: rgba(255, 255, 255, 160);
            """
        self.label.setStyleSheet(style)
        if self.card is None:
            return
        self.card.set_theme(is_dark)

    def enterEvent(self, event):
        """ 鼠标进入卡片时 """
        super(NormalCardItem, self).enterEvent(event)
        self.card.enter_event()

    def leaveEvent(self, event):
        """ 鼠标离开卡片时 """
        super(NormalCardItem, self).leaveEvent(event)
        self.card.leave_event()

    def clear(self):
        self.id = None
        if self.card is not None:
            self.card.clear()
            self.card.deleteLater()
        self.deleteLater()
