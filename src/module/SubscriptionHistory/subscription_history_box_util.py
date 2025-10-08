import json
from src.util import my_shiboken_util

from PySide6.QtWidgets import QVBoxLayout, QHeaderView, QTableWidget, QHBoxLayout, QPushButton, \
    QLabel, QTableWidgetItem
from PySide6.QtCore import QUrl
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

from src.client import common
from src.my_component.AgileTilesAcrylicWindow.AgileTilesAcrylicWindow import AgileTilesAcrylicWindow
from src.ui import style_util

# 状态和来源的映射字典
STATUS_MAP = {
    "EFFECTIVE": "有效",
    "INVALID": "失效"
}

SOURCE_MAP = {
    "INVITED": "被邀请奖励",
    "INVITE": "邀请人奖励",
    "PAY": "支付"
}

PLAN_MAP = {
    "1": "周卡",
    "2": "月卡",
    "3": "季卡",
    "4": "年卡"
}


class SubscriptionHistoryPopup(AgileTilesAcrylicWindow):

    history_reply = None

    def __init__(self, parent=None, use_parent=None, screen=None, current_user=None):
        super().__init__(parent=parent, is_dark=use_parent.is_dark, form_theme_mode=use_parent.form_theme_mode,
                         form_theme_transparency=use_parent.form_theme_transparency)
        self.use_parent = use_parent
        self.screen = screen
        self.current_user = current_user

        self.setWindowTitle("会员订阅记录")
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

        # 初始化网络管理器
        self.network_manager = QNetworkAccessManager(self)

        # 初始化分页参数
        self.current_page = 1
        self.total_pages = 1

        try:
            self.setWindowTitle("会员订阅记录")
            self.setMinimumWidth(800)
            self.setMinimumHeight(600)
            # 初始化界面
            self.init_ui()
            # 设置样式
            style_util.set_dialog_control_style(self, self.is_dark)
        except Exception as e:
            print(e)

        # 初始加载数据
        self.load_data()

    def init_ui(self):
        """设置UI布局"""
        # 根据主题设置颜色
        if self.is_dark:
            self.style_map = {
                "bg_color": "#1E1E1E",
                "text_color": "#E0E0E0",
            }
        else:
            self.style_map = {
                "bg_color": "#F5F7FA",
                "text_color": "#333333",
            }

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        self.widget_base.setLayout(main_layout)
        self.widget_base.setStyleSheet(f"background-color: {self.style_map['bg_color']};color: {self.style_map['text_color']};")

        # 创建表格
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["套餐", "状态", "来源"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.table)

        # 创建分页控件
        pagination_layout = QHBoxLayout()

        self.prev_btn = QPushButton("上一页")
        self.prev_btn.setMinimumHeight(30)
        self.prev_btn.clicked.connect(self.prev_page)
        pagination_layout.addWidget(self.prev_btn)

        self.page_label = QLabel("第1页/共1页")
        self.page_label.setMinimumHeight(30)
        pagination_layout.addWidget(self.page_label)

        self.next_btn = QPushButton("下一页")
        self.next_btn.setMinimumHeight(30)
        self.next_btn.clicked.connect(self.next_page)
        pagination_layout.addWidget(self.next_btn)

        main_layout.addLayout(pagination_layout)

        # 初始禁用分页按钮
        self.update_pagination_state()

    def load_data(self):
        """加载当前页的数据"""
        url = QUrl(f"{common.BASE_URL}/userSubscription/normal/page?current={self.current_page}&size=10")
        request = QNetworkRequest(url)
        request.setRawHeader(b"Authorization", self.use_parent.access_token.encode())
        # 发送网络请求
        self.history_reply = self.network_manager.get(request)
        self.history_reply.finished.connect(self.handle_response)

    def handle_response(self):
        """处理网络响应"""
        if self.history_reply.error() == QNetworkReply.NoError:
            data = self.history_reply.readAll().data()
            try:
                json_data = json.loads(data)
                if json_data["code"] == 0:
                    self.process_data(json_data["data"])
            except (json.JSONDecodeError, KeyError) as e:
                print(f"数据处理错误: {e}")
        else:
            print(f"网络错误: {self.history_reply.errorString()}")

        # 在执行删除操作前，检查C++对象是否存活
        if self.history_reply is not None and my_shiboken_util.is_qobject_valid(self.history_reply):
            self.history_reply.deleteLater()
        self.history_reply = None

    def process_data(self, data):
        """处理并显示数据"""
        # 更新分页信息
        self.total_pages = data["pages"]
        self.update_pagination_state()

        # 清空表格
        self.table.setRowCount(0)

        # 填充表格数据
        records = data["records"]
        for row, record in enumerate(records):
            self.table.insertRow(row)

            # 套餐（映射为中文）
            plan = PLAN_MAP.get(str(record["planId"]), str(record["planId"]))
            self.table.setItem(row, 0, QTableWidgetItem(plan))

            # 状态（映射为中文）
            status = STATUS_MAP.get(record["validStatus"], record["validStatus"])
            self.table.setItem(row, 1, QTableWidgetItem(status))

            # 来源（映射为中文）
            source = SOURCE_MAP.get(record["sourceType"], record["sourceType"])
            self.table.setItem(row, 2, QTableWidgetItem(source))

    def update_pagination_state(self):
        """更新分页控件状态"""
        # 更新页码标签
        self.page_label.setText(f"第{self.current_page}页/共{self.total_pages}页")

        # 更新按钮状态
        self.prev_btn.setEnabled(self.current_page > 1)
        self.next_btn.setEnabled(self.current_page < self.total_pages)

    def prev_page(self):
        """跳转到上一页"""
        if self.current_page > 1:
            self.current_page -= 1
            self.load_data()

    def next_page(self):
        """跳转到下一页"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.load_data()



# 在main_object中添加工单系统的入口函数
def show_subscription_history_dialog(main_object, current_user):
    """显示工单列表"""
    screen = main_object.toolkit.resolution_util.get_screen(main_object)
    dialog = SubscriptionHistoryPopup(None, use_parent=main_object, screen=screen, current_user=current_user)
    # dialog.refresh_geometry(screen)
    dialog.show()
    return dialog