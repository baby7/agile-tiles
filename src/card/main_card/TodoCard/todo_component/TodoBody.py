import copy
import uuid
from functools import partial

from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtCore import QSize

from src.card.main_card.TodoCard.todo_component.MyQListWidgetItemWidget import MyQListWidgetItemWidget

import src.util.time_util as time_util
from src.module import dialog_module


class TodoBody(object):

    Max_Todo_Count = 30
    Max_Todo_Title_Count = 20
    Max_Todo_Des_Count = 500
    
    main_object = None
    todo_type_list = None              # 待办事项分类列表
    proceed_data_list = []             # 待办事项数据列表
    complete_data_list = []            # 已办事项数据列表
    proceed_list_widget = None         # 待办事项listWidget
    complete_list_widget = None        # 已办事项listWidget
    proceed_widget_map = {}            # 待办事项widget字典
    complete_widget_map = {}           # 已办事项widget字典
    proceed_item_map = {}              # 待办事项item字典
    complete_item_map = {}             # 已办事项item字典
    todo_card = None      # 数据处理回调
    tab_widget_todo = None
    todo_type = None

    def __init__(self, main_object=None,
                 tab_widget_todo=None,
                 todo_type_list=None,
                 proceed_data_list=None,
                 complete_data_list=None,
                 proceed_list_widget=None,
                 complete_list_widget=None,
                 todo_card=None):
        self.main_object = main_object
        self.tab_widget_todo = tab_widget_todo
        self.todo_type_list = todo_type_list
        self.proceed_data_list = proceed_data_list
        self.complete_data_list = complete_data_list
        self.proceed_list_widget = proceed_list_widget
        self.complete_list_widget = complete_list_widget
        self.todo_card = todo_card

    def init(self):
        for todo_id, title, success, degree, warn, time_str, des, todo_type, create_time, complete_time in self.proceed_data_list:
            widget = MyQListWidgetItemWidget(self.proceed_list_widget, self.todo_card, todo_id, title, success, degree, warn, time_str)
            self.proceed_widget_map[todo_id] = widget
            widget.delete_button.clicked.connect(partial(self.delete_click, todo_id, True))
            widget.edit_button.clicked.connect(partial(self.edit_click, todo_id, True))
            widget.check_push_button.clicked.connect(partial(self.checked_click, todo_id, True))
            widget_item = QListWidgetItem(self.proceed_list_widget)
            widget_item.setSizeHint(widget.sizeHint())
            self.proceed_item_map[todo_id] = widget_item
            self.proceed_list_widget.addItem(widget_item)
            self.proceed_list_widget.setItemWidget(widget_item, widget)
        self.proceed_list_widget.itemDoubleClicked.connect(self.double_click)
        for todo_id, title, success, degree, warn, time_str, des, todo_type, create_time, complete_time in self.complete_data_list:
            widget = MyQListWidgetItemWidget(self.complete_list_widget, self.todo_card, todo_id, title, success, degree, warn, time_str)
            self.complete_widget_map[todo_id] = widget
            widget.delete_button.clicked.connect(partial(self.delete_click, todo_id, False))
            widget.edit_button.clicked.connect(partial(self.edit_click, todo_id, False))
            widget.check_push_button.clicked.connect(partial(self.checked_click, todo_id, False))
            widget_item = QListWidgetItem(self.complete_list_widget)
            widget_item.setSizeHint(widget.sizeHint())
            self.complete_item_map[todo_id] = widget_item
            self.complete_list_widget.addItem(widget_item)
            self.complete_list_widget.setItemWidget(widget_item, widget)
        self.complete_list_widget.itemDoubleClicked.connect(self.double_click)

    def set_todo_type(self, todo_type):
        self.todo_type = todo_type

    '''
    ********************************** 点击事件 ****************************************
    ↓                                                                                 ↓
    '''
    def delete_click(self, todo_id, todo_state):
        # 未登录的判断
        self.main_object.show_login_tip()
        if self.main_object.current_user['username'] == "LocalUser":
            return
        """
        删除按钮
        :param todo_id: 任务id
        :param todo_state: 任务状态(True表示进行中)
        """
        if not dialog_module.box_acknowledgement(self.main_object, "注意", f"确定要删除该待办事项吗？"):
            return
        if todo_state:
            print("[删除]从待办中删除id:{},数据列表:{}".format(todo_id, self.proceed_data_list))
            self.delete_one(todo_id, self.proceed_data_list, self.proceed_item_map, self.proceed_widget_map,
                       self.proceed_list_widget)
            print("[删除]从待办中删除完成id:{},数据列表:{}".format(todo_id, self.proceed_data_list))
        else:
            print("[删除]从完成中删除id:{},数据列表:{}".format(todo_id, self.complete_data_list))
            self.delete_one(todo_id, self.complete_data_list, self.complete_item_map, self.complete_widget_map,
                       self.complete_list_widget)
            print("[删除]从完成中删除完成id:{},数据列表:{}".format(todo_id, self.complete_data_list))
        self.todo_card.data_process_call_back(self.proceed_data_list, self.complete_data_list, self.todo_type)
    
    def checked_click(self, todo_id, todo_state):
        # 未登录的判断
        self.main_object.show_login_tip()
        if self.main_object.current_user['username'] == "LocalUser":
            return
        """
        勾选按钮
        :param todo_id: 任务id
        :param todo_state: 任务状态(True表示进行中)
        """
        if todo_state:
            # 从待办中删除
            print("[单选]从待办中删除id:{},数据列表:{}".format(todo_id, self.proceed_data_list))
            delete_data = self.delete_one(todo_id, self.proceed_data_list, self.proceed_item_map, self.proceed_widget_map,
                                     self.proceed_list_widget)
            print("[单选]从待办中删除完成id:{},数据列表:{}".format(todo_id, self.proceed_data_list))
            delete_data[2] = True
            delete_data[9] = time_util.get_datetime_str()
            # 加到完成中
            print("[单选]添加到完成中id:{},数据列表:{}".format(todo_id, self.complete_data_list))
            self.create_one(delete_data, self.complete_data_list, self.complete_list_widget, self.complete_widget_map,
                       self.complete_item_map)
            print("[单选]添加到完成完成id:{},数据列表:{}".format(todo_id, self.complete_data_list))
        else:
            # 从完成中删除
            print("[单选]从完成中删除id:{},数据列表:{}".format(todo_id, self.complete_data_list))
            delete_data = self.delete_one(todo_id, self.complete_data_list, self.complete_item_map,
                                     self.complete_widget_map, self.complete_list_widget)
            print("[单选]从完成中删除完成id:{},数据列表:{}".format(todo_id, self.complete_data_list))
            delete_data[2] = False
            delete_data[9] = "--"
            # 加到待办中
            print("[单选]添加到待办中id:{},数据列表:{}".format(todo_id, self.proceed_data_list))
            self.create_one(delete_data, self.proceed_data_list, self.proceed_list_widget, self.proceed_widget_map,
                       self.proceed_item_map)
            print("[单选]添加到待办完成id:{},数据列表:{}".format(todo_id, self.proceed_data_list))
        self.todo_card.data_process_call_back(self.proceed_data_list, self.complete_data_list, self.todo_type)
    
    def edit_click(self, todo_id, todo_state):
        # 未登录的判断
        self.main_object.show_login_tip()
        if self.main_object.current_user['username'] == "LocalUser":
            return
        data_list = None
        if todo_state:
            print("[编辑]从待办中编辑id:{},数据列表:{}".format(todo_id, self.proceed_data_list))
            data_list = self.proceed_data_list
        else:
            print("[编辑]从完成中编辑id:{},数据列表:{}".format(todo_id, self.complete_data_list))
            data_list = self.complete_data_list
        # 获取数据
        edit_data = None
        for todo_data_index in range(len(data_list)):
            if str(todo_id) == str(data_list[todo_data_index][0]):
                edit_data = data_list[todo_data_index]
        # 显示
        self.open_new_todo_view(input_data=edit_data)

    def double_click(self, item):
        if int(self.tab_widget_todo.currentIndex()) == 0:
            double_index = self.proceed_list_widget.currentRow()
            self.open_new_todo_view(input_data=self.proceed_data_list[double_index])
        else:
            double_index = self.complete_list_widget.currentRow()
            self.open_new_todo_view(input_data=self.complete_data_list[double_index])
    '''
    ↑                                                                                 ↑
    ********************************** 点击事件 ****************************************
    '''

    '''
    ********************************** 点击调用 ****************************************
    ↓                                                                                 ↓
    '''
    def open_new_todo_view(self, input_data=None, todo_type=None):
        # 未登录的判断
        self.main_object.show_login_tip()
        if self.main_object.current_user['username'] == "LocalUser":
            return
        # 限制数量
        if len(self.proceed_data_list) >= self.Max_Todo_Count or len(self.complete_data_list) >= self.Max_Todo_Count:
            dialog_module.box_information(self.main_object, "提示", "待办事项数量已达到上限！")
            return
        # 切换到编辑视图
        self.todo_card.stacked_widget.setCurrentIndex(2)
        # 确保编辑视图的主题是最新的
        self.todo_card.todo_edit_widget.refresh_theme()
        # 深拷贝防止数据改变
        input_data_copy = copy.deepcopy(input_data)
        self.todo_card.todo_edit_widget.set_data(input_data_copy, todo_type)
        # 连接编辑完成信号
        try:
            self.todo_card.todo_edit_widget.edit_finished.disconnect()
        except:
            pass
        self.todo_card.todo_edit_widget.edit_finished.connect(self.open_success_click)
        # 连接编辑取消信号
        try:
            self.todo_card.todo_edit_widget.edit_cancelled.disconnect()
        except:
            pass
        self.todo_card.todo_edit_widget.edit_cancelled.connect(lambda: self.todo_card.stacked_widget.setCurrentIndex(1))
    
    def open_success_click(self, input_data):
        # 这里不再需要从窗口获取数据，直接使用传入的input_data
        if input_data[0] is None or input_data[0] == "":
            # 限制数量
            if len(self.proceed_data_list) >= self.Max_Todo_Count or len(self.complete_data_list) >= self.Max_Todo_Count:
                dialog_module.box_information(self.main_object, "提示", "待办事项数量已达到上限！")
                return
            input_data[0] = str(uuid.uuid4())
            self.todo_add(input_data)
        else:
            self.todo_edit(input_data)

        # 切换回待办列表视图
        self.todo_card.stacked_widget.setCurrentIndex(1)
        self.todo_card.data_process_call_back(self.proceed_data_list, self.complete_data_list, self.todo_type)

    def todo_add(self, input_data):
        input_data[2] = False
        # 固定加到待办中
        print("[窗口]添加到待办中id:{},数据列表:{}".format(input_data[0], self.proceed_data_list))
        self.create_one(input_data, self.proceed_data_list, self.proceed_list_widget, self.proceed_widget_map,
                   self.proceed_item_map)
        print("[窗口]添加到待办中完成id:{},数据列表:{}".format(input_data[0], self.proceed_data_list))

    def todo_edit(self, input_data):
        if not input_data[2]:
            print("[窗口]编辑待办id:{},数据列表:{}".format(input_data[0], self.proceed_data_list))
            self.edit_ont(input_data, self.proceed_data_list, self.proceed_widget_map, self.proceed_item_map)
            print("[窗口]编辑待办完成id:{},数据列表:{}".format(input_data[0], self.proceed_data_list))
        else:
            print("[窗口]编辑完成id:{},数据列表:{}".format(input_data[0], self.complete_data_list))
            self.edit_ont(input_data, self.complete_data_list, self.complete_widget_map, self.complete_item_map)
            print("[窗口]编辑完成完成id:{},数据列表:{}".format(input_data[0], self.complete_data_list))

    '''
    ↑                                                                                 ↑
    ********************************** 点击调用 ****************************************
    '''
    def edit_ont(self, input_data, data_list, widget_map, item_map):
        checked_index = None
        todo_id = input_data[0]
        for todo_data_index in range(len(data_list)):
            if str(todo_id) == str(data_list[todo_data_index][0]):
                checked_index = todo_data_index
        data_list[checked_index] = input_data
        widget_map[todo_id].set_all(input_data[0], input_data[1], input_data[2],
                                    input_data[3], input_data[4], input_data[5])
        try:
            widget_map[todo_id].delete_button.clicked.disconnect()
        except Exception:
            pass
        try:
            widget_map[todo_id].check_push_button.clicked.disconnect()
        except Exception:
            pass
        if input_data[2]:
            print("编辑待办id:{},添加到待办单机触发:{}".format(input_data[0], self.proceed_data_list))
            widget_map[todo_id].delete_button.clicked.connect(partial(self.delete_click, todo_id, False))
            widget_map[todo_id].edit_button.clicked.connect(partial(self.edit_click, todo_id, False))
            widget_map[todo_id].check_push_button.clicked.connect(partial(self.checked_click, todo_id, False))
        else:
            print("编辑待办id:{},添加到完成单机触发:{}".format(input_data[0], self.proceed_data_list))
            widget_map[todo_id].delete_button.clicked.connect(partial(self.delete_click, todo_id, True))
            widget_map[todo_id].edit_button.clicked.connect(partial(self.edit_click, todo_id, True))
            widget_map[todo_id].check_push_button.clicked.connect(partial(self.checked_click, todo_id, True))
        if data_list[checked_index][4]:
            item_map[input_data[0]].setSizeHint(QSize(self.todo_card.card.width() - 20, 59))
        else:
            item_map[input_data[0]].setSizeHint(QSize(self.todo_card.card.width() - 20, 49))


    def delete_one(self, todo_id, data_list, item_map, widget_map, list_widget):
        delete_index = None
        delete_data = None
        for todo_data_index in range(len(data_list)):
            if str(todo_id) == str(data_list[todo_data_index][0]):
                delete_index = todo_data_index
                delete_data = data_list[todo_data_index]
        try:
            widget_map[todo_id].delete_button.clicked.disconnect()
        except Exception:
            pass
        try:
            widget_map[todo_id].check_push_button.clicked.disconnect()
        except Exception:
            pass
        try:
            widget_map[todo_id].degree_line.hide()
            widget_map[todo_id].degree_line.deleteLater()
        except Exception:
            pass
        del data_list[delete_index]
        del item_map[todo_id]
        del widget_map[todo_id]
        list_widget.takeItem(delete_index)
        return delete_data

    def create_one(self, create_data, data_list, list_widget, widget_map, item_map):
        data_list.append(create_data)
        todo_id = create_data[0]
        item = MyQListWidgetItemWidget(list_widget, self.todo_card, create_data[0], create_data[1], create_data[2],
                                       create_data[3], create_data[4], create_data[5])
        widget_map[todo_id] = item
        if create_data[2]:
            print("新增待办id:{},添加到待办单机触发:{}".format(create_data[0], self.proceed_data_list))
            item.delete_button.clicked.connect(partial(self.delete_click, todo_id, False))
            item.edit_button.clicked.connect(partial(self.edit_click, todo_id, False))
            item.check_push_button.clicked.connect(partial(self.checked_click, todo_id, False))
        else:
            print("新增待办id:{},添加到完成单机触发:{}".format(create_data[0], self.proceed_data_list))
            item.delete_button.clicked.connect(partial(self.delete_click, todo_id, True))
            item.edit_button.clicked.connect(partial(self.edit_click, todo_id, True))
            item.check_push_button.clicked.connect(partial(self.checked_click, todo_id, True))
        widget_item = QListWidgetItem(list_widget)
        widget_item.setSizeHint(item.sizeHint())
        item_map[todo_id] = widget_item
        list_widget.addItem(widget_item)
        list_widget.setItemWidget(widget_item, item)

    def refresh_theme(self, is_dark):
        try:
            for todo_id in self.complete_widget_map:
                self.complete_widget_map[todo_id].refresh_theme(is_dark)
            for todo_id in self.proceed_widget_map:
                self.proceed_widget_map[todo_id].refresh_theme(is_dark)
        except Exception as e:
            print("刷新待办主题失败:{}".format(e))