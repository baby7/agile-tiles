from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QApplication
from PySide6.QtCore import Qt, QTimer
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
import socket
import netifaces
from src.module import dialog_module
from src.ui import style_util


class IPInfoPopup(QWidget):

    def __init__(self, parent=None, main_object=None, is_dark=None):
        super().__init__(parent=parent)
        # 初始化
        self.parent = parent
        self.use_parent = main_object
        self.network_manager = QNetworkAccessManager(self)
        # 初始化界面
        self.init_ui()
        # 设置样式
        style_util.set_dialog_control_style(self, is_dark)
        # 获取并显示IP信息
        self.display_ip_info()
        # 延迟获取外网IP，确保界面先显示
        QTimer.singleShot(100, self.get_external_ip)

    def init_ui(self):
        # 主部件和布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(10, 5, 10, 5)

        # 局域网IPv4地址
        ipv4_label = QLabel("局域网IPv4地址：")
        ipv4_label.setStyleSheet("background: transparent;")
        main_layout.addWidget(ipv4_label)

        self.ipv4_display = QLineEdit()
        self.ipv4_display.setReadOnly(True)
        self.ipv4_display.setPlaceholderText("正在获取...")
        self.ipv4_display.setMinimumHeight(30)
        main_layout.addWidget(self.ipv4_display)

        # IPv6地址
        ipv6_label = QLabel("IPv6地址：")
        ipv6_label.setStyleSheet("background: transparent;")
        main_layout.addWidget(ipv6_label)

        self.ipv6_display = QLineEdit()
        self.ipv6_display.setReadOnly(True)
        self.ipv6_display.setPlaceholderText("正在获取...")
        self.ipv6_display.setMinimumHeight(30)
        main_layout.addWidget(self.ipv6_display)

        # 子网掩码
        subnet_label = QLabel("子网掩码：")
        subnet_label.setStyleSheet("background: transparent;")
        main_layout.addWidget(subnet_label)

        self.subnet_display = QLineEdit()
        self.subnet_display.setReadOnly(True)
        self.subnet_display.setPlaceholderText("正在获取...")
        self.subnet_display.setMinimumHeight(30)
        main_layout.addWidget(self.subnet_display)

        # 默认网关
        gateway_label = QLabel("默认网关：")
        gateway_label.setStyleSheet("background: transparent;")
        main_layout.addWidget(gateway_label)

        self.gateway_display = QLineEdit()
        self.gateway_display.setReadOnly(True)
        self.gateway_display.setPlaceholderText("正在获取...")
        self.gateway_display.setMinimumHeight(30)
        main_layout.addWidget(self.gateway_display)

        # 外网IP地址
        external_ip_label = QLabel("外网IP地址：")
        external_ip_label.setStyleSheet("background: transparent;")
        main_layout.addWidget(external_ip_label)

        self.external_ip_display = QLineEdit()
        self.external_ip_display.setReadOnly(True)
        self.external_ip_display.setPlaceholderText("加载中...")
        self.external_ip_display.setMinimumHeight(30)
        main_layout.addWidget(self.external_ip_display)
        main_layout.addStretch()

        # 复制IP信息按钮
        copy_button = QPushButton("复制IP信息")
        copy_button.clicked.connect(self.copy_ip_info)
        copy_button.setMinimumSize(120, 30)
        main_layout.addWidget(copy_button, alignment=Qt.AlignCenter)

        # 弹簧
        main_layout.addStretch()

    def get_ip_info(self):
        """获取本机IP信息"""
        ip_info = {
            'ipv4': '未知',
            'ipv6': '未知',
            'subnet_mask': '未知',
            'default_gateway': '未知'
        }

        try:
            # 获取主机名
            hostname = socket.gethostname()

            # 获取IPv4地址
            try:
                # 获取本机IP地址（排除回环地址）
                ipv4 = socket.gethostbyname(hostname)
                if ipv4.startswith('127.'):
                    # 如果获取到的是回环地址，尝试其他方法
                    ipv4 = self.get_local_ip()
                ip_info['ipv4'] = ipv4
            except:
                ip_info['ipv4'] = self.get_local_ip()

            # 使用netifaces获取更详细的网络信息
            try:
                # 获取默认网关
                gateways = netifaces.gateways()
                if 'default' in gateways and netifaces.AF_INET in gateways['default']:
                    gateway_info = gateways['default'][netifaces.AF_INET]
                    ip_info['default_gateway'] = gateway_info[0]

                # 获取网络接口详细信息
                interfaces = netifaces.interfaces()
                for interface in interfaces:
                    addrs = netifaces.ifaddresses(interface)
                    if netifaces.AF_INET in addrs:
                        for link in addrs[netifaces.AF_INET]:
                            if 'addr' in link and link['addr'] == ip_info['ipv4']:
                                if 'netmask' in link:
                                    ip_info['subnet_mask'] = link['netmask']

                    if netifaces.AF_INET6 in addrs:
                        ipv6_list = []
                        for link in addrs[netifaces.AF_INET6]:
                            addr = link['addr']
                            # 排除回环和链路本地地址
                            if not addr.startswith('fe80::') and not addr.startswith('::1'):
                                # 去除scope id
                                if '%' in addr:
                                    addr = addr.split('%')[0]
                                ip_info['ipv6'] = addr
                                break
                            if not addr.startswith('::1'):
                                ipv6_list.append(addr)
                        if ip_info['ipv6'] == '未知' and ipv6_list:
                            ip_info['ipv6'] = ",".join(ipv6_list)
            except ImportError:
                pass

            # 如果没有安装netifaces，使用简单方法获取IPv6
            if ip_info['ipv6'] == '未知':
                try:
                    ipv6_list = []
                    ipv6_info = socket.getaddrinfo(hostname, None, socket.AF_INET6)
                    for info in ipv6_info:
                        addr = info[4][0]
                        if not addr.startswith('fe80::') and not addr.startswith('::1'):
                            ip_info['ipv6'] = addr
                            break
                        if not addr.startswith('::1'):
                            ipv6_list.append(addr)
                    if ip_info['ipv6'] == '未知' and ipv6_list:
                        ip_info['ipv6'] = ",".join(ipv6_list)
                except Exception as e:
                    print(f"获取IPv6地址时出错: {e}")

        except Exception as e:
            print(f"获取IP信息时出错: {e}")

        return ip_info

    def get_local_ip(self):
        """获取本地IP地址的备用方法"""
        try:
            # 创建一个临时socket连接来获取本地IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return "未知"

    def display_ip_info(self):
        """显示IP信息到界面"""
        try:
            ip_info = self.get_ip_info()

            self.ipv4_display.setText(ip_info['ipv4'])
            self.ipv6_display.setText(ip_info['ipv6'])
            self.subnet_display.setText(ip_info['subnet_mask'])
            self.gateway_display.setText(ip_info['default_gateway'])

        except Exception as e:
            dialog_module.box_information(self.use_parent, "错误", "获取网络信息时出现错误")

    def get_external_ip(self):
        """异步获取外网IP地址"""
        self.external_ip_display.setPlaceholderText("加载中...")

        # 创建网络请求
        url = "http://www.3322.org/dyndns/getip"
        request = QNetworkRequest(url)

        # 发送请求
        self.reply = self.network_manager.get(request)
        self.reply.finished.connect(self.handle_external_ip_response)

    def handle_external_ip_response(self):
        """处理外网IP请求的响应"""
        try:
            if self.reply.error() == QNetworkReply.NoError:
                # 读取响应数据
                data = self.reply.readAll().data().decode('utf-8').strip()
                self.external_ip_display.setText(data)
            else:
                self.external_ip_display.setText("获取失败")
                print(f"获取外网IP失败: {self.reply.errorString()}")
        except Exception as e:
            self.external_ip_display.setText("获取失败")
            print(f"处理外网IP响应时出错: {e}")
        finally:
            self.reply.deleteLater()

    def copy_ip_info(self):
        """复制所有IP信息到剪贴板"""
        ip_info_text = (
            f"局域网IPv4地址: {self.ipv4_display.text() or self.ipv4_display.placeholderText()}\n"
            f"IPv6地址: {self.ipv6_display.text() or self.ipv6_display.placeholderText()}\n"
            f"子网掩码: {self.subnet_display.text() or self.subnet_display.placeholderText()}\n"
            f"默认网关: {self.gateway_display.text() or self.gateway_display.placeholderText()}\n"
            f"外网IP地址: {self.external_ip_display.text() or self.external_ip_display.placeholderText()}"
        )

        clipboard = QApplication.clipboard()
        clipboard.setText(ip_info_text)

        # 显示复制成功的提示
        dialog_module.box_information(self.use_parent, "成功", "IP信息已复制到剪贴板")

    def refresh_theme(self, main_object):
        # 设置样式
        style_util.set_dialog_control_style(self, main_object.is_dark)