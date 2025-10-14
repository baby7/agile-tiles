from PySide6.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton, QTextEdit
from PySide6.QtCore import Qt
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
import json

from src.ui import style_util


class IPLocationQueryPopup(QWidget):
    """IP归属地查询工具"""

    def __init__(self, parent=None, main_object=None, is_dark=None):
        super().__init__(parent=parent)
        # 初始化
        self.parent = parent
        self.use_parent = main_object
        self.network_manager = QNetworkAccessManager()
        self.network_manager.finished.connect(self.on_network_reply)

        # 初始化界面
        self.init_ui()
        # 设置样式
        style_util.set_dialog_control_style(self, is_dark)

    def init_ui(self):
        """初始化用户界面"""
        # 主部件和布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # IP地址输入
        ip_label = QLabel("IP地址:")
        ip_label.setStyleSheet("background: transparent;")
        main_layout.addWidget(ip_label)

        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("输入要查询的IP地址，留空则查询本机IP")
        main_layout.addWidget(self.ip_input)

        # 查询按钮
        self.query_button = QPushButton("查询")
        self.query_button.clicked.connect(self.on_query_clicked)
        main_layout.addWidget(self.query_button)

        # 结果显示区域
        result_label = QLabel("查询结果:")
        result_label.setStyleSheet("background: transparent;")
        main_layout.addWidget(result_label)

        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setMaximumHeight(200)
        main_layout.addWidget(self.result_display)

        # 说明标签
        note_label = QLabel("提示: 使用 ip-api.com 的免费API进行查询")
        note_label.setStyleSheet("font-size: 12px; color: #666; background: transparent;")
        note_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(note_label)

    def on_query_clicked(self):
        """查询按钮点击事件"""
        ip_address = self.ip_input.text().strip()

        # 禁用按钮防止重复点击
        self.query_button.setEnabled(False)
        self.query_button.setText("查询中...")
        self.result_display.setPlainText("正在查询，请稍候...")

        # 构建请求URL
        if ip_address:
            url = f"http://ip-api.com/json/{ip_address}?lang=zh-CN"
        else:
            url = "http://ip-api.com/json/?lang=zh-CN"

        # 发送网络请求
        request = QNetworkRequest(url)
        request.setHeader(QNetworkRequest.UserAgentHeader, "Mozilla/5.0")
        self.network_manager.get(request)

    def on_network_reply(self, reply):
        """处理网络回复"""
        # 重新启用查询按钮
        self.query_button.setEnabled(True)
        self.query_button.setText("查询")

        # 检查错误
        if reply.error():
            self.result_display.setPlainText(f"网络错误: {reply.errorString()}")
            reply.deleteLater()
            return

        # 读取和解析数据
        data = reply.readAll().data().decode('utf-8')
        reply.deleteLater()

        try:
            result = json.loads(data)
            self.display_result(result)
        except json.JSONDecodeError:
            self.result_display.setPlainText("解析响应数据失败")

    def display_result(self, result):
        """显示查询结果"""
        if result.get("status") == "success":
            country = result.get("country", "未知")
            region = result.get("regionName", "未知")
            city = result.get("city", "未知")
            isp = result.get("isp", "未知")
            org = result.get("org", "未知")
            query_ip = result.get("query", "未知")
            timezone = result.get("timezone", "未知")
            lat = result.get("lat", "未知")
            lon = result.get("lon", "未知")

            result_text = f"""IP地址: {query_ip}
国家: {country}
地区: {region}
城市: {city}
ISP: {isp}
组织: {org}
时区: {timezone}
经纬度: {lat}, {lon}"""

            self.result_display.setPlainText(result_text)
        else:
            error_message = result.get("message", "查询失败")
            self.result_display.setPlainText(f"查询失败: {error_message}")

    def refresh_theme(self, main_object):
        """刷新主题"""
        style_util.set_dialog_control_style(self, main_object.is_dark)