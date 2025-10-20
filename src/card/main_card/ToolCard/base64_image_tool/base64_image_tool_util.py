import base64
import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
                               QLabel, QLineEdit, QTextEdit, QPushButton,
                               QFileDialog, QScrollArea)


from src.module import dialog_module
from src.ui import style_util


class Base64ImageTool(QWidget):

    def __init__(self, parent=None, main_object=None, is_dark=None):
        super().__init__(parent=parent)
        # 初始化
        self.parent = parent
        self.use_parent = main_object
        self.current_image_path = None

        # 初始化界面
        self.init_ui()
        # 设置样式
        style_util.set_dialog_control_style(self, is_dark)

    def init_ui(self):
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 创建标签页
        self.tab_widget = QTabWidget()

        # 图片转Base64标签页
        self.image_to_base64_tab = self.create_image_to_base64_tab()
        # Base64转图片标签页
        self.base64_to_image_tab = self.create_base64_to_image_tab()

        # 添加标签页
        self.tab_widget.addTab(self.image_to_base64_tab, "图片转Base64")
        self.tab_widget.addTab(self.base64_to_image_tab, "Base64转图片")

        main_layout.addWidget(self.tab_widget)

    def create_image_to_base64_tab(self):
        """创建图片转Base64标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(5)
        layout.setContentsMargins(5, 5, 5, 5)

        # 图片选择区域
        image_select_layout = QHBoxLayout()

        self.image_path_input = QLineEdit()
        self.image_path_input.setPlaceholderText("选择图片文件...")
        self.image_path_input.setReadOnly(True)
        image_select_layout.addWidget(self.image_path_input)

        self.browse_button = QPushButton("浏览")
        self.browse_button.clicked.connect(self.browse_image)
        image_select_layout.addWidget(self.browse_button)

        layout.addLayout(image_select_layout)

        # 图片预览区域
        preview_label = QLabel("图片预览:")
        preview_label.setStyleSheet("background: transparent;")
        layout.addWidget(preview_label)

        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumHeight(150)
        self.preview_label.setStyleSheet("border: 1px solid #ccc;")
        self.preview_label.setText("预览将显示在这里")
        layout.addWidget(self.preview_label)

        # Base64结果显示区域
        result_label = QLabel("Base64编码结果:")
        result_label.setStyleSheet("background: transparent;")
        layout.addWidget(result_label)

        self.base64_output = QTextEdit()
        self.base64_output.setPlaceholderText("Base64编码将显示在这里...")
        self.base64_output.setMaximumHeight(120)
        layout.addWidget(self.base64_output)

        # 操作按钮
        button_layout = QHBoxLayout()

        self.encode_button = QPushButton("编码为Base64")
        self.encode_button.clicked.connect(self.encode_image_to_base64)
        button_layout.addWidget(self.encode_button)

        self.copy_button = QPushButton("复制结果")
        self.copy_button.clicked.connect(self.copy_base64_result)
        button_layout.addWidget(self.copy_button)

        layout.addLayout(button_layout)

        return tab

    def create_base64_to_image_tab(self):
        """创建Base64转图片标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(5)
        layout.setContentsMargins(5, 5, 5, 5)

        # Base64输入区域
        input_label = QLabel("Base64编码:")
        input_label.setStyleSheet("background: transparent;")
        layout.addWidget(input_label)

        self.base64_input = QTextEdit()
        self.base64_input.setPlaceholderText("请输入Base64编码字符串...")
        self.base64_input.setMaximumHeight(120)
        layout.addWidget(self.base64_input)

        # 图片显示区域
        result_label = QLabel("解码结果:")
        result_label.setStyleSheet("background: transparent;")
        layout.addWidget(result_label)

        # 使用滚动区域来显示图片
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumHeight(200)

        self.image_result_label = QLabel()
        self.image_result_label.setAlignment(Qt.AlignCenter)
        self.image_result_label.setStyleSheet("border: 1px solid #ccc;")
        self.image_result_label.setText("解码后的图片将显示在这里")
        self.image_result_label.setMinimumSize(200, 150)

        scroll_area.setWidget(self.image_result_label)
        layout.addWidget(scroll_area)

        # 操作按钮
        button_layout = QHBoxLayout()

        self.decode_button = QPushButton("解码为图片")
        self.decode_button.clicked.connect(self.decode_base64_to_image)
        button_layout.addWidget(self.decode_button)

        self.save_button = QPushButton("保存图片")
        self.save_button.clicked.connect(self.save_decoded_image)
        button_layout.addWidget(self.save_button)

        layout.addLayout(button_layout)

        return tab

    def browse_image(self):
        """浏览并选择图片文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择图片文件",
            "",
            "图片文件 (*.png *.jpg *.jpeg *.bmp *.gif *.ico)"
        )

        if file_path:
            self.current_image_path = file_path
            self.image_path_input.setText(file_path)
            self.preview_image(file_path)

    def preview_image(self, image_path):
        """预览图片"""
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            # 缩放图片以适应预览区域
            scaled_pixmap = pixmap.scaled(
                self.preview_label.width() - 20,
                self.preview_label.height() - 20,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.preview_label.setPixmap(scaled_pixmap)
        else:
            self.preview_label.setText("无法加载图片")

    def encode_image_to_base64(self):
        """将图片编码为Base64"""
        if not self.current_image_path:
            dialog_module.box_information(self.use_parent, "警告", "请先选择图片文件")
            return

        try:
            with open(self.current_image_path, 'rb') as image_file:
                image_data = image_file.read()
                base64_encoded = base64.b64encode(image_data).decode('utf-8')

                # 获取文件扩展名
                file_extension = os.path.splitext(self.current_image_path)[1].lower().replace('.', '')
                if file_extension == 'jpg':
                    file_extension = 'jpeg'

                # 构建data URL格式
                data_url = f"data:image/{file_extension};base64,{base64_encoded}"

                self.base64_output.setText(data_url)

        except Exception as e:
            dialog_module.box_information(self.use_parent, "错误", f"编码失败: {str(e)}")

    def copy_base64_result(self):
        """复制Base64结果到剪贴板"""
        base64_text = self.base64_output.toPlainText()
        if base64_text:
            self.base64_output.selectAll()
            self.base64_output.copy()
            dialog_module.box_information(self.use_parent, "成功", "Base64编码已复制到剪贴板")
        else:
            dialog_module.box_information(self.use_parent, "警告", "没有可复制的内容")

    def decode_base64_to_image(self):
        """将Base64解码为图片"""
        base64_text = self.base64_input.toPlainText().strip()
        if not base64_text:
            dialog_module.box_information(self.use_parent, "警告", "请输入Base64编码")
            return

        try:
            # 处理data URL格式
            if base64_text.startswith('data:image'):
                # 提取实际的base64数据部分
                base64_data = base64_text.split(',')[1]
            else:
                base64_data = base64_text

            # 解码base64
            image_data = base64.b64decode(base64_data)

            # 创建QPixmap
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)

            if not pixmap.isNull():
                # 缩放图片以适应显示区域
                scaled_pixmap = pixmap.scaled(
                    self.image_result_label.width() - 20,
                    self.image_result_label.height() - 20,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.image_result_label.setPixmap(scaled_pixmap)
                self.decoded_image_data = image_data
                self.decoded_pixmap = pixmap
            else:
                dialog_module.box_information(self.use_parent, "错误", "无法解码Base64数据为图片")

        except Exception as e:
            dialog_module.box_information(self.use_parent, "错误", f"解码失败: {str(e)}")

    def save_decoded_image(self):
        """保存解码后的图片"""
        if not hasattr(self, 'decoded_pixmap') or self.decoded_pixmap.isNull():
            dialog_module.box_information(self.use_parent, "警告", "没有可保存的图片")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存图片",
            "decoded_image.png",
            "PNG图片 (*.png);;JPEG图片 (*.jpg *.jpeg);;BMP图片 (*.bmp)"
        )

        if file_path:
            try:
                self.decoded_pixmap.save(file_path)
                dialog_module.box_information(self.use_parent, "成功", f"图片已保存到: {file_path}")
            except Exception as e:
                dialog_module.box_information(self.use_parent, "错误", f"保存失败: {str(e)}")

    def refresh_theme(self, main_object):
        """刷新主题"""
        style_util.set_dialog_control_style(self, main_object.is_dark)
