from PySide6.QtGui import Qt, QFont
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QVBoxLayout, QLabel, QHBoxLayout, QTextEdit, QPushButton,
    QScrollArea, QFrame, QWidget, QListWidget,
    QListWidgetItem, QAbstractItemView
)

from src.component.AgileTilesAcrylicWindow.AgileTilesAcrylicWindow import AgileTilesAcrylicWindow
from src.component.ImagePreviewWidget.ImagePreviewWidget import ImagePreviewWidget
from src.module.Ticket.TicketPopup.TicketPopup import TicketPopup
from src.module.Ticket.TicketSystem.TicketSystem import TicketSystem
from src.module.Box import message_box_util


class TicketDetailPopup(AgileTilesAcrylicWindow):
    """工单详情弹窗"""

    def __init__(self, parent=None, use_parent=None, screen=None, current_user=None, ticket_id=None, ticket_data=None):
        super().__init__(parent=parent, is_dark=use_parent.is_dark, form_theme_mode=use_parent.form_theme_mode,
                         form_theme_transparency=use_parent.form_theme_transparency)
        self.use_parent = use_parent
        self.screen = screen
        self.current_user = current_user
        self.ticket_id = ticket_id
        self.ticket_data = ticket_data

        self.setWindowTitle("工单详情")
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

        self.init_ui()

        # 从服务器加载
        self.load_ticket_details()

        self.showMaximized()

    def init_ui(self):
        # 根据主题设置颜色
        if self.is_dark:
            bg_color = "#1E1E1E"
            card_bg = "#252526"
            text_color = "#E0E0E0"
            border_color = "#3C3C3C"
            button_bg = "#007ACC"
            button_hover = "#0062A3"
            close_button_bg = "#F44336"
            close_button_hover = "#E57373"
            header_bg = "#333333"
        else:
            bg_color = "#F5F7FA"
            card_bg = "#FFFFFF"
            text_color = "#333333"
            border_color = "#DCDFE6"
            button_bg = "#2196F3"
            button_hover = "#64B5F6"
            close_button_bg = "#F44336"
            close_button_hover = "#EF9A9A"
            header_bg = "#E3F2FD"

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        self.widget_base.setLayout(main_layout)
        self.widget_base.setStyleSheet(f"background-color: {bg_color};")

        # 创建水平分割布局容器
        horizontal_container = QWidget()
        horizontal_layout = QHBoxLayout(horizontal_container)
        horizontal_layout.setSpacing(15)
        horizontal_layout.setContentsMargins(0, 0, 0, 0)

        # 左侧区域（标题+内容）
        left_column = QVBoxLayout()
        left_column.setSpacing(10)

        # 标题区域
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {header_bg};
                border-radius: 8px;
                padding: 15px;
                border: 1px solid {border_color};
            }}
        """)
        header_layout = QHBoxLayout(header_frame)

        # 标题
        self.title_label = QLabel()
        self.title_label.setFont(QFont("Microsoft YaHei", 9, QFont.Bold))
        self.title_label.setStyleSheet(f"color: {text_color}; padding: 3px 8px; border-radius: 4px;")
        self.title_label.setWordWrap(True)
        header_layout.addWidget(self.title_label)

        # 状态标签
        self.status_label = QLabel()
        self.status_label.setFont(QFont("Microsoft YaHei", 9))
        self.status_label.setStyleSheet(f"color: #FFFFFF; padding: 3px 8px; border-radius: 4px;")
        self.status_label.setMaximumWidth(80)
        header_layout.addWidget(self.status_label)

        # 创建时间
        self.date_label = QLabel()
        self.date_label.setFont(QFont("Microsoft YaHei", 9))
        self.date_label.setMaximumWidth(200)
        if self.is_dark:
            self.date_label.setStyleSheet("color: #A0A0A0;")
        else:
            self.date_label.setStyleSheet("color: #757575;")
        header_layout.addWidget(self.date_label)

        left_column.addWidget(header_frame)

        # 内容区域
        content_frame = QFrame()
        content_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {card_bg};
                border-radius: 8px;
                padding: 15px;
                border: 1px solid {border_color};
            }}
        """)
        content_layout = QVBoxLayout(content_frame)

        # 内容标题
        content_title = QLabel("问题描述")
        content_title.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        content_title.setStyleSheet(f"color: {text_color}; margin-bottom: 8px;")
        content_layout.addWidget(content_title)

        # 内容文本
        self.content_text = QTextEdit()
        self.content_text.setReadOnly(True)
        self.content_text.setFont(QFont("Microsoft YaHei", 10))
        self.content_text.setStyleSheet(f"""
            QTextEdit {{
                border: 1px solid {border_color};
                border-radius: 4px;
                padding: 10px;
                background-color: {card_bg};
                color: {text_color};
            }}
        """)
        self.content_text.setMinimumHeight(120)
        content_layout.addWidget(self.content_text)

        # 图片预览区域
        self.image_container = QWidget()
        self.image_container.setStyleSheet("border: none; background-color: transparent;")
        self.image_container_layout = QHBoxLayout(self.image_container)
        self.image_container_layout.setContentsMargins(0, 0, 0, 0)
        self.image_container_layout.setSpacing(10)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("border: none;")
        scroll_area.setWidget(self.image_container)

        content_layout.addWidget(scroll_area)
        left_column.addWidget(content_frame)

        # 将左侧列添加到水平布局
        horizontal_layout.addLayout(left_column, 2)  # 左侧占2/3宽度

        # 右侧区域（回复记录）
        right_column = QVBoxLayout()
        right_column.setSpacing(10)

        # 回复区域标题
        responses_title = QLabel("回复记录")
        responses_title.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        responses_title.setStyleSheet(f"color: {text_color};")
        right_column.addWidget(responses_title)

        # 回复列表区域
        responses_frame = QFrame()
        responses_frame.setMinimumWidth(700)
        responses_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {card_bg};
                border-radius: 8px;
                padding: 15px;
                border: 1px solid {border_color};
            }}
        """)
        responses_layout = QVBoxLayout(responses_frame)

        # 回复列表
        self.responses_list = QListWidget()
        self.responses_list.setStyleSheet(f"""
            QListWidget {{
                border: 1px solid {border_color};
                border-radius: 4px;
                background-color: {card_bg};
            }}
            QListWidget::item {{
                border-bottom: 1px solid {border_color};
                padding: 10px;
            }}
            QListWidget::item:selected {{
                background-color: {button_bg}20;
            }}
        """)
        self.responses_list.setSelectionMode(QAbstractItemView.NoSelection)
        responses_layout.addWidget(self.responses_list)

        right_column.addWidget(responses_frame)

        # 将右侧列添加到水平布局
        horizontal_layout.addLayout(right_column, 1)  # 右侧占1/3宽度

        # 将水平布局容器添加到主布局
        main_layout.addWidget(horizontal_container, 1)  # 使用拉伸因子1使其占据剩余空间

        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignRight)

        # 添加回复按钮
        self.add_response_btn = QPushButton("添加回复")
        self.add_response_btn.setFont(QFont("Microsoft YaHei", 10))
        self.add_response_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {button_bg};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
            }}
            QPushButton:hover {{
                background-color: {button_hover};
            }}
        """)
        self.add_response_btn.clicked.connect(self.open_add_response)
        button_layout.addWidget(self.add_response_btn)

        # 关闭工单按钮
        self.close_ticket_btn = QPushButton("关闭工单")
        self.close_ticket_btn.setFont(QFont("Microsoft YaHei", 10))
        self.close_ticket_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {close_button_bg};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
            }}
            QPushButton:hover {{
                background-color: {close_button_hover};
            }}
        """)
        self.close_ticket_btn.clicked.connect(self.close_ticket)
        button_layout.addWidget(self.close_ticket_btn)

        main_layout.addLayout(button_layout)

    # 其余方法保持不变...
    def load_ticket_details(self):
        """从服务器加载工单详情"""
        # 使用TicketSystem类获取工单详情
        if not hasattr(self.use_parent, 'ticket_system'):
            self.use_parent.ticket_system = TicketSystem(self.use_parent, self.use_parent.access_token)

        self.use_parent.ticket_system.fetch_ticket_details(
            self.ticket_id,
            lambda success, data: self.display_ticket_details(
                data) if success else message_box_util.box_acknowledgement(
                self.use_parent, "错误", f"加载工单详情失败: {data}")
        )

    def display_ticket_details(self, ticket_data):
        """显示工单详情"""
        self.ticket_data = ticket_data.get('ticket')
        if not ticket_data:
            return

        # 设置标题
        self.title_label.setText(self.ticket_data.get('title', '无标题'))

        # 设置状态
        status = self.ticket_data.get('status', '未知状态')

        if status == 'OPEN':
            status_text = "进行中"
            status_style = "background-color: #4CAF50;"
        elif status == 'CLOSED':
            status_text = "已关闭"
            status_style = "background-color: #9E9E9E;"
        else:
            status_text = status
            status_style = "background-color: #FF9800;"

        self.status_label.setText(status_text)
        self.status_label.setStyleSheet(status_style)

        # 设置日期
        self.date_label.setText(f"创建时间: {self.ticket_data.get('createTime', '')}")

        # 设置内容
        self.content_text.setPlainText(self.ticket_data.get('content', ''))

        # 加载图片
        self.load_images(ticket_data.get('files', []))

        # 加载回复
        self.load_responses(ticket_data.get('responses', []))

        # 根据状态更新按钮
        if status == 'CLOSED':
            self.add_response_btn.setEnabled(False)
            self.close_ticket_btn.setEnabled(False)
            self.close_ticket_btn.setText("已关闭")
            self.close_ticket_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: #9E9E9E;
                    color: white;
                }}
            """)
        else:
            self.add_response_btn.setEnabled(True)
            self.close_ticket_btn.setEnabled(True)
            self.close_ticket_btn.setText("关闭工单")

    def load_images(self, images):
        """加载图片预览"""
        # 清除现有图片
        for i in reversed(range(self.image_container_layout.count())):
            widget = self.image_container_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        if images is None:
            return

        # 添加新图片
        for image in images:
            # 创建预览小部件
            image_url = image.get('url', '')
            preview = ImagePreviewWidget(image_url, False)
            preview.setFixedSize(100, 100)
            self.image_container_layout.addWidget(preview)

    def load_responses(self, responses):
        """加载回复记录"""
        self.responses_list.clear()

        if responses is None:
            return

        # 按时间倒序排列
        responses_sorted = sorted(responses, key=lambda x: x.get('createTime', ''), reverse=True)

        for response in responses_sorted:

            response_data = response.get('response', [])
            response_files = response.get('files', [])  # 获取回复的图片列表

            # 创建回复项
            item = QListWidgetItem()
            # 根据是否有图片动态调整高度
            item_height = 300 if response_files else 130
            item.setSizeHint(QSize(0, item_height))

            # 创建自定义部件
            widget = QWidget()
            layout = QVBoxLayout(widget)
            layout.setContentsMargins(2, 2, 2, 2)

            # 回复者信息
            user_layout = QHBoxLayout()
            user_label = QLabel(f"{response.get('username', '未知用户')} ({response.get('role', '用户')})")
            user_label.setFont(QFont("Microsoft YaHei", 9, QFont.Bold))
            if self.is_dark:
                user_label.setStyleSheet("color: #E0E0E0;")
            else:
                user_label.setStyleSheet("color: #333333;")
            user_layout.addWidget(user_label)

            date_label = QLabel(response_data.get('createTime', ''))
            date_label.setFont(QFont("Microsoft YaHei", 8))
            if self.is_dark:
                date_label.setStyleSheet("color: #A0A0A0;")
            else:
                date_label.setStyleSheet("color: #757575;")
            user_layout.addWidget(date_label)
            user_layout.addStretch()
            layout.addLayout(user_layout)

            # 回复内容
            content_label = QTextEdit(response_data.get('content', ''))
            content_label.setReadOnly(True)
            content_label.setFont(QFont("Microsoft YaHei", 9))
            if self.is_dark:
                content_label.setStyleSheet("border: none; background-color: transparent; color: #E0E0E0;")
            else:
                content_label.setStyleSheet("border: none; background-color: transparent; color: #333333;")
            content_label.setFixedHeight(70)
            layout.addWidget(content_label)

            # ===== 新增图片预览区域 =====
            if response_files:
                # 图片容器
                image_container = QWidget()
                image_container.setStyleSheet("border: none; background-color: transparent;")
                image_layout = QHBoxLayout(image_container)
                image_layout.setContentsMargins(0, 0, 0, 0)
                image_layout.setSpacing(5)

                # 滚动区域
                scroll_area = QScrollArea()
                scroll_area.setWidgetResizable(True)
                scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
                scroll_area.setStyleSheet("border: none;")
                scroll_area.setMinimumHeight(110)
                scroll_area.setWidget(image_container)

                # 添加图片预览
                for file in response_files:
                    image_url = file.get('url', '')
                    if image_url:
                        preview = ImagePreviewWidget(image_url, False)
                        preview.setFixedSize(100, 100)
                        image_layout.addWidget(preview)

                layout.addWidget(scroll_area)
            # ===== 结束新增区域 =====

            # 添加到列表
            self.responses_list.addItem(item)
            self.responses_list.setItemWidget(item, widget)

    def open_add_response(self):
        """打开添加回复弹窗"""
        # 确保有ticket_id
        if not self.ticket_id:
            message_box_util.box_acknowledgement(self.use_parent, "错误", "无法确定工单ID")
            return

        # 创建回复弹窗
        response_popup = TicketPopup(
            parent=None,
            use_parent=self.use_parent,
            title="添加回复",
            screen=self.screen,
            current_user=self.current_user,
            mode="reply",
            ticket_id=self.ticket_id,
            ticket_title=self.ticket_data.get('title', '')
        )
        # response_popup.refresh_geometry(self.screen)
        response_popup.show()

        # 连接关闭信号以刷新详情
        response_popup.destroyed.connect(self.load_ticket_details)

    def close_ticket(self):
        """关闭工单"""
        if not self.ticket_id:
            message_box_util.box_acknowledgement(self.use_parent, "错误", "无法确定工单ID")
            return

        # 使用TicketSystem类关闭工单
        if not hasattr(self.use_parent, 'ticket_system'):
            self.use_parent.ticket_system = TicketSystem(self.use_parent, self.use_parent.access_token)

        self.use_parent.ticket_system.close_ticket(
            self.ticket_id,
            lambda success, msg: self.handle_close_ticket(success, msg)
        )

    def handle_close_ticket(self, success, message):
        """处理关闭工单结果"""
        if success:
            message_box_util.box_acknowledgement(self.use_parent, "成功", message)
            # 刷新工单详情
            self.load_ticket_details()
        else:
            message_box_util.box_acknowledgement(self.use_parent, "错误", f"关闭工单失败: {message}")