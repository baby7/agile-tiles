import json

from PySide6 import QtCore
from PySide6.QtCore import Slot, QUrl, Qt
from PySide6.QtGui import QIcon, QAction
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QPushButton, QTextEdit, \
    QApplication, QMenu, QPlainTextEdit

from src.card.MainCardManager.MainCard import MainCard
from src.client import common
from src.ui import style_util


class TranslateCard(MainCard):

    title = "翻译"
    name = "TranslateCard"
    support_size_list = ["Big"]
    # 只读参数
    x = None                # 坐标x
    y = None                # 坐标y
    size = None             # 大小(1_1:Point、1_2:MiniHor、2_1MiniVer、2_2Block、2_5)
    theme = None            # 主题(Light、Dark)
    width = 0               # 宽度
    height = 0              # 高度
    fillet_corner = 0       # 圆角大小
    # 可使用
    card = None             # 卡片本体
    data = None             # 数据
    toolkit = None          # 工具箱，具体参考文档
    logger = None           # 日志记录工具
    # 可调用
    save_data_func = None   # 保存数据(传参为一个字典)
    #
    is_first = True
    need_refresh_ui = False
    # 模块列表
    aggregation_module_list = []


    def __init__(self, main_object=None, parent=None, theme=None, card=None, cache=None, data=None,
                 toolkit=None, logger=None, save_data_func=None):
        super().__init__(main_object=main_object, parent=parent, theme=theme, card=card, cache=cache, data=data,
                         toolkit=toolkit, logger=logger, save_data_func=save_data_func)
        # 当前翻译引擎
        self.current_engine = "百度"
        # 网络管理器
        self.network_manager = QNetworkAccessManager(self)

    def init_ui(self):
        super().init_ui()
        # 创建主控件
        central_widget = QWidget(self.card)
        central_widget.setGeometry(QtCore.QRect(0, 0, self.card.width(), self.card.height()))
        central_widget.setStyleSheet("background-color: transparent; border: none;")

        # 主布局
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # 顶部信息条
        self.info_bar = QLabel()
        self.info_bar.setAlignment(Qt.AlignCenter)
        self.info_bar.setFixedHeight(30)
        self.info_bar.setContentsMargins(5, 0, 5, 0)
        self.info_bar.setStyleSheet("font-weight: bold; font-size: 12px;")
        main_layout.addWidget(self.info_bar)

        # 顶部工具栏
        toolbar_layout = QHBoxLayout()
        main_layout.addLayout(toolbar_layout)

        # 引擎选择下拉框
        self.engine_combo = QComboBox()
        self.engine_combo.setMinimumHeight(24)
        self.engine_combo.setMinimumWidth(60)
        self.engine_combo.addItems(["百度", "有道"])
        self.engine_combo.currentTextChanged.connect(self.set_engine)
        toolbar_layout.addWidget(self.engine_combo)
        toolbar_layout.addStretch()

        # 源语言下拉框
        self.source_lang_combo = QComboBox()
        self.source_lang_combo.setMinimumHeight(24)
        self.source_lang_combo.setMinimumWidth(40)
        self.source_lang_combo.addItems(["英", "中", "日", "韩", "俄", "法", "德"])
        self.source_lang_combo.setCurrentText("英")
        toolbar_layout.addWidget(self.source_lang_combo)

        # 切换按钮
        self.swap_button = QPushButton()
        self.swap_button.setMinimumHeight(24)
        self.swap_button.setMinimumWidth(30)
        self.swap_button.setIcon(QIcon.fromTheme("swap"))
        self.swap_button.setToolTip("切换语言")
        self.swap_button.clicked.connect(self.swap_languages)
        toolbar_layout.addWidget(self.swap_button)

        # 目标语言下拉框
        self.target_lang_combo = QComboBox()
        self.target_lang_combo.setMinimumHeight(24)
        self.target_lang_combo.setMinimumWidth(40)
        self.target_lang_combo.addItems(["中", "英", "日", "韩", "俄", "法", "德"])
        self.target_lang_combo.setCurrentText("中")
        toolbar_layout.addWidget(self.target_lang_combo)
        toolbar_layout.addStretch()

        # 翻译按钮
        self.translate_button = QPushButton("翻译")
        self.translate_button.setMinimumHeight(24)
        self.translate_button.setMinimumWidth(60)
        self.translate_button.clicked.connect(self.translate_text)
        toolbar_layout.addWidget(self.translate_button)

        # 文本编辑区域
        text_layout = QVBoxLayout()
        main_layout.addLayout(text_layout, 1)

        # 源文本输入
        self.source_text = QPlainTextEdit()
        self.source_text.setPlaceholderText("输入要翻译的文本...")
        self.source_text.setContextMenuPolicy(Qt.CustomContextMenu)
        self.source_text.customContextMenuRequested.connect(self.show_source_context_menu)
        self.source_text.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # 设置最大文本长度（5000字符）
        self.source_text.textChanged.connect(self.limit_text_length)
        text_layout.addWidget(self.source_text)

        # 目标文本显示
        self.target_text = QPlainTextEdit()
        self.target_text.setPlaceholderText("翻译结果将显示在这里...")
        self.target_text.setContextMenuPolicy(Qt.CustomContextMenu)
        self.target_text.customContextMenuRequested.connect(self.show_target_context_menu)
        self.source_text.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        text_layout.addWidget(self.target_text)

        # 状态栏布局
        status_widget = QWidget()
        status_layout = QHBoxLayout(status_widget)
        status_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(status_widget)

        # 状态标签（左对齐）
        self.status_label = QLabel("就绪 | 当前引擎: 百度")
        status_layout.addWidget(self.status_label)

        # 添加弹簧使复制按钮右对齐
        status_layout.addStretch(1)

        # 清空按钮（右对齐）
        self.clear_button = QPushButton("清空")
        self.clear_button.setMinimumHeight(24)
        self.clear_button.setMinimumWidth(60)
        self.clear_button.clicked.connect(self.clear_text)
        status_layout.addWidget(self.clear_button)

        # 复制结果按钮（右对齐）
        self.copy_button = QPushButton("复制结果")
        self.copy_button.setMinimumHeight(24)
        self.copy_button.setMinimumWidth(80)
        self.copy_button.clicked.connect(self.copy_result)
        status_layout.addWidget(self.copy_button)

        # 填充部分信息
        self.set_info_bar(0)
        # 请求并更新对话次数信息
        self.update_call_count()

    def show_source_context_menu(self, position):
        # 创建中文右键菜单
        menu = QMenu()

        # 添加菜单项
        undo_action = QAction("撤销", self.source_text)
        undo_action.triggered.connect(self.source_text.undo)
        menu.addAction(undo_action)

        redo_action = QAction("重做", self.source_text)
        redo_action.triggered.connect(self.source_text.redo)
        menu.addAction(redo_action)

        menu.addSeparator()

        cut_action = QAction("剪切", self.source_text)
        cut_action.triggered.connect(self.source_text.cut)
        menu.addAction(cut_action)

        copy_action = QAction("复制", self.source_text)
        copy_action.triggered.connect(self.source_text.copy)
        menu.addAction(copy_action)

        paste_action = QAction("粘贴", self.source_text)
        paste_action.triggered.connect(self.source_text.paste)
        menu.addAction(paste_action)

        menu.addSeparator()

        select_all_action = QAction("全选", self.source_text)
        select_all_action.triggered.connect(self.source_text.selectAll)
        menu.addAction(select_all_action)

        menu.addSeparator()

        # 翻译选中文本
        translate_selected_action = QAction("翻译选中文本", self.source_text)
        translate_selected_action.triggered.connect(self.translate_selected_text)
        menu.addAction(translate_selected_action)

        # 显示菜单
        menu.exec_(self.source_text.viewport().mapToGlobal(position))

    def show_target_context_menu(self, position):
        # 创建中文右键菜单（简化版）
        menu = QMenu()

        copy_action = QAction("复制", self.target_text)
        copy_action.triggered.connect(self.target_text.copy)
        menu.addAction(copy_action)

        select_all_action = QAction("全选", self.target_text)
        select_all_action.triggered.connect(self.target_text.selectAll)
        menu.addAction(select_all_action)

        menu.addSeparator()

        # 复制到源文本框
        copy_to_source_action = QAction("复制到源文本框", self.target_text)
        copy_to_source_action.triggered.connect(self.copy_to_source)
        menu.addAction(copy_to_source_action)

        # 显示菜单
        menu.exec_(self.target_text.viewport().mapToGlobal(position))

    def translate_selected_text(self):
        # 获取选中的文本
        cursor = self.source_text.textCursor()
        selected_text = cursor.selectedText().strip()

        if selected_text:
            # 设置选中文本为源文本
            self.source_text.setPlainText(selected_text)
            # 触发翻译
            self.translate_text()
        else:
            # 如果没有选中文本，翻译全部文本
            self.translate_text()

    def copy_to_source(self):
        # 将目标文本框内容复制到源文本框
        text = self.target_text.toPlainText().strip()
        if text:
            self.source_text.setPlainText(text)
            self.status_label.setText("已复制到源文本框")

    def update_call_count(self):
        """请求并更新对话次数信息"""
        url = QUrl(common.BASE_URL + "/translate/todayCalls")
        request = QNetworkRequest(url)
        request.setRawHeader(b"Authorization", bytes(self.main_object.token, "utf-8"))

        # 使用临时网络管理器获取调用次数
        temp_manager = QNetworkAccessManager(self)
        reply = temp_manager.get(request)

        def handle_reply():
            if reply.error() == QNetworkReply.NoError:
                data = reply.readAll()
                json_data = json.loads(str(data, 'utf-8'))
                today_calls = json_data.get("data", 0)

                # 根据会员状态显示不同信息
                self.set_info_bar(today_calls)
            else:
                error = reply.errorString()
                print(f"获取调用次数失败: {error}")
                self.info_bar.setText("获取对话次数信息失败")
                self.info_bar.setStyleSheet(
                    "background-color: rgba(255, 255, 255, 0.1); "
                    "border-radius: 5px; "
                    "color: orange; "
                    "font-weight: bold; "
                    "font-size: 12px;"
                )

            reply.deleteLater()

        reply.finished.connect(handle_reply)

    def set_info_bar(self, today_calls):
        # 根据会员状态显示不同信息
        if self.main_object.is_vip:
            text = f"会员用户无对话次数限制，今天已使用{today_calls}次"
            color = "rgba(4, 115, 247, 0.8)"
        else:
            text = f"非会员每天限制10次对话，今天已使用{today_calls}次"
            color = "rgba(243, 207, 19, 0.8)"

        # 根据主题设置背景
        if self.is_dark:
            bg_color = "rgba(255, 255, 255, 0.1)"
        else:
            bg_color = "rgb(255, 255, 255)"

        # 设置信息条样式和内容
        self.info_bar.setText(text)
        self.info_bar.setStyleSheet(
            f"background-color: {bg_color}; "
            f"border-radius: 5px; "
            f"color: {color}; "
            f"font-weight: bold; "
            f"font-size: 12px;"
        )

    def set_engine(self, engine):
        self.current_engine = engine
        self.status_label.setText(f"就绪 | 当前引擎: {engine}")

    def swap_languages(self):
        # 交换当前选择的语言
        source_lang = self.source_lang_combo.currentText()
        target_lang = self.target_lang_combo.currentText()

        self.source_lang_combo.setCurrentText(target_lang)
        self.target_lang_combo.setCurrentText(source_lang)

        # 交换文本内容
        # source_text = self.source_text.toPlainText()
        # target_text = self.target_text.toPlainText()
        #
        # self.source_text.setPlainText(target_text)
        # self.target_text.setPlainText(source_text)

    def limit_text_length(self):
        """限制文本框的最大字符数"""
        MAX_LENGTH = 5000  # 最大字符数

        # 确定是哪个文本框触发的
        text_edit = self.sender()

        # 获取当前文本
        text = text_edit.toPlainText()

        # 检查是否超过最大长度
        if len(text) > MAX_LENGTH:
            # 获取当前光标位置
            cursor = text_edit.textCursor()
            position = cursor.position()

            # 截断文本
            text_edit.blockSignals(True)  # 暂时阻塞信号，避免递归调用
            text_edit.setPlainText(text[:MAX_LENGTH])
            text_edit.blockSignals(False)

            # 恢复光标位置
            cursor.setPosition(min(position, MAX_LENGTH))
            text_edit.setTextCursor(cursor)

            # 显示提示信息
            self.status_label.setText(f"文本长度超过{MAX_LENGTH}字符，已自动截断")

    def translate_text(self):
        # 获取输入文本
        text = self.source_text.toPlainText().strip()
        if not text:
            self.target_text.setPlainText("")
            return

        # 获取语言代码
        source_lang = self.source_lang_combo.currentText()
        target_lang = self.target_lang_combo.currentText()

        try:
            source_code = LANG_CODES[self.current_engine][source_lang]
            target_code = LANG_CODES[self.current_engine][target_lang]
        except KeyError:
            self.target_text.setPlainText("错误: 不支持的语言组合")
            return

        # 准备请求数据
        engine = "youdao" if self.current_engine == "有道" else "baidu"
        data = {
            "engine": engine,
            "text": text,
            "sourceLang": source_code,
            "targetLang": target_code
        }

        # 创建网络请求
        url = QUrl(common.BASE_URL + "/translate")
        request = QNetworkRequest(url)
        request.setRawHeader(b"Authorization", bytes(self.main_object.token, "utf-8"))
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")

        # 发送POST请求
        self.status_label.setText("翻译中...")
        self.translate_button.setEnabled(False)

        reply = self.network_manager.post(
            request,
            json.dumps(data).encode('utf-8')
        )
        reply.finished.connect(lambda: self.handle_response(reply))

    @Slot()
    def handle_response(self, reply):
        # 请求并更新对话次数信息
        self.update_call_count()

        self.translate_button.setEnabled(True)

        # 检查错误
        if reply.error() != QNetworkReply.NoError:
            self.target_text.setPlainText(f"网络错误: {reply.errorString()}")
            self.status_label.setText("网络错误")
            reply.deleteLater()
            return

        # 解析响应
        data = reply.readAll().data()
        try:
            response = json.loads(data)
            if response.get("code") == 0:
                result = response.get("data", {}).get("result", "")
                self.target_text.setPlainText(result)
                self.status_label.setText("翻译完成")
            else:
                error_msg = response.get("msg", "未知错误")
                self.target_text.setPlainText(f"API错误: {error_msg}")
                self.status_label.setText("API错误")
        except json.JSONDecodeError:
            self.target_text.setPlainText("错误: 无效的响应格式")
            self.status_label.setText("解析错误")

        reply.deleteLater()

    def copy_result(self):
        clipboard = QApplication.clipboard()
        result_text = self.target_text.toPlainText()
        if result_text:
            clipboard.setText(result_text)
            self.status_label.setText("结果已复制到剪贴板")
        else:
            self.status_label.setText("无内容可复制")

    def clear_text(self):
        self.source_text.setPlainText("")
        self.target_text.setPlainText("")

    def refresh_data(self, date_time_str):
        super().refresh_data(date_time_str)

    def refresh_ui(self, date_time_str):
        super().refresh_ui(date_time_str)
        super().refresh_ui_end(date_time_str)

    def refresh_theme(self):
        if not super().refresh_theme():
            return False
        is_dark = self.is_dark()
        # 调整下拉框样式
        style_util.set_combo_box_style(self.engine_combo, is_dark)
        style_util.set_combo_box_style(self.source_lang_combo, is_dark)
        style_util.set_combo_box_style(self.target_lang_combo, is_dark)
        # 调整按钮样式
        style_util.set_button_style(self.translate_button, is_dark)
        style_util.set_button_style(self.copy_button, is_dark)
        style_util.set_button_style(self.clear_button, is_dark)
        # 调整交换按钮样式
        image_path = "static/img/IconPark/svg/Arrows/switch.svg"
        if is_dark:
            pixmap = self.toolkit.image_util.load_light_svg(image_path)
        else:
            pixmap = self.toolkit.image_util.load_dark_svg(image_path)
        self.swap_button.setIcon(QIcon(pixmap))
        # 字符串过滤区域样式调整
        if is_dark:
            text_edit_style = """
            QPlainTextEdit {
                border-radius: 10px;
                border: 1px solid white;
                background: transparent;
            }""" + style_util.scroll_bar_style
        else:
            text_edit_style = """
            QPlainTextEdit {
                border-radius: 10px;
                border: 1px solid black;
                background: transparent;
            }""" + style_util.scroll_bar_style
        self.source_text.setStyleSheet(text_edit_style)
        self.target_text.setStyleSheet(text_edit_style)
        # 提示信息
        self.info_bar.setStyleSheet("background: rgba(125, 125, 125, 60); font-weight: bold; font-size: 12px;")


# 语言代码映射
LANG_CODES = {
    "有道": {
        "中": "zh-CHS",
        "英": "en",
        "日": "ja",
        "韩": "ko",
        "俄": "ru",
        "法": "fr",
        "德": "de"
    },
    "百度": {
        "中": "zh",
        "英": "en",
        "日": "jp",
        "韩": "kor",
        "俄": "ru",
        "法": "fra",
        "德": "de"
    }
}