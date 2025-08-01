from PySide6.QtGui import Qt, QFont
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFrame, QWidget, QListWidget,
    QListWidgetItem
)

from src.component.AgileTilesAcrylicWindow.AgileTilesAcrylicWindow import AgileTilesAcrylicWindow
from src.module.Ticket.TicketDetailPopup.TicketDetailPopup import TicketDetailPopup
from src.module.Ticket.TicketPopup.TicketPopup import TicketPopup
from src.module.Ticket.TicketSystem.TicketSystem import TicketSystem
from src.module.Box import message_box_util


class TicketListPopup(AgileTilesAcrylicWindow):
    """工单列表弹窗"""

    style_map = {}

    def __init__(self, parent=None, use_parent=None, screen=None, current_user=None):
        super().__init__(parent=parent, is_dark=use_parent.is_dark, form_theme_mode=use_parent.form_theme_mode,
                         form_theme_transparency=use_parent.form_theme_transparency)
        self.use_parent = use_parent
        self.screen = screen
        self.current_user = current_user

        self.setWindowTitle("工单列表")
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

        self.init_ui()
        self.load_tickets()
        # 最大化
        self.showMaximized()

    def init_ui(self):
        # 根据主题设置颜色
        if self.is_dark:
            self.style_map = {
                "bg_color": "#1E1E1E",
                "card_bg": "#252526",
                "text_color": "#E0E0E0",
                "border_color": "#3C3C3C",
                "button_bg": "#007ACC",
                "button_hover": "#0062A3",
                "status_open": "#F44336",
                "status_closed": "#E57373"
            }
        else:
            self.style_map = {
                "bg_color": "#F5F7FA",
                "card_bg": "#FFFFFF",
                "text_color": "#333333",
                "border_color": "#DCDFE6",
                "button_bg": "#2196F3",
                "button_hover": "#64B5F6",
                "status_open": "#4CAF50",
                "status_closed": "#9E9E9E"
            }

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        self.widget_base.setLayout(main_layout)
        self.widget_base.setStyleSheet(f"background-color: {self.style_map['bg_color']};")

        # 标题区域
        header_layout = QHBoxLayout()

        title_label = QLabel("会员专属工单")
        title_label.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        title_label.setStyleSheet(f"color: {self.style_map['text_color']};")
        header_layout.addWidget(title_label)

        # 新建工单按钮
        new_ticket_btn = QPushButton("新建工单")
        new_ticket_btn.setFont(QFont("Microsoft YaHei", 10))
        new_ticket_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.style_map['button_bg']};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
            }}
            QPushButton:hover {{
                background-color: {self.style_map['button_hover']};
            }}
        """)
        new_ticket_btn.clicked.connect(self.open_new_ticket)
        header_layout.addWidget(new_ticket_btn)

        main_layout.addLayout(header_layout)

        # 列表区域
        list_frame = QFrame()
        list_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.style_map['card_bg']};
                border-radius: 8px;
                border: 1px solid {self.style_map['border_color']};
            }}
        """)
        list_layout = QVBoxLayout(list_frame)
        list_layout.setContentsMargins(0, 0, 0, 0)

        # 列表控件
        self.ticket_list = QListWidget()
        self.ticket_list.setStyleSheet(f"""
            QListWidget {{
                border: none;
                background-color: transparent;
                color: {self.style_map['text_color']};
            }}
            QListWidget::item {{
                border-bottom: 1px solid {self.style_map['border_color']};
                padding: 15px;
            }}
            QListWidget::item:selected {{
                background-color: {self.style_map['button_bg']};
            }}
        """)
        self.ticket_list.itemDoubleClicked.connect(self.open_ticket_detail)
        list_layout.addWidget(self.ticket_list)

        main_layout.addWidget(list_frame)

    def load_tickets(self):
        """加载工单列表"""
        # 初始化工单系统
        if not hasattr(self.use_parent, 'ticket_system'):
            self.use_parent.ticket_system = TicketSystem(self.use_parent)

        # 获取工单列表
        self.use_parent.ticket_system.fetch_tickets(
            lambda success, data: self.display_tickets(data) if success else message_box_util.box_acknowledgement(
                self.use_parent, "错误", f"加载工单列表失败: {data}")
        )

    def display_tickets(self, tickets):
        """显示工单列表"""
        self.ticket_list.clear()

        # 按时间倒序排列
        tickets_sorted = sorted(tickets, key=lambda x: x.get('createTime', ''), reverse=True)

        for ticket in tickets_sorted:
            # 创建列表项
            item = QListWidgetItem()
            item.setData(Qt.UserRole, ticket)  # 存储工单数据
            item.setSizeHint(QSize(0, 80))  # 设置项高度

            # 创建自定义部件
            widget = QWidget()
            layout = QVBoxLayout(widget)
            layout.setContentsMargins(5, 5, 5, 5)

            # 标题和状态
            header_layout = QHBoxLayout()

            # 标题
            title_label = QLabel(ticket.get('title', '无标题'))
            title_label.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
            title_label.setMinimumHeight(40)
            if self.is_dark:
                title_label.setStyleSheet("color: #E0E0E0;")
            else:
                title_label.setStyleSheet("color: #333333;")
            header_layout.addWidget(title_label)

            # 日期
            date_label = QLabel(ticket.get('createTime', ''))
            date_label.setFont(QFont("Microsoft YaHei", 8))
            date_label.setMaximumWidth(200)
            date_label.setMinimumHeight(40)
            if self.is_dark:
                date_label.setStyleSheet("color: #A0A0A0;")
            else:
                date_label.setStyleSheet("color: #757575;")
            header_layout.addWidget(date_label)

            # 状态
            status = ticket.get('status', 'unknown')
            status_label = QLabel()
            status_label.setFont(QFont("Microsoft YaHei", 9))
            status_label.setMaximumWidth(80)
            status_label.setMinimumHeight(40)
            if status == 'OPEN':
                status_label.setText("进行中")
                status_label.setStyleSheet(
                    "color: #FFFFFF; background-color: #4CAF50; padding: 2px 8px; border-radius: 4px;")
            elif status == 'CLOSED':
                status_label.setText("已关闭")
                status_label.setStyleSheet(
                    "color: #FFFFFF; background-color: #9E9E9E; padding: 2px 8px; border-radius: 4px;")
            else:
                status_label.setText(status)
                status_label.setStyleSheet(
                    "color: #FFFFFF; background-color: #FF9800; padding: 2px 8px; border-radius: 4px;")
            header_layout.addWidget(status_label)

            # 查看按钮
            view_btn = QPushButton("查看")
            view_btn.setFont(QFont("Microsoft YaHei", 8))
            view_btn.setMaximumWidth(80)
            view_btn.setMinimumHeight(40)
            # 设置按钮样式
            btn_style = f"""
                QPushButton {{
                    background-color: {self.style_map['button_bg']};
                    color: white;
                    border: none;
                    border-radius: 4px;
                }}
                QPushButton:hover {{
                    background-color: {self.style_map['button_hover']};
                }}
            """
            view_btn.setStyleSheet(btn_style)
            # 存储工单数据到按钮属性
            view_btn.ticket_data = ticket
            view_btn.clicked.connect(self.open_ticket_detail_by_button)
            header_layout.addWidget(view_btn)

            layout.addLayout(header_layout)

            # 添加到列表
            self.ticket_list.addItem(item)
            self.ticket_list.setItemWidget(item, widget)

    def open_ticket_detail_by_button(self):
        """通过按钮打开工单详情"""
        # 获取发送信号的按钮对象
        button = self.sender()
        if hasattr(button, 'ticket_data'):
            ticket_data = button.ticket_data
            detail_popup = TicketDetailPopup(
                parent=None,
                use_parent=self.use_parent,
                screen=self.screen,
                current_user=self.current_user,
                ticket_id=ticket_data.get('id'),
                ticket_data=ticket_data
            )
            detail_popup.show()
            detail_popup.destroyed.connect(self.load_tickets)

    def open_new_ticket(self):
        """打开新建工单弹窗"""
        ticket_popup = TicketPopup(
            parent=None,
            use_parent=self.use_parent,
            title="新建工单",
            screen=self.screen,
            current_user=self.current_user,
            mode="create"
        )
        # ticket_popup.refresh_geometry(self.screen)
        ticket_popup.show()

        # 连接关闭信号以刷新列表
        ticket_popup.destroyed.connect(self.load_tickets)

    def open_ticket_detail(self, item):
        """打开工单详情"""
        ticket_data = item.data(Qt.UserRole)
        if ticket_data:
            detail_popup = TicketDetailPopup(
                parent=None,
                use_parent=self.use_parent,
                screen=self.screen,
                current_user=self.current_user,
                ticket_id=ticket_data.get('id'),
                ticket_data=ticket_data
            )
            # detail_popup.refresh_geometry(self.screen)
            detail_popup.show()

            # 连接关闭信号以刷新列表
            detail_popup.destroyed.connect(self.load_tickets)


# 在main_object中添加工单系统的入口函数
def show_ticket_list_dialog(main_object, current_user):
    """显示工单列表"""
    screen = main_object.toolkit.resolution_util.get_screen(main_object)
    dialog = TicketListPopup(None, use_parent=main_object, screen=screen, current_user=current_user)
    # dialog.refresh_geometry(screen)
    dialog.show()
    return dialog


def show_new_ticket_dialog(main_object, current_user):
    """显示新建工单弹窗"""
    screen = main_object.toolkit.resolution_util.get_screen(main_object)
    dialog = TicketPopup(
        None,
        use_parent=main_object,
        title="新建工单",
        screen=screen,
        current_user=current_user,
        mode="create"
    )
    # dialog.refresh_geometry(screen)
    dialog.show()
    return dialog