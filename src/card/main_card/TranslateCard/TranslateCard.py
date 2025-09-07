import json

from PySide6 import QtCore
from PySide6.QtCore import Slot, QUrl, Qt, QTimer
from PySide6.QtGui import QIcon, QAction, QCursor
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QPushButton, QApplication, QMenu, QPlainTextEdit

from src.card.MainCardManager.MainCard import MainCard
from src.module.Box import text_box_util
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
    # 调用次数
    today_calls = 0
    # ocr部分
    captured_pixmap = None


    def __init__(self, main_object=None, parent=None, theme=None, card=None, cache=None, data=None,
                 toolkit=None, logger=None, save_data_func=None):
        super().__init__(main_object=main_object, parent=parent, theme=theme, card=card, cache=cache, data=data,
                         toolkit=toolkit, logger=logger, save_data_func=save_data_func)
        # 当前翻译引擎
        self.current_engine = "有道"
        # 网络管理器
        self.network_manager = QNetworkAccessManager(self)

    def clear(self):
        try:
            try:
                self.swap_button.clicked.disconnect()
            except Exception as e:
                print(e)
            try:
                self.translate_button.clicked.disconnect()
            except Exception as e:
                print(e)
            try:
                self.clear_button.clicked.disconnect()
            except Exception as e:
                print(e)
            try:
                self.copy_button.clicked.disconnect()
            except Exception as e:
                print(e)
            try:
                self.info_bar.hide()
                self.info_bar.deleteLater()
                self.engine_combo.hide()
                self.engine_combo.deleteLater()
                self.source_lang_combo.hide()
                self.source_lang_combo.deleteLater()
                self.swap_button.hide()
                self.swap_button.deleteLater()
                self.target_lang_combo.hide()
                self.target_lang_combo.deleteLater()
                self.translate_button.hide()
                self.translate_button.deleteLater()
                self.source_text.hide()
                self.source_text.deleteLater()
                self.target_text.hide()
                self.target_text.deleteLater()
                self.status_label.hide()
                self.status_label.deleteLater()
                self.clear_button.hide()
                self.clear_button.deleteLater()
                self.copy_button.hide()
                self.copy_button.deleteLater()
            except Exception as e:
                print(e)
            super().clear()
        except Exception as e:
            print(e)

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
        self.engine_combo.addItems(["有道", "百度"])
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
        self.swap_button.clicked.connect(self.swap_languages)
        self.swap_button.setCursor(QCursor(Qt.PointingHandCursor))     # 鼠标手形
        toolbar_layout.addWidget(self.swap_button)

        # 目标语言下拉框
        self.target_lang_combo = QComboBox()
        self.target_lang_combo.setMinimumHeight(24)
        self.target_lang_combo.setMinimumWidth(40)
        self.target_lang_combo.addItems(["中", "英", "日", "韩", "俄", "法", "德"])
        self.target_lang_combo.setCurrentText("中")
        toolbar_layout.addWidget(self.target_lang_combo)
        toolbar_layout.addStretch()

        # OCR按钮
        self.ocr_button = QPushButton("截图翻译")
        self.ocr_button.setMinimumHeight(24)
        self.ocr_button.setMinimumWidth(80)
        self.ocr_button.clicked.connect(self.main_object.start_screenshot)
        toolbar_layout.addWidget(self.ocr_button)

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
        self.source_text.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.source_text.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # 设置最大文本长度（5000字符）
        self.source_text.textChanged.connect(self.limit_text_length)
        text_layout.addWidget(self.source_text)

        # 目标文本显示
        self.target_text = QPlainTextEdit()
        self.target_text.setPlaceholderText("翻译结果将显示在这里...")
        self.target_text.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.source_text.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        text_layout.addWidget(self.target_text)

        # 状态栏布局
        status_widget = QWidget()
        status_layout = QHBoxLayout(status_widget)
        status_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(status_widget)

        # 状态标签（左对齐）
        self.status_label = QLabel("就绪 | 当前引擎: 有道")
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
        self.set_info_bar()
        # 请求并更新对话次数信息
        self.update_call_count()
        # 连接事件
        self.source_text.customContextMenuRequested.connect(self.show_source_context_menu)
        self.target_text.customContextMenuRequested.connect(self.show_target_context_menu)

    def show_source_context_menu(self, position):
        print("显示源文本菜单")

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
        menu.exec(self.source_text.viewport().mapToGlobal(position))

    def show_target_context_menu(self, position):
        print("显示目标文本菜单")

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
        menu.exec(self.target_text.viewport().mapToGlobal(position))

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
        url = QUrl(common.BASE_URL + "/translate/normal/todayCalls")
        request = QNetworkRequest(url)
        request.setRawHeader(b"Authorization", bytes(self.main_object.access_token, "utf-8"))

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

    def set_info_bar(self):
        # 根据会员状态显示不同信息
        if self.main_object.is_vip:
            if self.today_calls >= 1000:
                text = f"尊敬的会员用户，您今天已使用{self.today_calls}次，已超限"
                color = "rgba(255, 140, 0, 0.8)"
                self.info_bar.show()
            else:
                text = f"会员用户畅享使用，今天已使用{self.today_calls}次"
                color = "rgba(4, 115, 247, 0.8)"
                self.info_bar.hide()
        else:
            text = f"非会员每天限制10次翻译，今天已使用{self.today_calls}次"
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
        # self.info_bar.setStyleSheet("background: rgba(125, 125, 125, 60); font-weight: bold; font-size: 12px;")

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

    def screenshot_captured(self, pixmap, do_job="translate"):
        # 保存截图
        self.captured_pixmap = pixmap
        # 更新状态
        self.status_label.setText("截图完成,正在压缩图片...")
        try:
            # 这里使用压缩后的版本
            base64_data = self.toolkit.image_util.compress_pixmap_for_baidu(pixmap)
        except ValueError as e:
            self.status_label.setText("图片太大，压缩失败")
            self.source_text.setPlainText("")
            return
        self.status_label.setText("压缩完成,正在识图...")
        # 发送ocr请求
        self.ocr(base64_data, do_job)

    def ocr(self, base64_data: str, do_job: str):
        # 准备请求数据
        engine = "baidu"
        data = {
            "engine": engine,
            "imageBase64": base64_data
        }

        # 创建网络请求
        url = QUrl(common.BASE_URL + "/ocr/normal")
        request = QNetworkRequest(url)
        request.setRawHeader(b"Authorization", bytes(self.main_object.access_token, "utf-8"))
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")

        # 发送POST请求
        if do_job == "translate":
            self.status_label.setText("识图中...")
        self.translate_button.setEnabled(False)

        reply = self.network_manager.post(
            request,
            json.dumps(data).encode('utf-8')
        )
        reply.finished.connect(lambda: self.handle_ocr_response(reply, do_job))
        reply.errorOccurred.connect(lambda: self.handle_ocr_error(reply))

    @Slot()
    def handle_ocr_response(self, ocr_reply, do_job):
        # 检查错误
        if ocr_reply.error() != QNetworkReply.NoError:
            if do_job == "translate":
                self.target_text.setPlainText(f"网络错误: {ocr_reply.errorString()}")
                self.status_label.setText("网络错误")
            ocr_reply.deleteLater()
            return
        # 解析响应
        data = ocr_reply.readAll().data()
        try:
            response = json.loads(data)
            if response.get("code") == 0:
                result = response.get("data", {}).get("text", "")
                if do_job == "translate":
                    self.source_text.setPlainText(result)
                    self.status_label.setText("识图完成")
                    # 然后再进行翻译
                    self.translate_text()
                else:
                    text_box_util.show_text_dialog(self.main_object, "识图完成", {
                        "content": result,
                        "size": [600, 600],
                        "longText": True,
                        "markdown": True
                    })
            else:
                error_msg = response.get("msg", "未知错误")
                if do_job == "translate":
                    self.source_text.setPlainText("")
                    self.status_label.setText(error_msg)
                    self.translate_button.setEnabled(True)
                else:
                    self.main_object.toolkit.message_box_util.box_information(
                        self.main_object, "失败", "未知错误")
        except json.JSONDecodeError:
            if do_job == "translate":
                self.source_text.setPlainText("")
                self.status_label.setText("解析错误")
                self.translate_button.setEnabled(True)
            else:
                self.main_object.toolkit.message_box_util.box_information(
                    self.main_object, "失败", "解析错误")
        ocr_reply.deleteLater()

    @Slot()
    def handle_ocr_error(self, ocr_reply, do_job):
        if do_job == "translate":
            self.target_text.setPlainText("")
            self.status_label.setText("网络错误")
        else:
            self.main_object.toolkit.message_box_util.box_information(
                self.main_object, "失败", "网络错误")
        ocr_reply.deleteLater()

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
        url = QUrl(common.BASE_URL + "/translate/normal")
        request = QNetworkRequest(url)
        request.setRawHeader(b"Authorization", bytes(self.main_object.access_token, "utf-8"))
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")

        # 发送POST请求
        self.status_label.setText("翻译中...")
        self.translate_button.setEnabled(False)

        reply = self.network_manager.post(
            request,
            json.dumps(data).encode('utf-8')
        )
        reply.finished.connect(lambda: self.handle_translate_response(reply))

    @Slot()
    def handle_translate_response(self, reply):
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

    def show_form(self):
        """
        隐藏窗口
        """
        # 设置输入焦点
        self.source_text.setFocus()

    def refresh_theme(self):
        if not super().refresh_theme():
            return False
        is_dark = self.is_dark()
        # 调整下拉框样式
        style_util.set_combo_box_style(self.engine_combo, is_dark)
        style_util.set_combo_box_style(self.source_lang_combo, is_dark)
        style_util.set_combo_box_style(self.target_lang_combo, is_dark)
        # 调整按钮样式
        style_util.set_button_style(self.ocr_button, is_dark)
        style_util.set_button_style(self.translate_button, is_dark)
        style_util.set_button_style(self.copy_button, is_dark)
        style_util.set_button_style(self.clear_button, is_dark)
        # 调整交换按钮样式
        style_util.set_button_style(self.swap_button, icon_path="Arrows/switch", is_dark=is_dark, style_change=False)
        # 字符串过滤区域样式调整
        if is_dark:
            text_edit_style = """
            QPlainTextEdit {
                border-radius: 10px;
                border: 1px solid white;
                background: transparent;
                selection-color: white;
                selection-background-color: #0078d4;
            }""" + style_util.scroll_bar_style
        else:
            text_edit_style = """
            QPlainTextEdit {
                border-radius: 10px;
                border: 1px solid black;
                background: transparent;
                selection-color: white;
                selection-background-color: #0078d4;
            }""" + style_util.scroll_bar_style
        self.source_text.setStyleSheet(text_edit_style)
        self.target_text.setStyleSheet(text_edit_style)
        # 提示信息
        self.set_info_bar()


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