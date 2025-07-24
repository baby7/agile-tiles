# coding:utf-8
from functools import partial
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Signal, Qt

from src.card.main_card.TodoCard.component.new_todo_form import Ui_Form
import src.ui.style_util as style_util

from src.component.AgileTilesAcrylicWindow.AgileTilesAcrylicWindow import AgileTilesAcrylicWindow
from src.component.QSelectTimeWidget.QSelectTimeWidget import QSelectTimeWidget
from src.component.QSelectTimeWidget.QSelectDateWidget import QSelectDateWidget

import src.util.time_util as time_util

select_style = """
    border-radius: 10px;
    border: 1px solid #border-color;
    color: rgb(255, 255, 255);
    background-color: #COLOR;"""

no_select_style = """
    border-radius: 10px;
    border: none;
    color: rgb(255, 255, 255);
    background-color: #COLOR;"""

group_box_style = """
    color: rgb(34, 34, 34);
    border-radius: 10px;
    border: 1px solid black;
    background-color: rgb(255, 255, 255);
"""

group_box_dark_style = """
    color: rgb(255, 255, 255);
    border-radius: 10px;
    border: 1px solid white;
    background-color: rgb(34, 34, 34);
"""


class NewTodoWindow(AgileTilesAcrylicWindow, Ui_Form):

    setting_signal = Signal(str)

    input_data = ["", "", False, "Third", False, "", "", "", "", ""]
    def __init__(self, parent=None, use_parent=None, todo_type_list=None, input_data=None, todo_type=None):
        super(NewTodoWindow, self).__init__(is_dark=use_parent.is_dark, form_theme_mode=use_parent.form_theme_mode,
                                                 form_theme_transparency=use_parent.form_theme_transparency)
        self.input_data = ["", "", False, "First", False, "", "", "", "", ""]
        self.setupUi(self)
        # 初始化布局
        self.widget_base.setLayout(self.gridLayout_3)
        self.gridLayout_3.setContentsMargins(10, 10, 10, 10)
        # 设置标题栏
        if input_data is None:
            self.setWindowTitle("灵卡面板 - 新建待办事项")
        else:
            self.setWindowTitle("灵卡面板 - 编辑待办事项")
        self.titleBar.minBtn.close()
        self.titleBar.maxBtn.close()
        # 根据todo_type_list补全下拉列表
        for todo_type_item in todo_type_list:
            self.combo_box.addItem(todo_type_item["title"])
        # 样式调整
        self.combo_box.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.combo_box.view().window().setAttribute(Qt.WA_TranslucentBackground)
        style_util.set_dialog_control_style(self, self.is_dark)
        # 计算居中的位置
        group_width = 240
        group_height = 320
        group_locate = QtCore.QPoint(self.width() / 2 - group_width / 2, self.height() / 2 - group_height / 2)
        # 新增QGroupBox
        self.time_choice = QtWidgets.QGroupBox(self)
        self.time_choice.setObjectName(u"time_choice")
        self.time_choice.setFixedSize(QtCore.QSize(group_width, group_height))
        self.time_choice.move(group_locate)
        self.time_choice.setStyleSheet(group_box_style if not self.is_dark else group_box_dark_style)
        self.time_choice.hide()
        self.date_choice = QtWidgets.QGroupBox(self)
        self.date_choice.setObjectName(u"time_choice")
        self.date_choice.setFixedSize(QtCore.QSize(group_width, group_height))
        self.date_choice.move(group_locate)
        self.date_choice.setStyleSheet(group_box_style if not self.is_dark else group_box_dark_style)
        self.date_choice.hide()
        # 按钮连接事件
        self.push_button_cancel.clicked.connect(self.close)
        self.push_button_date.clicked.connect(self.show_hide_date_widget)
        self.push_button_time.clicked.connect(self.show_hide_time_widget)
        self.push_button_importance_exigency.clicked.connect(partial(self.select_one, "importance_exigency"))
        self.push_button_no_importance_exigency.clicked.connect(partial(self.select_one, "no_importance_exigency"))
        self.push_button_importance_no_exigency.clicked.connect(partial(self.select_one, "importance_no_exigency"))
        self.push_button_no_importance_no_exigency.clicked.connect(partial(self.select_one, "no_importance_no_exigency"))
        # 初始化时间选择
        self.m_pTimeWidget = QSelectTimeWidget(self.time_choice, self.is_dark)
        self.m_pTimeWidget.setGeometry(10, 10, 220, 300)
        self.m_pTimeWidget.commit_success.connect(self.MsgReceived_CaseTime_NewTime)
        self.m_pTimeWidget.commit_cancel.connect(self.show_hide_time_widget)
        self.m_pTimeWidget.SetSelectNewCalendarTime("12:00:00")
        # 初始化日期选择
        self.m_pDateWidget = QSelectDateWidget(self.date_choice, self.is_dark)
        self.m_pDateWidget.setGeometry(10, 10, 220, 300)
        self.m_pDateWidget.commit_success.connect(self.MsgReceived_CaseDate_NewDate)
        self.m_pDateWidget.commit_cancel.connect(self.show_hide_date_widget)
        self.m_pDateWidget.SetSelectNewCalendarTime("2024-05-26")
        # 初始化数据
        if input_data is not None:
            self.input_data = input_data
            self.line_edit_title.setText(input_data[1])
            self.text_edit_des.setText(input_data[6])
            if input_data[3] == "First":
                self.select_one("importance_exigency")
            elif input_data[3] == "Second":
                self.select_one("no_importance_exigency")
            elif input_data[3] == "Third":
                self.select_one("importance_no_exigency")
            else:
                self.select_one("no_importance_no_exigency")
            if input_data[4]:
                self.check_box.setChecked(True)
            else:
                self.check_box.setChecked(False)
            if input_data[5] is None or input_data[5] == "":
                input_data[5] = time_util.get_datetime_hour_str()
            self.push_button_date.setText(input_data[5][:10])
            self.push_button_time.setText(input_data[5][11:])
            self.m_pDateWidget.SetSelectNewCalendarTime(input_data[5][:10])
            self.m_pTimeWidget.SetSelectNewCalendarTime(input_data[5][11:])
            self.combo_box.setCurrentText(input_data[7])
            self.label_show_create_time.setText(input_data[8])
            self.label_show_complete.setText("已完成" if str(input_data[2]) == "True" else "未完成")
            self.label_show_complete_time.setText(input_data[9])
        else:
            self.select_one("importance_exigency")
            date_time_str = time_util.get_datetime_hour_str()
            self.push_button_date.setText(date_time_str[:10])
            self.push_button_time.setText(date_time_str[11:])
            self.m_pDateWidget.SetSelectNewCalendarTime(date_time_str[:10])
            self.m_pTimeWidget.SetSelectNewCalendarTime(date_time_str[11:])
            self.combo_box.setCurrentText(todo_type)
        style_util.set_dialog_control_style(self, self.is_dark)
        if self.is_dark:
            widget_style = """
                border-radius: 10px;
                border: none;
                color: rgb(200, 200, 200);
                background-color: rgba(0, 0, 0, 160);
            """
        else:
            widget_style = """
                border-radius: 10px;
                border: none;
                color: rgb(0, 0, 0);
                background-color: rgba(255, 255, 255, 160);
            """
        self.top_widget.setStyleSheet(widget_style)
        self.bottom_widget.setStyleSheet(widget_style)
        # 设置输入焦点
        self.line_edit_title.setFocus()
        # 添加界面回车跳转（焦点移到下一个输入框）
        self.line_edit_title.returnPressed.connect(
            lambda: self.text_edit_des.setFocus()
        )

    def select_one(self, check_type):
        # 颜色透明度
        transparency = "0.3" if self.is_dark else "0.6"
        # 边框颜色
        border_color = "rgb(200, 200, 200)" if self.is_dark else "rgb(34, 34, 34)"
        self.push_button_importance_exigency.setStyleSheet(
            no_select_style.replace("#COLOR", f"rgba(255, 46, 44, {transparency})"))
        self.push_button_no_importance_exigency.setStyleSheet(
            no_select_style.replace("#COLOR", f"rgba(20, 185, 62, {transparency})"))
        self.push_button_importance_no_exigency.setStyleSheet(
            no_select_style.replace("#COLOR", f"rgba(243, 207, 19, {transparency})"))
        self.push_button_no_importance_no_exigency.setStyleSheet(
            no_select_style.replace("#COLOR", f"rgba(4, 115, 247, {transparency})"))
        if check_type == "importance_exigency":
            self.push_button_importance_exigency.setStyleSheet(
                select_style.replace("#COLOR", f"rgba(255, 46, 44, {transparency})")
                .replace("#border-color", border_color))
            self.input_data[3] = "First"
        elif check_type == "no_importance_exigency":
            self.push_button_no_importance_exigency.setStyleSheet(
                select_style.replace("#COLOR", f"rgba(20, 185, 62, {transparency})")
                .replace("#border-color", border_color))
            self.input_data[3] = "Second"
        elif check_type == "importance_no_exigency":
            self.push_button_importance_no_exigency.setStyleSheet(
                select_style.replace("#COLOR", f"rgba(243, 207, 19, {transparency})")
                .replace("#border-color", border_color))
            self.input_data[3] = "Third"
        else:
            self.push_button_no_importance_no_exigency.setStyleSheet(
                select_style.replace("#COLOR", f"rgba(4, 115, 247, {transparency})")
                .replace("#border-color", border_color))
            self.input_data[3] = "Fourth"

    def MsgReceived_CaseTime_NewTime(self, data):
        self.push_button_time.setText(data)
        self.show_hide_time_widget()

    def MsgReceived_CaseDate_NewDate(self, data):
        self.push_button_date.setText(data)
        self.show_hide_date_widget()

    def show_hide_date_widget(self):
        if self.date_choice.isHidden():
            self.date_choice.show()
        else:
            self.date_choice.hide()

    def show_hide_time_widget(self):
        if self.time_choice.isHidden():
            self.time_choice.show()
        else:
            self.time_choice.hide()