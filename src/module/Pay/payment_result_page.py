from PySide6.QtGui import Qt, QFont, QPixmap
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QWidget


class PaymentResultPage(QWidget):
    """支付结果页面组件"""
    # 定义信号：完成按钮点击和重试按钮点击
    completeClicked = Signal()
    retryClicked = Signal()

    def __init__(self, parent=None, is_dark=None):
        super().__init__(parent=parent)
        self.is_dark = is_dark
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 40, 20, 40)
        layout.setSpacing(30)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 结果图标
        self.result_icon = QLabel()
        self.result_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_icon.setMinimumSize(100, 100)
        self.result_icon.setStyleSheet("background: transparent;")
        layout.addWidget(self.result_icon)

        # 结果标题
        self.result_title = QLabel()
        self.result_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        self.result_title.setFont(title_font)
        self.result_title.setStyleSheet("background: transparent;")
        layout.addWidget(self.result_title)

        # 结果描述
        self.result_description = QLabel()
        self.result_description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_font = QFont()
        desc_font.setPointSize(16)
        self.result_description.setFont(desc_font)
        self.result_description.setWordWrap(True)
        self.result_description.setStyleSheet("background: transparent;")
        layout.addWidget(self.result_description)

        # 操作按钮容器
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout.setSpacing(20)

        button_font = QFont()
        button_font.setPointSize(14)
        # 完成按钮
        self.complete_button = QPushButton("完成")
        self.complete_button.setFixedSize(120, 45)
        self.complete_button.setFont(button_font)
        self.complete_button.clicked.connect(self.completeClicked.emit)  # 连接信号
        button_layout.addWidget(self.complete_button)
        # 重试按钮
        self.retry_button = QPushButton("重新支付")
        self.retry_button.setFixedSize(120, 45)
        self.retry_button.setFont(button_font)
        self.retry_button.clicked.connect(self.retryClicked.emit)  # 连接信号
        button_layout.addWidget(self.retry_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def set_result(self, success: bool, message: str = None):
        """设置支付结果页面显示的内容
        :param success: 支付是否成功
        :param message: 自定义消息，如果为空则使用默认消息
        """
        if success:
            self.result_title.setText("支付成功！")
            self.result_title.setStyleSheet(
                "background: transparent;" + ("color: #2ecc71;" if not self.is_dark else "color: #a5d6a7;")
            )
            self.result_description.setText(message or "您的订阅已成功开通，感谢您的支持！")
            # 加载成功图标
            success_icon = QPixmap("./static/img/IconPark/green/Character/check-one.png")  # 使用资源文件中的图标
            if success_icon.isNull():
                success_icon = QPixmap(100, 100)
                success_icon.fill(Qt.GlobalColor.transparent)
            self.result_icon.setPixmap(success_icon)
            # 按钮状态
            self.complete_button.setVisible(True)
            self.retry_button.setVisible(False)
        else:
            self.result_title.setText("支付失败")
            self.result_title.setStyleSheet(
                "background: transparent;" + ("color: #e74c3c;" if not self.is_dark else "color: #ef9a9a;")
            )
            self.result_description.setText(message or "支付未完成，请检查支付状态或重试")
            # 加载失败图标
            failed_icon = QPixmap("./static/img/IconPark/green/Character/close-one.png")  # 使用资源文件中的图标
            if failed_icon.isNull():
                failed_icon = QPixmap(100, 100)
                failed_icon.fill(Qt.GlobalColor.transparent)
            self.result_icon.setPixmap(failed_icon)
            # 按钮状态
            self.complete_button.setVisible(False)
            self.retry_button.setVisible(True)
