# coding:utf-8
import json
from functools import partial

from PySide6.QtCore import Signal, QUrlQuery, QUrl, QDateTime
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PySide6.QtWidgets import QVBoxLayout, QListWidget, QWidget, QHBoxLayout, QLabel, QPushButton, QListWidgetItem

from src.client import common
from src.component.AgileTilesAcrylicWindow.AgileTilesAcrylicWindow import AgileTilesAcrylicWindow
import src.ui.style_util as style_util
from src.constant import data_save_constant
from src.module.UserData.HistoryRecover.user_data_history_recover_form import Ui_Form
from src.module.Box import message_box_util


class UserServerRecoverWindow(AgileTilesAcrylicWindow, Ui_Form):

    use_parent = None
    setting_signal = Signal(str)
    mode_list = None
    tab_list_widgets = []
    recover_btn_list = []
    delete_btn_list = []

    def __init__(self, parent=None, use_parent=None):
        super(UserServerRecoverWindow, self).__init__(is_dark=use_parent.is_dark, form_theme_mode=use_parent.form_theme_mode,
                                                 form_theme_transparency=use_parent.form_theme_transparency)
        self.setupUi(self)
        # 初始化
        self.use_parent = use_parent
        # 布局初始化
        self.widget_base.setLayout(self.gridLayout)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        # 设置标题栏
        self.setWindowTitle("灵卡面板 - 恢复历史数据")
        self.titleBar.minBtn.close()
        self.titleBar.maxBtn.close()
        # 初始化界面布局
        self._init_ui()
        # 设置样式
        style_util.set_dialog_control_style(self, self.is_dark)
        # 初始化属性
        self.network_manager = QNetworkAccessManager(self)
        self._init_network()
        self.load_data()

    def __del__(self):
        try:
            # 终止所有网络请求
            for reply in self.network_manager.findChildren(QNetworkReply):
                reply.abort()
                reply.deleteLater()

            # 清空引用（改为重新赋值空列表）
            self.tab_list_widgets = []
            self.recover_btn_list = []
            self.delete_btn_list = []

            # 父类析构
            super().__del__()
        except Exception as e:
            print(f"析构异常: {e}")

    def _init_ui(self):
        # 初始化选项卡列表控件
        for index in range(self.tabWidget.count()):
            tab = self.tabWidget.widget(index)
            layout = QVBoxLayout(tab)
            list_widget = QListWidget()
            list_widget.setStyleSheet("QListWidget { border: none; }")
            layout.addWidget(list_widget)
            self.tab_list_widgets.append(list_widget)

    def _init_network(self):
        """初始化网络相关设置"""
        self.frequency_mapping = ['original', '1h', '1d', '1m', '1y']

    def load_data(self):
        """加载所有选项卡的数据"""
        print("加载所有选项卡的数据")
        for tab_index in range(len(self.frequency_mapping)):
            self.request_tab_data(tab_index)

    def request_tab_data(self, tab_index):
        """请求指定选项卡的数据"""
        if self.use_parent.current_user is None or self.use_parent.access_token is None:
            return
        frequency = self.frequency_mapping[tab_index]
        print(f"请求{frequency}的数据")
        url = QUrl(common.BASE_URL + "/userData/normal/history")
        query = QUrlQuery()
        query.addQueryItem("username", self.use_parent.current_user["username"])  # 应从配置获取实际用户名
        query.addQueryItem("frequency", frequency)
        url.setQuery(query)

        request = QNetworkRequest(url)
        request.setRawHeader(b"Authorization", self.use_parent.access_token.encode('utf-8'))
        reply = self.network_manager.get(request)
        reply.tab_index = tab_index  # 存储选项卡索引
        reply.finished.connect(self.handle_response)

    def handle_response(self):
        """处理网络响应"""
        print("处理网络响应")
        reply = self.sender()
        if reply.error() == QNetworkReply.NoError:
            data = json.loads(reply.readAll().data())
            if data["code"] == 0:
                self.update_tab_list(reply.tab_index, data["data"])
            else:
                print(f"Error fetching data: {data}")
        else:
            print(f"Error fetching data: {reply.errorString()}")
        reply.deleteLater()

    def update_tab_list(self, tab_index, data_list):
        """更新指定选项卡的列表"""
        # 新增有效性检查
        if not self.isVisible():  # 检查窗口是否可见
            print("窗口不可见")
            return
        print("更新指定选项卡的列表")
        # 检查索引有效性
        if (tab_index >= len(self.tab_list_widgets) or
            not self.tab_list_widgets[tab_index].isWidgetType()):
            return
        list_widget = self.tab_list_widgets[tab_index]
        list_widget.clear()

        for data in data_list:
            print(data)
            item_widget = QWidget()
            layout = QHBoxLayout(item_widget)
            layout.setContentsMargins(5, 2, 5, 2)

            # 时间显示
            timestamp = data["timestamp"]
            dt = QDateTime.fromMSecsSinceEpoch(timestamp)
            time_label = QLabel(dt.toString("yyyy年MM月dd日 HH:mm:ss"))
            layout.addWidget(time_label, 4)

            # 恢复按钮
            recover_btn = QPushButton("从此节点恢复")
            recover_btn.setObjectName("recoverBtn")
            recover_btn.clicked.connect(partial(self._handle_recover, data))
            self.recover_btn_list.append(recover_btn)
            layout.addWidget(recover_btn, 3)

            # 删除按钮
            delete_btn = QPushButton("删除")
            delete_btn.setObjectName("deleteBtn")
            delete_btn.clicked.connect(partial(self._handle_delete, data))
            self.delete_btn_list.append(delete_btn)
            layout.addWidget(delete_btn, 2)

            # 创建列表项
            list_item = QListWidgetItem()
            list_item.setSizeHint(item_widget.sizeHint())
            list_widget.addItem(list_item)
            list_widget.setItemWidget(list_item, item_widget)

    def _handle_recover(self, data):
        """处理恢复操作"""
        print(f"Recovering data: {data['dataHash']}")

        # 构造请求参数
        url = QUrl(common.BASE_URL + "/userData/normal/history/one")
        query = QUrlQuery()
        query.addQueryItem("username", self.use_parent.current_user["username"])
        query.addQueryItem("frequency", self.frequency_mapping[self.tabWidget.currentIndex()])
        query.addQueryItem("frequencyDataId", str(data["id"]))  # 假设data中包含id字段
        url.setQuery(query)

        # 发送GET请求
        request = QNetworkRequest(url)
        request.setRawHeader(b"Authorization", self.use_parent.access_token.encode('utf-8'))
        reply = self.network_manager.get(request)
        reply.finished.connect(lambda: self._handle_recover_response(reply, data))

    def _handle_recover_response(self, reply, data):
        """处理恢复响应"""
        if reply.error() == QNetworkReply.NoError:
            response = json.loads(reply.readAll().data())
            if response["code"] == 0:
                print(f"恢复数据成功: {response['data']}")
                user_data_record = response["data"]
                main_data = json.loads(user_data_record["data"])
                self.use_parent.main_data = main_data
                self.use_parent.local_trigger_data_update(trigger_type=data_save_constant.TRIGGER_TYPE_DATA_RECOVER,
                                                      in_data=main_data)
                message_box_util.box_information(self.use_parent, "提示信息", "恢复数据成功")
            else:
                print(f"恢复失败: {response['msg']}")
                message_box_util.box_information(self.use_parent, "错误信息", "恢复数据失败，请稍后重试")
        else:
            print(f"请求失败: {reply.errorString()}")
        reply.deleteLater()

    def _handle_delete(self, data):
        """处理删除操作"""
        url = QUrl(common.BASE_URL + "/userData/normal/history/one")
        query = QUrlQuery()
        query.addQueryItem("username", self.use_parent.current_user["username"])
        query.addQueryItem("frequency", self.frequency_mapping[self.tabWidget.currentIndex()])
        query.addQueryItem("frequencyDataId", str(data["id"]))  # 假设data中包含id字段
        url.setQuery(query)

        # 发送DELETE请求
        request = QNetworkRequest(url)
        request.setRawHeader(b"Authorization", self.use_parent.access_token.encode('utf-8'))
        reply = self.network_manager.deleteResource(request)  # 使用DELETE方法
        reply.finished.connect(lambda: self._handle_delete_response(reply))

    def _handle_delete_response(self, reply):
        """处理删除响应"""
        if reply.error() == QNetworkReply.NoError:
            response = json.loads(reply.readAll().data())
            if response["code"] == 0 and response["data"]:
                print("删除成功，刷新列表")
                self.request_tab_data(self.tabWidget.currentIndex())
                message_box_util.box_information(self.use_parent, "提示信息", "删除数据成功")
            else:
                print(f"删除失败: {response['msg']}")
                message_box_util.box_information(self.use_parent, "错误信息", "删除数据失败，请稍后重试")
        else:
            print(f"请求失败: {reply.errorString()}")
        reply.deleteLater()

    def closeEvent(self, event):
        """重写关闭事件处理"""
        # 终止所有网络请求
        for reply in self.network_manager.findChildren(QNetworkReply):
            reply.abort()
            reply.deleteLater()

        # 清空控件引用
        self.tab_list_widgets.clear()
        self.recover_btn_list.clear()
        self.delete_btn_list.clear()

        event.accept()