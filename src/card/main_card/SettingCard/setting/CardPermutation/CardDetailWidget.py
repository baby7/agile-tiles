import json
import traceback

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy, QFrame, QTextBrowser
)
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QPixmap, QTextCursor, QCursor, QColor
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

from src.client import common


class CardDetailWidget(QWidget):
    detailClose = Signal(dict)  # 新增信号用于传递卡片数据

    def __init__(self, parent=None, use_parent=None, card_id=None, is_dark=False):
        super().__init__(parent)
        self.use_parent = use_parent
        self.card_id = card_id
        self.is_dark = is_dark
        # 创建网络管理器
        self.network_manager = QNetworkAccessManager(self)
        self.network_manager.finished.connect(self.handle_response)
        # 初始化UI
        self.init_ui()
        self.re_init(self.card_id)

    def re_init(self, card_id=None):
        self.card_id = card_id
        # 初始化测试数据
        test_data = {
            "id": 0,
            "title": "卡片标题",
            "description": "卡片详情",
            "developer": {
                "nickName": "开发者名称"
            },
            "openSourceUrl": "https://github.com",
            "cardIcon": {
                "url": None
            },
            "currentVersion": {
                "version": "v0.0.1",
                "file": {"size": 0},
                "createTime": "2000-01-01 00:00:00",
                "supportSizeList": [
                    "2_2"
                ]
            },
            "versionHistory": [
                {
                    "version": "v0.0.1",
                    "description": "更新说明",
                    "createTime": "2000-01-01 00:00:00"
                },
                {
                    "version": "v0.0.2",
                    "description": "修复了已知问题\n优化了性能表现",
                    "createTime": "2000-02-01 10:30:00"
                }
            ]
        }
        self.parse_card_data(test_data)
        # 发送请求
        self.fetch_card_data()

    def create_close_button(self):
        btn = QtWidgets.QPushButton()
        btn.setIcon(self.get_icon(icon_path="Character/close-one", custom_theme="red"))
        btn.setIconSize(QSize(20, 20))
        btn.setStyleSheet("background: transparent;")
        btn.clicked.connect(self.close_detail)
        btn.setCursor(QCursor(Qt.PointingHandCursor))  # 鼠标手形
        return btn

    def close_detail(self):
        self.detailClose.emit("")
        self.hide()

    def get_icon(self, icon_path, custom_theme=None):
        if custom_theme is not None:
            theme = custom_theme
        else:
            theme = "dark" if self.is_dark else "light"
        return QtGui.QIcon(f"./static/img/IconPark/{theme}/{icon_path}.png")

    def init_ui(self):
        # 主题颜色定义
        if self.is_dark:
            # 深色主题
            self.colors = {
                "main_bg": QColor(34, 34, 34, 240),
                "card_bg": QColor(45, 45, 45),
                "history_bg": QColor(40, 40, 40),
                "history_border": QColor(60, 60, 60),
                "text_primary": QColor(240, 240, 240),
                "text_secondary": QColor(180, 180, 180),
                "text_tertiary": QColor(150, 150, 150),
                "link": QColor(100, 180, 255),
                "border": QColor(80, 80, 80),
                "divider": QColor(60, 60, 60),
                "icon_bg": QColor(60, 60, 60),
                "icon_border": QColor(100, 100, 100),
                "title_bar": QColor(50, 50, 50),
            }
        else:
            # 浅色主题
            self.colors = {
                "main_bg": QColor(255, 255, 255, 240),
                "card_bg": QColor(248, 249, 250),
                "history_bg": QColor(255, 255, 255),
                "history_border": QColor(224, 224, 224),
                "text_primary": QColor(33, 37, 41),
                "text_secondary": QColor(73, 80, 87),
                "text_tertiary": QColor(108, 117, 125),
                "link": QColor(30, 136, 229),
                "border": QColor(206, 212, 218),
                "divider": QColor(224, 224, 224),
                "icon_bg": QColor(240, 240, 240),
                "icon_border": QColor(200, 200, 200),
                "title_bar": QColor(245, 245, 245),
            }

        # 基础样式设置
        self.setGeometry(QtCore.QRect(0, 0, self.parent().width(), self.parent().height()))
        # 主容器
        main_widget = QtWidgets.QWidget(self)
        main_widget.setGeometry(QtCore.QRect(
            int(self.width() * 0.1),
            int(self.height() * 0.05),
            int(self.width() * 0.8),
            int(self.height() * 0.9)
        ))
        main_widget.setStyleSheet(f"""
            background-color: {self.colors["main_bg"].name()};
            border-radius: 15px;
            color: {self.colors["text_primary"].name()};
        """)

        # 主布局
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # 顶部工具栏
        top_layout = QtWidgets.QHBoxLayout()
        close_btn = self.create_close_button()
        top_layout.addItem(
            QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        top_layout.addWidget(close_btn)
        main_layout.addLayout(top_layout)

        # 顶部卡片信息区域
        top_frame = QFrame()
        top_frame.setFrameShape(QFrame.StyledPanel)
        top_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors["card_bg"].name()};
                border-radius: 12px;
                border: 0px solid #FF8D16;
            }}
        """)
        top_layout = QHBoxLayout(top_frame)
        top_layout.setContentsMargins(20, 20, 20, 20)
        top_layout.setSpacing(30)

        # 图标区域
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(120, 120)
        self.icon_label.setAlignment(Qt.AlignCenter)
        top_layout.addWidget(self.icon_label)

        # 右侧文本信息
        info_layout = QVBoxLayout()
        info_layout.setSpacing(12)

        # 标题
        self.title_label = QLabel()
        self.title_label.setStyleSheet(
            f"font-size: 24px; font-weight: bold; color: {self.colors['text_primary'].name()};")
        info_layout.addWidget(self.title_label)

        # 详情
        self.description_label = QLabel()
        self.description_label.setWordWrap(True)
        self.description_label.setStyleSheet(
            f"font-size: 14px; color: {self.colors['text_secondary'].name()}; line-height: 1.5;")
        self.description_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        info_layout.addWidget(self.description_label)

        # 元数据网格
        meta_layout = QHBoxLayout()
        meta_layout.setSpacing(20)

        # 左侧元数据
        left_meta = QVBoxLayout()
        left_meta.setSpacing(8)

        self.version_label = QLabel()  # 当前版本
        self.version_label.setStyleSheet(f"font-size: 13px; color: {self.colors['text_tertiary'].name()};")
        left_meta.addWidget(self.version_label)

        self.size_label = QLabel()  # 文件大小
        self.size_label.setStyleSheet(f"font-size: 13px; color: {self.colors['text_tertiary'].name()};")
        left_meta.addWidget(self.size_label)

        # 右侧元数据
        right_meta = QVBoxLayout()
        right_meta.setSpacing(8)

        self.developer_label = QLabel()  # 开发者
        self.developer_label.setStyleSheet(f"font-size: 13px; color: {self.colors['text_tertiary'].name()};")
        right_meta.addWidget(self.developer_label)

        self.repo_label = QLabel()  # 开源地址
        self.repo_label.setStyleSheet(f"font-size: 13px; color: {self.colors['link'].name()};")
        self.repo_label.setOpenExternalLinks(True)
        right_meta.addWidget(self.repo_label)

        meta_layout.addLayout(left_meta)
        meta_layout.addLayout(right_meta)
        meta_layout.addStretch()
        info_layout.addLayout(meta_layout)

        # 支持大小
        self.support_size_label = QLabel()
        self.support_size_label.setStyleSheet(f"font-size: 13px; color: {self.colors['text_tertiary'].name()};")
        self.support_size_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        info_layout.addWidget(self.support_size_label)

        top_layout.addLayout(info_layout)

        main_layout.addWidget(top_frame)

        # 版本历史区域
        history_frame = QFrame()
        history_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors["history_bg"].name()};
                border-radius: 12px;
                border: 1px solid {self.colors["history_border"].name()};
            }}
        """)
        history_layout = QVBoxLayout(history_frame)
        history_layout.setContentsMargins(0, 0, 0, 0)

        # 版本历史标题
        history_title = QLabel("版本历史")
        history_title.setStyleSheet(f"""
            QLabel {{
                background-color: {self.colors["title_bar"].name()};
                font-size: 18px;
                font-weight: bold;
                color: {self.colors["text_primary"].name()};
                padding: 15px 20px;
                border-bottom: 1px solid {self.colors["divider"].name()};
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
            }}
        """)
        history_layout.addWidget(history_title)

        # 版本历史内容区域
        self.version_browser = QTextBrowser()
        self.version_browser.setStyleSheet(f"""
            QTextBrowser {{
                background-color: transparent;
                border: none;
                padding: 15px 20px;
                font-size: 13px;
                color: {self.colors["text_secondary"].name()};
            }}
            QTextBrowser a {{
                color: {self.colors["link"].name()};
            }}
        """)
        self.version_browser.setOpenExternalLinks(True)
        history_layout.addWidget(self.version_browser)

        main_layout.addWidget(history_frame, 1)  # 添加伸缩因子使版本历史区域可扩展

        # 添加底部留白
        # main_layout.addStretch(1)

    def fetch_card_data(self):
        """请求卡片数据"""
        url = f"{common.BASE_URL}/cardStore/normal/{self.card_id}"
        request = QNetworkRequest(url)
        request.setRawHeader(b"Authorization", self.use_parent.access_token.encode())
        self.network_manager.get(request)

    def handle_response(self, reply):
        """处理网络响应"""
        if reply.error() != QNetworkReply.NoError:
            print(f"Cloud data error: {reply.errorString()}")
            reply.deleteLater()
            return

        try:
            data = json.loads(bytes(reply.readAll()).decode('utf-8'))
            # 确保返回的数据结构正确
            if "data" in data:
                result = data["data"]
                self.parse_card_data(result)
            else:
                print(f"Invalid cloud data structure: {data}")
        except Exception as e:
            print(f"Error parsing cloud data: {str(e)}")

    def parse_card_data(self, data):
        """解析卡片数据并更新UI"""
        try:
            # 设置图标
            self.load_icon(data)

            # 设置文本信息
            self.title_label.setText(data.setdefault("title", "未知标题"))
            self.description_label.setText(data.setdefault("description", "无描述信息"))

            # 设置元数据
            current_version = data.setdefault("currentVersion", {})
            self.version_label.setText(f"最新版本: {current_version.setdefault('version', '未知')}")

            # 转换文件大小
            size_str = "0B"
            if "file" in current_version and current_version["file"] is not None:
                size_bytes = current_version["file"].setdefault("size", 0)
                size_str = self.format_size(size_bytes)
            self.size_label.setText(f"文件大小: {size_str}")

            # 开发者
            developer_title = "未知"
            if "developer" in data and data["developer"] is not None:
                developer_title = data["developer"].setdefault("title", "未知")
            self.developer_label.setText(f"开发者: {developer_title}")

            # 开源地址
            repo_url = data.setdefault("openSourceUrl", "")
            if repo_url:
                self.repo_label.setText(f"开源地址: <a href='{repo_url}'>{repo_url}</a>")
                self.repo_label.show()
            else:
                self.repo_label.setText("开源地址: 未开源")
                self.repo_label.hide()

            # 卡片大小
            if 'supportSizeList' in current_version and len(current_version.setdefault('supportSizeList')) > 0:
                self.support_size_label.setText(
                    f"卡片大小(宽×高): {', '.join(current_version.setdefault('supportSizeList')).replace('_', '×')}")
            else:
                self.support_size_label.setText(f"卡片大小(宽×高): 未知")

            # 生成版本历史Markdown
            self.generate_version_history(data.setdefault("versionHistory", []))

        except Exception as e:
            traceback.print_exc()

    def load_icon(self, data):
        """异步加载图标"""
        # 设置图标背景样式
        self.icon_label.setStyleSheet(f"""
            QLabel {{
                background-color: {self.colors["icon_bg"].name()};
                border-radius: 15px;
                border: 1px solid {self.colors["icon_border"].name()};
            }}
        """)

        # 设置默认图标
        default_icon = QPixmap(
            f"./static/img/IconPark/{'light' if self.is_dark else 'dark'}/Abstract/application-one.png")
        self.icon_label.setPixmap(default_icon.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # 如果有自定义图标URL则加载
        if "cardIcon" not in data or data["cardIcon"] is None:
            return
        card_icon = data["cardIcon"]
        if "url" not in card_icon or card_icon["url"] is None:
            return
        request = QNetworkRequest(card_icon["url"])
        self.network_manager.get(request)

    def generate_version_history(self, versions):
        """生成版本历史的Markdown内容"""
        if not versions or len(versions) == 0:
            self.version_browser.setPlainText("暂无版本历史记录")
            return

        # 处理 createTime 为 None 的情况
        def get_create_time(v):
            time_str = v.get("createTime")
            # 当 createTime 为 None 时返回空字符串
            return time_str if time_str is not None else ""

        # 按创建时间倒序排列（最新版本在最前面）
        versions.sort(key=get_create_time, reverse=True)

        markdown_content = ""

        for idx, version in enumerate(versions):
            # 版本号
            version_num = version.get("version", "未知版本")
            # 文件大小
            size_str = "0B"
            if "file" in version and version["file"] is not None:
                size_bytes = version["file"].setdefault("size", 0)
                size_str = self.format_size(size_bytes)
            # 创建时间
            create_time = version.get("createTime", "未知时间")
            # 更新说明
            description = version.get("description", "无更新说明")

            # 添加版本标题
            markdown_content += f"## 🚀 {version_num}\n\n"

            # 添加元数据
            if create_time:
                markdown_content += f"- **发布日期**: {create_time.split(' ')[0]}\n"
            else:
                markdown_content += f"- **发布日期**: 未知\n"
            markdown_content += f"- **文件大小**: {size_str}\n\n"

            # 添加更新说明
            markdown_content += f"{'无更新说明' if description is None else description}\n\n"

            # 如果不是最后一个版本，添加分隔线
            if idx < len(versions) - 1:
                markdown_content += "---\n\n"

        # 设置Markdown内容
        self.version_browser.setMarkdown(markdown_content)

        # 滚动到顶部
        self.version_browser.moveCursor(QTextCursor.Start)

    def format_size(self, size_bytes):
        """转换文件大小为易读格式"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 ** 2:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 ** 3:
            return f"{size_bytes / (1024 ** 2):.1f} MB"
        else:
            return f"{size_bytes / (1024 ** 3):.1f} GB"