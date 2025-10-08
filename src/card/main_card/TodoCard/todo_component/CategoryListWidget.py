#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import partial
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import QListWidget, QListWidgetItem, QLabel, QRubberBand, QPushButton
from PySide6 import QtCore, QtGui, QtWidgets

from src.constant.list_widget_constant import scroll_bar_style
from src.ui import style_util


class CategoryListWidget(QListWidget):

    card_map_list = []
    card_item_list = []

    show_hide_todo_group = None
    remove_todo_type_click = None

    def __init__(self, parent, show_hide_todo_group, remove_todo_type_click):
        super(CategoryListWidget, self).__init__(parent=parent)
        self.show_hide_todo_group = show_hide_todo_group
        self.remove_todo_type_click = remove_todo_type_click
        self.setStyleSheet(
        """
        QListWidget {outline: 0px;background-color: transparent;}
        QListWidget::item:selected {border-radius: 2px;border: 0px solid rgb(0, 0, 0);}
        QListWidget::item:selected:!active {border-radius: 2px;border: 0px solid transparent;}
        QListWidget::item:selected:active {border-radius: 2px;border: 0px solid rgb(0, 0, 0);}
        QListWidget::item:hover {border-radius: 2px;border: 0px solid rgb(0, 0, 0);}
        """ + scroll_bar_style)
        self.resize(400, 400)
        # 隐藏横向滚动条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # 不能编辑
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 忽略放
        self.setDefaultDropAction(Qt.IgnoreAction)
        # 设置从左到右、自动换行、依次排列
        self.setFlow(QtWidgets.QListView.LeftToRight)
        self.setWrapping(True)
        self.setResizeMode(QtWidgets.QListView.Adjust)
        # item的间隔
        self.setSpacing(5)
        # 橡皮筋(用于框选效果)
        self._rubberPos = None
        self._rubberBand = QRubberBand(QRubberBand.Rectangle, self)

    def set_card_map_list(self, card_map_list):
        self.card_map_list = card_map_list
        # 先清理老的
        self.remove_items()
        # 初始化
        self.init_items()

    def make_item(self, size, cname):
        item = QListWidgetItem(self)
        item.setData(Qt.UserRole + 1, cname)  # 把颜色放进自定义的data里面
        item.setSizeHint(size)
        label = QLabel(self)  # 自定义控件
        label.setMargin(2)  # 往内缩进2
        label.resize(size)
        # pixmap = QPixmap(size.scaled(size.width() - 4, size.height() - 4, Qt.IgnoreAspectRatio))  # 调整尺寸
        # pixmap.fill(QColor(cname))
        # label.setPixmap(pixmap)
        color = QColor(cname)
        color_str = str(color.red()) + "," + str(color.green()) + "," + str(color.blue())
        label.setStyleSheet(
        """
            border-style: solid;
            border-radius: 12px;
            border: 0px solid gray;
            background-color: rgb({});
        """.format(color_str))
        self.setItemWidget(item, label)

    def make_item_by_card(self, card_map):
        interval = 10       # 间隔
        interval_size = 5   # 左边两个，中间一个，右边两个，总计5个间隔
        width = int((self.parent().width() - interval * interval_size) / 2)
        height = 90
        size = QSize(width, height)
        item = QListWidgetItem(self)
        item.setSizeHint(size)
        # 背景板
        background_label = QLabel(self)  # 自定义控件
        background_label.setMargin(2)  # 往内缩进2
        background_label.resize(size)
        background_label.setStyleSheet("""
        QLabel {
            border-style: solid;
            border-radius: 10px;
            border: 1px solid white;
            background-color:rgba(255, 255, 255, 200);
        }""")
        # 详细按钮
        font = QtGui.QFont()
        font.setPointSize(11)
        push_button_detail = QPushButton(background_label)  # 自定义控件
        push_button_detail.setFont(font)
        push_button_detail.setGeometry(QtCore.QRect(5, 30, width - 10, 55))
        push_button_detail.setText(card_map["title"])
        push_button_detail.setCursor(Qt.CursorShape.PointingHandCursor)
        push_button_detail.setStyleSheet("""
        QPushButton {
            text-align: left;
            padding-left: 10px;
            border-style: solid;
            border-radius: 12px;
            border: 0px solid black;
            background-color: rgba(0, 0, 0, 20);
        }
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 125);
            border: 1px solid rgba(0, 0, 0, 100);
        }
        """)
        # 美化左上角长条
        line_label = QLabel(background_label)  # 自定义控件
        line_label.setGeometry(QtCore.QRect(10, 12, width - 40, 6))
        line_label.setStyleSheet("""
        QLabel {
            border-style: solid;
            border-radius: 3px;
            border: 0px solid black;
            background-color: rgba(0, 0, 0, 20);
        }
        """)
        # 右上角删除按钮
        delete_button = QtWidgets.QPushButton(background_label)
        delete_button.setGeometry(QtCore.QRect(background_label.size().width() - 10 - 18, 5, 22, 22))
        delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_button.setStyleSheet("""
        QPushButton {
            border: none;
            border-radius: 11px;
            background-color:transparent;
        }
        QPushButton:hover {
            background-color: rgba(125, 125, 125, 80);
        }""")
        delete_button.setIcon(style_util.get_icon_by_path("Character/close-one", custom_color="#FF0000"))
        delete_button.setText("")
        delete_button.setObjectName("setting_button")
        self.setItemWidget(item, background_label)
        push_button_detail.clicked.connect(partial(self.show_hide_todo_group, card_map["title"]))
        delete_button.clicked.connect(partial(self.remove_todo_type_click, card_map["title"]))
        return background_label, line_label, delete_button, push_button_detail

    def init_items(self):
        for card_map in self.card_map_list:
            self.card_item_list.append(self.make_item_by_card(card_map))

    def remove_items(self):
        """
        清除所有item
        """
        self.card_item_list = []
        # 记录当前item的数量
        count = self.count()
        # 从最后一个item开始移除，以避免索引变化的问题
        for index in reversed(range(count)):
            item = self.item(index)
            widget = self.itemWidget(item)
            if widget is not None:
                # 断开所有信号连接
                try:
                    # 尝试断开QPushButton的点击事件连接
                    self.disconnect_all(widget)
                except TypeError:
                    # 如果不是QPushButton，则忽略
                    pass
            self.takeItem(index)

    def disconnect_all(self, widget):
        """
        辅助函数，用于断开一个QWidget上的所有信号连接
        """
        meta_obj = widget.metaObject()
        for i in range(meta_obj.methodCount()):
            method = meta_obj.method(i)
            if method.methodType() == QtCore.QMetaMethod.Signal:
                # 获取信号对象
                signal_name = method.name().data().decode()
                signal = getattr(widget, signal_name, None)
                if signal is not None:
                    try:
                        # 断开所有连接
                        signal.disconnect()
                    except (TypeError, RuntimeError):
                        # 如果断开失败，可能是没有连接或者已经断开，可以忽略
                        pass
    def refresh_theme(self, is_dark=False):
        # 卡片类型列表中的样式调整
        for card_item in self.card_item_list:
            background_label, line_label, delete_button, push_button_detail = card_item
            if is_dark:
                background_label.setStyleSheet("""
                QLabel {
                    border-style: solid;
                    border-radius: 10px;
                    border: 1px solid black;
                    background-color:rgba(0, 0, 0, 200);
                }""")
                push_button_detail.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding-left: 10px;
                    border-style: solid;
                    border-radius: 12px;
                    border: 0px solid black;
                    background-color: rgba(255, 255, 255, 20);
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 50);
                }""")
                line_label.setStyleSheet("""
                QLabel {
                    border-style: solid;
                    border-radius: 3px;
                    border: 0px solid black;
                    background-color: rgba(255, 255, 255, 20);
                }""")
            else:
                background_label.setStyleSheet("""
                QLabel {
                    border-style: solid;
                    border-radius: 10px;
                    border: 1px solid white;
                    background-color:rgba(240, 242, 244, 200);
                }""")
                push_button_detail.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding-left: 10px;
                    border-style: solid;
                    border-radius: 12px;
                    border: 0px solid black;
                    background-color: rgba(0, 0, 0, 20);
                }
                QPushButton:hover {
                    background-color: rgba(0, 0, 0, 50);
                }""")
                line_label.setStyleSheet("""
                QLabel {
                    border-style: solid;
                    border-radius: 3px;
                    border: 0px solid black;
                    background-color: rgba(0, 0, 0, 20);
                }
                """)
            delete_button.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 11px;
                background-color:transparent;
            }
            QPushButton:hover {
                background-color: rgba(125, 125, 125, 80);
            }""")
            delete_button.setIcon(style_util.get_icon_by_path("Character/close-one", custom_color="#FF0000"))