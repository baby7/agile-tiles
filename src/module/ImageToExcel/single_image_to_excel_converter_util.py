import os
import base64
import json

from PySide6 import QtGui
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog
from PySide6.QtCore import Signal, QObject, QThread, QUrl, QEventLoop, Qt
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

from src.client import common
from src.component.AgileTilesAcrylicWindow.AgileTilesAcrylicWindow import AgileTilesAcrylicWindow
from src.module.Box import message_box_util
from src.ui import style_util, image_util


# 真实云端API调用
def call_cloud_api(access_token, network_manager, image_path, engine="baidu"):
    """调用真实云端API，返回base64编码的Excel内容"""
    # 使用QPixmap读取
    pixmap = QtGui.QPixmap(image_path)
    try:
        # 这里使用压缩后的版本
        base64_data = image_util.compress_pixmap_for_baidu(pixmap)
    except ValueError as e:
        raise Exception(f"文件读取错误")

    # 准备请求数据
    request_data = {
        "engine": engine,
        "imageBase64": base64_data
    }

    # 创建网络请求
    url = QUrl(common.BASE_URL + "/ocr/normal/excel")
    request = QNetworkRequest(QUrl(url))
    request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")
    request.setRawHeader(b"Authorization", bytes(access_token, "utf-8"))

    # 发送POST请求
    reply = network_manager.post(
        request,
        json.dumps(request_data).encode('utf-8')
    )

    # 等待请求完成
    loop = QEventLoop()
    reply.finished.connect(loop.quit)
    loop.exec()

    # 检查网络错误
    if reply.error() != QNetworkReply.NoError:
        raise Exception(f"网络错误: {reply.errorString()}")

    # 解析响应
    response_data = json.loads(reply.readAll().data().decode('utf-8'))
    print(f"响应数据:{reply.readAll().data().decode('utf-8')}")

    if str(response_data.get("code")) != "0":
        raise Exception(f"请稍后重试")

    # 返回Excel数据
    return response_data["data"]["excelFile"]


class ConversionSignals(QObject):
    """信号类，用于线程与UI之间的通信"""
    conversion_finished = Signal(bool, str)  # 转换完成信号 (成功标志, 消息)


class SingleImageConversionWorker(QThread):
    """单图片转换工作线程"""

    def __init__(self, access_token, image_path, output_path, signals):
        super().__init__()
        self.access_token = access_token
        self.image_path = image_path
        self.output_path = output_path
        self.signals = signals

    def run(self):
        """执行转换任务"""
        network_manager = QNetworkAccessManager()

        try:
            # 调用真实云端API
            excel_base64 = call_cloud_api(self.access_token, network_manager, self.image_path)

            # 保存base64解码后的内容到Excel文件
            excel_data = base64.b64decode(excel_base64)
            with open(self.output_path, 'wb') as f:
                f.write(excel_data)

            self.signals.conversion_finished.emit(True, "转换成功")

        except Exception as e:
            self.signals.conversion_finished.emit(False, f"转换失败: {str(e)}")


class SingleImageToExcelConverterDialog(AgileTilesAcrylicWindow):
    conversion_thread = None

    def __init__(self, parent=None, use_parent=None, title=None, content=None, pixmap=None):
        super().__init__(parent=parent, is_dark=use_parent.is_dark, form_theme_mode=use_parent.form_theme_mode,
                         form_theme_transparency=use_parent.form_theme_transparency)
        # 初始化
        self.parent = parent
        self.use_parent = use_parent
        self.pixmap = pixmap
        # 设置标题栏
        self.setWindowTitle(title)  # 设置到标题栏
        self.titleBar.minBtn.close()
        self.titleBar.maxBtn.close()
        self.setMinimumSize(300, 400)

        # 转换状态和输出路径
        self.conversion_success = False
        self.output_path = ""

        # 初始化界面
        self.init_ui()
        # 设置样式
        style_util.set_dialog_control_style(self, self.is_dark)

        # 启动转换
        self.start_conversion()

    def init_ui(self):
        """初始化用户界面"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        self.widget_base.setLayout(main_layout)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.addStretch()

        # 图片显示区域
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(300, 200)
        self.image_label.setStyleSheet("border: 1px solid gray; background-color: white;")

        if self.pixmap:
            # 缩放图片以适应标签大小
            scaled_pixmap = self.pixmap.scaled(300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
        else:
            self.image_label.setText("无图片")

        main_layout.addWidget(self.image_label)

        # 转换状态区域
        self.status_label = QLabel("准备转换...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFixedHeight(30)
        self.status_label.setStyleSheet("background: transparent; border: none;")
        main_layout.addWidget(self.status_label)

        # 按钮区域
        button_layout = QHBoxLayout()

        self.save_as_btn = QPushButton("另存为")
        self.save_as_btn.clicked.connect(self.save_as)
        self.save_as_btn.setEnabled(False)  # 初始不可用

        button_layout.addWidget(self.save_as_btn)
        main_layout.addLayout(button_layout)

        # 状态栏
        self.status_bar_label = QLabel("就绪")
        self.status_bar_label.setStyleSheet("background: transparent; border: none;")
        main_layout.addWidget(self.status_bar_label)
        main_layout.addStretch()

    def start_conversion(self):
        """开始转换"""
        if self.use_parent.current_user is None or self.use_parent.current_user["username"] is None:
            message_box_util.box_information(self.use_parent, "提醒", f"未知错误，请重新登录")
            return
        if not self.use_parent.is_login:
            message_box_util.box_information(self.use_parent, "提示信息", "请先登录")
            return
        if not self.use_parent.is_vip:
            message_box_util.box_information(self.use_parent, "提示信息", "会员专属功能，请开通会员后使用哦")
            return

        # 创建临时文件路径
        temp_dir = os.path.join(os.path.expanduser("~"), "Temp")
        os.makedirs(temp_dir, exist_ok=True)
        self.output_path = os.path.join(temp_dir, "converted_image.xlsx")

        # 保存图片到临时文件
        temp_image_path = os.path.join(temp_dir, "temp_image.png")
        if self.pixmap:
            self.pixmap.save(temp_image_path)

        # 更新UI状态
        self.status_label.setText("转换中...")
        self.save_as_btn.setEnabled(False)

        # 创建信号对象
        self.conversion_signals = ConversionSignals()
        self.conversion_signals.conversion_finished.connect(self.conversion_finished)

        # 创建并启动工作线程
        self.conversion_thread = SingleImageConversionWorker(
            access_token=self.use_parent.access_token,
            image_path=temp_image_path,
            output_path=self.output_path,
            signals=self.conversion_signals
        )
        self.conversion_thread.start()

        self.status_bar_label.setText("转换中...")

    def conversion_finished(self, success, message):
        """转换完成"""
        self.conversion_success = success
        self.status_label.setText(message)

        if success:
            self.save_as_btn.setEnabled(True)
            self.status_bar_label.setText("转换完成，可以另存为")
        else:
            self.save_as_btn.setEnabled(False)
            self.status_bar_label.setText("转换失败")

    def save_as(self):
        """另存为操作"""
        if not self.conversion_success:
            message_box_util.box_information(self.use_parent, "警告", "只有转换成功的文件才能另存为")
            return

        save_path, _ = QFileDialog.getSaveFileName(
            self, "另存为", "converted_image.xlsx", "Excel文件 (*.xlsx)"
        )

        if save_path:
            try:
                # 复制已转换的文件到新位置
                with open(self.output_path, 'rb') as src, open(save_path, 'wb') as dst:
                    dst.write(src.read())
                message_box_util.box_information(self.use_parent, "成功", f"文件已保存到: {save_path}")
            except Exception as e:
                message_box_util.box_information(self.use_parent, "错误", f"保存文件失败: {str(e)}")


def show_single_image_to_excel_converter_dialog(main_object, title, pixmap):
    """显示单图片转换对话框"""
    dialog = SingleImageToExcelConverterDialog(None, main_object, title, None, pixmap)
    dialog.refresh_geometry(main_object.toolkit.resolution_util.get_screen(main_object))
    dialog.show()
    return dialog
