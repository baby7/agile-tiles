import uuid
from PySide6.QtGui import QTextOption
from PySide6.QtWidgets import (QLabel, QLineEdit, QPushButton, QVBoxLayout,
                               QWidget, QHBoxLayout, QSpinBox, QCheckBox,
                               QTextEdit, QComboBox, QApplication)
from src.module import dialog_module
from src.ui import style_util


class UUIDGeneratorPopup(QWidget):

    def __init__(self, parent=None, main_object=None, is_dark=None):
        super().__init__(parent=parent)
        # 初始化
        self.parent = parent
        self.use_parent = main_object
        # 初始化界面
        self.init_ui()
        # 设置样式
        self.setStyleSheet("background: transparent; border: none; padding: 3px;")
        style_util.set_dialog_control_style(self, is_dark)
        # 生成初始UUID
        self.generate_uuids()

    def refresh_theme(self, main_object):
        """刷新主题"""
        style_util.set_dialog_control_style(self, main_object.is_dark)

    def init_ui(self):
        # 主部件和布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # 选项区域
        options_layout = QVBoxLayout()

        # UUID长度选择
        length_layout = QHBoxLayout()
        length_label = QLabel("UUID长度:")
        length_label.setMinimumWidth(120)
        length_label.setStyleSheet("background: transparent;")
        length_layout.addWidget(length_label)

        self.length_combo = QComboBox()
        self.length_combo.setMinimumHeight(30)
        self.length_combo.addItems(["8", "16", "24", "32", "36 (有连接符)"])
        self.length_combo.setCurrentIndex(4)  # 默认选择36
        length_layout.addWidget(self.length_combo, 1)
        options_layout.addLayout(length_layout)

        # 生成数量
        count_layout = QHBoxLayout()
        count_label = QLabel("生成数量:")
        count_label.setMinimumWidth(120)
        count_label.setStyleSheet("background: transparent;")
        count_layout.addWidget(count_label)

        self.count_spin = QSpinBox()
        self.count_spin.setRange(1, 1000)
        self.count_spin.setValue(10)
        self.count_spin.setMinimumHeight(30)
        count_layout.addWidget(self.count_spin, 1)
        options_layout.addLayout(count_layout)

        # 分隔符
        separator_layout = QHBoxLayout()
        separator_label = QLabel("分隔符(支持\\n和\\t):")
        separator_label.setMinimumWidth(120)
        separator_label.setStyleSheet("background: transparent;")
        separator_layout.addWidget(separator_label)

        self.separator_input = QLineEdit(",\\n")
        self.separator_input.setMinimumHeight(30)
        separator_layout.addWidget(self.separator_input, 1)

        options_layout.addLayout(separator_layout)

        # 复选框选项
        checkboxes_layout = QHBoxLayout()

        self.uppercase_check = QCheckBox("大写字母")
        checkboxes_layout.addWidget(self.uppercase_check)

        self.quotes_check = QCheckBox("添加引号")
        checkboxes_layout.addWidget(self.quotes_check)

        options_layout.addLayout(checkboxes_layout)
        main_layout.addLayout(options_layout)

        # 按钮布局
        button_layout = QHBoxLayout()

        # 生成按钮
        generate_button = QPushButton("生成 UUID")
        generate_button.setMinimumHeight(30)
        generate_button.clicked.connect(self.generate_uuids)
        button_layout.addWidget(generate_button)

        # 复制按钮
        copy_button = QPushButton("复制 UUID")
        copy_button.setMinimumHeight(30)
        copy_button.clicked.connect(self.copy_uuids)
        button_layout.addWidget(copy_button)

        # 清空按钮
        clear_button = QPushButton("清空")
        clear_button.setMinimumHeight(30)
        clear_button.clicked.connect(self.clear_uuids)
        button_layout.addWidget(clear_button)

        main_layout.addLayout(button_layout)

        # UUID显示区域
        self.uuid_display = QTextEdit()
        self.uuid_display.setReadOnly(True)
        self.uuid_display.setWordWrapMode(QTextOption.WrapMode.WrapAnywhere)        # 禁用智能换行改为按照宽度换行
        main_layout.addWidget(self.uuid_display)

    def generate_uuids(self):
        """生成UUIDs并显示"""
        try:
            # 获取选项
            count = self.count_spin.value()
            separator = self.separator_input.text()
            uppercase = self.uppercase_check.isChecked()
            add_quotes = self.quotes_check.isChecked()

            # 处理分隔符中的转义字符
            separator = separator.replace("\\n", "\n").replace("\\t", "\t")

            # 获取长度选项
            length_option = self.length_combo.currentText()
            if length_option == "36 (有连接符)":
                format_length = 36
                use_hyphens = True
            else:
                format_length = int(length_option)
                use_hyphens = False

            # 生成UUIDs
            uuids = []
            for _ in range(count):
                # 生成UUID4
                uuid_obj = uuid.uuid4()

                # 根据选项格式化
                if use_hyphens:
                    uuid_str = str(uuid_obj)
                else:
                    uuid_str = uuid_obj.hex[:format_length]

                # 应用大写选项
                if uppercase:
                    uuid_str = uuid_str.upper()

                # 应用引号选项
                if add_quotes:
                    uuid_str = f'"{uuid_str}"'

                uuids.append(uuid_str)

            # 使用分隔符连接所有UUID
            result = separator.join(uuids)

            # 显示结果
            self.uuid_display.setPlainText(result)

        except Exception as e:
            dialog_module.box_information(self.use_parent, "错误", f"生成UUID时出错: {str(e)}")

    def copy_uuids(self):
        """复制UUIDs到剪贴板"""
        if not self.uuid_display.toPlainText().strip():
            dialog_module.box_information(self.use_parent, "提示", "没有UUID可复制")
            return
        QApplication.clipboard().setText(self.uuid_display.toPlainText())
        dialog_module.box_information(self.use_parent, "复制成功", "UUID已复制到剪贴板")

    def clear_uuids(self):
        """清空UUID显示区域"""
        self.uuid_display.clear()