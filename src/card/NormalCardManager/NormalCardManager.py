#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import zipfile
import json
import uuid
from functools import cmp_to_key

from PySide6.QtCore import QSize, QPoint
from PySide6.QtWidgets import QLabel, QWidget
from PySide6 import QtWidgets
from src.card.NormalCardManager.NormalCardItem import NormalCardItem
from src.constant import card_constant
from src.util import file_util, version_util


class NormalCardManager(QWidget):
    # 可以拖进来的QListWidget

    first_load = True       # 第一次加载

    parent = None
    label = None
    layout = None

    plugin_info = {}  # 结构示例：{ "插件A": { "v1.0.0": "/path/to/uuid1", "v0.9.0": "/path/to/uuid2" } }

    HEADER_HEIGHT = card_constant.HEADER_HEIGHT     # 顶部高度
    CARD_WIDTH = card_constant.CARD_WIDTH           # 卡片宽度
    CARD_HEIGHT = card_constant.CARD_HEIGHT         # 卡片高度
    CARD_INTERVAL = card_constant.CARD_INTERVAL     # 卡片间距

    user_card_data_list = []  # 用户卡片数据列表
    user_card_item_list = []  # 用户卡片对象列表
    user_long_time_data = None
    toolkit = None
    info_logger = None
    save_data_func = None

    def __init__(self, parent=None, main_object=None, *args, **kwargs):
        super(NormalCardManager, self).__init__(parent, *args, **kwargs)
        self.parent = main_object
        self.resize(self.parent.width(), self.parent.height())
        self.setAcceptDrops(True)
        # 透明
        self.setStyleSheet("background:transparent;")
        self.lower()

    def set_card_map_list(self, user_card_list, user_long_time_data,
                          toolkit=None, info_logger=None, save_data_func=None):
        self.reload_plugin_file()
        self.cleanup_old_versions()
        self.resize(self.parent.width(), self.parent.height())
        self.user_card_data_list = user_card_list
        self.user_long_time_data = user_long_time_data
        self.toolkit = toolkit
        self.info_logger = info_logger
        self.save_data_func = save_data_func
        self.render_card_list()

    def reload_plugin_file(self):
        """
        重新加载插件ZIP文件
        1. 遍历插件目录的ZIP文件
        2. 验证config.json有效性
        3. 生成UUID目录并解压
        """
        plugin_dir = os.path.join(os.getcwd(), "plugin")
        for filename in os.listdir(plugin_dir):
            if not filename.lower().endswith('.zip'):
                continue
            zip_path = os.path.join(plugin_dir, filename)
            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    # 基础校验
                    if 'config.json' not in zip_ref.namelist():
                        print(f"错误: {filename} 缺少config.json文件")
                        continue
                    # 读取插件信息（仅校验，不用于目录命名）
                    with zip_ref.open('config.json') as f:
                        config = json.load(f)
                        if not config.get('name', '').strip():
                            print(f"警告: {filename} 缺少有效插件名称")
                            continue
                    # 生成UUID目录
                    target_dir = os.path.join(plugin_dir, str(uuid.uuid4()))
                    # 解压文件
                    if not file_util.extract_zip(zip_path, target_dir):
                        print(f"解压失败: {filename}")
            except zipfile.BadZipFile:
                print(f"错误: {filename} 不是有效的ZIP文件")
            except Exception as e:
                print(f"处理 {filename} 时发生错误: {str(e)}")
            # 删除该zip文件
            try:
                os.remove(zip_path)
            except Exception as e:
                print(f"删除 {filename} 时发生错误: {str(e)}")

    def scan_plugins(self):
        """
        遍历插件目录并建立插件信息索引
        """
        self.plugin_info.clear()
        plugin_dir = os.path.join(os.getcwd(), "plugin")

        for dir_name in os.listdir(plugin_dir):
            dir_path = os.path.join(plugin_dir, dir_name)
            config_path = os.path.join(dir_path, 'config.json')

            if not os.path.isdir(dir_path) or not os.path.exists(config_path):
                continue

            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    plugin_name = config.get('name', '').strip()
                    version = config.get('version', '').strip().lower()

                    if not plugin_name or not version:
                        continue

                    # 统一版本格式（移除可能存在的v前缀）
                    version = version.lstrip('v')

                    # 存储结构：插件名称 -> 版本 -> 目录路径
                    if plugin_name not in self.plugin_info:
                        self.plugin_info[plugin_name] = {}
                    self.plugin_info[plugin_name][version] = dir_path

            except Exception as e:
                print(f"读取插件配置失败：{dir_path} - {str(e)}")

    def cleanup_old_versions(self):
        """
        清理旧版本插件（保留每个插件的最新版本）
        """
        self.scan_plugins()  # 先更新插件信息
        for plugin_name, versions in self.plugin_info.items():
            if len(versions) <= 1:
                continue
            # 获取所有版本列表
            version_list = list(versions.keys())
            # 使用cmp_to_key进行排序
            version_list.sort(
                key=cmp_to_key(version_util.compare_versions),
                reverse=True  # 降序排列（最新版本在前）
            )
            # 保留最新版本
            latest_version = version_list[0]
            if self.first_load:
                print(f"准备删除旧版本：{plugin_name} v{version_list[1:]}")
                # 只处理旧版本（跳过最新版）
                for old_version in version_list[1:]:
                    old_path = versions[old_version]
                    if file_util.atomic_delete(old_path):
                        del self.plugin_info[plugin_name][old_version]
                        print(f"成功删除：{plugin_name} v{old_version}")
                    else:
                        print(f"保留目录：{old_path}（删除失败）")
        self.first_load = False

    def get_card_list(self):
        card_list = []
        for card_item in self.user_card_item_list:
            if card_item.card is None:
                continue
            card_list.append(card_item.card)
        return card_list

    def clear_all(self):
        """
        清空所有卡片
        :return:
        """
        print("类CardManager开始:clear_all函数")
        for card_item in self.user_card_item_list:
            if card_item.card:
                card_item.card.clear()  # 确保调用卡片清理
            card_item.clear()
            card_item.deleteLater()
        self.user_card_item_list = []
        print("类CardManager结束:clear_all函数")

    def render_card_list(self):
        """
        渲染卡片列表
        """
        # 先清理
        if len(self.user_card_item_list) > 0:
            self.user_card_item_list = []
        if self.layout is not None and self.label is not None:
            self.layout.removeWidget(self.label)
        if self.label is not None:
            self.label.clear()
        # 基础
        self.label = QLabel(self)
        self.label.move(QPoint(0, 0))
        self.label.resize(QSize(self.width(), self.height()))
        for user_card_map in self.user_card_data_list:
            card_name = user_card_map["name"]
            if card_name == "MainCard":
                continue
            # 位置
            x = int(int(user_card_map["x"]) - 1) * self.CARD_WIDTH + int(user_card_map["x"]) * self.CARD_INTERVAL
            y = int(int(user_card_map["y"]) - 1) * self.CARD_HEIGHT + int(user_card_map["y"]) * self.CARD_INTERVAL + self.HEADER_HEIGHT
            # 大小
            card_width = int(user_card_map["size"].split("_")[0])
            card_height = int(user_card_map["size"].split("_")[1])
            width = card_width * self.CARD_WIDTH + (card_width - 1) * self.CARD_INTERVAL
            height = card_height * self.CARD_HEIGHT + (card_height - 1) * self.CARD_INTERVAL
            size = QSize(width, height)
            # 调整
            if card_name == "ImageCard":
                card_name = card_name + "_" + user_card_map["size"]
            card_item = self.build_card(self.label, x, y, size, card_name, user_card_map)
            # 卡片
            self.user_card_item_list.append(card_item)
        # 布局
        self.layout = QtWidgets.QStackedLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

    def build_card(self, widget, x, y, size, card_name, user_card_map):
        # 数据
        long_time_data = None
        if card_name in self.user_long_time_data:
            long_time_data = self.user_long_time_data[card_name]
        card_item = NormalCardItem(self.parent, widget, self.plugin_info, self.parent.is_dark, size, user_card_map, long_time_data,
                                   self.toolkit, self.info_logger, self.save_data_func)
        card_item.resize(size)
        card_item.move(QPoint(x, y))
        if card_item.card is not None:
            card_item.card.init_ui()
            card_item.set_theme(self.parent.is_dark)
        return card_item

    def set_theme(self):
        for card_item in self.user_card_item_list:
            card_item.set_theme(self.parent.is_dark)

    def show_form(self):
        for card_item in self.user_card_item_list:
            try:
                card_item.card.show_form()
            except Exception as e:
                print(e)

    def hide_form(self):
        for card_item in self.user_card_item_list:
            try:
                card_item.card.hide_form()
            except Exception as e:
                print(e)

    def refresh_card_list(self, normal_card_data_update_list, enduring_changes):
        """
        对需要改变的卡片列表进行数据更新
        """
        for card_item in self.user_card_item_list:
            name = card_item.name
            size = card_item.size
            x = card_item.data_x
            y = card_item.data_y
            for card in normal_card_data_update_list:
                if card["name"] == name and card["size"] == size and card["x"] == x and card["y"] == y:
                    cache_data = card["data"]
                    if hasattr(card_item, 'update_cache'):
                        card_item.card.update_cache(cache=cache_data)
                    if name in enduring_changes:
                        enduring_data = enduring_changes[name]
                        enduring_data_type = enduring_data["type"]
                        if enduring_data_type == "added" or enduring_data_type == "removed":
                            enduring_real_data = enduring_data["data"]
                        else:
                            enduring_real_data = enduring_data["new_data"]
                        if hasattr(card_item, 'update_data'):
                            card_item.card.update_data(data=enduring_real_data)
                        if hasattr(card_item, 'update_all'):
                            card_item.card.update_all(cache=cache_data, data=enduring_real_data)
                    break
