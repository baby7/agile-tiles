import os
import base64
import json
from pathlib import Path

from PySide6 import QtGui
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                               QFileDialog, QGroupBox, QLabel, QComboBox,
                               QLineEdit, QAbstractItemView, QRadioButton,
                               QButtonGroup)
from PySide6.QtCore import Signal, QObject, QThread, QUrl, QEventLoop, QMutex, Qt
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

from src.client import common
from src.my_component.AgileTilesAcrylicWindow.AgileTilesAcrylicWindow import AgileTilesAcrylicWindow
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
    progress_updated = Signal(int, str)  # 进度更新信号 (行索引, 状态)
    conversion_finished = Signal()  # 转换完成信号


class ConversionWorker(QThread):
    """转换工作线程"""

    def __init__(self, access_token, file_list, output_dir, signals):
        super().__init__()
        self.access_token = access_token
        self.file_list = file_list
        self.output_dir = output_dir
        self.signals = signals
        self._stop_flag = False
        self._mutex = QMutex()

    def stop(self):
        """请求停止转换"""
        self._mutex.lock()
        self._stop_flag = True
        self._mutex.unlock()

    def should_stop(self):
        """检查是否应该停止转换"""
        self._mutex.lock()
        stop = self._stop_flag
        self._mutex.unlock()
        return stop

    def run(self):
        """执行转换任务"""
        network_manager = QNetworkAccessManager()

        for i, file_info in enumerate(self.file_list):
            if self.should_stop():
                break

            file_path, status = file_info
            if status == "转换成功":
                continue  # 跳过已转换成功的文件

            # 更新状态为"转换中"
            self.signals.progress_updated.emit(i, "转换中")

            try:
                # 调用真实云端API
                excel_base64 = call_cloud_api(self.access_token, network_manager, file_path)

                # 生成输出文件名
                file_name = Path(file_path).stem
                output_file = os.path.join(self.output_dir, f"{file_name}.xlsx")

                # 保存base64解码后的内容到Excel文件
                excel_data = base64.b64decode(excel_base64)
                with open(output_file, 'wb') as f:
                    f.write(excel_data)

                # 更新状态为"转换成功"
                self.signals.progress_updated.emit(i, "转换成功")

            except Exception as e:
                self.signals.progress_updated.emit(i, f"转换失败: {str(e)}")

        self.signals.conversion_finished.emit()


class ImageToExcelConverterDialog(AgileTilesAcrylicWindow):
    file_list = []  # 存储文件信息: (文件路径, 状态)
    conversion_thread = None
    # 调用次数
    today_calls = 0

    def __init__(self, parent=None, use_parent=None, title=None, content=None):
        super().__init__(parent=parent, is_dark=use_parent.is_dark, form_theme_mode=use_parent.form_theme_mode,
                         form_theme_transparency=use_parent.form_theme_transparency)
        # 初始化
        self.parent = parent
        self.use_parent = use_parent
        # 设置标题栏
        self.setWindowTitle(title)  # 设置到标题栏
        self.titleBar.minBtn.close()
        self.titleBar.maxBtn.close()
        self.setMinimumSize(900, 600)
        # 初始化界面
        self.init_ui()
        # 设置样式
        style_util.set_dialog_control_style(self, self.is_dark)

    def init_ui(self):
        """初始化用户界面"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        self.widget_base.setLayout(main_layout)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # 顶部信息条
        self.info_bar = QLabel()
        self.info_bar.setAlignment(Qt.AlignCenter)
        self.info_bar.setFixedHeight(30)
        self.info_bar.setContentsMargins(5, 0, 5, 0)
        self.info_bar.setStyleSheet("font-weight: bold; font-size: 12px;")
        main_layout.addWidget(self.info_bar)

        # 顶部按钮区域
        top_button_layout = QHBoxLayout()

        self.import_image_btn = QPushButton("导入图片")
        self.import_image_btn.clicked.connect(self.import_images)

        self.import_folder_btn = QPushButton("导入图片文件夹")
        self.import_folder_btn.clicked.connect(self.import_folder)

        self.clear_list_btn = QPushButton("清空列表")
        self.clear_list_btn.clicked.connect(self.clear_list)

        top_button_layout.addWidget(self.import_image_btn)
        top_button_layout.addWidget(self.import_folder_btn)
        top_button_layout.addWidget(self.clear_list_btn)
        top_button_layout.addStretch()

        main_layout.addLayout(top_button_layout)

        # 文件列表表格
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels(["文件名", "原始格式", "文件大小", "转换状态", "操作", "删除"])

        # 设置列宽分配策略，确保操作列有足够空间
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # 文件名列自适应
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # 原始格式自适应内容
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # 文件大小自适应内容
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # 转换状态自适应内容
        header.setSectionResizeMode(4, QHeaderView.Fixed)  # 操作列固定宽度
        header.setSectionResizeMode(5, QHeaderView.Fixed)  # 删除列固定宽度

        # 设置固定列宽
        self.table_widget.setColumnWidth(4, 250)  # 操作列宽度设为250像素
        self.table_widget.setColumnWidth(5, 80)  # 删除列宽度设为80像素

        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 调整行高
        self.table_widget.verticalHeader().setDefaultSectionSize(40)

        main_layout.addWidget(self.table_widget)

        # 底部设置区域
        bottom_layout = QHBoxLayout()

        # 导出设置
        export_group = QGroupBox("导出设置")
        export_group.setStyleSheet("QGroupBox{border: 1px solid rgba(125, 125, 125, 125); padding-top: 8px;}")
        export_layout = QVBoxLayout(export_group)

        # 导出格式
        format_layout = QHBoxLayout()
        self.export_title_label = QLabel("导出格式:")
        self.export_title_label.setStyleSheet("background: transparent; border: none;")
        format_layout.addWidget(self.export_title_label)
        self.format_combo = QComboBox()
        self.format_combo.addItem("xlsx")
        self.format_combo.setEnabled(False)  # 固定为xlsx，不可编辑
        format_layout.addWidget(self.format_combo)
        self.export_des_label = QLabel("(现在仅支持xlsx格式)")
        self.export_des_label.setStyleSheet("background: transparent; border: none;")
        format_layout.addWidget(self.export_des_label)
        format_layout.addStretch()
        export_layout.addLayout(format_layout)

        # 导出目录选项
        export_dir_layout = QHBoxLayout()

        self.export_original_radio = QRadioButton("原文件夹目录")
        self.export_custom_radio = QRadioButton("自定义目录")
        self.export_original_radio.setChecked(True)

        self.export_dir_group = QButtonGroup()
        self.export_dir_group.addButton(self.export_original_radio)
        self.export_dir_group.addButton(self.export_custom_radio)
        self.export_dir_group.buttonToggled.connect(self.on_export_dir_changed)

        export_dir_layout.addWidget(self.export_original_radio)
        export_dir_layout.addWidget(self.export_custom_radio)

        # 导出目录选择
        self.export_dir_edit = QLineEdit()
        self.export_dir_edit.setPlaceholderText("选择导出目录...")
        self.export_dir_edit.setEnabled(False)
        export_dir_layout.addWidget(self.export_dir_edit)
        self.browse_dir_btn = QPushButton("浏览...")
        self.browse_dir_btn.clicked.connect(self.browse_export_dir)
        self.browse_dir_btn.setEnabled(False)
        export_dir_layout.addWidget(self.browse_dir_btn)
        export_layout.addLayout(export_dir_layout)

        bottom_layout.addWidget(export_group)

        # 按钮部分
        self.convert_btn = QPushButton("开始转换")
        self.convert_btn.clicked.connect(self.toggle_conversion)
        self.convert_btn.setMinimumHeight(60)
        self.convert_btn.setMinimumWidth(60)
        bottom_layout.addWidget(self.convert_btn)

        main_layout.addLayout(bottom_layout)

        # 状态栏
        self.status_bar_label = QLabel("就绪")
        self.status_bar_label.setStyleSheet("background: transparent; border: none;")
        main_layout.addWidget(self.status_bar_label)

        # 填充部分信息
        self.set_info_bar()
        # 请求并更新对话次数信息
        self.update_call_count()

    def update_call_count(self):
        """请求并更新对话次数信息"""
        url = QUrl(common.BASE_URL + "/ocr/normal/excel/todayCalls")
        request = QNetworkRequest(url)
        request.setRawHeader(b"Authorization", bytes(self.use_parent.access_token, "utf-8"))

        # 使用临时网络管理器获取调用次数
        temp_manager = QNetworkAccessManager(self)
        reply = temp_manager.get(request)

        def handle_reply():
            if reply.error() == QNetworkReply.NoError:
                data = reply.readAll()
                json_data = json.loads(str(data, 'utf-8'))
                self.today_calls = json_data.get("data", 0)

                # 根据会员状态显示不同信息
                self.set_info_bar()
            else:
                error = reply.errorString()
                print(f"获取调用次数失败: {error}")
                self.info_bar.setText("获取图片转Excel次数失败")
                self.info_bar.setStyleSheet(
                    "background-color: rgba(255, 255, 255, 0.1); "
                    "border-radius: 5px; "
                    "color: orange; "
                    "font-weight: bold; "
                    "font-size: 12px;"
                )

            reply.deleteLater()

        reply.finished.connect(handle_reply)

    def set_info_bar(self):
        # 根据会员状态显示不同信息
        if self.use_parent.is_vip:
            if self.today_calls >= 200:
                text = f"尊敬的会员用户，您今天已使用{self.today_calls}次，已超限"
                color = "rgba(255, 140, 0, 0.8)"
                self.info_bar.show()
            else:
                text = f"会员用户畅享使用，今天已使用{self.today_calls}次"
                color = "rgba(4, 115, 247, 0.8)"
                self.info_bar.hide()
        else:
            text = f"图片转换功能仅限会员用户使用"
            color = "rgba(255, 140, 0, 0.8)"
            self.info_bar.show()

        # 设置信息条样式和内容
        self.info_bar.setText(text)
        self.info_bar.setStyleSheet(
            f"background-color: rgba(125, 125, 125, 60); "
            f"border-radius: 10px; "
            f"color: {color}; "
            f"font-weight: bold; "
            f"font-size: 12px;"
        )

    def on_export_dir_changed(self, button, checked):
        """导出目录选项变化处理"""
        if button == self.export_custom_radio and checked:
            self.export_dir_edit.setEnabled(True)
            self.browse_dir_btn.setEnabled(True)
        else:
            self.export_dir_edit.setEnabled(False)
            self.browse_dir_btn.setEnabled(False)

    def import_images(self):
        """导入单个或多个图片文件"""
        file_dialog = QFileDialog()
        file_paths, _ = file_dialog.getOpenFileNames(
            self, "选择图片文件", "",
            "图片文件 (*.png *.jpg *.jpeg *.bmp *.tiff *.tif)"
        )

        if file_paths:
            self.add_files_to_list(file_paths)

    def import_folder(self):
        """导入文件夹中的所有图片"""
        folder_path = QFileDialog.getExistingDirectory(self, "选择图片文件夹")

        if folder_path:
            image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif')
            file_paths = []

            for root, _, files in os.walk(folder_path):
                for file in files:
                    if file.lower().endswith(image_extensions):
                        file_paths.append(os.path.join(root, file))

            if file_paths:
                self.add_files_to_list(file_paths)
            else:
                message_box_util.box_information(self.use_parent, "提示", "所选文件夹中没有找到图片文件")

    def add_files_to_list(self, file_paths):
        """添加文件到列表"""
        for file_path in file_paths:
            # 检查文件是否已经在列表中
            if any(file_path == path for path, _ in self.file_list):
                continue

            # 获取文件信息
            file_name = os.path.basename(file_path)
            file_ext = os.path.splitext(file_name)[1].lower()
            file_size = self.get_file_size(file_path)

            # 添加到文件列表
            self.file_list.append((file_path, "待识别"))

            # 添加到表格
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)

            self.table_widget.setItem(row_position, 0, QTableWidgetItem(file_name))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(file_ext))
            self.table_widget.setItem(row_position, 2, QTableWidgetItem(file_size))
            self.table_widget.setItem(row_position, 3, QTableWidgetItem("待识别"))

            # 操作按钮（初始为空，转换成功后添加）
            self.table_widget.setCellWidget(row_position, 4, QWidget())

            # 删除按钮
            delete_btn = QPushButton("删除")
            style_util.set_button_style(delete_btn, self.is_dark)
            delete_btn.clicked.connect(lambda: self.delete_file(row_position))
            self.table_widget.setCellWidget(row_position, 5, delete_btn)

        self.status_bar_label.setText(f"已添加 {len(file_paths)} 个文件")

    def get_file_size(self, file_path):
        """获取文件大小并格式化"""
        size = os.path.getsize(file_path)
        units = ['B', 'KB', 'MB', 'GB']
        unit_index = 0

        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1

        return f"{size:.2f} {units[unit_index]}"

    def clear_list(self):
        """清空文件列表"""
        if self.file_list:
            confirm = message_box_util.box_acknowledgement(
                self.use_parent, "确认清空", f"确定要清空文件列表吗？")
            if confirm:
                self.file_list.clear()
                self.table_widget.setRowCount(0)
                self.status_bar_label.setText("已清空文件列表")
        else:
            message_box_util.box_information(self.use_parent, "提示", "文件列表已为空")

    def browse_export_dir(self):
        """选择导出目录"""
        folder_path = QFileDialog.getExistingDirectory(self, "选择导出目录")

        if folder_path:
            self.export_dir_edit.setText(folder_path)

    def toggle_conversion(self):
        """开始或停止转换"""
        if self.convert_btn.text() == "开始转换":
            self.start_conversion()
        else:
            self.stop_conversion()

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

        if not self.file_list:
            message_box_util.box_information(self.use_parent, "警告", "请先添加图片文件")
            return

        # 确定导出目录
        if self.export_original_radio.isChecked():
            # 使用第一个文件的目录作为导出目录
            first_file_path = self.file_list[0][0]
            output_dir = os.path.dirname(first_file_path)
        else:
            output_dir = self.export_dir_edit.text()
            if not output_dir:
                message_box_util.box_information(self.use_parent, "警告", "请选择导出目录")
                return

        # 创建导出目录（如果不存在）
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            message_box_util.box_information(self.use_parent, "错误", f"无法创建导出目录: {str(e)}")
            return

        # 更新UI状态
        self.convert_btn.setText("停止转换")
        self.import_image_btn.setEnabled(False)
        self.import_folder_btn.setEnabled(False)
        self.clear_list_btn.setEnabled(False)
        self.browse_dir_btn.setEnabled(False)
        self.export_original_radio.setEnabled(False)
        self.export_custom_radio.setEnabled(False)

        # 创建信号对象
        self.conversion_signals = ConversionSignals()
        self.conversion_signals.progress_updated.connect(self.update_conversion_status)
        self.conversion_signals.conversion_finished.connect(self.conversion_finished)

        # 创建并启动工作线程
        self.conversion_thread = ConversionWorker(
            access_token=self.use_parent.access_token,
            file_list=self.file_list,
            output_dir=output_dir,
            signals=self.conversion_signals
        )
        self.conversion_thread.start()

        self.status_bar_label.setText("转换中...")

    def stop_conversion(self):
        """停止转换"""
        if self.conversion_thread:
            self.conversion_thread.stop()
        self.status_bar_label.setText("正在停止转换...")

    def update_conversion_status(self, row_index, status):
        """更新转换状态"""
        self.table_widget.item(row_index, 3).setText(status)

        # 如果转换成功，添加操作按钮
        if status == "转换成功":
            operation_widget = QWidget()
            operation_layout = QHBoxLayout(operation_widget)
            operation_layout.setContentsMargins(0, 0, 0, 0)
            operation_layout.setSpacing(5)  # 减少按钮间距

            open_export_dir_btn = QPushButton("导出目录")
            style_util.set_button_style(open_export_dir_btn, self.is_dark)
            open_export_dir_btn.setFixedWidth(70)  # 设置固定宽度
            open_export_dir_btn.clicked.connect(lambda: self.open_export_dir_click(row_index))
            operation_layout.addWidget(open_export_dir_btn)

            save_as_btn = QPushButton("另存为")
            style_util.set_button_style(save_as_btn, self.is_dark)
            save_as_btn.setFixedWidth(60)  # 设置固定宽度
            save_as_btn.clicked.connect(lambda: self.save_as(row_index))
            operation_layout.addWidget(save_as_btn)

            reidentify_btn = QPushButton("重新识别")
            style_util.set_button_style(reidentify_btn, self.is_dark)
            reidentify_btn.setFixedWidth(70)  # 设置固定宽度
            reidentify_btn.clicked.connect(lambda: self.reidentify(row_index))
            operation_layout.addWidget(reidentify_btn)

            self.table_widget.setCellWidget(row_index, 4, operation_widget)

        # 更新文件列表中的状态
        if 0 <= row_index < len(self.file_list):
            file_path, _ = self.file_list[row_index]
            self.file_list[row_index] = (file_path, status)

    def conversion_finished(self):
        """转换完成"""
        self.convert_btn.setText("开始转换")
        self.import_image_btn.setEnabled(True)
        self.import_folder_btn.setEnabled(True)
        self.clear_list_btn.setEnabled(True)
        self.browse_dir_btn.setEnabled(True)
        self.export_original_radio.setEnabled(True)
        self.export_custom_radio.setEnabled(True)
        self.status_bar_label.setText("转换完成")
        # 请求并更新对话次数信息
        self.update_call_count()

    def open_export_dir_click(self, row_index):
        """打开导出目录操作"""
        if 0 <= row_index < len(self.file_list):
            file_path, status = self.file_list[row_index]
            # 使用原始目录
            if self.export_original_radio.isChecked():
                self.open_dir(file_path)
            else:
                # 使用自定义目录
                if self.export_dir_edit.text():
                    self.open_dir(self.export_dir_edit.text())
                else:
                    message_box_util.box_information(self.use_parent, "提示", f"请选择导出目录")

    def open_dir(self, file_path):
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
            message_box_util.box_information(self.use_parent, "错误", f"无法打开目录: {str(e)}")

    def save_as(self, row_index):
        """另存为操作"""
        if 0 <= row_index < len(self.file_list):
            file_path, status = self.file_list[row_index]

            if status == "转换成功":
                file_name = os.path.basename(file_path)
                base_name = os.path.splitext(file_name)[0]

                # 确定默认目录
                if self.export_original_radio.isChecked():
                    default_dir = os.path.dirname(file_path)
                else:
                    default_dir = self.export_dir_edit.text()

                default_path = os.path.join(default_dir, f"{base_name}.xlsx")

                save_path, _ = QFileDialog.getSaveFileName(
                    self, "另存为", default_path, "Excel文件 (*.xlsx)"
                )

                if save_path:
                    try:
                        # 复制已转换的文件到新位置
                        source_file = os.path.join(default_dir, f"{base_name}.xlsx")
                        with open(source_file, 'rb') as src, open(save_path, 'wb') as dst:
                            dst.write(src.read())
                        message_box_util.box_information(self.use_parent, "成功", "文件已另存为")
                    except Exception as e:
                        message_box_util.box_information(self.use_parent, "错误", f"保存文件失败: {str(e)}")
            else:
                message_box_util.box_information(self.use_parent, "警告", "只有转换成功的文件才能另存为")

    def reidentify(self, row_index):
        """重新识别操作"""
        if 0 <= row_index < len(self.file_list):
            file_path, status = self.file_list[row_index]

            # 重置状态为"待识别"
            self.file_list[row_index] = (file_path, "待识别")
            self.table_widget.item(row_index, 3).setText("待识别")

            # 移除操作按钮
            self.table_widget.setCellWidget(row_index, 4, QWidget())

    def delete_file(self, row_index):
        """删除文件"""
        if 0 <= row_index < len(self.file_list):
            confirm = message_box_util.box_acknowledgement(
                self.use_parent, "确认删除", f"确定要删除这个文件吗？")
            if confirm:
                self.file_list.pop(row_index)
                self.table_widget.removeRow(row_index)
                self.status_bar_label.setText("文件已删除")


def show_image_to_excel_converter_dialog(main_object, title, content=None):
    """显示对话框"""
    dialog = ImageToExcelConverterDialog(None, main_object, title, content)
    dialog.refresh_geometry(main_object.toolkit.resolution_util.get_screen(main_object))
    dialog.show()
    return dialog