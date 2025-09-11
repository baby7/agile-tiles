from functools import partial

from PySide6.QtWidgets import QLabel, QFrame, QApplication

from src.card.main_card.TodoCard.component.CategoryListWidget import CategoryListWidget
from src.card.MainCardManager.MainCard import MainCard
from src.card.main_card.TodoCard.component.TodoBody import TodoBody
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QRect, QTimer

from src.card.main_card.TodoCard.component.TodoEditWidget import TodoEditWidget
from src.constant import data_save_constant
from src.module import dialog_module
from src.thread_list import todo_thread
import src.ui.style_util as style_util

"""
大致数据结构:
{
    "typeList": [
        {
            "title": "默认",
            "sort": 1
        }
    ],
    "todoList": [
        {
            "id": "4ab462c6-7474-426c-b033-6c41d48f4d20",
            "title": "今天要把第三个任务整一整",
            "complete": true,
            "level": "First",
            "remind": true,
            "remindTime": "2024-05-25 00:00:00",
            "desc": "今天要把第三个任务整一整今天要把第三个任务整一整今天要把第三个任务整一整",
            "type": "默认"
        }
    ]
}
"""
class TodoCard(MainCard):

    title = "待办清单"
    name = "TodoCard"
    support_size_list = ["Big"]
    # 只读参数
    x = None                # 坐标x
    y = None                # 坐标y
    size = None             # 大小(1_1:Point、1_2:MiniHor、2_1:MiniVer、2_2:Block、2_5、Big:Big)
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
    # 待写入
    todo_list = []          # 任务列表
    todo_type_list = []     # 任务类型列表
    proceed_data_list = []
    complete_data_list = []
    todo_body = None

    Max_Todo_Type_Title_Count = 20
    Max_Todo_Type_Count = 50

    def __init__(self, main_object=None, parent=None, theme=None, card=None, cache=None, data=None,
                 toolkit=None, logger=None, save_data_func=None):
        super().__init__(main_object=main_object, parent=parent, theme=theme, card=card, cache=cache, data=data,
                         toolkit=toolkit, logger=logger, save_data_func=save_data_func)
        self.todo_list = self.data['todoList']
        self.todo_type_list = self.data['typeList']

    def clear(self):
        try:
            self.todo_area.setVisible(False)
            self.todo_area.deleteLater()
            self.todo_area_group.setVisible(False)
            self.todo_area_group.deleteLater()
            self.scrollAreaWidgetContents_10.setVisible(False)
            self.scrollAreaWidgetContents_10.deleteLater()
            self.scrollAreaWidgetContents_11.setVisible(False)
            self.scrollAreaWidgetContents_11.deleteLater()
            self.todo_thread_object.stop()
        except Exception as e:
            print(e)
        super().clear()

    def init_ui(self):
        super().init_ui()
        # 选择
        self.scrollAreaWidgetContents_10 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_10.setGeometry(QtCore.QRect(0, 0, self.card.width(), self.card.height()))
        self.scrollAreaWidgetContents_10.setObjectName("scrollAreaWidgetContents_10")
        self.scrollAreaWidgetContents_11 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_11.setGeometry(QtCore.QRect(0, 0, self.card.width(), self.card.height()))
        self.scrollAreaWidgetContents_11.setObjectName("scrollAreaWidgetContents_11")
        self.todo_area = QtWidgets.QScrollArea(self.card)
        self.todo_area.setGeometry(QtCore.QRect(0, 0, self.card.width(), self.card.height()))
        font = QtGui.QFont()
        font.setBold(True)
        # font.setWeight(75)
        self.todo_area.setFont(font)
        self.todo_area.setStyleSheet("border-style: solid;\n"
                                     "border-radius: 10px;\n"
                                     "border: 0px solid black;\n"
                                     "border-color: rgba(255, 255, 255, 0);\n"
                                     "background-color:transparent;")
        self.todo_area.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.todo_area.setLineWidth(1)
        self.todo_area.setWidgetResizable(True)
        self.todo_area.setObjectName("todo_area")
        self.label_todo_type_title = QtWidgets.QLabel(self.scrollAreaWidgetContents_10)
        self.label_todo_type_title.setGeometry(QtCore.QRect(30, 5, self.card.width() - 30, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_todo_type_title.setFont(font)
        self.label_todo_type_title.setStyleSheet("border: 0px solid #FF8D16;\n"
                                                 "border-radius: 0px;\n"
                                                 "background-color:transparent;")
        self.label_todo_type_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_todo_type_title.setObjectName("label_todo_type_title")
        self.line_head = QFrame(self.scrollAreaWidgetContents_10)
        self.line_head.setGeometry(QRect(-1, 30, self.card.width() + 2, 1))
        self.line_head.setStyleSheet("border: 1px solid black;")
        self.line_head.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_head.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_head.setObjectName("line_head")
        self.push_button_todo_add = QtWidgets.QPushButton(self.scrollAreaWidgetContents_10)
        self.push_button_todo_add.setGeometry(QtCore.QRect(self.card.width() - 24 - 3, 3, 24, 24))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.push_button_todo_add.setFont(font)
        self.push_button_todo_add.setObjectName("push_button_todo_add")
        self.push_button_todo_back = QtWidgets.QPushButton(self.scrollAreaWidgetContents_10)
        self.push_button_todo_back.setGeometry(QtCore.QRect(3, 3, 24, 24))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.push_button_todo_back.setFont(font)
        self.push_button_todo_back.setText("")
        self.push_button_todo_back.setObjectName("push_button_todo_back")
        # 下方切换
        self.tab_widget_todo = QtWidgets.QTabWidget(self.scrollAreaWidgetContents_10)
        self.tab_widget_todo.setGeometry(QRect(0, 30, self.card.width(), self.card.height() - 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        # font.setWeight(50)
        self.tab_widget_todo.setFont(font)
        self.tab_widget_todo.setTabPosition(QtWidgets.QTabWidget.North)
        self.tab_widget_todo.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tab_widget_todo.setObjectName("tab_widget_todo")
        self.tab_widget_tab_todo = QtWidgets.QWidget()
        self.tab_widget_tab_todo.setObjectName("tab_widget_tab_todo")
        self.todo_list_widget_todo = QtWidgets.QListWidget(self.tab_widget_tab_todo)
        self.todo_list_widget_todo.setGeometry(QtCore.QRect(0, 0, self.card.width(), 501))
        self.todo_list_widget_todo.setAutoScroll(True)
        self.todo_list_widget_todo.setAutoScrollMargin(16)
        self.todo_list_widget_todo.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.todo_list_widget_todo.setObjectName("todo_list_widget_todo")
        self.tab_widget_todo.addTab(self.tab_widget_tab_todo, "")
        self.tab_widget_tab_ok = QtWidgets.QWidget()
        self.tab_widget_tab_ok.setObjectName("tab_widget_tab_ok")
        self.todo_list_widget_success = QtWidgets.QListWidget(self.tab_widget_tab_ok)
        self.todo_list_widget_success.setGeometry(QtCore.QRect(0, 0, self.card.width(), 501))
        self.todo_list_widget_success.setAutoScroll(True)
        self.todo_list_widget_success.setAutoScrollMargin(16)
        self.todo_list_widget_success.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.todo_list_widget_success.setObjectName("todo_list_widget_success")
        self.tab_widget_todo.addTab(self.tab_widget_tab_ok, "")
        self.todo_area_title_line = QFrame(self.todo_area)
        self.todo_area_title_line.setObjectName(u"todo_area_title_line")
        self.todo_area_title_line.setGeometry(QRect(-1, 30, self.card.width() + 2, 1))
        self.todo_area_title_line.setStyleSheet("border: 1px solid black;")
        self.todo_area_title_line.setFrameShadow(QFrame.Plain)
        self.todo_area_title_line.setLineWidth(2)
        self.todo_area_title_line.setFrameShape(QFrame.HLine)
        self.todo_area_group = QtWidgets.QScrollArea(self.card)
        self.todo_area_group.setGeometry(QtCore.QRect(0, 0, self.card.width(), 581))
        font = QtGui.QFont()
        font.setBold(True)
        # font.setWeight(75)
        self.todo_area_group.setFont(font)
        self.todo_area_group.setStyleSheet("border-style: solid;"
                                           "border-radius: 10px;"
                                           "border: 1px solid black;"
                                           "border-color: rgba(255, 255, 255, 0);"
                                           "background-color:transparent;")
        self.todo_area_group.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.todo_area_group.setLineWidth(1)
        self.todo_area_group.setWidgetResizable(True)
        self.todo_area_group.setObjectName("todo_area_group")
        self.todo_area_group.setWidget(self.scrollAreaWidgetContents_11)
        self.todo_area.setWidget(self.scrollAreaWidgetContents_10)
        self.todo_area.raise_()
        self.todo_list_widget_todo.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.todo_list_widget_todo.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.todo_list_widget_success.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.todo_list_widget_success.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.tab_widget_todo.setTabText(self.tab_widget_todo.indexOf(self.tab_widget_tab_todo), "待办")
        self.tab_widget_todo.setTabText(self.tab_widget_todo.indexOf(self.tab_widget_tab_ok), "完成")
        self.label_todo_type_title.setText("生活")
        self.push_button_todo_back.clicked.connect(partial(self.show_hide_todo_group, None))
        # 待办事项时间线程
        self.todo_thread_object = todo_thread.TodoThread()
        self.todo_thread_object.set_task_list(self.todo_list)
        self.todo_thread_object.start()
        # 待办事项分类标题
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_title = QLabel(self.todo_area_group)  # 自定义控件
        self.label_title.setFont(font)
        self.label_title.setGeometry(QRect(3, 5, self.card.width() - 3, 21))
        self.label_title.setText("待办事项分类列表")
        self.label_title.setStyleSheet("""QLabel {border: 0px solid black;background-color:transparent;}""")
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.line_title = QtWidgets.QFrame(self.todo_area_group)
        self.line_title.setGeometry(QtCore.QRect(0, 30, self.card.width(), 1))
        self.line_title.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_title.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_title.setObjectName("line")
        # 样式调整
        style_util.set_tab_widget_style(self.tab_widget_todo, self.is_dark())
        # 待办事项分类右上角添加按钮
        self.add_button = QtWidgets.QPushButton(self.todo_area_group)
        self.add_button.setGeometry(QtCore.QRect(self.card.width() - 24 - 3, 3, 24, 24))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.add_button.setFont(font)
        self.add_button.setObjectName("add_button")
        # 待办事项分类初始化
        self.stash_list_widget = CategoryListWidget(self.todo_area_group,
                                                    self.show_hide_todo_group,
                                                    self.remove_todo_type_clicked)
        self.stash_list_widget.set_card_map_list(self.todo_type_list)
        self.stash_list_widget.move(12, 40)
        self.stash_list_widget.resize(self.card.width(), self.card.height() - 80)
        self.stash_list_widget.raise_()
        self.add_button.clicked.connect(self.add_todo_type_clicked)
        self.todo_area.hide()
        # 创建堆栈窗口
        self.stacked_widget = QtWidgets.QStackedWidget(self.card)
        self.stacked_widget.setGeometry(QtCore.QRect(0, 0, self.card.width(), self.card.height()))
        self.stacked_widget.setObjectName("stacked_widget")
        # 将现有的分类列表和待办列表添加到堆栈中
        self.stacked_widget.addWidget(self.todo_area_group)     # 索引0 - 分类列表
        self.stacked_widget.addWidget(self.todo_area)           # 索引1 - 待办列表
        # 创建编辑视图
        self.todo_edit_widget = TodoEditWidget(self.card, self.todo_type_list, self)
        self.stacked_widget.addWidget(self.todo_edit_widget)    # 索引2 - 编辑视图
        # 默认显示分类列表
        self.stacked_widget.setCurrentIndex(0)
        # 修改返回按钮的连接
        self.push_button_todo_back.clicked.connect(self.on_back_clicked)

    # 添加返回按钮处理函数
    def on_back_clicked(self):
        current_index = self.stacked_widget.currentIndex()
        if current_index == 1:  # 从待办列表返回
            self.stacked_widget.setCurrentIndex(0)  # 返回分类列表
        elif current_index == 2:  # 从编辑视图返回
            # 根据是否有待办类型决定返回到哪里
            if self.todo_body and self.todo_body.todo_type:
                self.stacked_widget.setCurrentIndex(1)  # 返回待办列表
            else:
                self.stacked_widget.setCurrentIndex(0)  # 返回分类列表

    def refresh_data(self, date_time_str):
        super().refresh_data(date_time_str)

    def refresh_ui(self, date_time_str):
        super().refresh_ui(date_time_str)
        super().refresh_ui_end(date_time_str)

    def show_hide_todo_group(self, todo_type):
        if todo_type is None:
            # 返回分类列表
            self.stacked_widget.setCurrentIndex(0)  # 分类列表视图
            return
        print(todo_type)
        # 初始化待办事项数据
        if self.todo_body is not None:
            try:
                self.push_button_todo_add.clicked.disconnect()
                self.todo_body.proceed_list_widget.itemDoubleClicked.disconnect()
                self.todo_body.complete_list_widget.itemDoubleClicked.disconnect()
            except:
                pass
            self.todo_body = None
            self.todo_list_widget_todo.clear()
            self.todo_list_widget_success.clear()
        # 初始化数据
        self.proceed_data_list = []
        self.complete_data_list = []
        for todo_data in self.todo_list:
            if not todo_data['complete']:
                self.proceed_data_list.append([
                    todo_data["id"],
                    todo_data["title"],
                    todo_data['complete'],
                    todo_data['level'],
                    todo_data['remind'],
                    todo_data['remindTime'],
                    todo_data['desc'],
                    todo_data["type"],
                    todo_data['createTime'],
                    todo_data['completeTime']
                ])
            else:
                self.complete_data_list.append([
                    todo_data["id"],
                    todo_data["title"],
                    todo_data['complete'],
                    todo_data['level'],
                    todo_data['remind'],
                    todo_data['remindTime'],
                    todo_data['desc'],
                    todo_data["type"],
                    todo_data['createTime'],
                    todo_data['completeTime']
                ])
        # 筛选类型
        proceed_data_list = []
        for proceed_data in self.proceed_data_list:
            if todo_type == proceed_data[7]:
                proceed_data_list.append(proceed_data)
        complete_data_list = []
        for complete_data in self.complete_data_list:
            if todo_type == complete_data[7]:
                complete_data_list.append(complete_data)
        # 创建待办事项主体
        self.todo_body = TodoBody(self.main_object, self.tab_widget_todo, self.todo_type_list, proceed_data_list, complete_data_list,
                                  self.todo_list_widget_todo, self.todo_list_widget_success, self)
        self.push_button_todo_add.clicked.connect(partial(self.todo_body.open_new_todo_view, None, todo_type))
        self.todo_body.set_todo_type(todo_type)
        self.todo_body.init()
        self.label_todo_type_title.setText(todo_type)
        # 切换到待办列表视图
        self.stacked_widget.setCurrentIndex(1)  # 待办列表视图

    def data_process_call_back(self, proceed_data_list, complete_data_list, todo_type):
        # 剔除类型为todo_type的
        todo_list = []
        for todo_data in self.todo_list:
            if todo_data["type"] != todo_type:
                todo_list.append(todo_data)
        self.todo_list.clear()
        for todo_data in todo_list:
            self.todo_list.append(todo_data)
        # 再合并
        for todo_data in proceed_data_list:
            self.todo_list.append({
                "id": todo_data[0],
                "title": todo_data[1],
                "complete": todo_data[2],
                "level": todo_data[3],
                "remind": todo_data[4],
                "remindTime": todo_data[5],
                "desc": todo_data[6],
                "type": todo_data[7],
                "createTime": todo_data[8],
                "completeTime": todo_data[9]
            })
        for todo_data in complete_data_list:
            self.todo_list.append({
                "id": todo_data[0],
                "title": todo_data[1],
                "complete": todo_data[2],
                "level": todo_data[3],
                "remind": todo_data[4],
                "remindTime": todo_data[5],
                "desc": todo_data[6],
                "type": todo_data[7],
                "createTime": todo_data[8],
                "completeTime": todo_data[9]
            })
        self.todo_thread_object.set_task_list(self.todo_list)
        # 保存数据
        self.save_data_func(in_data=self.data, card_name=self.name, data_type=data_save_constant.DATA_TYPE_ENDURING)

    def add_todo_type_clicked(self):
        # 限制分类数量
        if len(self.todo_type_list) >= self.Max_Todo_Type_Count:
            dialog_module.box_information(self.main_object, "提示", f"待办事项分类数量已达到上限，不能超过{self.Max_Todo_Type_Count}个！")
            return
        todo_type = dialog_module.box_input(self.main_object, "添加", "待办事项分类名称：")
        if todo_type is None:
            return
        if todo_type == "":
            dialog_module.box_information(self.main_object, "提示", "待办事项分类不能为空！")
            return
        # 强制处理所有待处理的事件
        QApplication.processEvents()
        # 使用定时器延迟创建新布局，确保删除操作完成
        QTimer.singleShot(10, lambda : self.add_todo_type_clicked_delayed(todo_type))

    def add_todo_type_clicked_delayed(self, todo_type):
        if todo_type == "":
            dialog_module.box_information(self.main_object, "提示", "待办事项分类名称不能为空！")
            return
        # 判断重复
        for todo_data in self.todo_type_list:
            if todo_data["title"] == todo_type:
                dialog_module.box_information(self.main_object, "提示", "待办事项分类名称重复！")
                return
        # 限制字数
        if len(todo_type) > self.Max_Todo_Type_Title_Count:
            dialog_module.box_information(self.main_object, "提示", f"待办事项分类名称过长，不能超过{self.Max_Todo_Type_Title_Count}字！")
            return
        # 限制分类数量
        if len(self.todo_type_list) >= self.Max_Todo_Type_Count:
            dialog_module.box_information(self.main_object, "提示", f"待办事项分类数量已达到上限，不能超过{self.Max_Todo_Type_Count}个！")
            return
        # 添加分类
        self.todo_type_list.append({
            "title": todo_type
        })
        # 刷新待办分类面板
        self.stash_list_widget.set_card_map_list(self.todo_type_list)
        # 保存数据
        self.save_data_func(in_data=self.data, card_name=self.name, data_type=data_save_constant.DATA_TYPE_ENDURING)
        # 刷新主题
        self.refresh_theme()
        # 确保当前显示的是分类列表
        self.stacked_widget.setCurrentIndex(0)

    def remove_todo_type_clicked(self, todo_type):
        if not dialog_module.box_acknowledgement(self.main_object, "注意",
                                            f"确定要删除 {todo_type} 分类吗？这将删除该分类下的所有待办事项！"):
            return
        print("删除 待办事项分类：", todo_type)
        # 删除 todo_type_list 中对应的 todo_type
        indices_to_remove = [i for i, todo_data in enumerate(self.todo_type_list) if todo_data["title"] == todo_type]
        indices_to_remove.reverse()
        for index in indices_to_remove:
            del self.todo_type_list[index]
        # 从 todo_list 中删除所有 type=todo_type 的待办事项
        indices_to_remove = [i for i, todo in enumerate(self.todo_list) if todo.get('type') == todo_type]
        indices_to_remove.reverse()
        for index in indices_to_remove:
            del self.todo_list[index]
        # 刷新待办分类面板
        self.stash_list_widget.set_card_map_list(self.todo_type_list)
        # 保存数据
        self.save_data_func(in_data=self.data, card_name=self.name, data_type=data_save_constant.DATA_TYPE_ENDURING)
        # 刷新主题
        self.refresh_theme()
        # 确保当前显示的是分类列表
        self.stacked_widget.setCurrentIndex(0)

    def refresh_theme(self):
        super().refresh_theme()
        # 设置按钮样式
        push_button_style = """
        QPushButton {
            border: none;
            border-radius: 12px;
            background-color:transparent;
        }
        QPushButton:hover {
            background-color: rgba(125, 125, 125, 80);
        }"""
        self.add_button.setStyleSheet(push_button_style)
        self.push_button_todo_add.setStyleSheet(push_button_style)
        self.push_button_todo_back.setStyleSheet(push_button_style)
        style_util.set_button_style(self.add_button, icon_path="Character/add-one", is_dark=self.is_dark(), style_change=False)
        style_util.set_button_style(self.push_button_todo_add, icon_path="Character/add-one", is_dark=self.is_dark(), style_change=False)
        style_util.set_button_style(self.push_button_todo_back, icon_path="Edit/return", is_dark=self.is_dark(), style_change=False)
        # 其他
        if self.is_dark():
            line_style = "border: 1px solid white;"
        else:
            line_style = "border: 1px solid black;"
        self.line_head.setStyleSheet(line_style)
        self.line_title.setStyleSheet(line_style)
        self.todo_area_title_line.setStyleSheet(line_style)
        # 设置 tab_widget_todo 的主题
        style_util.set_tab_widget_style(self.tab_widget_todo, self.is_dark())
        if self.stash_list_widget is not None:
            self.stash_list_widget.refresh_theme(self.is_dark())
        # 设置 todo_body 的主题
        if self.todo_body is not None:
            self.todo_body.refresh_theme(self.is_dark())
        # 设置 todo_list_widget 的样式
        select_style = """
        QListWidget::item:hover {
            border-radius: 10px;
            margin-top: 3px;
            margin-bottom: 4px;
            margin-left: 12px;
            margin-right: 23px;
            background-color: rgba(125, 125, 125, 80);
        }
        QListWidget::item:selected {
            border-radius: 10px;
            margin-top: 3px;
            margin-bottom: 4px;
            margin-left: 12px;
            margin-right: 23px;
            background-color: rgba(125, 125, 125, 80);
        }"""
        self.todo_list_widget_todo.setStyleSheet(select_style)
        self.todo_list_widget_success.setStyleSheet(select_style)
        # 设置编辑视图的主题
        if hasattr(self, 'todo_edit_widget') and self.todo_edit_widget:
            self.todo_edit_widget.refresh_theme()

    def update_data(self, data=None):
        """
        更新持久数据事件
        """
        # 1. 停止现有线程
        if hasattr(self, 'todo_thread_object') and self.todo_thread_object:
            try:
                self.todo_thread_object.stop()
            except:
                pass

        # 2. 清除现有UI组件
        self._cleanup_ui()

        # 3. 更新数据
        self.data = data
        self.todo_list = self.data['todoList']
        self.todo_type_list = self.data['typeList']

        # 4. 重新初始化UI
        self.init_ui()

        # 5. 刷新主题
        self.refresh_theme()

    def _cleanup_ui(self):
        """清理UI组件"""
        # 断开信号连接
        try:
            self.push_button_todo_add.clicked.disconnect()
            self.push_button_todo_back.clicked.disconnect()
            self.add_button.clicked.disconnect()
        except:
            pass

        # 清理分类列表组件
        if hasattr(self, 'stash_list_widget') and self.stash_list_widget:
            try:
                self.stash_list_widget.setVisible(False)
                self.stash_list_widget.deleteLater()
            except:
                pass
            self.stash_list_widget = None

        # 清理待办事项主体组件
        if hasattr(self, 'todo_body') and self.todo_body:
            self.todo_body = None

        # 清理其他UI组件
        widgets_to_clean = [
            'scrollAreaWidgetContents_10', 'scrollAreaWidgetContents_11',
            'todo_area', 'label_todo_type_title', 'line_head',
            'push_button_todo_add', 'push_button_todo_back',
            'tab_widget_todo', 'todo_area_title_line', 'todo_area_group',
            'label_title', 'line_title', 'add_button'
        ]

        for widget_name in widgets_to_clean:
            widget = getattr(self, widget_name, None)
            if widget is not None:
                try:
                    widget.setVisible(False)
                    widget.deleteLater()
                except:
                    pass
                setattr(self, widget_name, None)

        # 清空列表控件
        try:
            self.todo_list_widget_todo.clear()
            self.todo_list_widget_success.clear()
        except:
            pass

        # 清空数据缓存
        self.proceed_data_list = []
        self.complete_data_list = []

        # 重置组件引用
        self.todo_list_widget_todo = None
        self.todo_list_widget_success = None
