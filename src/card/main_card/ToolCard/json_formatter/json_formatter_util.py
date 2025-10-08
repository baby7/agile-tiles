import json
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton,
                               QComboBox, QLabel, QSplitter, QGroupBox)
from PySide6.QtCore import Qt, QRect, QSize, Signal, QPoint
from PySide6.QtGui import QFont, QTextOption, QColor, QPainter

from src.my_component.AgileTilesAcrylicWindow.AgileTilesAcrylicWindow import AgileTilesAcrylicWindow
from src.module.Box import message_box_util
from src.ui import style_util


class LineNumberArea(QWidget):
    """行号区域部件"""

    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)


class NumberedTextEdit(QTextEdit):
    """带行号显示的文本编辑器"""
    # 定义信号
    blockCountChanged = Signal(int)
    updateRequest = Signal(QRect, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.line_number_area = LineNumberArea(self)

        # 连接信号和槽
        self.document().blockCountChanged.connect(self._on_block_count_changed)
        self.verticalScrollBar().valueChanged.connect(self._on_scroll)
        self.cursorPositionChanged.connect(self._on_cursor_position_changed)

        self.updateRequest.connect(self.update_line_number_area)
        self.blockCountChanged.connect(self.update_line_number_area_width)

        self.update_line_number_area_width(0)

    def _on_block_count_changed(self, new_block_count):
        """处理文档块数量变化的信号"""
        self.blockCountChanged.emit(new_block_count)

    def _on_scroll(self):
        """处理滚动事件"""
        self.updateRequest.emit(self.viewport().rect(), 0)

    def _on_cursor_position_changed(self):
        """处理光标位置变化"""
        self.updateRequest.emit(self.viewport().rect(), 0)

    def line_number_area_width(self):
        """计算行号区域的宽度"""
        digits = 1
        count = max(1, self.document().blockCount())
        while count >= 10:
            count //= 10
            digits += 1
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def update_line_number_area_width(self, _):
        """更新边距以容纳行号区域"""
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        """更新行号区域"""
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        """重写 resize 事件"""
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(),
                                                self.line_number_area_width(), cr.height()))

    def firstVisibleBlock(self):
        """获取第一个可见的文本块"""
        # 通过光标位置找到第一个可见块
        cursor = self.cursorForPosition(QPoint(0, 0))
        return cursor.block()

    def blockBoundingGeometry(self, block):
        """获取文本块的几何信息"""
        # 使用文档布局获取块的边界矩形
        block_rect = self.document().documentLayout().blockBoundingRect(block)
        # 转换为整数坐标
        return QRect(
            int(block_rect.x()),
            int(block_rect.y()),
            int(block_rect.width()),
            int(block_rect.height())
        )

    def contentOffset(self):
        """获取内容偏移量"""
        # 返回视图端口的内容偏移量
        return QPoint(self.horizontalScrollBar().value(), self.verticalScrollBar().value())

    def blockBoundingRect(self, block):
        """获取文本块的边界矩形"""
        # 使用文档布局获取块的边界矩形
        block_rect = self.document().documentLayout().blockBoundingRect(block)
        # 转换为整数坐标
        return QRect(
            int(block_rect.x()),
            int(block_rect.y()),
            int(block_rect.width()),
            int(block_rect.height())
        )

    def line_number_area_paint_event(self, event):
        """绘制行号"""
        painter = QPainter(self.line_number_area)
        # painter.fillRect(event.rect(), QColor(240, 240, 240))

        # 获取第一个可见块
        block = self.firstVisibleBlock()
        if not block.isValid():
            return

        block_number = block.blockNumber()
        # 获取块的几何信息并应用内容偏移
        block_geom = self.blockBoundingGeometry(block)
        content_offset = self.contentOffset()
        top = block_geom.translated(-content_offset).top()
        bottom = top + self.blockBoundingRect(block).height()

        # 只绘制可见区域的行号
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor(100, 100, 100))
                painter.drawText(0, int(top), self.line_number_area.width() - 3,
                                 self.fontMetrics().height(),
                                 Qt.AlignRight, number)

            block = block.next()
            if not block.isValid():
                break

            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1



class JSONFormatter(AgileTilesAcrylicWindow):
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
        self.setMinimumSize(1200, 800)
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

        # 第一个QGroupBox - 缩进、驼峰、应用键名转换
        group_box1 = QGroupBox("选项操作功能")
        group_box1.setStyleSheet("QGroupBox{border: 1px solid rgba(125, 125, 125, 125); padding: 8px;}")
        group_box1.setMinimumHeight(50)
        toolbar_layout1 = QHBoxLayout()
        toolbar_layout1.setSpacing(10)

        # 缩进选择
        indent_label = QLabel("缩进:")
        indent_label.setStyleSheet("background: transparent;")
        self.indent_combo = QComboBox()
        self.indent_combo.setMinimumHeight(30)
        self.indent_combo.addItems(["2空格", "4空格", "制表符"])
        self.indent_combo.setCurrentIndex(1)
        toolbar_layout1.addWidget(indent_label)
        toolbar_layout1.addWidget(self.indent_combo)

        # 驼峰转换选项
        camel_label = QLabel("键名转换:")
        camel_label.setStyleSheet("background: transparent;")
        self.camel_case_combo = QComboBox()
        self.camel_case_combo.setMinimumHeight(30)
        self.camel_case_combo.addItems(["小驼峰", "大驼峰", "下划线"])
        toolbar_layout1.addWidget(camel_label)
        toolbar_layout1.addWidget(self.camel_case_combo)

        self.convert_keys_btn = QPushButton("应用")
        self.convert_keys_btn.setMinimumWidth(80)
        self.convert_keys_btn.setMinimumHeight(30)
        self.convert_keys_btn.clicked.connect(self.convert_keys)
        toolbar_layout1.addWidget(self.convert_keys_btn)

        toolbar_layout1.addStretch(1)  # 添加弹性空间
        group_box1.setLayout(toolbar_layout1)

        # 第二个QGroupBox - 其他操作功能
        group_box2 = QGroupBox("直接操作功能")
        group_box2.setStyleSheet("QGroupBox{border: 1px solid rgba(125, 125, 125, 125); padding: 8px;}")
        group_box2.setMinimumHeight(50)
        toolbar_layout2 = QHBoxLayout()
        toolbar_layout2.setSpacing(10)

        # 功能按钮
        self.format_btn = QPushButton("格式化")
        self.format_btn.setMinimumWidth(80)
        self.format_btn.setMinimumHeight(30)
        self.format_btn.clicked.connect(self.format_json)
        toolbar_layout2.addWidget(self.format_btn)

        self.compress_btn = QPushButton("压缩")
        self.compress_btn.setMinimumWidth(60)
        self.compress_btn.setMinimumHeight(30)
        self.compress_btn.clicked.connect(self.compress_json)
        toolbar_layout2.addWidget(self.compress_btn)

        self.validate_btn = QPushButton("校验")
        self.validate_btn.setMinimumWidth(60)
        self.validate_btn.setMinimumHeight(30)
        self.validate_btn.clicked.connect(self.validate_json)
        toolbar_layout2.addWidget(self.validate_btn)

        self.escape_btn = QPushButton("转义")
        self.escape_btn.setMinimumWidth(60)
        self.escape_btn.setMinimumHeight(30)
        self.escape_btn.clicked.connect(self.escape_json)
        toolbar_layout2.addWidget(self.escape_btn)

        self.unescape_btn = QPushButton("去除转义")
        self.unescape_btn.setMinimumWidth(100)
        self.unescape_btn.setMinimumHeight(30)
        self.unescape_btn.clicked.connect(self.unescape_json)
        toolbar_layout2.addWidget(self.unescape_btn)

        self.unicode_to_cn_btn = QPushButton("Unicode转中文")
        self.unicode_to_cn_btn.setMinimumWidth(150)
        self.unicode_to_cn_btn.setMinimumHeight(30)
        self.unicode_to_cn_btn.clicked.connect(self.unicode_to_chinese)
        toolbar_layout2.addWidget(self.unicode_to_cn_btn)

        self.cn_to_unicode_btn = QPushButton("中文转Unicode")
        self.cn_to_unicode_btn.setMinimumWidth(150)
        self.cn_to_unicode_btn.setMinimumHeight(30)
        self.cn_to_unicode_btn.clicked.connect(self.chinese_to_unicode)
        toolbar_layout2.addWidget(self.cn_to_unicode_btn)

        self.sort_asc_btn = QPushButton("键名正序")
        self.sort_asc_btn.setMinimumWidth(100)
        self.sort_asc_btn.setMinimumHeight(30)
        self.sort_asc_btn.clicked.connect(self.sort_json_asc)
        toolbar_layout2.addWidget(self.sort_asc_btn)

        self.sort_desc_btn = QPushButton("键名倒序")
        self.sort_desc_btn.setMinimumWidth(100)
        self.sort_desc_btn.setMinimumHeight(30)
        self.sort_desc_btn.clicked.connect(self.sort_json_desc)
        toolbar_layout2.addWidget(self.sort_desc_btn)

        toolbar_layout2.addStretch(1)  # 添加弹性空间
        group_box2.setLayout(toolbar_layout2)

        # 将两个QGroupBox添加到主布局
        main_layout.addWidget(group_box1)
        main_layout.addWidget(group_box2)

        # 创建分割器放置两个文本编辑框
        splitter = QSplitter(Qt.Horizontal)
        splitter.setChildrenCollapsible(False)

        # 左侧输入区域
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)

        input_label = QLabel("JSON输入")
        left_layout.addWidget(input_label)

        # 输入文本框
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("请输入JSON内容...")
        self.input_text.setFont(QFont("Consolas", 11))
        self.input_text.setWordWrapMode(QTextOption.WrapAnywhere)
        left_layout.addWidget(self.input_text)

        # 右侧输出区域
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)

        output_label = QLabel("处理结果")
        right_layout.addWidget(output_label)

        # 输出文本框 - 使用带行号的版本
        self.output_text = NumberedTextEdit()
        self.output_text.setPlaceholderText("格式化结果将显示在这里...")
        self.output_text.setFont(QFont("Consolas", 11))
        self.output_text.setReadOnly(True)
        self.output_text.setWordWrapMode(QTextOption.WrapAnywhere)
        right_layout.addWidget(self.output_text)

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([600, 600])

        main_layout.addWidget(splitter, 1)  # 1表示拉伸因子

        # 状态栏
        # self.statusBar().showMessage('就绪')

    def get_json_text(self):
        """获取输入文本"""
        return self.input_text.toPlainText().strip()

    def set_output_text(self, text):
        """设置输出文本"""
        self.output_text.setPlainText(text)

    def show_error(self, message):
        """显示错误信息"""
        message_box_util.box_information(self.use_parent, "错误", message)
        # self.statusBar().showMessage(f"错误: {message}")

    def show_success(self, message):
        """显示成功信息"""
        pass
        # self.statusBar().showMessage(message)

    def get_indent(self):
        """获取缩进设置"""
        indent_option = self.indent_combo.currentText()
        if indent_option == "2空格":
            return 2
        elif indent_option == "4空格":
            return 4
        elif indent_option == "制表符":
            return "\t"
        return 4

    def try_parse_json(self, text):
        """尝试解析JSON，返回解析后的对象或None"""
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            self.show_error(f"JSON解析错误: {str(e)}")
            return None

    def format_json(self):
        """格式化JSON"""
        text = self.get_json_text()
        if not text:
            self.show_error("输入为空")
            return

        parsed = self.try_parse_json(text)
        if parsed is None:
            return

        indent = self.get_indent()
        try:
            formatted = json.dumps(parsed, indent=indent, ensure_ascii=False)
            self.set_output_text(formatted)
            self.show_success("格式化成功")
        except Exception as e:
            self.show_error(f"格式化失败: {str(e)}")

    def compress_json(self):
        """压缩JSON"""
        text = self.get_json_text()
        if not text:
            self.show_error("输入为空")
            return

        parsed = self.try_parse_json(text)
        if parsed is None:
            return

        try:
            compressed = json.dumps(parsed, separators=(',', ':'), ensure_ascii=False)
            self.set_output_text(compressed)
            self.show_success("压缩成功")
        except Exception as e:
            self.show_error(f"压缩失败: {str(e)}")

    def validate_json(self):
        """校验JSON"""
        text = self.get_json_text()
        if not text:
            self.show_error("输入为空")
            return

        try:
            json.loads(text)
            self.show_success("JSON格式正确")
            message_box_util.box_information(self.use_parent, "校验结果", "JSON格式正确")
        except json.JSONDecodeError as e:
            self.show_error(f"JSON格式错误: {str(e)}")

    def escape_json(self):
        """转义JSON字符串"""
        text = self.get_json_text()
        if not text:
            self.show_error("输入为空")
            return

        try:
            # 将文本作为字符串处理，而不是JSON对象
            escaped = json.dumps(text, ensure_ascii=False)
            self.set_output_text(escaped)
            self.show_success("转义成功")
        except Exception as e:
            self.show_error(f"转义失败: {str(e)}")

    def unescape_json(self):
        """去除转义"""
        text = self.get_json_text()
        if not text:
            self.show_error("输入为空")
            return

        try:
            # 尝试解析JSON字符串
            unescaped = json.loads(text)
            # 如果解析后是字符串，直接显示
            if isinstance(unescaped, str):
                self.set_output_text(unescaped)
            else:
                # 如果是其他类型，转换为JSON字符串
                self.set_output_text(json.dumps(unescaped, ensure_ascii=False))
            self.show_success("去除转义成功")
        except Exception as e:
            self.show_error(f"去除转义失败: {str(e)}")

    def unicode_to_chinese(self):
        """Unicode转中文"""
        text = self.get_json_text()
        if not text:
            self.show_error("输入为空")
            return

        try:
            # 先解析JSON，然后确保输出时不使用ASCII编码
            parsed = json.loads(text)
            converted = json.dumps(parsed, indent=self.get_indent(), ensure_ascii=False)
            self.set_output_text(converted)
            self.show_success("Unicode转中文成功")
        except Exception as e:
            self.show_error(f"Unicode转中文失败: {str(e)}")

    def chinese_to_unicode(self):
        """中文转Unicode"""
        text = self.get_json_text()
        if not text:
            self.show_error("输入为空")
            return

        try:
            # 解析JSON，然后使用ASCII编码输出
            parsed = json.loads(text)
            converted = json.dumps(parsed, indent=self.get_indent(), ensure_ascii=True)
            self.set_output_text(converted)
            self.show_success("中文转Unicode成功")
        except Exception as e:
            self.show_error(f"中文转Unicode失败: {str(e)}")

    def sort_json_asc(self):
        """键名正序排序"""
        text = self.get_json_text()
        if not text:
            self.show_error("输入为空")
            return

        parsed = self.try_parse_json(text)
        if parsed is None:
            return

        try:
            sorted_json = self._sort_json_object(parsed, reverse=False)
            formatted = json.dumps(sorted_json, indent=self.get_indent(), ensure_ascii=False)
            self.set_output_text(formatted)
            self.show_success("键名正序排序成功")
        except Exception as e:
            self.show_error(f"排序失败: {str(e)}")

    def sort_json_desc(self):
        """键名倒序排序"""
        text = self.get_json_text()
        if not text:
            self.show_error("输入为空")
            return

        parsed = self.try_parse_json(text)
        if parsed is None:
            return

        try:
            sorted_json = self._sort_json_object(parsed, reverse=True)
            formatted = json.dumps(sorted_json, indent=self.get_indent(), ensure_ascii=False)
            self.set_output_text(formatted)
            self.show_success("键名倒序排序成功")
        except Exception as e:
            self.show_error(f"排序失败: {str(e)}")

    def _sort_json_object(self, obj, reverse=False):
        """递归排序JSON对象的键"""
        if isinstance(obj, dict):
            sorted_obj = {}
            for key in sorted(obj.keys(), reverse=reverse):
                sorted_obj[key] = self._sort_json_object(obj[key], reverse)
            return sorted_obj
        elif isinstance(obj, list):
            return [self._sort_json_object(item, reverse) for item in obj]
        else:
            return obj

    def convert_keys(self):
        """键名转换"""
        text = self.get_json_text()
        if not text:
            self.show_error("输入为空")
            return

        parsed = self.try_parse_json(text)
        if parsed is None:
            return

        try:
            # 获取选择的转换类型
            conversion_type = self.camel_case_combo.currentText()

            if conversion_type == "小驼峰":
                converted = self._convert_keys_to_camel_case(parsed, lower_first=True)
            elif conversion_type == "大驼峰":
                converted = self._convert_keys_to_camel_case(parsed, lower_first=False)
            elif conversion_type == "下划线":
                converted = self._convert_keys_to_snake_case(parsed)
            else:
                converted = parsed

            formatted = json.dumps(converted, indent=self.get_indent(), ensure_ascii=False)
            self.set_output_text(formatted)
            self.show_success("键名转换成功")
        except Exception as e:
            self.show_error(f"键名转换失败: {str(e)}")

    def _convert_keys_to_camel_case(self, obj, lower_first=True):
        """递归将对象中的键转换为驼峰命名

        Args:
            obj: 要转换的JSON对象
            lower_first: 是否将第一个字母小写(小驼峰)
        """
        if isinstance(obj, dict):
            new_dict = {}
            for key, value in obj.items():
                # 将键转换为驼峰命名
                camel_key = self._to_camel_case(key, lower_first)
                new_dict[camel_key] = self._convert_keys_to_camel_case(value, lower_first)
            return new_dict
        elif isinstance(obj, list):
            return [self._convert_keys_to_camel_case(item, lower_first) for item in obj]
        else:
            return obj

    def _convert_keys_to_snake_case(self, obj):
        """递归将对象中的键转换为下划线命名"""
        if isinstance(obj, dict):
            new_dict = {}
            for key, value in obj.items():
                # 将键转换为下划线命名
                snake_key = self._to_snake_case(key)
                new_dict[snake_key] = self._convert_keys_to_snake_case(value)
            return new_dict
        elif isinstance(obj, list):
            return [self._convert_keys_to_snake_case(item) for item in obj]
        else:
            return obj

    def _to_camel_case(self, s, lower_first=True):
        """将字符串转换为驼峰命名

        Args:
            s: 要转换的字符串
            lower_first: 是否将第一个字母小写(小驼峰)
        """
        # 先转换为下划线格式的统一格式
        s = self._to_snake_case(s)

        # 分割单词并转换为驼峰
        parts = s.split('_')
        if not parts:
            return s

        result = parts[0].lower() if lower_first else parts[0].capitalize()
        for part in parts[1:]:
            if part:
                result += part.capitalize()

        return result

    def _to_snake_case(self, s):
        """将字符串转换为下划线命名"""
        # 如果已经是下划线命名，直接返回
        if '_' in s and s.islower():
            return s

        # 处理驼峰命名
        result = []
        for i, c in enumerate(s):
            if c.isupper():
                if i > 0 and s[i - 1].islower():
                    result.append('_')
                if i > 0 and i < len(s) - 1 and s[i + 1].islower():
                    result.append('_')
                result.append(c.lower())
            else:
                result.append(c)

        return ''.join(result).replace('__', '_')


def show_json_formatter_dialog(main_object, title, content):
    """显示json格式化对话框"""
    dialog = JSONFormatter(None, main_object, title, content)
    dialog.refresh_geometry(main_object.toolkit.resolution_util.get_screen(main_object))
    dialog.show()
    return dialog