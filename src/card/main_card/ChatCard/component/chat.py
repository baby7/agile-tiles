# coding:utf-8
import json

from PySide6.QtCore import Signal, Qt, QUrl, QEasingCurve, QPropertyAnimation
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QApplication, \
    QComboBox, QScrollArea, QSizePolicy

from src.card.main_card.ChatCard.component.ChatBubble.ChatBubble import ChatBubble
from src.card.main_card.ChatCard.component.EnterTextEdit.EnterTextEdit import EnterTextEdit
from src.card.main_card.ChatCard.component.chat_form import Ui_Form
from src.client import common
from src.component.AgileTilesAcrylicWindow.AgileTilesAcrylicWindow import AgileTilesAcrylicWindow
import src.ui.style_util as style_util


class ChatWindow(AgileTilesAcrylicWindow, Ui_Form):
    use_parent = None
    setting_config = None
    setting_signal = Signal(str)
    mode_list = None

    def __init__(self, parent=None, use_parent=None, ai_title=None, ai_actor=None, content=None, icon=None):
        super(ChatWindow, self).__init__(is_dark=use_parent.is_dark, form_theme_mode=use_parent.form_theme_mode,
                                         form_theme_transparency=use_parent.form_theme_transparency)
        self.setupUi(self)
        # 初始化
        self.use_parent = use_parent
        self.ai_title = ai_title
        self.ai_actor = ai_actor        # 角色名称
        self.content = content          # 包含人设和开场白
        self.icon = icon                # 图标
        # 布局初始化
        self.verticalLayout = QVBoxLayout()
        self.widget_base.setLayout(self.verticalLayout)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        # 顶部信息条
        self.info_bar = QLabel()
        self.info_bar.setAlignment(Qt.AlignCenter)
        self.info_bar.setFixedHeight(30)
        self.info_bar.setContentsMargins(5, 0, 5, 0)
        self.info_bar.setStyleSheet("font-weight: bold; font-size: 12px;")
        self.verticalLayout.addWidget(self.info_bar)
        # 设置标题栏
        if ai_actor:
            self.setWindowTitle(f"灵卡面板 - {ai_actor}角色扮演")
        else:
            self.setWindowTitle("灵卡面板 - 智能对话")
        self.titleBar.minBtn.close()
        self.titleBar.maxBtn.close()
        # 添加滚动动画控制器
        self.scroll_anim = None
        # 模型对照表
        self.mode_map = {
            "DeepSeek-V3": { "provider": "deepseek", "model": "deepseek-chat" },
            "Deepseek-R1": { "provider": "deepseek", "model": "deepseek-reasoner" },

            "通义千问-Plus": { "provider": "qwen", "model": "qwen-plus" },
            "通义千问-Turbo": { "provider": "qwen", "model": "qwen-turbo" },
            "通义千问-Max": { "provider": "qwen", "model": "qwen-max" },

            "文心一言-X1-Turbo": { "provider": "ernie", "model": "ernie-x1-turbo-32k" },
            "文心一言-4.5-Turbo": { "provider": "ernie", "model": "ernie-4.5-turbo-128k" },
            "文心一言-4.5-Turbo-VL": { "provider": "ernie", "model": "ernie-4.5-turbo-vl-preview" },

            "豆包-Seed-1.6": { "provider": "doubao", "model": "doubao-seed-1-6-250615" },
            "豆包-Seed-1.6-Thinking": { "provider": "doubao", "model": "doubao-seed-1-6-thinking-250615" },

            "混元-T1": { "provider": "hunyuan", "model": "hunyuan-T1" },
            "混元-TurboS": { "provider": "hunyuan", "model": "hunyuan-TurboS" },
            "混元-Standard": { "provider": "hunyuan", "model": "hunyuan-standard" },

            "讯飞星火4.0-Ultra": { "provider": "spark", "model": "4.0Ultra" },
            "讯飞星火-Max": { "provider": "spark", "model": "generalv3.5" },
            "讯飞星火-Pro": { "provider": "spark", "model": "generalv3" },
            "讯飞星火-Lite": { "provider": "spark", "model": "lite" },
        }
        # 模型选择
        self.mode_list = self.mode_map.keys()
        # 添加历史消息存储
        self.history = []
        # 初始化
        self.init_ui(ai_title)
        # 设置样式
        style_util.set_dialog_control_style(self, self.is_dark)
        # 新增：异常结束原因映射表
        self.finish_reason_map = {
            "length": "输出长度达到限制",
            "content_filter": "内容被过滤",
            "insufficient_system_resource": "资源不足，请求中断"
        }
        # 初始化角色
        self.init_actor(ai_actor, content)
        if ai_actor is not None:
            self.model_selector.hide()

    def init_ui(self, ai_title):
        # 聊天区域
        self.chat_scroll = QScrollArea()
        self.chat_scroll.setWidgetResizable(True)
        self.chat_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.chat_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.chat_scroll.setStyleSheet(style_util.scroll_bar_style)
        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setAlignment(Qt.AlignTop)
        self.chat_layout.setSpacing(5)
        self.chat_layout.setContentsMargins(10, 10, 10, 10)
        self.chat_scroll.setWidget(self.chat_container)
        self.verticalLayout.addWidget(self.chat_scroll)

        # 输入区域
        input_widget = QWidget()
        input_widget.setMaximumHeight(120)
        input_widget.setMinimumHeight(80)

        main_input_layout = QHBoxLayout(input_widget)
        main_input_layout.setContentsMargins(10, 10, 10, 10)

        self.input_field = EnterTextEdit()
        self.input_field.setMaximumHeight(100)
        self.input_field.setPlaceholderText("输入消息...(Shift+Enter 换行/Enter发送)")
        self.input_field.setAcceptRichText(False)
        # 连接回车信号到发送方法
        self.input_field.returnPressed.connect(self.send_message)
        main_input_layout.addWidget(self.input_field, 4)

        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(5)

        self.model_selector = QComboBox()
        self.model_selector.setMinimumHeight(40)
        self.model_selector.addItems(self.mode_list)
        right_layout.addWidget(self.model_selector)

        self.send_btn = QPushButton("发送")
        self.send_btn.setMinimumHeight(40)
        self.send_btn.clicked.connect(self.send_message)
        right_layout.addWidget(self.send_btn)

        main_input_layout.addWidget(right_container, 1)
        self.verticalLayout.addWidget(input_widget)

        # 头像
        self.user_avatar = self.create_avatar(is_user=True, is_vip=self.use_parent.is_vip)
        self.bot_avatar_map = {
            "deepseek": self.create_avatar(is_user=False, provider="deepseek"),
            "qwen": self.create_avatar(is_user=False, provider="qwen"),
            "ernie": self.create_avatar(is_user=False, provider="ernie"),
            "doubao": self.create_avatar(is_user=False, provider="doubao"),
            "hunyuan": self.create_avatar(is_user=False, provider="hunyuan"),
            "spark": self.create_avatar(is_user=False, provider="spark"),
        }
        # 透明占位头像
        self.transparent_avatar = self.create_transparent_avatar()

        # 网络管理器
        self.network_manager = QNetworkAccessManager(self)

        # SSE相关状态
        self.current_reply_bubble = None  # 最终回复气泡
        self.current_reasoning_bubble = None  # 思考过程气泡
        self.current_reply = ""
        self.current_reasoning = ""
        self.sse_reply = None
        self.buffer = bytearray()
        self.current_ai_message_container = None  # 记录当前AI消息容器
        self.stop_button = None  # 结束对话按钮
        self.stop_response_tag = False

        # 初始化模型选择
        if ai_title == "DeepSeek":
            self.model_selector.setCurrentText("Deepseek-R1")
        elif ai_title == "通义千问":
            self.model_selector.setCurrentText("通义千问-Max")
        elif ai_title == "文心一言":
            self.model_selector.setCurrentText("文心一言-X1-Turbo")
        elif ai_title == "混元":
            self.model_selector.setCurrentText("混元-Pro")
        elif ai_title == "讯飞星火":
            self.model_selector.setCurrentText("讯飞星火4.0-Ultra")
        elif ai_title == "豆包":
            self.model_selector.setCurrentText("豆包-Seed-1.6-Thinking")
        else:
            self.model_selector.setCurrentText("Deepseek-V3")

        # 设置输入焦点
        self.input_field.setFocus()

        # 填充部分信息
        self.set_info_bar(0)
        # 请求并更新对话次数信息
        self.update_call_count()

    def init_actor(self, ai_actor, content):
        # 角色设定，添加开场白
        if ai_actor and content:
            # 获取当前选中的模型对应的provider
            model_title = self.model_selector.currentText()
            provider = self.mode_map[model_title]["provider"]

            # 添加系统消息（角色设定）
            self.history.append({
                "role": "system",
                "content": content["persona"]
            })

            # 添加开场白并显示
            self.add_message(content["prologue"], is_user=False, provider=provider, is_actor=True)

            # 将开场白添加到历史记录
            self.history.append({
                "role": "assistant",
                "content": content["prologue"]
            })

    def update_call_count(self):
        """请求并更新对话次数信息"""
        url = QUrl(common.BASE_URL + "/chat/normal/todayCalls")
        request = QNetworkRequest(url)
        request.setRawHeader(b"Authorization", bytes(self.use_parent.access_token, "utf-8"))

        # 使用临时网络管理器获取调用次数
        temp_manager = QNetworkAccessManager(self)
        reply = temp_manager.get(request)

        def handle_reply():
            if reply.error() == QNetworkReply.NoError:
                data = reply.readAll()
                json_data = json.loads(str(data, 'utf-8'))
                today_calls = json_data.get("data", 0)

                # 根据会员状态显示不同信息
                self.set_info_bar(today_calls)
            else:
                error = reply.errorString()
                print(f"获取调用次数失败: {error}")
                self.info_bar.setText("获取对话次数信息失败")
                self.info_bar.setStyleSheet(
                    "background-color: rgba(255, 255, 255, 0.1); "
                    "border-radius: 5px; "
                    "color: orange; "
                    "font-weight: bold; "
                    "font-size: 12px;"
                )

            reply.deleteLater()

        reply.finished.connect(handle_reply)

    def set_info_bar(self, today_calls):
        # 根据会员状态显示不同信息
        if self.use_parent.is_vip:
            text = f"会员用户无对话次数限制，今天已使用{today_calls}次"
            color = "rgba(4, 115, 247, 0.8)"
        else:
            text = f"非会员每天限制3次对话，今天已使用{today_calls}次"
            color = "rgba(243, 207, 19, 0.8)"

        # 根据主题设置背景
        if self.is_dark:
            bg_color = "rgba(255, 255, 255, 0.1)"
        else:
            bg_color = "rgb(255, 255, 255)"

        # 设置信息条样式和内容
        self.info_bar.setText(text)
        self.info_bar.setStyleSheet(
            f"background-color: {bg_color}; "
            f"border-radius: 5px; "
            f"color: {color}; "
            f"font-weight: bold; "
            f"font-size: 12px;"
        )

    def smooth_scroll_to(self, target_value, duration=500):
        """平滑滚动到指定位置"""
        scrollbar = self.chat_scroll.verticalScrollBar()
        current_value = scrollbar.value()

        # 如果已经在目标位置，直接返回
        if current_value == target_value:
            return

        # 取消正在进行的动画
        if self.scroll_anim and self.scroll_anim.state() == QPropertyAnimation.Running:
            self.scroll_anim.stop()

        # 创建新动画
        self.scroll_anim = QPropertyAnimation(scrollbar, b"value")
        self.scroll_anim.setDuration(duration)
        self.scroll_anim.setStartValue(current_value)
        self.scroll_anim.setEndValue(target_value)
        self.scroll_anim.setEasingCurve(QEasingCurve.OutQuad)  # 使用平滑的缓动曲线
        self.scroll_anim.start()

    def scroll_to_bottom(self, must_scroll=False):
        """平滑滚动到底部"""
        scrollbar = self.chat_scroll.verticalScrollBar()

        # 如果滚动条距离底部太远就不滚动
        if not must_scroll and (scrollbar.maximum() - scrollbar.value()) > 50:
            return

        # 使用平滑滚动动画
        self.smooth_scroll_to(scrollbar.maximum())

    def resizeEvent(self, event):
        super().resizeEvent(event)

        # 使用动画更新气泡宽度
        self.update_bubble_widths_with_animation()

    def update_bubble_widths_with_animation(self, duration=500):
        """使用动画更新气泡宽度"""
        for i in range(self.chat_layout.count()):
            widget = self.chat_layout.itemAt(i).widget()
            if widget:
                for child in widget.findChildren(ChatBubble):
                    if child.parent() and child.parent().parent():
                        max_width = int(child.parent().parent().width() * 0.95)

                        # 使用动画平滑过渡
                        if child.maximumWidth() != max_width:
                            anim = QPropertyAnimation(child, b"maximumWidth")
                            anim.setDuration(duration)
                            anim.setStartValue(child.maximumWidth())
                            anim.setEndValue(max_width)
                            anim.setEasingCurve(QEasingCurve.OutQuad)
                            anim.start()

    def create_avatar(self, is_user=False, is_vip=False, provider="deepseek"):
        if is_user:
            if is_vip:
                return QPixmap("./static/img/user/head_vip.png")
            else:
                return QPixmap("./static/img/user/head_normal.png")
        else:
            # 判断是否有自定义图标
            if self.icon is not None and "png:" in self.icon:
                image_end_path = self.icon.replace("png:", "")
                return QPixmap("static/img/IconPark/png/" + image_end_path)
            image_path = "./static/img/IconPark/svg/Custom/" + provider + ".svg"
            if self.is_dark:
                return self.use_parent.toolkit.image_util.load_light_svg(image_path)
            else:
                return self.use_parent.toolkit.image_util.load_dark_svg(image_path)

    def create_transparent_avatar(self):
        """创建透明占位头像"""
        pixmap = QPixmap(40, 40)
        pixmap.fill(Qt.transparent)
        return pixmap

    def add_message(self, text, is_user, is_reasoning=False, parent_container=None, provider="deepseek", is_actor=False):
        """
        添加消息气泡
        :param text: 消息文本
        :param is_user: 是否是用户消息
        :param is_reasoning: 是否是思考气泡
        :param parent_container: 父容器（用于AI消息的思考和回复气泡共享同一容器）
        :param provider: ai厂商
        :param is_actor: 是否是角色，角色需要开场白
        :return: 气泡控件
        """
        # 如果是AI消息且没有指定父容器，创建新的消息容器
        if not is_user and not parent_container:
            # 创建消息行容器
            parent_container = QWidget()
            container_layout = QHBoxLayout(parent_container)
            container_layout.setContentsMargins(0, 0, 0, 0)
            container_layout.setSpacing(10)

            # 创建头像标签
            avatar_label = QLabel()
            avatar_label.setPixmap(self.bot_avatar_map[provider])
            avatar_label.setFixedSize(40, 40)
            avatar_label.setScaledContents(True)
            avatar_label.setStyleSheet("""
            QLabel {
                background-color: rgb(255, 255, 255);
                border: 0px solid white;
                border-radius: 5px;
            }""")

            # 创建气泡容器（垂直布局，用于放置思考气泡和回复气泡）
            bubble_container = QWidget()
            bubble_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            bubble_layout = QVBoxLayout(bubble_container)
            bubble_layout.setContentsMargins(0, 0, 0, 0)
            bubble_layout.setSpacing(2)  # 减小气泡间距

            # 创建角色的开场白气泡
            if is_actor:
                bubble = ChatBubble(
                    text=text,
                    is_user=is_user,
                    is_dark=self.is_dark,
                    is_reasoning=is_reasoning
                )
                bubble_layout.addWidget(bubble)

            # 设置对齐方式
            container_layout.addWidget(avatar_label, 1, alignment=Qt.AlignTop)
            container_layout.addWidget(bubble_container, 3)
            container_layout.addStretch(1)

            # 添加到聊天区域
            self.chat_layout.addWidget(parent_container)
            self.current_ai_message_container = parent_container

            if is_actor:
                # 返回气泡容器用于后续添加气泡
                return bubble_container, parent_container

            # 新增：创建底部布局（包含停止按钮和结束提示标签）
            bottom_container = QWidget()
            bottom_container.setFixedHeight(30)  # 固定高度
            bottom_layout = QHBoxLayout(bottom_container)
            bottom_layout.setContentsMargins(40, 0, 40, 0)  # 左右边距
            bottom_layout.setSpacing(5)

            # 左侧占位弹簧
            bottom_layout.addStretch(3)

            # 新增：结束提示标签
            self.finish_reason_label = QLabel()
            self.finish_reason_label.setVisible(False)  # 初始不可见
            self.finish_reason_label.setAlignment(Qt.AlignCenter)
            self.finish_reason_label.setStyleSheet("""
                QLabel {
                    background-color: rgba(255, 100, 100, 0.15);
                    border-radius: 5px;
                    padding: 2px 8px;
                    font-size: 10px;
                    color: #ff3333;
                    font-weight: bold;
                }
            """)
            bottom_layout.addWidget(self.finish_reason_label, 1)

            # 结束对话按钮
            self.stop_button = QPushButton()
            self.stop_button.setIcon(QIcon("./static/img/IconPark/red/Character/close-one.png"))
            self.stop_button.setText("结束对话")
            self.stop_button.setToolTip("结束回答")
            self.stop_button.setFixedHeight(24)
            self.stop_button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 100, 100, 0.2);
                    border: none;
                    border-radius: 12px;
                    padding: 2px 8px;
                    font-size: 10px;
                    color: #ff3333;
                }
                QPushButton:hover {
                    background-color: rgba(255, 100, 100, 0.3);
                }
                QPushButton:pressed {
                    background-color: rgba(255, 100, 100, 0.4);
                }
            """)
            self.stop_button.clicked.connect(self.stop_response)
            bottom_layout.addWidget(self.stop_button, 1, alignment=Qt.AlignRight)

            # 右侧占位弹簧
            bottom_layout.addStretch(3)

            # 添加到底部布局
            self.chat_layout.addWidget(bottom_container)
            self.scroll_to_bottom(must_scroll=True)

            # 返回气泡容器用于后续添加气泡
            return bubble_container, parent_container

        # 如果是用户消息，创建完整的消息容器
        elif is_user:
            # 创建消息行容器
            message_container = QWidget()
            container_layout = QHBoxLayout(message_container)
            container_layout.setContentsMargins(0, 0, 0, 0)
            container_layout.setSpacing(10)

            # 创建头像标签
            avatar_label = QLabel()
            avatar_label.setPixmap(self.user_avatar)
            avatar_label.setFixedSize(40, 40)
            avatar_label.setScaledContents(True)
            avatar_label.setStyleSheet("""
            QLabel {
                background-color: rgb(255, 255, 255);
                border: 0px solid white;
                border-radius: 5px;
            }""")

            # 创建气泡容器
            bubble_container = QWidget()
            bubble_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            bubble_layout = QVBoxLayout(bubble_container)
            bubble_layout.setContentsMargins(0, 0, 0, 0)
            bubble_layout.setSpacing(0)

            # 创建气泡
            bubble = ChatBubble(
                text=text,
                is_user=is_user,
                is_dark=self.is_dark,
                is_reasoning=is_reasoning
            )
            bubble_layout.addWidget(bubble)

            # 计算最大宽度
            max_width = int(QApplication.primaryScreen().size().width() * 0.8)
            bubble.setMaximumWidth(max_width)

            # 设置对齐方式
            container_layout.addStretch(1)
            container_layout.addWidget(bubble_container, 3)
            container_layout.addWidget(avatar_label, 1, alignment=Qt.AlignTop)

            self.chat_layout.addWidget(message_container)
            self.scroll_to_bottom()

            return bubble, message_container

        # 如果是AI消息的子气泡（思考或回复）
        else:
            # 获取父容器中的气泡布局
            bubble_container = parent_container.layout().itemAt(1).widget().layout()

            # 创建气泡
            bubble = ChatBubble(
                text=text,
                is_user=is_user,
                is_dark=self.is_dark,
                is_reasoning=is_reasoning
            )

            # 计算最大宽度
            max_width = int(QApplication.primaryScreen().size().width() * 0.8)
            bubble.setMaximumWidth(max_width)

            # 思考气泡放在顶部，回复气泡放在底部
            if is_reasoning:
                bubble_container.insertWidget(0, bubble)
            else:
                bubble_container.addWidget(bubble)

            self.scroll_to_bottom(must_scroll=True)
            return bubble, parent_container

    def send_message(self):
        text = self.input_field.toPlainText().strip()
        if not text:
            return

        # 禁用控件
        self.set_controls_enabled(False)

        # 获取模型
        model_title = self.model_selector.currentText()
        provider = self.mode_map[model_title]["provider"]
        model = self.mode_map[model_title]["model"]

        self.input_field.clear()
        self.add_message(text, True)

        # 将用户消息添加到历史记录
        self.history.append({"role": "user", "content": text})

        # 创建AI消息容器（包含气泡布局）
        bubble_container, message_container = self.add_message("", False, provider=provider)
        self.current_ai_message_container = message_container

        # 在容器中添加实际回复气泡（初始状态）
        self.current_reply_bubble, _ = self.add_message("▌", False, is_reasoning=False,
                                                        parent_container=message_container, provider=provider)
        self.current_reply_bubble.setVisible(True)
        self.current_reply = ""

        # 初始状态不创建思考气泡
        self.current_reasoning_bubble = None
        self.current_reasoning = ""

        self.buffer = bytearray()

        # 取消任何正在进行的请求
        if self.sse_reply and self.sse_reply.isRunning():
            self.sse_reply.abort()
            self.sse_reply.deleteLater()

        # 准备SSE请求
        url = QUrl(common.BASE_URL + "/chat/normal/stream")
        request = QNetworkRequest(url)
        request.setRawHeader(b"Authorization", bytes(self.use_parent.access_token, "utf-8"))
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")

        # 创建请求数据
        request_data = {
            "messages": self.history,
            "provider": provider,
            "model": model
        }
        data = json.dumps(request_data)
        data_str = data.encode('utf-8')
        print("请求数据:", request_data)

        # 发送POST请求
        self.sse_reply = self.network_manager.post(request, data_str)

        # 连接信号
        self.sse_reply.readyRead.connect(self.handle_ready_read)
        self.sse_reply.finished.connect(self.handle_finished)
        self.sse_reply.errorOccurred.connect(self.handle_error)

    def handle_ready_read(self):
        if not self.sse_reply:
            return
        # 确保停止按钮可见
        if self.stop_button:
            self.stop_button.setVisible(True)

        self.buffer.extend(self.sse_reply.readAll())

        while b'\n' in self.buffer:
            line_end = self.buffer.index(b'\n')
            line = bytes(self.buffer[:line_end]).decode('utf-8', errors='ignore').strip()
            del self.buffer[:line_end + 1]

            if line.startswith("data:"):
                is_end = False
                try:
                    json_data = json.loads(line[5:].strip())
                    content = json_data.get("content", "")
                    reasoning_content = json_data.get("reasoningContent", "")
                    is_finished = json_data.get("isFinished", False)
                    # 新增：获取结束原因
                    finish_reason = json_data.get("finishReason", "")

                    # 1. 接收到思考信息：展示思考气泡，隐藏实际回复气泡
                    if reasoning_content and not self.current_reasoning_bubble:
                        # 创建思考气泡（位于回复气泡上方）
                        self.current_reasoning_bubble, _ = self.add_message("▌", False, is_reasoning=True,
                                                                            parent_container=self.current_ai_message_container)
                        self.current_reasoning = "思考:\n"
                        self.current_reply_bubble.setVisible(False)  # 隐藏回复气泡

                    # 更新思考气泡
                    if reasoning_content and self.current_reasoning_bubble:
                        self.current_reasoning += reasoning_content
                        display_text = self.current_reasoning + ("▌" if not is_finished else "")
                        self.current_reasoning_bubble.setMarkdown(display_text)
                        self.current_reasoning_bubble.adjustSize()

                    # 2. 接收到实际回复内容：展示实际回复气泡，如果思考气泡没有内容就隐藏思考气泡
                    if content and self.current_reasoning_bubble:
                        # 显示回复气泡
                        self.current_reply_bubble.setVisible(True)
                        # 如果思考气泡没有内容就隐藏思考气泡
                        if self.current_reasoning == "":
                            self.current_reasoning_bubble.setVisible(False)

                    # 更新回复气泡
                    if content and self.current_reply_bubble:
                        self.current_reply += content
                        display_text = self.current_reply + ("▌" if not is_finished else "")
                        self.current_reply_bubble.setMarkdown(display_text)
                        self.current_reply_bubble.adjustSize()

                    # 滚动到底部
                    self.scroll_to_bottom()

                    # 如果结束则重置状态并将AI回复添加到历史记录
                    if is_finished:
                        is_end = True
                        # 移除气泡中的光标
                        if self.current_reasoning_bubble:
                            self.current_reasoning_bubble.setMarkdown(self.current_reasoning)
                        if self.current_reply_bubble:
                            self.current_reply_bubble.setMarkdown(self.current_reply)

                        # 将AI回复添加到历史记录
                        if self.current_reply:
                            self.history.append({
                                "role": "system",
                                "content": self.current_reply
                            })

                        # 新增：处理结束原因提示
                        self.handle_finish_reason(finish_reason)

                        # 重置状态
                        self.current_reasoning_bubble = None
                        self.current_reply_bubble = None
                        self.current_ai_message_container = None
                        self.current_reasoning = ""
                        self.current_reply = ""
                except json.JSONDecodeError:
                    print(f"JSON解析错误: {line}")
                if is_end:
                    break

    # 新增：处理结束原因提示的方法
    def handle_finish_reason(self, finish_reason):
        """根据结束原因显示提示标签"""
        if not finish_reason or finish_reason == "stop":
            # 正常结束，隐藏标签
            self.finish_reason_label.setVisible(False)
            return

        # 异常结束，显示提示
        reason_text = self.finish_reason_map.get(finish_reason, "未知错误")
        self.finish_reason_label.setText(f"⚠️ {reason_text}")
        self.finish_reason_label.setVisible(True)

        # 隐藏停止按钮（因为已经结束了）
        if self.stop_button:
            self.stop_button.setVisible(False)

    def handle_finished(self):
        # 重新启用控件
        self.set_controls_enabled(True)
        # 隐藏停止按钮
        if self.stop_button:
            self.stop_button.setVisible(False)

        try:
            if self.sse_reply:
                if self.buffer:
                    try:
                        line = bytes(self.buffer).decode('utf-8', errors='ignore').strip()
                        if line.startswith("data:"):
                            json_data = json.loads(line[5:].strip())
                            content = json_data.get("content", "")
                            reasoning_content = json_data.get("reasoningContent", "")
                            is_finished = json_data.get("isFinished", False)

                            # 更新气泡
                            if reasoning_content and self.current_reasoning_bubble:
                                self.current_reasoning += reasoning_content
                                self.current_reasoning_bubble.setMarkdown(self.current_reasoning)

                            if content and self.current_reply_bubble:
                                self.current_reply += content
                                self.current_reply_bubble.setMarkdown(self.current_reply)

                            # 处理未完成的回复
                            if is_finished and self.current_reply:
                                self.history.append({
                                    "role": "system",
                                    "content": self.current_reply
                                })
                    except json.JSONDecodeError:
                        print("完成时JSON解析错误")

                # 确保重置状态
                if self.current_reasoning_bubble:
                    self.current_reasoning_bubble.setMarkdown(self.current_reasoning)

                if self.current_reply_bubble:
                    self.current_reply_bubble.setMarkdown(self.current_reply)

                    # 确保将最终回复添加到历史记录
                    if self.current_reply:
                        self.history.append({
                            "role": "system",
                            "content": self.current_reply
                        })

                self.current_reasoning_bubble = None
                self.current_reply_bubble = None
                self.current_ai_message_container = None
                self.current_reasoning = ""
                self.current_reply = ""

                # 设置输入焦点
                self.input_field.setFocus()

                # 清理资源
                self.sse_reply.deleteLater()
                self.sse_reply = None
                self.buffer = bytearray()
        except Exception as e:
            print(f"处理完成时错误: {e}")

        # 更新对话次数信息
        self.update_call_count()

    def handle_error(self, code):
        # 重新启用控件
        self.set_controls_enabled(True)
        # 停止响应的tag
        if self.stop_response_tag:
            return
        # 只有真正的网络错误才显示错误信息
        try:
            if self.sse_reply:
                # 尝试读取响应体获取错误详情
                error_data = self.sse_reply.readAll()
                try:
                    # 解析JSON响应
                    json_data = json.loads(bytes(self.buffer).decode('utf-8'))
                    cloud_error = json_data.get("error", "未知错误")
                    if cloud_error == "Too Many Requests":
                        cloud_error = "今日使用次数已达上限"
                except:
                    # 解析失败则使用HTTP错误信息
                    cloud_error = self.sse_reply.errorString()

                # 更新气泡显示错误信息
                if self.current_reply_bubble:
                    error_msg = f"**网络错误**\n```\n{cloud_error}\n```"
                    self.current_reply_bubble.setMarkdown(error_msg)

                if self.current_reasoning_bubble:
                    self.current_reasoning_bubble.setMarkdown("请求失败")

                # 移除最后一条用户消息（因为请求失败）
                if self.history and self.history[-1]["role"] == "user":
                    self.history.pop()

                self.current_reasoning_bubble = None
                self.current_reply_bubble = None
                self.current_ai_message_container = None
                self.current_reasoning = ""
                self.current_reply = ""

                self.sse_reply.deleteLater()
                self.sse_reply = None
                self.buffer = bytearray()
        except Exception as e:
            print(f"处理错误时发生错误: {e}")

        # 隐藏停止按钮
        if self.stop_button:
            self.stop_button.setVisible(False)

    def stop_response(self):
        """停止当前AI回答"""
        self.stop_response_tag = True
        try:
            # 重新启用控件
            self.set_controls_enabled(True)

            if self.sse_reply and self.sse_reply.isRunning():
                # 终止SSE请求
                self.sse_reply.abort()

                # 获取当前内容
                current_content = ""

                # 更新气泡显示已停止（不显示错误信息）
                if self.current_reply_bubble:
                    # 移除光标并添加停止提示
                    current_content = self.current_reply.replace("▌", "")
                    self.current_reply_bubble.setMarkdown(current_content + "\n\n**回答已停止**")

                # 如果有思考气泡，也更新其内容
                if self.current_reasoning_bubble:
                    current_reasoning = self.current_reasoning.replace("▌", "")
                    self.current_reasoning_bubble.setMarkdown(current_reasoning)

                # 将已接收的内容添加到历史记录（如果内容不为空）
                if self.current_reply.strip():
                    self.history.append({
                        "role": "system",
                        "content": current_content
                    })

                # 新增：用户手动停止时不显示结束原因提示
                self.finish_reason_label.setVisible(False)

                # 重置状态
                self.current_reasoning_bubble = None
                self.current_reply_bubble = None
                self.current_ai_message_container = None
                self.current_reasoning = ""
                self.current_reply = ""

                # 清理资源
                if self.sse_reply is not None:
                    self.sse_reply.deleteLater()
                self.sse_reply = None
                self.buffer = bytearray()

                # 隐藏停止按钮
                if self.stop_button:
                    self.stop_button.setVisible(False)

                # 设置输入焦点
                self.input_field.setFocus()

                # 更新对话次数信息
                self.update_call_count()
        except Exception as e:
            print(f"停止响应时发生错误：{e}")
            # 重新启用控件
            self.set_controls_enabled(True)

        # 停止响应
        self.stop_response_tag = True

    def set_controls_enabled(self, enabled):
        """设置输入控件启用状态"""
        self.send_btn.setEnabled(enabled)
        self.model_selector.setEnabled(enabled)
        self.input_field.setEnabled(enabled)
        # 根据状态设置输入框提示文本
        if enabled:
            self.input_field.setPlaceholderText("输入消息...(Shift+Enter 换行/Enter发送)")
        else:
            self.input_field.setPlaceholderText("AI正在思考中...")

    def closeEvent(self, event):
        # 清理动画
        if self.scroll_anim:
            self.scroll_anim.stop()
            self.scroll_anim.deleteLater()
        super().closeEvent(event)