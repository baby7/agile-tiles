import os
import socket
import traceback
from io import BytesIO
from PySide6.QtCore import Qt, QThread, QRect, QTimer
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget,
                               QListWidgetItem, QFileDialog, QTabWidget, QFrame, QApplication, QSpinBox)
from src.card.MainCardManager.MainCard import MainCard
from src.constant import data_save_constant
from src.ui import style_util
from src.util import browser_util


class IpnCard(MainCard):
    """局域网文件传输卡片"""

    title = "局域网文件传输"
    name = "IpnCard"
    support_size_list = ["Big"]

    # 只读参数
    x = None
    y = None
    size = None
    theme = None
    width = 0
    height = 0
    fillet_corner = 0

    # 可使用
    card = None
    data = None
    toolkit = None
    logger = None

    # 可调用
    save_data_func = None

    # 默认端口
    DEFAULT_PORT = 6688

    def __init__(self, main_object=None, parent=None, theme=None, card=None, cache=None, data=None,
                 toolkit=None, logger=None, save_data_func=None):
        super().__init__(main_object=main_object, parent=parent, theme=theme, card=card, cache=cache, data=data,
                         toolkit=toolkit, logger=logger, save_data_func=save_data_func)
        # 初始化数据(这里不直接使用setdefault是为了避免每次初始化都调用get_download_path函数)
        if "ipnData" not in self.cache:
            self.cache["ipnData"] = {"files": [], "texts": [], "port": self.DEFAULT_PORT, "uploadDir": self.get_download_path()}
        self.ipn_data = self.cache.get("ipnData")
        # 获取端口
        self.port = self.ipn_data["port"]
        # 获取用户主目录
        self.upload_dir = self.ipn_data["uploadDir"]
        # 其他
        self.server = None
        self.server_thread = None
        self.server_worker = None

    def clear(self):
        """清理资源"""
        try:
            pass
        except Exception as e:
            print(e)
        super().clear()

    def init_ui(self):
        """初始化UI"""
        super().init_ui()

        # 创建中央部件和布局
        central_widget = QWidget(self.card)
        central_widget.setGeometry(QRect(0, 0, self.card.width(), self.card.height()))
        central_widget.setStyleSheet("background-color: transparent; border: none;")
        layout = QVBoxLayout(central_widget)
        # 创建服务控制区域
        self.create_service_control(layout)
        # 创建文件管理区域
        self.create_file_management(layout)
        # 状态栏布局
        status_widget = QWidget()
        status_layout = QHBoxLayout(status_widget)
        status_layout.setContentsMargins(15, 0, 0, 0)
        # 状态标签（左对齐）
        self.bottom_status_label = QLabel("")
        status_layout.addWidget(self.bottom_status_label)
        layout.addWidget(status_widget)
        # 修改状态栏
        self.bottom_status_label.setText("就绪")

    def get_local_ip(self):
        """获取本机局域网IP地址"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"

    def get_download_path(self):
        # 获取用户主目录
        home_dir = os.path.expanduser("~")
        print("获取用户主目录成功:", home_dir)
        # 1. os.path.expanduser("~") + "Downloads"
        print("1.尝试使用用户下载目录")
        upload_dir = os.path.join(home_dir, "Downloads")
        make_status = self.make_download_path(upload_dir, create=False)
        if make_status:
            print("1.获取用户下载目录成功:", upload_dir)
            return upload_dir
        # 2. os.path.expanduser("~") + "Documents"
        print("2.尝试使用用户文档目录")
        upload_dir = os.path.join(home_dir, "Documents")
        make_status = self.make_download_path(upload_dir, create=False)
        if make_status:
            print("2.尝试使用用户文档目录成功:", upload_dir)
            return upload_dir
        # 3. os.path.expanduser("~") + 软件名称 + "ipn_uploads"
        print("3.尝试使用用户主目录设置软件下载目录")
        upload_dir = os.path.join(home_dir, self.main_object.app_name, "ipn_uploads")
        make_status = self.make_download_path(upload_dir)
        if make_status:
            print("3.尝试使用用户主目录设置软件下载目录成功:", upload_dir)
            return upload_dir
        # 4. 软件安装目录 + "ipn_uploads"
        print("4.尝试使用软件安装目录设置软件下载目录")
        upload_dir = os.path.join(self.main_object.app_dir, "ipn_uploads")
        make_status = self.make_download_path(upload_dir)
        if make_status:
            print("4.尝试使用软件安装目录设置软件下载目录成功:", upload_dir)
            return upload_dir
        # 5. 空路径
        print("5.直接使用空路径")
        return ""

    def make_download_path(self, upload_dir, create=True):
        if os.path.exists(upload_dir):
            return True
        if not create:
            return False
        try:
            os.makedirs(upload_dir)
            return True
        except Exception as e:
            return False

    def can_save_file(self, upload_dir):
        """检查程序是否可能需要管理员权限"""
        # 尝试在程序文件所在目录创建测试文件
        try:
            test_file = os.path.join(upload_dir, "test_write_GYe8omhoVEXOZeLlNYt77pZMfDwoPuZN.tmp")
            with open(test_file, 'w') as f:
                f.write("test")
            os.unlink(test_file)
            return True
        except PermissionError:
            return False

    def create_service_control(self, layout):
        # 服务控制框架
        self.service_frame = QFrame()
        self.service_frame.setStyleSheet("background-color: transparent; border: none;")
        service_layout = QVBoxLayout(self.service_frame)
        service_layout.setContentsMargins(15, 5, 15, 5)
        # 标题
        title = QLabel("局域网文件传输")
        title.setStyleSheet("background-color: transparent; border: none;")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        service_layout.addWidget(title)
        # 服务端口设置
        port_layout = QHBoxLayout()
        port_label = QLabel("服务端口:")
        port_label.setStyleSheet("background-color: transparent; border: none;")
        port_label.setMinimumWidth(60)
        self.port_edit = QSpinBox()
        self.port_edit.setMaximum(65535)
        self.port_edit.setMinimum(1)
        self.port_edit.setValue(self.port)
        self.default_port_btn = QPushButton("默认")
        self.default_port_btn.clicked.connect(self.set_default_port)
        port_layout.addWidget(port_label)
        port_layout.addWidget(self.port_edit, 1)
        port_layout.addWidget(self.default_port_btn)
        service_layout.addLayout(port_layout)

        # 上传文件夹设置
        upload_layout = QHBoxLayout()
        upload_label = QLabel("上传路径:")
        upload_label.setStyleSheet("background-color: transparent; border: none;")
        upload_label.setMinimumWidth(60)
        self.upload_dir_edit = QPushButton(self.upload_dir)
        self.upload_dir_edit.setToolTip("点击打开上传文件夹")
        self.upload_dir_edit.clicked.connect(self.open_upload_dir)
        self.select_upload_btn = QPushButton("选择")
        self.select_upload_btn.clicked.connect(self.select_upload_dir)
        upload_layout.addWidget(upload_label)
        upload_layout.addWidget(self.upload_dir_edit, 1)
        upload_layout.addWidget(self.select_upload_btn)
        service_layout.addLayout(upload_layout)

        # 访问链接
        link_layout = QHBoxLayout()
        link_label = QLabel("访问链接:")
        link_label.setStyleSheet("background-color: transparent; border: none;")
        link_label.setMinimumWidth(60)
        self.link_edit = QPushButton()
        self.link_edit.setToolTip("点击打开访问链接")
        self.link_edit.clicked.connect(self.open_link)
        self.copy_link_btn = QPushButton("复制")
        self.copy_link_btn.clicked.connect(self.copy_link)
        self.qr_btn = QPushButton("二维码")
        self.qr_btn.clicked.connect(self.toggle_qr_code)
        link_layout.addWidget(link_label)
        link_layout.addWidget(self.link_edit, 1)
        link_layout.addWidget(self.copy_link_btn)
        link_layout.addWidget(self.qr_btn)
        service_layout.addLayout(link_layout)

        # 服务状态和控制按钮
        status_layout = QHBoxLayout()
        status_label = QLabel("服务状态:")
        status_label.setStyleSheet("background-color: transparent; border: none;")
        status_label.setMinimumWidth(60)
        self.status_label = QLabel("已停止")
        status_font = QFont()
        status_font.setPointSize(12)
        self.status_label.setFont(status_font)
        self.status_label.setStyleSheet("background-color: transparent; border: none; color: #ff3b30;")

        # 启动和停止按钮
        self.start_button = QPushButton("启动服务")
        self.start_button.setObjectName("startButton")
        self.stop_button = QPushButton("停止服务")
        self.stop_button.setObjectName("stopButton")
        self.stop_button.setEnabled(False)

        status_layout.addWidget(status_label)
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        status_layout.addWidget(self.start_button)
        status_layout.addWidget(self.stop_button)
        service_layout.addLayout(status_layout)

        # 二维码显示层 (初始隐藏)
        self.qr_frame = QFrame()
        self.qr_frame.setVisible(False)
        qr_layout = QVBoxLayout(self.qr_frame)
        qr_layout.setAlignment(Qt.AlignCenter)
        qr_layout.setContentsMargins(0, 0, 0, 0)

        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignCenter)
        self.qr_label.setFixedSize(180, 180)
        self.qr_label.setText("二维码将在这里显示")
        self.qr_label.setStyleSheet("border: 1px solid #d1d1d6; background-color: white;")
        qr_layout.addWidget(self.qr_label)

        qr_note = QLabel("扫描二维码访问")
        qr_note.setAlignment(Qt.AlignCenter)
        qr_layout.addWidget(qr_note)

        service_layout.addWidget(self.qr_frame)

        # 连接按钮信号
        self.start_button.clicked.connect(self.start_server)
        self.stop_button.clicked.connect(self.stop_server)
        self.port_edit.textChanged.connect(self.update_link_display)

        # 初始化链接显示和二维码
        QTimer.singleShot(100, self.update_link_display)

        layout.addWidget(self.service_frame)

    def toggle_qr_code(self):
        """切换二维码显示"""
        self.qr_frame.setVisible(not self.qr_frame.isVisible())

    def create_file_management(self, layout):
        # 文件管理区域
        self.file_tabs = QTabWidget()

        # 文件管理标签
        file_widget = QWidget()
        file_layout = QVBoxLayout(file_widget)

        # 文件操作按钮
        file_buttons = QHBoxLayout()
        self.upload_file_btn = QPushButton("上传文件")
        self.upload_folder_btn = QPushButton("上传文件夹")
        self.delete_file_btn = QPushButton("删除选中")
        self.clear_files_btn = QPushButton("清空")  # 新增：清空文件列表按钮
        self.refresh_btn = QPushButton("刷新")

        file_buttons.addWidget(self.upload_file_btn)
        file_buttons.addWidget(self.upload_folder_btn)
        file_buttons.addWidget(self.delete_file_btn)
        file_buttons.addWidget(self.clear_files_btn)  # 添加清空按钮
        file_buttons.addWidget(self.refresh_btn)
        file_buttons.addStretch()

        file_layout.addLayout(file_buttons)

        # 文件列表
        self.file_list = QListWidget()
        QTimer.singleShot(100, self.refresh_file_list)
        file_layout.addWidget(self.file_list)

        # 文本管理标签
        text_widget = QWidget()
        text_layout = QVBoxLayout(text_widget)

        # 文本操作按钮
        text_buttons = QHBoxLayout()
        self.upload_text_btn = QPushButton("上传文本")
        self.delete_text_btn = QPushButton("删除选中")
        self.clear_texts_btn = QPushButton("清空")  # 新增：清空文本列表按钮
        self.refresh_text_btn = QPushButton("刷新")

        text_buttons.addWidget(self.upload_text_btn)
        text_buttons.addWidget(self.delete_text_btn)
        text_buttons.addWidget(self.clear_texts_btn)  # 添加清空按钮
        text_buttons.addWidget(self.refresh_text_btn)
        text_buttons.addStretch()

        text_layout.addLayout(text_buttons)

        # 文本列表
        self.text_list = QListWidget()
        QTimer.singleShot(100, self.refresh_text_list)
        text_layout.addWidget(self.text_list)

        # 添加标签页
        self.file_tabs.addTab(file_widget, "文件管理")
        self.file_tabs.addTab(text_widget, "文本管理")

        # 连接按钮信号
        self.upload_file_btn.clicked.connect(self.upload_file)
        self.upload_folder_btn.clicked.connect(self.upload_folder)
        self.delete_file_btn.clicked.connect(self.delete_file)
        self.clear_files_btn.clicked.connect(self.clear_files)  # 连接清空文件列表方法
        self.upload_text_btn.clicked.connect(self.upload_text)
        self.delete_text_btn.clicked.connect(self.delete_text)
        self.clear_texts_btn.clicked.connect(self.clear_texts)  # 连接清空文本列表方法
        self.refresh_btn.clicked.connect(self.refresh_file_list)
        self.refresh_text_btn.clicked.connect(self.refresh_text_list)

        layout.addWidget(self.file_tabs)

    def refresh_file_list(self):
        self.file_list.clear()
        for item in self.ipn_data["files"]:
            uploader = item.get("uploader", "未知")
            list_item = QListWidgetItem(
                f"{'📁' if item['type'] == 'folder' else '📄'} {item['name']} (上传者: {uploader})")
            list_item.setData(Qt.UserRole, item)
            self.file_list.addItem(list_item)

    def refresh_text_list(self):
        self.text_list.clear()
        for item in self.ipn_data["texts"]:
            uploader = item.get("uploader", "未知")
            # 显示文本的前30个字符
            display_text = item["content"][:30] + "..." if len(item["content"]) > 30 else item["content"]
            list_item = QListWidgetItem(f"📝 {display_text} (上传者: {uploader})")
            list_item.setData(Qt.UserRole, item)
            self.text_list.addItem(list_item)

    def save_data(self):
        self.ipn_data["port"] = self.port_edit.value()
        self.ipn_data["uploadDir"] = self.upload_dir_edit.text()
        self.cache = {
            "ipnData": self.ipn_data,
        }
        self.save_data_func(need_upload=False, in_data=self.cache, card_name=self.name, data_type=data_save_constant.DATA_TYPE_CACHE)


    def update_link_display(self):
        port = str(self.port_edit.value())
        ip = self.get_local_ip()
        link = f"http://{ip}:{port}"
        self.link_edit.setText(link)
        self.generate_qr_code(link)

    def open_link(self):
        browser_util.open_url(self.link_edit.text())

    def open_upload_dir(self):
        file_path = self.upload_dir_edit.text()
        try:
            # 在文件管理器中打开并选中文件
            if os.name == 'nt':  # Windows
                file_path = file_path.replace("/", "\\")
                os.system(f'explorer /select,\""{file_path}"\"')
            elif os.name == 'posix':  # macOS
                os.system(f'open -R "{file_path}"')
            else:  # Linux
                os.system(f'xdg-open "{os.path.dirname(file_path)}"')
        except Exception as e:
            self.logger.card_error("本地局域网文件传输", f"打开文件失败: {str(e)}")

    def generate_qr_code(self, text):
        """生成二维码并显示"""
        import qrcode
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(text)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            # 转换为QPixmap
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            pixmap = QPixmap()
            pixmap.loadFromData(buffer.getvalue())

            # 缩放并显示
            self.qr_label.setPixmap(pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        except Exception as e:
            print(f"生成二维码失败: {e}")
            self.qr_label.setText("二维码生成失败")

    def copy_link(self):
        """复制链接到剪贴板"""
        clipboard = QApplication.clipboard()
        clipboard.setText(self.link_edit.text())
        self.bottom_status_label.setText("链接已复制到剪贴板")

    def set_default_port(self):
        self.port_edit.setValue(self.DEFAULT_PORT)

    def select_upload_dir(self):
        """选择上传目录"""
        if self.server and self.server_worker and self.server_worker._active:
            self.toolkit.dialog_module.box_information(self.main_object, "警告", "请先停止服务再更改上传目录")
            return
        dir_path = QFileDialog.getExistingDirectory(self.main_object, "选择上传目录")
        if dir_path:
            self.upload_dir = dir_path
            self.upload_dir_edit.setText(dir_path)
            # 更新数据
            self.save_data()
            # 确保上传目录存在
            if not os.path.exists(self.upload_dir):
                try:
                    os.makedirs(self.upload_dir)
                except Exception as e:
                    self.toolkit.dialog_module.box_information(self.main_object, "错误", f"无法创建上传目录: {e}")
                    return

    def start_server(self):
        from src.card.main_card.IpnCard.server.HttpServerHandler import HttpServerHandler
        from src.card.main_card.IpnCard.server.ServerWorker import ServerWorker
        from src.card.main_card.IpnCard.server.FileServer import FileServer
        try:
            if self.upload_dir is None or self.upload_dir == "" or not os.path.exists(self.upload_dir):
                self.toolkit.dialog_module.box_information(self.main_object, "错误", "请选择上传目录")
                return
            if not self.can_save_file(self.upload_dir):
                self.toolkit.dialog_module.box_information(self.main_object, "错误", "该上传目录暂无权限保存，您可以选择其他目录或者以管理员权限启动灵卡面板")
                return

            port = self.port_edit.value()
            if port < 1024 or port > 65535:
                self.toolkit.dialog_module.box_information(self.main_object, "错误", "端口号必须在1024-65535之间")
                return

            self.port = port

            # 创建服务器
            server_address = ("0.0.0.0", self.port)
            self.server = FileServer(server_address, HttpServerHandler, self.ipn_data, self.upload_dir,
                                     self.on_data_updated)

            # 设置服务器socket为非阻塞
            self.server.socket.setblocking(False)

            # 判断之前的服务器是否在运行，运行就停止
            try:
                if self.server_thread or self.server_worker:
                    self.server_thread.quit()
                    self.server_thread.wait(2000)
                    if self.server_thread.isRunning():
                        self.server_thread.terminate()
                    self.server_thread = None
                    self.server_worker = None
            except Exception as e:
                self.main_object.info_logger.error(f"{traceback.format_exc()}")

            # 创建服务器工作器和线程
            self.server_worker = ServerWorker(self.server)
            self.server_thread = QThread()

            # 将工作器移动到线程中
            self.server_worker.moveToThread(self.server_thread)

            # 连接信号和槽
            self.server_thread.started.connect(self.server_worker.start_server)
            self.server_worker.error_occurred.connect(self.on_server_error)
            self.server_worker.server_started.connect(self.on_server_started)
            self.server_worker.server_stopped.connect(self.on_server_stopped)
            self.server_worker.server_stopped.connect(self.server_thread.quit)
            self.server_worker.server_stopped.connect(self.server_thread.wait)
            self.server_worker.data_updated.connect(self.on_data_updated)  # 连接数据更新信号

            # 启动线程
            self.server_thread.start()

        except Exception as e:
            self.main_object.info_logger.error(f"启动服务器失败:{traceback.format_exc()}")
            self.toolkit.dialog_module.box_information(self.main_object, "错误", f"启动服务器失败: {str(e)}")

    def stop_server(self):
        if self.server_worker:
            # 在工作器所在的线程中调用停止方法
            try:
                self.server_worker.stop_server()
            except Exception as e:
                self.main_object.info_logger.error(f"停止服务器失败:{traceback.format_exc()}")
                self.toolkit.dialog_module.box_information(self.main_object, "错误", f"停止服务器失败: {str(e)}")

    def on_server_started(self):
        """服务器启动成功时的处理"""
        print("服务器已启动")
        self.status_label.setText("运行中")
        self.status_label.setStyleSheet("background-color: transparent; border: none; color: #34c759;")
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.port_edit.setEnabled(False)
        ip = self.get_local_ip()
        self.bottom_status_label.setText(f"服务已在 {ip}:{self.port} 启动")

    def on_server_stopped(self):
        """服务器停止时的处理"""
        print("服务器已停止")
        self.status_label.setText("已停止")
        self.status_label.setStyleSheet("background-color: transparent; border: none; color: #ff3b30;")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.port_edit.setEnabled(True)
        self.bottom_status_label.setText("服务已停止")

    def on_server_error(self, error_msg):
        """服务器出错时的处理"""
        print("服务器出错:", error_msg)
        self.toolkit.dialog_module.box_information(self.main_object, "错误", error_msg)
        self.stop_server()

    def on_data_updated(self):
        """数据更新时的处理"""
        self.save_data()  # 保存到JSON文件
        self.refresh_file_list()  # 刷新文件列表
        self.refresh_text_list()  # 刷新文本列表
        self.bottom_status_label.setText("数据已更新")  # 显示状态信息

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self.main_object, "选择要上传的文件")
        if file_path:
            file_name = os.path.basename(file_path)
            file_info = {
                "name": file_name,
                "path": file_path,
                "type": "file",
                "size": os.path.getsize(file_path),
                "uploader": self.get_local_ip()  # 添加上传者IP
            }
            self.ipn_data["files"].append(file_info)
            self.save_data()
            self.refresh_file_list()
            self.bottom_status_label.setText(f"已添加文件: {file_name}")

    def upload_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self.main_object, "选择要上传的文件夹")
        if folder_path:
            folder_name = os.path.basename(folder_path)
            folder_info = {
                "name": folder_name,
                "path": folder_path,
                "type": "folder",
                "uploader": self.get_local_ip()  # 添加上传者IP
            }
            self.ipn_data["files"].append(folder_info)
            self.save_data()
            self.refresh_file_list()
            self.bottom_status_label.setText(f"已添加文件夹: {folder_name}")

    def delete_file(self):
        current_item = self.file_list.currentItem()
        if current_item:
            item_data = current_item.data(Qt.UserRole)
            self.ipn_data["files"].remove(item_data)
            self.save_data()
            self.refresh_file_list()
            self.bottom_status_label.setText("已删除选中项")
        else:
            self.toolkit.dialog_module.box_information(self.main_object, "警告", "请先选择一个文件或文件夹")

    def clear_files(self):
        """清空文件列表"""
        if not self.ipn_data["files"]:
            return
        if not self.toolkit.dialog_module.box_acknowledgement(self.main_object, "确认清空", f"确定要清空所有文件吗？此操作不可撤销。"):
            return
        self.ipn_data["files"] = []
        self.save_data()
        self.refresh_file_list()
        self.bottom_status_label.setText("已清空文件列表")

    def upload_text(self):
        content = self.toolkit.dialog_module.box_input(self.main_object, "上传文本", "请输入文本内容：", text_type="text")
        if content is None:
            return
        if content == "":
            self.toolkit.dialog_module.box_information(self.main_object, "提示", "文本内容不能为空！")
            return
        text_info = {
            "content": content,
            "type": "text",
            "uploader": self.get_local_ip()  # 添加上传者IP
        }
        self.ipn_data["texts"].append(text_info)
        self.save_data()
        self.refresh_text_list()
        self.bottom_status_label.setText("已添加文本")

    def delete_text(self):
        current_item = self.text_list.currentItem()
        if current_item:
            item_data = current_item.data(Qt.UserRole)
            self.ipn_data["texts"].remove(item_data)
            self.save_data()
            self.refresh_text_list()
            self.bottom_status_label.setText("已删除选中文本")
        else:
            self.toolkit.dialog_module.box_information(self.main_object, "警告", "请先选择一个文本")

    def clear_texts(self):
        """清空文本列表"""
        if not self.ipn_data["texts"]:
            return
        if not self.toolkit.dialog_module.box_acknowledgement(self.main_object, "确认清空", f"确定要清空所有文本吗？此操作不可撤销。"):
            return
        self.ipn_data["texts"] = []
        self.save_data()
        self.refresh_text_list()
        self.bottom_status_label.setText("已清空文本列表")

    def refresh_theme(self):
        """刷新主题"""
        if not super().refresh_theme():
            return False
        is_dark = self.is_dark()
        # 调整按钮样式
        button_list = [
            self.default_port_btn, self.select_upload_btn, self.upload_dir_edit, self.link_edit, self.copy_link_btn, self.qr_btn, self.start_button,
            self.stop_button, self.upload_file_btn, self.upload_folder_btn, self.delete_file_btn, self.clear_files_btn,
            self.refresh_btn, self.upload_text_btn, self.delete_text_btn, self.clear_texts_btn, self.refresh_text_btn
        ]
        for button in button_list:
            style_util.set_button_style(button, is_dark)
        # 按钮文字左对齐和提示样式修改
        left_text_button_list = [self.upload_dir_edit, self.link_edit]
        for button in left_text_button_list:
            # 按钮文字左对齐
            button.setStyleSheet(button.styleSheet().replace("QPushButton {", "QPushButton {text-align: left;"))
            if is_dark:
                button.setStyleSheet(button.styleSheet() + "QToolTip{background-color: #484848; color:#ffffff;}")
            else:
                button.setStyleSheet(button.styleSheet() + "QToolTip{background-color: #ffffff; color:#484848;}")
        # 设置输入框的样式
        style_util.set_spin_box_style(self.port_edit, self.main_object.is_dark)
        # 设置分类的样式
        style_util.set_tab_widget_style(self.file_tabs, self.is_dark())
        # 设置主题
        if is_dark:
            self.service_frame.setStyleSheet("""
                QFrame {
                    background: transparent;
                    border: 1px solid black;
                }""")
        else:
            self.service_frame.setStyleSheet("""
                QFrame {
                    background: transparent;
                    border: 1px solid white;
                }""")

    def refresh_data(self, date_time_str):
        """刷新数据"""
        super().refresh_data(date_time_str)
        pass

    def refresh_ui(self, date_time_str):
        """刷新UI"""
        super().refresh_ui(date_time_str)
        super().refresh_ui_end(date_time_str)
