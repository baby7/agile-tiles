import os
import shutil
from pathlib import Path
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QListWidget, QPushButton, QCheckBox,
                               QGroupBox, QLineEdit, QLabel, QFileDialog, QRadioButton, QButtonGroup,
                               QSplitter, QTextEdit, QScrollArea)
from PySide6.QtCore import Qt, QThread, Signal

from src.my_component.AgileTilesAcrylicWindow.AgileTilesAcrylicWindow import AgileTilesAcrylicWindow
from src.module.Box import message_box_util
from src.ui import style_util


class RuleWidget(QWidget):
    """单个规则控件"""
    removeRequested = Signal(QWidget)

    def __init__(self, parent=None, rule_type="rename"):
        super().__init__(parent)
        self.rule_type = rule_type
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        if self.rule_type == "rename":
            self.find_input = QLineEdit()
            self.find_input.setPlaceholderText("关键字")
            self.replace_input = QLineEdit()
            self.replace_input.setPlaceholderText("替换为")

            layout.addWidget(QLabel("关键字:"))
            layout.addWidget(self.find_input)
            layout.addWidget(QLabel("替换为:"))
            layout.addWidget(self.replace_input)
        else:  # delete rule
            self.rule_input = QLineEdit()
            self.rule_input.setPlaceholderText("输入匹配规则（如 .txt 或 temp）")
            layout.addWidget(self.rule_input)

        self.remove_btn = QPushButton("删除")
        self.remove_btn.clicked.connect(lambda: self.removeRequested.emit(self))
        layout.addWidget(self.remove_btn)

    def get_rule(self):
        if self.rule_type == "rename":
            return (self.find_input.text(), self.replace_input.text())
        else:
            return self.rule_input.text()


class FileWorker(QThread):
    """后台文件操作线程"""
    progress = Signal(str)
    finished = Signal()
    error = Signal(str)

    def __init__(self, operation_type, file_list, rename_rules=None,
                 delete_rules=None, match_type="and", replace_ext=False):
        super().__init__()
        self.operation_type = operation_type  # "rename" 或 "delete"
        self.file_list = file_list
        self.rename_rules = rename_rules or []
        self.delete_rules = delete_rules or []
        self.match_type = match_type
        self.replace_ext = replace_ext
        self.is_canceled = False

    def run(self):
        try:
            if self.operation_type == "rename":
                self._perform_rename()
            elif self.operation_type == "delete":
                self._perform_delete()
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.finished.emit()

    def _perform_rename(self):
        for i, file_path in enumerate(self.file_list):
            if self.is_canceled:
                break

            try:
                path = Path(file_path)
                if not path.exists():
                    continue

                parent_dir = path.parent
                old_name = path.name if self.replace_ext else path.stem
                extension = "" if self.replace_ext else path.suffix

                # 应用所有重命名规则
                new_name = old_name
                for find, replace in self.rename_rules:
                    if find:  # 确保查找内容不为空
                        new_name = new_name.replace(find, replace)

                # 添加序号
                new_name = new_name.replace("{n}", str(i + 1))

                new_path = parent_dir / f"{new_name}{extension}"

                # 如果目标文件已存在，添加数字后缀
                counter = 1
                original_new_path = new_path
                while new_path.exists() and new_path != path:
                    name_part = original_new_path.stem
                    ext_part = original_new_path.suffix
                    new_path = original_new_path.parent / f"{name_part}_{counter}{ext_part}"
                    counter += 1

                if new_path != path:
                    path.rename(new_path)
                    self.progress.emit(f"重命名: {path.name} -> {new_path.name}")
            except Exception as e:
                self.error.emit(f"重命名 {file_path} 时出错: {str(e)}")

    def _perform_delete(self):
        for file_path in self.file_list:
            if self.is_canceled:
                break

            try:
                path = Path(file_path)
                if not path.exists():
                    continue

                name = path.name

                # 检查是否匹配删除规则
                should_delete = self._should_delete(name)

                if should_delete:
                    if path.is_file():
                        path.unlink()
                        self.progress.emit(f"删除文件: {name}")
                    else:
                        shutil.rmtree(path)
                        self.progress.emit(f"删除文件夹: {name}")
            except Exception as e:
                self.error.emit(f"删除 {file_path} 时出错: {str(e)}")

    def _should_delete(self, filename):
        if not self.delete_rules:
            return False

        name_without_ext = Path(filename).stem
        extension = Path(filename).suffix

        if self.match_type == "and":  # 所有规则都必须匹配
            for rule in self.delete_rules:
                rule = rule.strip()
                if not rule:
                    continue

                if rule.startswith("."):  # 扩展名规则
                    if extension != rule:
                        return False
                else:  # 文件名规则
                    if rule not in name_without_ext and rule not in filename:
                        return False
            return True
        else:  # "or" 任意规则匹配即可
            for rule in self.delete_rules:
                rule = rule.strip()
                if not rule:
                    continue

                if rule.startswith("."):  # 扩展名规则
                    if extension == rule:
                        return True
                else:  # 文件名规则
                    if rule in name_without_ext or rule in filename:
                        return True
            return False

    def cancel(self):
        self.is_canceled = True


class FileOperationDialog(AgileTilesAcrylicWindow):
    current_files = []
    rename_rules = []
    delete_rules = []
    worker = None

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
        self.setMinimumSize(1000, 700)
        # 初始化界面
        self.init_ui()
        # 设置样式
        style_util.set_dialog_control_style(self, self.is_dark)

    def init_ui(self):
        # 主部件和布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        self.widget_base.setLayout(main_layout)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # 创建选项卡
        self.tabs = QTabWidget()
        self.rename_tab = QWidget()
        self.delete_tab = QWidget()

        self.tabs.addTab(self.rename_tab, "批量重命名")
        self.tabs.addTab(self.delete_tab, "批量删除")

        # 设置重命名选项卡
        self._setup_rename_tab()
        # 设置删除选项卡
        self._setup_delete_tab()

        # 日志区域
        log_group = QGroupBox("操作日志")
        log_group.setStyleSheet("QGroupBox{border: 1px solid rgba(125, 125, 125, 125); padding-top: 8px;}")
        log_layout = QVBoxLayout()
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        log_group.setLayout(log_layout)

        # 添加到主布局
        main_layout.addWidget(self.tabs)
        main_layout.addWidget(log_group, 1)

    def _setup_rename_tab(self):
        layout = QVBoxLayout(self.rename_tab)

        # 上部：导入和控制区域
        control_group = QGroupBox("导入设置")
        control_group.setStyleSheet("QGroupBox{border: 1px solid rgba(125, 125, 125, 125); padding-top: 8px;}")
        control_layout = QHBoxLayout()

        self.include_subdirs_rename = QCheckBox("包含子文件夹")
        self.include_subdirs_rename.setChecked(True)

        self.import_btn_rename = QPushButton("导入文件夹")
        self.import_btn_rename.clicked.connect(self.import_folder_rename)

        self.clear_btn_rename = QPushButton("清空列表")
        self.clear_btn_rename.clicked.connect(self.clear_list_rename)

        control_layout.addWidget(self.include_subdirs_rename)
        control_layout.addStretch()
        control_layout.addWidget(self.import_btn_rename)
        control_layout.addWidget(self.clear_btn_rename)
        control_group.setLayout(control_layout)

        # 中部：文件列表和重命名设置
        mid_splitter = QSplitter(Qt.Horizontal)

        # 文件列表
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("文件列表:"))
        self.file_list_rename = QListWidget()
        self.file_list_rename.setStyleSheet("QListWidget{border: 1px solid rgba(125, 125, 125, 125);}")
        left_layout.addWidget(self.file_list_rename)
        left_widget.setLayout(left_layout)

        # 重命名设置
        right_widget = QWidget()
        right_layout = QVBoxLayout()

        rename_rule_group = QGroupBox("重命名规则")
        rename_rule_group.setStyleSheet("QGroupBox{border: 1px solid rgba(125, 125, 125, 125); padding-top: 8px;}")
        rule_layout = QVBoxLayout()

        # 规则列表区域
        rules_scroll = QScrollArea()
        rules_scroll.setWidgetResizable(True)
        rules_scroll.setMinimumHeight(200)

        self.rename_rules_widget = QWidget()
        self.rename_rules_layout = QVBoxLayout(self.rename_rules_widget)
        self.rename_rules_layout.addStretch()

        rules_scroll.setWidget(self.rename_rules_widget)

        # 添加规则按钮
        self.add_rename_rule_btn = QPushButton("添加规则")
        self.add_rename_rule_btn.clicked.connect(self.add_rename_rule)

        rule_help = QLabel("可用变量: {n}=序号\n规则将按顺序应用")
        rule_help.setWordWrap(True)

        self.replace_ext_checkbox = QCheckBox("应用规则到文件扩展名")
        self.replace_ext_checkbox.setChecked(True)

        rule_layout.addWidget(rules_scroll)
        rule_layout.addWidget(self.add_rename_rule_btn)
        rule_layout.addWidget(rule_help)
        rule_layout.addWidget(self.replace_ext_checkbox)
        rename_rule_group.setLayout(rule_layout)

        self.execute_rename_btn = QPushButton("执行重命名")
        self.execute_rename_btn.clicked.connect(self.execute_rename)

        right_layout.addWidget(rename_rule_group)
        right_layout.addStretch()
        right_layout.addWidget(self.execute_rename_btn)
        right_widget.setLayout(right_layout)

        mid_splitter.addWidget(left_widget)
        mid_splitter.addWidget(right_widget)
        mid_splitter.setSizes([400, 300])

        # 添加到重命名选项卡布局
        layout.addWidget(control_group)
        layout.addWidget(mid_splitter, 1)

        # 添加一个初始规则
        self.add_rename_rule()

    def _setup_delete_tab(self):
        layout = QVBoxLayout(self.delete_tab)

        # 上部：导入和控制区域
        control_group = QGroupBox("导入设置")
        control_group.setStyleSheet("QGroupBox{border: 1px solid rgba(125, 125, 125, 125); padding-top: 8px;}")
        control_layout = QHBoxLayout()

        self.include_subdirs_delete = QCheckBox("包含子文件夹")
        self.include_subdirs_delete.setChecked(True)

        self.import_btn_delete = QPushButton("导入文件夹")
        self.import_btn_delete.clicked.connect(self.import_folder_delete)

        self.clear_btn_delete = QPushButton("清空列表")
        self.clear_btn_delete.clicked.connect(self.clear_list_delete)

        control_layout.addWidget(self.include_subdirs_delete)
        control_layout.addStretch()
        control_layout.addWidget(self.import_btn_delete)
        control_layout.addWidget(self.clear_btn_delete)
        control_group.setLayout(control_layout)

        # 中部：文件列表和删除设置
        mid_splitter = QSplitter(Qt.Horizontal)

        # 文件列表
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("文件列表:"))
        self.file_list_delete = QListWidget()
        self.file_list_delete.setStyleSheet("QListWidget{border: 1px solid rgba(125, 125, 125, 125);}")
        left_layout.addWidget(self.file_list_delete)
        left_widget.setLayout(left_layout)

        # 删除设置
        right_widget = QWidget()
        right_layout = QVBoxLayout()

        delete_rule_group = QGroupBox("删除规则")
        delete_rule_group.setStyleSheet("QGroupBox{border: 1px solid rgba(125, 125, 125, 125); padding-top: 8px;}")
        rule_layout = QVBoxLayout()

        # 匹配类型
        match_type_layout = QHBoxLayout()
        match_type_layout.addWidget(QLabel("匹配类型:"))
        self.match_and = QRadioButton("与(AND)")
        self.match_or = QRadioButton("或(OR)")
        self.match_and.setChecked(True)

        match_type_group = QButtonGroup()
        match_type_group.addButton(self.match_and)
        match_type_group.addButton(self.match_or)

        match_type_layout.addWidget(self.match_and)
        match_type_layout.addWidget(self.match_or)
        match_type_layout.addStretch()

        # 规则列表区域
        rules_scroll = QScrollArea()
        rules_scroll.setWidgetResizable(True)
        rules_scroll.setMinimumHeight(200)

        self.delete_rules_widget = QWidget()
        self.delete_rules_layout = QVBoxLayout(self.delete_rules_widget)
        self.delete_rules_layout.addStretch()

        rules_scroll.setWidget(self.delete_rules_widget)

        # 添加规则按钮
        self.add_delete_rule_btn = QPushButton("添加规则")
        self.add_delete_rule_btn.clicked.connect(self.add_delete_rule)

        rule_help = QLabel("提示: 输入文件名部分或扩展名(如 .txt)")
        rule_help.setWordWrap(True)

        self.include_ext_checkbox = QCheckBox("包含文件扩展名")
        self.include_ext_checkbox.setChecked(True)

        rule_layout.addLayout(match_type_layout)
        rule_layout.addWidget(rules_scroll)
        rule_layout.addWidget(self.add_delete_rule_btn)
        rule_layout.addWidget(rule_help)
        rule_layout.addWidget(self.include_ext_checkbox)
        delete_rule_group.setLayout(rule_layout)

        self.execute_delete_btn = QPushButton("执行删除")
        self.execute_delete_btn.clicked.connect(self.execute_delete)

        right_layout.addWidget(delete_rule_group)
        right_layout.addStretch()
        right_layout.addWidget(self.execute_delete_btn)
        right_widget.setLayout(right_layout)

        mid_splitter.addWidget(left_widget)
        mid_splitter.addWidget(right_widget)
        mid_splitter.setSizes([400, 300])

        # 添加到删除选项卡布局
        layout.addWidget(control_group)
        layout.addWidget(mid_splitter, 1)

        # 添加一个初始规则
        self.add_delete_rule()

    def add_rename_rule(self):
        rule_widget = RuleWidget(rule_type="rename")
        rule_widget.removeRequested.connect(self.remove_rename_rule)
        self.rename_rules.append(rule_widget)
        self.rename_rules_layout.insertWidget(self.rename_rules_layout.count() - 1, rule_widget)

    def remove_rename_rule(self, rule_widget):
        if len(self.rename_rules) <= 1:
            message_box_util.box_information(self.use_parent, "警告", "至少需要保留一个规则")
            return

        self.rename_rules.remove(rule_widget)
        rule_widget.deleteLater()

    def add_delete_rule(self):
        rule_widget = RuleWidget(rule_type="delete")
        rule_widget.removeRequested.connect(self.remove_delete_rule)
        self.delete_rules.append(rule_widget)
        self.delete_rules_layout.insertWidget(self.delete_rules_layout.count() - 1, rule_widget)

    def remove_delete_rule(self, rule_widget):
        if len(self.delete_rules) <= 1:
            message_box_util.box_information(self.use_parent, "警告", "至少需要保留一个规则")
            return

        self.delete_rules.remove(rule_widget)
        rule_widget.deleteLater()

    def import_folder_rename(self):
        folder = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder:
            self._import_files(folder, self.include_subdirs_rename.isChecked(), self.file_list_rename)

    def import_folder_delete(self):
        folder = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder:
            self._import_files(folder, self.include_subdirs_delete.isChecked(), self.file_list_delete)

    def _import_files(self, folder, include_subdirs, list_widget):
        list_widget.clear()
        self.current_files.clear()

        try:
            if include_subdirs:
                for root, dirs, files in os.walk(folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        self.current_files.append(file_path)
                        list_widget.addItem(file_path)
                    for dir in dirs:
                        dir_path = os.path.join(root, dir)
                        self.current_files.append(dir_path)
                        list_widget.addItem(dir_path)
            else:
                for item in os.listdir(folder):
                    item_path = os.path.join(folder, item)
                    if os.path.exists(item_path):
                        self.current_files.append(item_path)
                        list_widget.addItem(item_path)

            self.log_text.append(f"已导入 {list_widget.count()} 个项目从 {folder}")
        except Exception as e:
            message_box_util.box_information(self.use_parent, "错误", f"导入文件时出错: {str(e)}")

    def clear_list_rename(self):
        self.file_list_rename.clear()
        self.current_files.clear()

    def clear_list_delete(self):
        self.file_list_delete.clear()
        self.current_files.clear()

    def execute_rename(self):
        if not self.current_files:
            message_box_util.box_information(self.use_parent, "警告", "请先导入文件或文件夹")
            return

        # 收集所有规则
        rename_rules = []
        for rule_widget in self.rename_rules:
            find, replace = rule_widget.get_rule()
            if find:  # 只有查找内容不为空时才添加规则
                rename_rules.append((find, replace))

        if not rename_rules:
            message_box_util.box_information(self.use_parent, "警告", "请至少添加一个有效的重命名规则")
            return

        # 确认操作
        confirm = message_box_util.box_acknowledgement(
            self.use_parent, "确认", f"确定要对 {len(self.current_files)} 个项目执行重命名操作吗?")
        if not confirm:
            return

        # 禁用按钮，防止重复操作
        self.execute_rename_btn.setEnabled(False)

        # 创建并启动工作线程
        self.worker = FileWorker(
            "rename",
            self.current_files,
            rename_rules=rename_rules,
            replace_ext=self.replace_ext_checkbox.isChecked()
        )
        self.worker.progress.connect(self.log_text.append)
        self.worker.finished.connect(self.on_operation_finished)
        self.worker.error.connect(self.on_operation_error)
        self.worker.start()

    def execute_delete(self):
        if not self.current_files:
            message_box_util.box_information(self.use_parent, "警告", "请先导入文件或文件夹")
            return

        # 收集所有规则
        delete_rules = []
        for rule_widget in self.delete_rules:
            rule = rule_widget.get_rule()
            if rule:  # 只有规则不为空时才添加
                delete_rules.append(rule)

        if not delete_rules:
            message_box_util.box_information(self.use_parent, "警告", "请至少添加一个有效的删除规则")
            return

        # 确认操作
        confirm = message_box_util.box_acknowledgement(
            self.use_parent, "确认", f"确定要对 {len(self.current_files)} 个项目执行删除操作吗?\n此操作不可撤销!")
        if not confirm:
            return

        # 禁用按钮，防止重复操作
        self.execute_delete_btn.setEnabled(False)

        # 创建并启动工作线程
        match_type = "and" if self.match_and.isChecked() else "or"
        self.worker = FileWorker(
            "delete",
            self.current_files,
            delete_rules=delete_rules,
            match_type=match_type,
            replace_ext=self.include_ext_checkbox.isChecked()
        )
        self.worker.progress.connect(self.log_text.append)
        self.worker.finished.connect(self.on_operation_finished)
        self.worker.error.connect(self.on_operation_error)
        self.worker.start()

    def on_operation_finished(self):
        if self.tabs.currentIndex() == 0:  # 重命名选项卡
            self.execute_rename_btn.setEnabled(True)
        else:  # 删除选项卡
            self.execute_delete_btn.setEnabled(True)
        self.log_text.append("操作完成!")
        # 清空列表
        if self.tabs.currentIndex() == 0:  # 重命名选项卡
            self.clear_list_rename()
        elif self.tabs.currentIndex() == 1:  # 删除选项卡
            self.clear_list_delete()

    def on_operation_error(self, error_msg):
        self.log_text.append(f"错误: {error_msg}")

    def closeEvent(self, event):
        # 确保在关闭应用前停止工作线程
        if self.worker and self.worker.isRunning():
            self.worker.cancel()
            self.worker.wait()
        event.accept()


def show_file_operation_dialog(main_object, title, content):
    """显示对话框"""
    dialog = FileOperationDialog(None, main_object, title, content)
    dialog.refresh_geometry(main_object.toolkit.resolution_util.get_screen(main_object))
    dialog.show()
    return dialog
