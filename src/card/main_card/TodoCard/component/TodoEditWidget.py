# coding:utf-8
import uuid
from functools import partial
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Signal, Qt

from src.card.main_card.TodoCard.component.new_todo_form import Ui_Form
import src.ui.style_util as style_util

from src.component.QSelectTimeWidget.QSelectTimeWidget import QSelectTimeWidget
from src.component.QSelectTimeWidget.QSelectDateWidget import QSelectDateWidget

import src.util.time_util as time_util
from src.module import dialog_module

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


class TodoEditWidget(QtWidgets.QWidget, Ui_Form):
    edit_finished = Signal(list)  # 编辑完成信号
    edit_cancelled = Signal()  # 编辑取消信号

    def __init__(self, parent=None, todo_type_list=None, todo_card=None):
        super(TodoEditWidget, self).__init__(parent)
        self.setupUi(self)
        self.todo_card = todo_card
        self.input_data = ["", "", False, "First", False, "", "", "", "", ""]

        # 设置背景样式
        self.set_background_style()

        # 根据todo_type_list补全下拉列表
        for todo_type_item in todo_type_list:
            self.combo_box.addItem(todo_type_item["title"])

        # 样式调整
        self.combo_box.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.combo_box.view().window().setAttribute(Qt.WA_TranslucentBackground)
        style_util.set_dialog_control_style(self, self.todo_card.is_dark())

        # 按钮连接事件
        self.push_button_cancel.clicked.connect(self.on_cancel)
        self.push_button_ok.clicked.connect(self.on_ok)
        self.push_button_date.clicked.connect(self.show_hide_date_widget)
        self.push_button_time.clicked.connect(self.show_hide_time_widget)
        self.push_button_importance_exigency.clicked.connect(partial(self.select_one, "importance_exigency"))
        self.push_button_no_importance_exigency.clicked.connect(partial(self.select_one, "no_importance_exigency"))
        self.push_button_importance_no_exigency.clicked.connect(partial(self.select_one, "importance_no_exigency"))
        self.push_button_no_importance_no_exigency.clicked.connect(
            partial(self.select_one, "no_importance_no_exigency"))

        # 初始化时间选择组件
        self.time_choice = QtWidgets.QGroupBox(self)
        self.time_choice.setObjectName(u"time_choice")
        self.time_choice.setFixedSize(QtCore.QSize(240, 320))
        self.time_choice.setStyleSheet(group_box_style if not self.todo_card.is_dark() else group_box_dark_style)
        self.time_choice.hide()

        self.date_choice = QtWidgets.QGroupBox(self)
        self.date_choice.setObjectName(u"time_choice")
        self.date_choice.setFixedSize(QtCore.QSize(240, 320))
        self.date_choice.setStyleSheet(group_box_style if not self.todo_card.is_dark() else group_box_dark_style)
        self.date_choice.hide()

        # 初始化时间选择
        self.m_pTimeWidget = QSelectTimeWidget(self.time_choice, self.todo_card.is_dark())
        self.m_pTimeWidget.setGeometry(10, 10, 220, 300)
        self.m_pTimeWidget.commit_success.connect(self.MsgReceived_CaseTime_NewTime)
        self.m_pTimeWidget.commit_cancel.connect(self.show_hide_time_widget)
        self.m_pTimeWidget.SetSelectNewCalendarTime("12:00:00")

        # 初始化日期选择
        self.m_pDateWidget = QSelectDateWidget(self.date_choice, self.todo_card.is_dark())
        self.m_pDateWidget.setGeometry(10, 10, 220, 300)
        self.m_pDateWidget.commit_success.connect(self.MsgReceived_CaseDate_NewDate)
        self.m_pDateWidget.commit_cancel.connect(self.show_hide_date_widget)
        self.m_pDateWidget.SetSelectNewCalendarTime("2024-05-26")

        # 设置输入焦点
        self.line_edit_title.setFocus()
        # 添加界面回车跳转（焦点移到下一个输入框）
        self.line_edit_title.returnPressed.connect(
            lambda: self.text_edit_des.setFocus()
        )

    def set_background_style(self):
        """设置编辑视图的背景样式"""
        if self.todo_card.is_dark():
            # 深色主题背景
            background_style = """
                background-color: rgba(30, 30, 30, 220);
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 80);
            """
            widget_style = """
                background-color: rgba(0, 0, 0, 160);
                color: rgb(200, 200, 200);
                border-radius: 10px;
                border: none;
            """
        else:
            # 浅色主题背景
            background_style = """
                background-color: rgba(240, 240, 240, 220);
                border-radius: 10px;
                border: 1px solid rgba(0, 0, 0, 80);
            """
            widget_style = """
                background-color: rgba(255, 255, 255, 160);
                color: rgb(0, 0, 0);
                border-radius: 10px;
                border: none;
            """

        # 应用主背景样式
        self.setStyleSheet(f"TodoEditWidget {{ {background_style} }}")

        # 应用顶部和底部小部件样式
        self.top_widget.setStyleSheet(widget_style)
        self.bottom_widget.setStyleSheet(widget_style)

    def set_data(self, input_data=None, todo_type=None):
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
            self.input_data = ["", "", False, "First", False, "", "", "", "", ""]
            # 清楚
            self.line_edit_title.clear()
            self.text_edit_des.clear()
            self.check_box.setChecked(False)
            self.label_show_create_time.clear()
            self.label_show_complete.clear()
            self.label_show_complete_time.clear()
            # 设置默认值
            self.select_one("importance_exigency")
            date_time_str = time_util.get_datetime_hour_str()
            self.push_button_date.setText(date_time_str[:10])
            self.push_button_time.setText(date_time_str[11:])
            self.m_pDateWidget.SetSelectNewCalendarTime(date_time_str[:10])
            self.m_pTimeWidget.SetSelectNewCalendarTime(date_time_str[11:])
            if todo_type:
                self.combo_box.setCurrentText(todo_type)
            else:
                self.combo_box.clear()

        # 调整布局
        self.adjustSize()

    def on_ok(self):
        # 验证标题不能为空
        if self.line_edit_title.text() == "":
            dialog_module.box_information(self.todo_card.main_object, "提示", "待办事项标题不能为空！")
            return

        # 限制标题字数
        if len(self.line_edit_title.text()) > self.todo_card.todo_body.Max_Todo_Title_Count:
            dialog_module.box_information(self.todo_card.main_object, "提示",
                                             f"待办事项标题字数不能超过{self.todo_card.todo_body.Max_Todo_Title_Count}字！")
            return

        # 限制详情字数
        if len(self.text_edit_des.toPlainText()) > self.todo_card.todo_body.Max_Todo_Des_Count:
            dialog_module.box_information(self.todo_card.main_object, "提示",
                                             f"待办事项详情字数不能超过{self.todo_card.todo_body.Max_Todo_Des_Count}字！")
            return

        # 获取信息
        self.input_data[1] = self.line_edit_title.text()
        self.input_data[3] = "First"
        if self.check_box.isChecked():
            self.input_data[4] = True
            self.input_data[5] = self.push_button_date.text() + " " + self.push_button_time.text()
        else:
            self.input_data[4] = False
            self.input_data[5] = ""
        self.input_data[6] = self.text_edit_des.toPlainText()
        self.input_data[7] = self.combo_box.currentText()

        if not self.input_data[0]:  # 新建事项
            # self.input_data[0] = str(uuid.uuid4())
            self.input_data[8] = time_util.get_datetime_str()
            self.input_data[9] = "--"

        # 发送完成信号
        self.edit_finished.emit(self.input_data)

    def on_cancel(self):
        self.edit_cancelled.emit()

    def select_one(self, check_type):
        # 颜色透明度
        transparency = "0.3" if self.todo_card.is_dark() else "0.6"
        # 边框颜色
        border_color = "rgb(200, 200, 200)" if self.todo_card.is_dark() else "rgb(34, 34, 34)"
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

    def refresh_theme(self):
        """刷新编辑视图的主题"""
        self.set_background_style()

        # 刷新时间选择器和日期选择器的主题
        # if hasattr(self, 'm_pTimeWidget'):
        #     self.m_pTimeWidget.refresh_theme(self.todo_card.is_dark())
        # if hasattr(self, 'm_pDateWidget'):
        #     self.m_pDateWidget.refresh_theme(self.todo_card.is_dark())

        # 刷新其他控件的样式
        style_util.set_dialog_control_style(self, self.todo_card.is_dark())
