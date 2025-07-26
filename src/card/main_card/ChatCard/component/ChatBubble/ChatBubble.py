from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class ChatBubble(QTextBrowser):
    def __init__(self, parent=None, text="", is_user=True, is_dark=False, is_reasoning=False):
        super().__init__(parent)

        # self.setOpenLinks(False)
        self.setMarkdown(text)

        # 尺寸策略
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 连接文档大小变化信号
        self.document().documentLayout().documentSizeChanged.connect(self.adjustSize)

        # 根据主题、消息类型和思考状态设置样式
        if is_dark:
            # 深色主题配色
            if is_user:
                # 用户消息
                bg_color = "#2a2a2a"
                text_color = "#e0e0e0"
                link_color = "#b0b0ff"
            elif is_reasoning:
                # AI思考过程
                bg_color = "#333333"  # 稍亮的灰色
                text_color = "#b0b0b0"  # 浅灰色文字
                link_color = "#9090ff"
                border_color = "#555555"  # 边框颜色
            else:
                # AI正常回复
                bg_color = "#1e1e1e"
                text_color = "#f0f0f0"
                link_color = "#b0b0ff"
        else:
            # 浅色主题配色
            if is_user:
                # 用户消息
                bg_color = "#f0f0f0"
                text_color = "#333333"
                link_color = "#5050b0"
            elif is_reasoning:
                # AI思考过程
                bg_color = "#f5f5f5"  # 浅灰色背景
                text_color = "#666666"  # 深灰色文字
                link_color = "#404090"
                border_color = "#d0d0d0"  # 边框颜色
            else:
                # AI正常回复
                bg_color = "#eaeaea"
                text_color = "#333333"
                link_color = "#5050b0"

        # 构建样式表
        style = f"""
            QTextBrowser {{
                border: none;
                border-radius: 10px;
                padding-left: 10px;
                padding-right: 10px;
                padding-top: 10px;
                padding-bottom: 20px;
                background-color: {bg_color};
                color: {text_color};
                margin: 0;
        """

        # 为思考气泡添加特殊样式
        if is_reasoning:
            style += f"""
                border: 1px solid {border_color};
                border-bottom-left-radius: 0;
                border-bottom-right-radius: 0;
                margin-bottom: 1px;
            """

        style += f"""
            }}
            QTextBrowser a {{
                color: {link_color};
                text-decoration: none;
            }}
            QTextBrowser a:hover {{
                text-decoration: underline;
            }}
        """

        self.setStyleSheet(style)

    def adjustSize(self):
        # 动态调整高度
        height = int(self.document().size().height() + 40)
        self.setFixedHeight(height)

        # 动态调整宽度（最大不超过父容器的95%）
        if self.parent() and self.parent().parent():
            max_width = int(self.parent().parent().width() * 0.95)
            self.setMaximumWidth(max_width)

    def contextMenuEvent(self, event):
        # 创建自定义右键菜单
        menu = QMenu(self)

        # 添加汉化菜单项
        copy_action = menu.addAction("复制")
        select_all_action = menu.addAction("全选")

        # 连接动作信号
        copy_action.triggered.connect(self.copy)
        select_all_action.triggered.connect(self.selectAll)

        # 美化菜单样式（与当前主题一致）
        if hasattr(self, 'is_dark') and self.is_dark:  # 深色主题
            menu.setStyleSheet("""
                QMenu {
                    background-color: #2a2a2a;
                    color: #e0e0e0;
                    border: 1px solid #555555;
                    border-radius: 5px;
                    padding: 5px;
                }
                QMenu::item:selected {
                    background-color: #3a3a3a;
                }
            """)
        else:  # 浅色主题
            menu.setStyleSheet("""
                QMenu {
                    background-color: #f5f5f5;
                    color: #333333;
                    border: 1px solid #d0d0d0;
                    border-radius: 5px;
                    padding: 5px;
                }
                QMenu::item:selected {
                    background-color: #e0e0e0;
                }
            """)

        menu.exec(event.globalPos())
