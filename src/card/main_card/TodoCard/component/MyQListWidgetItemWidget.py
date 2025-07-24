# -*- coding: utf-8 -*-
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QFrame
from PySide6.QtCore import Qt


def get_font(family, size):
    font = QtGui.QFont()
    font.setFamily(family)
    font.setPointSize(size)
    return font

def get_icon_park_path(icon_position, is_dark):
    icon_theme_folder = "light" if is_dark else "dark"
    return QIcon("./static/img/IconPark/" + icon_theme_folder + "/" + icon_position + ".png")


class MyQListWidgetItemWidget(QWidget):

    # 控件
    label_title = None
    blank_left_label = None
    check_push_button = None
    delete_button = None
    degree_line = None
    blank_label = None
    warn_label = None
    separation_line = None
    # 布局
    main_layout = None
    layout = None
    check_and_blank_layout = None
    title_and_warn_layout = None
    # 其他
    is_dark = False
    todo_card = None

    def __init__(self, parent=None, todo_card=None, todo_id="", title="", success=False, degree="First", warn=False, time_str=""):
        super(MyQListWidgetItemWidget, self).__init__(parent)
        self.todo_card = todo_card
        self.is_dark = self.todo_card.is_dark()
        self.todo_id = todo_id
        self.parent = parent
        self.degree = degree
        self.success = success
        self.init_ui(title, success, degree, warn, time_str)
        self.refresh_theme(self.is_dark)

    def init_ui(self, title, success, degree, warn, time_str):
        # 标题
        self.label_title = self.create_label(title, "思源黑体", 11, 260, 23)
        # 勾选框左边的占位
        self.blank_left_label = self.create_label("", "", 0, 5, 10)
        # 勾选框
        self.check_push_button = self.create_check_button(success)
        # 删除按钮
        self.delete_button = self.create_delete_button()
        # 程度条
        self.degree_line = self.create_degree_line(degree, warn)
        # 提醒时间
        if warn:
            self.blank_label = self.create_label("", "", 0, 1, 10)
            self.warn_label = self.create_label("🔔 " + time_str, "思源黑体", 9, 160, 18)
        else:
            self.blank_label = None
            self.warn_label = None
        # 分隔符
        self.separation_line = self.create_separation_line()
        # 布局
        self.setup_layout(warn)

    def create_label(self, text, font_family, font_size, width, height):
        label = QtWidgets.QLabel(self.parent)
        label.setFont(get_font(font_family, font_size))
        label.setFixedSize(width, height)
        label.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        label.setText(text)
        return label

    def create_check_button(self, success):
        button = QtWidgets.QPushButton(self.parent)
        button.setFixedSize(22, 22)
        button.setIconSize(QtCore.QSize(18, 18))
        button.setFont(get_font("思源黑体", 9))
        push_button_style = """
        QPushButton {
            border: none;
            border-radius: 11px;
            background-color:transparent;
        }
        QPushButton:hover {
            background-color: rgba(125, 125, 125, 80);
        }"""
        button.setStyleSheet(push_button_style)
        if success:
            button.setIcon(get_icon_park_path("Character/check-one", self.is_dark))
        else:
            button.setIcon(get_icon_park_path("Graphics/round", self.is_dark))
        return button

    def create_delete_button(self):
        button = QtWidgets.QPushButton(self.parent)
        button.setFixedSize(22, 22)
        return button

    def create_degree_line(self, degree, warn):
        line = QFrame(self.parent)
        line.setFixedSize(6, 50 if warn else 40)
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        degree_colors = {
            "First": "rgba(255, 46, 44, 0.6)",
            "Second": "rgba(20, 185, 62, 0.6)",
            "Third": "rgba(243, 207, 19, 0.6)",
            "Other": "rgba(4, 115, 247, 0.6)"
        }
        color = degree_colors.get(degree, degree_colors["Other"])
        line.setStyleSheet(f"border-style: solid;border-radius: 3px;color: {color};"
                           f"border-color: {color};background-color: {color};")
        return line

    def create_separation_line(self):
        line = QFrame(self.parent)
        line.setFixedSize(self.todo_card.card.width() - 20, 1)
        line.setMaximumHeight(1)
        line.setStyleSheet("color: rgba(200, 200, 200, 0.3);border-color: rgba(200, 200, 200, 0.3);"
                           "background-color: rgba(200, 200, 200, 0.3);")
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        return line

    def setup_layout(self, warn):
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setContentsMargins(3, 4, 3, 0)
        self.main_layout.addWidget(self.degree_line)
        self.main_layout.addWidget(self.blank_left_label)

        self.check_and_blank_layout = QtWidgets.QVBoxLayout()
        self.check_and_blank_layout.setContentsMargins(0, 0, 0, 0)
        self.check_and_blank_layout.addWidget(self.check_push_button)
        if warn:
            self.check_and_blank_layout.addWidget(self.blank_label)

        self.main_layout.addLayout(self.check_and_blank_layout)

        self.title_and_warn_layout = QtWidgets.QVBoxLayout()
        self.title_and_warn_layout.setContentsMargins(0, 0, 0, 0)
        self.title_and_warn_layout.addWidget(self.label_title)
        if warn:
            self.title_and_warn_layout.addWidget(self.warn_label)

        self.main_layout.addLayout(self.title_and_warn_layout)
        self.main_layout.addWidget(self.delete_button)
        self.main_layout.setAlignment(self.delete_button, Qt.AlignmentFlag.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addLayout(self.main_layout)
        self.layout.addWidget(self.separation_line)
        self.setLayout(self.layout)

    def set_all(self, todo_id="", title="", success=False, degree="First", warn=False, time_str=""):
        self.todo_id = todo_id
        self.label_title.setText(title)
        self.success = success
        self.degree = degree
        self.degree_line = self.create_degree_line(degree, warn)
        if warn:
            if self.blank_label is None:
                self.blank_label = self.create_label("", "", 0, 1, 10)
                self.warn_label = self.create_label("🔔 " + time_str, "思源黑体", 9, 160, 18)
                self.check_and_blank_layout.addWidget(self.blank_label)
                self.title_and_warn_layout.addWidget(self.warn_label)
            else:
                self.warn_label.setText("🔔 " + time_str)
        else:
            if self.blank_label is not None:
                self.check_and_blank_layout.removeWidget(self.blank_label)
                self.title_and_warn_layout.removeWidget(self.warn_label)
                self.blank_label.clear()
                self.blank_label = None
                self.warn_label.clear()
                self.warn_label = None
        self.refresh_theme(self.is_dark)

    def refresh_theme(self, is_dark):
        self.is_dark = is_dark
        # 定义深色和浅色主题的颜色
        if is_dark:
            background_color = "rgba(30, 30, 30, 255)"  # 深色背景
            border_color = "rgba(255, 255, 255, 200)"  # 白色边框
            degree_colors = {
                "First": "rgba(255, 46, 44, 0.8)",  # 红色
                "Second": "rgba(20, 185, 62, 0.8)",  # 绿色
                "Third": "rgba(243, 207, 19, 0.8)",  # 黄色
                "Other": "rgba(4, 115, 247, 0.8)"  # 蓝色
            }
        else:
            background_color = "rgba(255, 255, 255, 255)"  # 浅色背景
            border_color = "rgba(0, 0, 0, 255)"  # 黑色边框
            degree_colors = {
                "First": "rgba(255, 46, 44, 0.6)",  # 红色
                "Second": "rgba(20, 185, 62, 0.6)",  # 绿色
                "Third": "rgba(243, 207, 19, 0.6)",  # 黄色
                "Other": "rgba(4, 115, 247, 0.6)"  # 蓝色
            }
        # 更新标题标签样式
        self.label_title.setStyleSheet(f"background-color:transparent;")
        # 更新勾选框样式
        push_button_style = """
        QPushButton {
            border: none;
            border-radius: 11px;
            background-color:transparent;
        }
        QPushButton:hover {
            background-color: rgba(125, 125, 125, 80);
        }"""
        self.check_push_button.setStyleSheet(push_button_style)
        if self.success:
            self.check_push_button.setIcon(get_icon_park_path("Character/check-one", self.is_dark))
        else:
            self.check_push_button.setIcon(get_icon_park_path("Graphics/round", self.is_dark))
        # 更新删除按钮样式
        self.delete_button.setStyleSheet(push_button_style)
        self.delete_button.setIcon(QIcon("./static/img/IconPark/red/Character/close-one.png"))
        # 更新程度条样式
        degree_color = degree_colors.get(self.degree, degree_colors["Other"])
        self.degree_line.setStyleSheet(
            f"border-style: solid; border-radius: 3px; color: {degree_color}; "
            f"border-color: {degree_color}; background-color: {degree_color};"
        )
        # 更新提醒时间标签样式
        if self.warn_label:
            self.warn_label.setStyleSheet(f"background-color:transparent;")
        # 更新分隔符样式
        self.separation_line.setStyleSheet(
            f"color: {border_color}; border-color: {border_color}; background-color: {border_color};"
        )
