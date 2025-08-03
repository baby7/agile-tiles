import re
import os
import time
import cchardet as cchardet
from src.card.MainCardManager.MainCard import MainCard
from PySide6 import QtCore
from PySide6.QtCore import QRect, Qt, QCoreApplication
from PySide6.QtGui import QFont, QColor
from PySide6.QtWidgets import (QWidget, QFrame, QLabel, QPushButton, QScrollArea, QTabWidget, QTextBrowser,
                               QTreeWidget, QComboBox, QFileDialog, QPlainTextEdit, QTreeWidgetItem, QScrollBar, QHBoxLayout, QSizePolicy)
import src.ui.style_util as style_util
import src.module.Box.message_box_util as message_box_util
from src.constant import data_save_constant


def get_encoding(file):
    # 二进制方式读取，获取字节数据，检测类型
    with open(file, 'rb') as f:
        return cchardet.detect(f.read())['encoding']


class BookCard(MainCard):
    title = "阅读"
    name = "BookCard"
    support_size_list = ["Big"]
    # 只读参数
    x = None  # 坐标x
    y = None  # 坐标y
    size = None  # 大小(1_1:Point、1_2:MiniHor、2_1MiniVer、2_2Block、2_5)
    theme = None  # 主题(Light、Dark)
    width = 0  # 宽度
    height = 0  # 高度
    fillet_corner = 0  # 圆角大小
    # 可使用
    card = None  # 卡片本体
    data = None  # 数据
    toolkit = None  # 工具箱，具体参考文档
    logger = None  # 日志记录工具
    # 可调用
    save_data_func = None  # 保存数据(传参为一个字典)
    # 默认值
    DEFAULT_FONT_SIZE = "10"
    DEFAULT_LINE_SPACING = "1.0"
    DEFAULT_TEXT_FILTRATION = ""
    # 待写入
    current_file = None
    current_chapter = None
    font_size = DEFAULT_FONT_SIZE
    line_spacing = DEFAULT_LINE_SPACING
    text_filtration = DEFAULT_TEXT_FILTRATION

    book_filename = None
    book_chapters = []
    book_lines = None

    def __init__(self, main_object=None, parent=None, theme=None, card=None, cache=None, data=None,
                 toolkit=None, logger=None, save_data_func=None):
        super().__init__(main_object=main_object, parent=parent, theme=theme, card=card, cache=cache, data=data,
                         toolkit=toolkit, logger=logger, save_data_func=save_data_func)
        self.book_data = self.data.setdefault(self.hardware_id, {})
        self.init_config()

    def init_config(self):
        self.font_size = self.book_data.setdefault("fontSize", self.DEFAULT_FONT_SIZE)
        self.line_spacing = self.book_data.setdefault("lineSpacing", self.DEFAULT_LINE_SPACING)
        self.text_filtration = self.book_data.setdefault("textFiltration", self.DEFAULT_TEXT_FILTRATION)
        self.current_file = self.book_data.setdefault("currentFile", None)
        self.current_chapter = self.book_data.setdefault("currentChapter", None)

    def clear(self):
        try:
            self.book_tab_widget.setVisible(False)
            self.book_tab_widget.deleteLater()
            self.book_area.setVisible(False)
            self.book_area.deleteLater()
        except Exception as e:
            print(e)
        super().clear()

    def init_ui(self):
        super().init_ui()
        font = QFont()
        font.setBold(True)
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        font2 = QFont()
        font2.setPointSize(11)
        font2.setBold(True)
        font2.setKerning(True)
        font3 = QFont()
        font3.setPointSize(10)
        # 主要区域
        self.book_area = QScrollArea(self.card)
        self.book_area.setObjectName(u"book_area")
        self.book_area.setGeometry(QtCore.QRect(0, 0, self.card.width(), self.card.height()))
        self.book_area.setFont(font)
        self.book_area.setStyleSheet(u"border-style: solid;\n"
                                     "border-radius: 10px;\n"
                                     "border: 0px solid black;\n"
                                     "border-color: rgba(255, 255, 255, 0);\n"
                                     "background: transparent;")
        self.book_area.setFrameShape(QFrame.StyledPanel)
        self.book_area.setLineWidth(1)
        self.book_area.setWidgetResizable(True)
        self.scrollAreaWidgetContents_12 = QWidget()
        self.scrollAreaWidgetContents_12.setObjectName(u"scrollAreaWidgetContents_12")
        self.scrollAreaWidgetContents_12.setGeometry(QRect(0, 0, self.card.width(), self.card.height()))
        # 总选项卡
        self.book_tab_widget = QTabWidget(self.scrollAreaWidgetContents_12)
        self.book_tab_widget.setObjectName(u"book_tab_widget")
        self.book_tab_widget.setGeometry(QRect(0, 0, self.card.width(), self.card.height()))
        self.book_tab_widget.setFont(font1)
        self.book_tab_widget.setTabPosition(QTabWidget.North)
        self.book_tab_widget.setTabShape(QTabWidget.Rounded)
        # 书籍选择区域
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        # 书籍选择区域 - 标题下划线
        self.text_line_select_title = QFrame(self.tab_5)
        self.text_line_select_title.setObjectName(u"text_line_select_title")
        self.text_line_select_title.setGeometry(QRect(10, 70, self.card.width() - 40, 1))
        self.text_line_select_title.setStyleSheet("border: 1px solid black;")
        self.text_line_select_title.setFrameShadow(QFrame.Plain)
        self.text_line_select_title.setLineWidth(2)
        self.text_line_select_title.setFrameShape(QFrame.HLine)
        font5 = QFont()
        font5.setPointSize(11)
        font5.setBold(False)
        # 书籍选择区域 - 选择按钮
        self.push_button_book_select = QPushButton(self.tab_5)
        self.push_button_book_select.setObjectName(u"push_button_book_select")
        self.push_button_book_select.setGeometry(QRect(self.card.width() / 2 - (130 / 2) - 10, 20, 130, 30))
        font6 = QFont()
        font6.setPointSize(11)
        self.push_button_book_select.setFont(font6)
        # 书籍选择区域 - 书籍信息
        self.text_label_book_browser = QTextBrowser(self.tab_5)
        self.text_label_book_browser.setObjectName(u"text_label_book_browser")
        self.text_label_book_browser.setGeometry(QRect(20, 100, self.card.width() - 60, 456))
        self.text_label_book_browser.setFont(font3)
        self.text_label_book_browser.setStyleSheet(u"QTextBrowser {\n"
                                                   "    border-style: solid;\n"
                                                   "    border-radius: 10px;\n"
                                                   "    border: 0px solid black;\n"
                                                   "    border-color: rgb(0, 0, 0);\n"
                                                   "    background: transparent;\n"
                                                   "}" + style_util.scroll_bar_style)
        self.book_tab_widget.addTab(self.tab_5, "")
        # 目录区域
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        # 目录区域 - 目录
        self.book_tree_widget = QTreeWidget(self.tab_3)
        self.book_tree_widget.headerItem().setText(0, "")
        self.book_tree_widget.setObjectName(u"book_tree_widget")
        self.book_tree_widget.setGeometry(QRect(20, 20, self.card.width() - 60, self.card.height() - 95))
        self.book_tree_widget.setFont(font3)
        self.book_tree_widget.setIndentation(10)
        self.book_tree_widget.setColumnCount(1)
        self.book_tree_widget.setAlternatingRowColors(True)
        self.book_tree_widget.setRootIsDecorated(False)
        self.book_tab_widget.addTab(self.tab_3, "")

        # 内容标签页 - 重构布局
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.book_chapter_title = QLabel(self.tab)
        self.book_chapter_title.setObjectName(u"book_chapter_title")
        self.book_chapter_title.setGeometry(QRect(3, 5, self.card.width() - 20, 21))
        self.book_chapter_title.setFont(font5)
        self.book_chapter_title.setStyleSheet(u"border: 0px solid #FF8D16;\n"
                                              "border-radius: 0px;\n"
                                              "background-color: rgba(0, 0, 0, 0);")
        self.book_chapter_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 横线
        self.text_line_content_title = QFrame(self.tab)
        self.text_line_content_title.setObjectName(u"text_line_content_title")
        self.text_line_content_title.setGeometry(QRect(0, 30, self.card.width(), 1))
        self.text_line_content_title.setStyleSheet("border: 1px solid black;")
        self.text_line_content_title.setFrameShadow(QFrame.Plain)
        self.text_line_content_title.setLineWidth(2)
        self.text_line_content_title.setFrameShape(QFrame.HLine)

        # 创建阅读区域容器
        self.reading_container = QWidget(self.tab)
        self.reading_container.setObjectName(u"reading_container")
        self.reading_container.setGeometry(QRect(0, 31, self.card.width() - 22, self.book_tab_widget.height() - 87))

        # 使用水平布局放置阅读区域和滚动条
        self.horizontal_layout = QHBoxLayout(self.reading_container)
        self.horizontal_layout.setSpacing(0)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)

        # 文本内容区域
        self.text_browser_book = QTextBrowser(self.reading_container)
        self.text_browser_book.setObjectName(u"text_browser_book")
        self.text_browser_book.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.text_browser_book.setFont(font3)
        self.text_browser_book.setStyleSheet(style_util.scroll_bar_style)
        self.text_browser_book.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # 创建外部滚动条
        self.external_scrollbar = QScrollBar(Qt.Vertical, self.reading_container)
        self.external_scrollbar.setObjectName(u"external_scrollbar")
        self.external_scrollbar.setFixedWidth(10)  # 设置滚动条宽度

        # 将文本区域和滚动条添加到布局
        self.horizontal_layout.addWidget(self.text_browser_book)
        self.horizontal_layout.addWidget(self.external_scrollbar)

        # 同步滚动条和文本区域的滚动
        self.text_browser_book.verticalScrollBar().valueChanged.connect(self.external_scrollbar.setValue)
        self.external_scrollbar.valueChanged.connect(self.text_browser_book.verticalScrollBar().setValue)

        # 翻页按钮
        button_width = self.card.width() // 6  # 按钮宽度为卡片宽度的1/6

        # 上一页按钮 - 放在阅读区域左侧外部
        self.push_button_book_chapter_last = QPushButton(self.tab)
        self.push_button_book_chapter_last.setObjectName(u"push_button_book_chapter_last")
        self.push_button_book_chapter_last.setGeometry(QRect(0, 31, button_width, self.reading_container.height()))
        self.push_button_book_chapter_last.setFont(font1)

        # 下一页按钮 - 放在阅读区域右侧外部
        self.push_button_book_chapter_next = QPushButton(self.tab)
        self.push_button_book_chapter_next.setObjectName(u"push_button_book_chapter_next")
        self.push_button_book_chapter_next.setGeometry(
            QRect(self.card.width() - button_width - 35, 31, button_width, self.reading_container.height()))
        self.push_button_book_chapter_next.setFont(font1)

        self.book_tab_widget.addTab(self.tab, "")

        # 设置区域
        self.tab_11 = QWidget()
        self.tab_11.setObjectName(u"tab_11")
        # 设置区域 - 标题下划线
        self.text_label_setting_filtration_left = QLabel(self.tab_11)
        self.text_label_setting_filtration_left.setObjectName(u"text_label_setting_filtration_left")
        self.text_label_setting_filtration_left.setGeometry(QRect(40, 110, self.card.width() - 80, 31))
        self.text_label_setting_filtration_left.setFont(font5)
        self.text_label_setting_filtration_left.setStyleSheet(u"border: 0px solid #FF8D16;\n"
                                                              "border-radius: 0px;\n"
                                                              "background-color: rgba(0, 0, 0, 0);")
        self.text_label_setting_filtration_left.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        # 设置区域 - 字符串过滤列表
        self.text_setting_edit_filtration = QPlainTextEdit(self.tab_11)
        self.text_setting_edit_filtration.setObjectName(u"text_setting_edit_filtration")
        self.text_setting_edit_filtration.setGeometry(QRect(10, 145, self.card.width() - 40, 341))
        self.text_setting_edit_filtration.setFont(font3)
        self.text_setting_edit_filtration.setStyleSheet(u"QPlainTextEdit {\n"
                                                        "    border-style: solid;\n"
                                                        "    border-radius: 10px;\n"
                                                        "    border: 1px solid black;\n"
                                                        "    border-color: rgb(0, 0, 0);\n"
                                                        "    background: transparent;\n"
                                                        "}\n" + style_util.scroll_bar_style)
        # 设置区域 - 字号label
        self.text_label_setting_font_size_left = QLabel(self.tab_11)
        self.text_label_setting_font_size_left.setObjectName(u"text_label_setting_font_size_left")
        self.text_label_setting_font_size_left.setGeometry(QRect(20, 30, 61, 21))
        self.text_label_setting_font_size_left.setFont(font5)
        self.text_label_setting_font_size_left.setStyleSheet(u"border: 0px solid #FF8D16;\n"
                                                             "border-radius: 0px;\n"
                                                             "background-color: rgba(0, 0, 0, 0);")
        self.text_label_setting_font_size_left.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        # 设置区域 - 字号
        self.text_label_setting_font_size_minus = QLabel(self.tab_11)
        self.text_label_setting_font_size_minus.setObjectName(u"text_label_setting_font_size_minus")
        self.text_label_setting_font_size_minus.setGeometry(QRect(140, 30, 61, 21))
        self.text_label_setting_font_size_minus.setFont(font5)
        self.text_label_setting_font_size_minus.setStyleSheet(u"border: 0px solid #FF8D16;\n"
                                                              "border-radius: 0px;\n"
                                                              "background-color: rgba(0, 0, 0, 0);")
        self.text_label_setting_font_size_minus.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # 设置区域 - 字号减小
        self.text_push_button_setting_font_size_minus = QPushButton(self.tab_11)
        self.text_push_button_setting_font_size_minus.setObjectName(u"text_push_button_setting_font_size_minus")
        self.text_push_button_setting_font_size_minus.setGeometry(QRect(80, 30, 61, 22))
        self.text_push_button_setting_font_size_minus.setFont(font1)
        # 设置区域 - 字号增加
        self.text_push_button_setting_font_size_add = QPushButton(self.tab_11)
        self.text_push_button_setting_font_size_add.setObjectName(u"text_push_button_setting_font_size_add")
        self.text_push_button_setting_font_size_add.setGeometry(QRect(200, 30, 61, 22))
        self.text_push_button_setting_font_size_add.setFont(font1)
        # 设置区域 - 文本间距label
        self.text_label_setting_interval_left = QLabel(self.tab_11)
        self.text_label_setting_interval_left.setObjectName(u"text_label_setting_interval_left")
        self.text_label_setting_interval_left.setGeometry(QRect(20, 70, 61, 21))
        self.text_label_setting_interval_left.setFont(font5)
        self.text_label_setting_interval_left.setStyleSheet(u"border: 0px solid #FF8D16;\n"
                                                            "border-radius: 0px;\n"
                                                            "background-color: rgba(0, 0, 0, 0);")
        self.text_label_setting_interval_left.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        # 设置区域 - 文本间距
        self.text_interval_combo_box = QComboBox(self.tab_11)
        self.text_interval_combo_box.addItem("")
        self.text_interval_combo_box.addItem("")
        self.text_interval_combo_box.addItem("")
        self.text_interval_combo_box.setObjectName(u"text_interval_combo_box")
        self.text_interval_combo_box.setGeometry(QRect(80, 70, 121, 22))
        self.text_interval_combo_box.setFont(font3)
        # 设置区域 - 缺点按钮
        self.text_push_button_setting_sure = QPushButton(self.tab_11)
        self.text_push_button_setting_sure.setObjectName(u"text_push_button_setting_sure")
        self.text_push_button_setting_sure.setGeometry(QRect(self.card.width() / 2 - 65, 500, 131, 31))
        self.text_push_button_setting_sure.setFont(font5)
        self.book_tab_widget.addTab(self.tab_11, "")

        self.book_area.setWidget(self.scrollAreaWidgetContents_12)
        self.book_tab_widget.setCurrentIndex(0)
        # 其他初始化
        self.push_button_book_select.setText(QCoreApplication.translate("Form", "选择书籍", None))
        self.book_tab_widget.setTabText(self.book_tab_widget.indexOf(self.tab_5),
                                        QCoreApplication.translate("Form", "选书", None))
        self.book_tab_widget.setTabText(self.book_tab_widget.indexOf(self.tab_3),
                                        QCoreApplication.translate("Form", "章节", None))
        self.book_chapter_title.setText(QCoreApplication.translate("Form", "章节名", None))
        self.text_browser_book.setHtml(QCoreApplication.translate("Form",
                                                                  "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                                  "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n"
                                                                  "</style></head><body style=\" font-size:10pt; font-weight:400; font-style:normal;\">\n"
                                                                  "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>",
                                                                  None))
        self.book_tab_widget.setTabText(self.book_tab_widget.indexOf(self.tab),
                                        QCoreApplication.translate("Form", "内容", None))
        self.text_label_setting_filtration_left.setText(
            QCoreApplication.translate("Form", "字符串过滤列表（支持正则）：", None))
        self.text_setting_edit_filtration.setPlainText(
            QCoreApplication.translate("Form", u"百度仙逆吧\n"
                                               "\\(顶点小说手打小说\\)\n"
                                               "①⑥kxs网更新最快\n"
                                               "\\s*♀♀♀♀♀♀.{1}♀♀♀♀♀♀\n"
                                               "\\s*︴︴︴︴︴︴︴︴︴︴.{1}︴\n"
                                               "【花花更新】\n"
                                               "\\s*║┆┆┆┆.{0,1}║\n"
                                               "www.uu234.com", None))
        self.text_label_setting_font_size_left.setText(QCoreApplication.translate("Form", "字号：", None))
        self.text_push_button_setting_font_size_minus.setText(QCoreApplication.translate("Form", u"A-", None))
        self.text_push_button_setting_font_size_add.setText(QCoreApplication.translate("Form", u"A+", None))
        self.text_label_setting_interval_left.setText(QCoreApplication.translate("Form", "间距：", None))
        self.text_interval_combo_box.setItemText(0, QCoreApplication.translate("Form", u"0.5", None))
        self.text_interval_combo_box.setItemText(1, QCoreApplication.translate("Form", u"1.0", None))
        self.text_interval_combo_box.setItemText(2, QCoreApplication.translate("Form", u"1.5", None))
        self.text_push_button_setting_sure.setText(QCoreApplication.translate("Form", "确定", None))
        self.text_label_setting_font_size_minus.setText(QCoreApplication.translate("Form", u"10", None))
        self.book_tab_widget.setTabText(self.book_tab_widget.indexOf(self.tab_11),
                                        QCoreApplication.translate("Form", "设置", None))
        # 设置浏览器不打开链接
        self.text_browser_book.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        # 绑定按钮事件
        self.push_button_book_select.clicked.connect(self.push_button_book_select_click)
        self.text_push_button_setting_sure.clicked.connect(self.save_setting)
        self.push_button_book_chapter_last.clicked.connect(self.show_last)
        self.push_button_book_chapter_next.clicked.connect(self.show_next)
        self.text_push_button_setting_font_size_minus.clicked.connect(self.font_size_minus)
        self.text_push_button_setting_font_size_add.clicked.connect(self.font_size_add)
        # 初始化书籍信息
        self.init_book_info()
        # 初始化设置信息
        self.init_setting_info()
        # 添加延迟确保布局完成(临时方案)
        QtCore.QTimer.singleShot(1000, self.update_scrollbar_range)
        QtCore.QTimer.singleShot(3000, self.update_scrollbar_range)
        QtCore.QTimer.singleShot(5000, self.update_scrollbar_range)
        QtCore.QTimer.singleShot(7000, self.update_scrollbar_range)
        QtCore.QTimer.singleShot(10000, self.update_scrollbar_range)
        QtCore.QTimer.singleShot(15000, self.update_scrollbar_range)

    def refresh_data(self, date_time_str):
        super().refresh_data(date_time_str)

    def refresh_ui(self, date_time_str):
        super().refresh_ui(date_time_str)
        super().refresh_ui_end(date_time_str)

    def update_data(self, data=None):
        """
        更新持久数据事件
        """
        if self.data == data:
            return
        # 重新初始化配置
        self.data = data
        self.book_data = self.data.setdefault(self.hardware_id, {})
        self.init_config()
        # 初始化书籍信息
        self.init_book_info()
        # 初始化设置信息
        self.init_setting_info()
        # 添加延迟确保布局完成(临时方案)
        QtCore.QTimer.singleShot(1000, self.update_scrollbar_range)

    # 初始化设置
    def init_book_info(self):
        # 如果之前打开过文件，则直接加载文件
        if self.current_file:
            self.load_file(self.current_file)
            self.book_tab_widget.setCurrentIndex(2)
        else:
            self.book_tab_widget.setCurrentIndex(0)

    def init_setting_info(self):
        self.text_label_setting_font_size_minus.setText(self.font_size)
        self.text_interval_combo_box.setCurrentText(self.line_spacing)
        self.text_setting_edit_filtration.setPlainText(self.text_filtration)

    # 保存设置
    def save_info(self):
        self.book_data["currentFile"] = self.current_file
        self.book_data["currentChapter"] = self.current_chapter
        # 保存数据
        self.save_data_func(in_data=self.cache, card_name=self.name, data_type=data_save_constant.DATA_TYPE_ENDURING)

    def save_setting(self):
        self.font_size = self.text_label_setting_font_size_minus.text()
        self.line_spacing = self.text_interval_combo_box.currentText()
        self.text_filtration = self.text_setting_edit_filtration.toPlainText()
        self.book_data["fontSize"] = self.font_size
        self.book_data["lineSpacing"] = self.line_spacing
        self.book_data["textFiltration"] = self.text_filtration
        # 保存数据
        self.save_data_func(in_data=self.cache, card_name=self.name, data_type=data_save_constant.DATA_TYPE_ENDURING)
        # 显示内容
        self.show_content()
        # 提示
        message_box_util.box_information(self.main_object, "成功", "修改阅读设置成功")

    def push_button_book_select_click(self):
        # 弹出QFileDialog窗口。getOpenFileName()方法的第一个参数是说明文字，
        # 第二个参数是默认打开的文件夹路径。默认情况下显示所有类型的文件。
        if not self.current_file:
            path = '/'
        else:
            path = self.current_file
        self.current_chapter = 0
        file_name = QFileDialog.getOpenFileName(self.card, '打开书籍', path, filter='*.txt')
        self.load_file(file_name[0])

    def load_file(self, file):
        # 文件不为空
        if file:
            # 判断文件是否存在
            if not os.path.exists(file):
                return
            # 更改目前打开的文件
            self.current_file = file
            self.book_filename = file.split('/')[-1].split('.')[0]
            # 获取文件的编码格式
            encodings = get_encoding(file)
            with open(file, 'r', encoding=encodings, errors='ignore') as f:
                # 打开文件,生成章节目录
                self.book_chapters = []
                # 包含了txt文本的全部内容
                self.book_lines = f.readlines()
                # 一种匹配章节目录的规则
                self.matching_chapter_name()
            # 如果没有可用的目录,那就显示全部
            if not self.book_chapters:
                self.book_chapters.append({self.book_filename: 0})
            # 设置章节目录
            self.set_chapters()
            # 设置文本浏览器的内容
            self.show_content()
            # 跳转目录
            self.book_tab_widget.setCurrentIndex(1)
            self.save_info()
            # 文件大小(MB)
            book_size = self.toolkit.file_util.get_file_size(file)
            # 总字数
            book_total_words = self.toolkit.file_util.get_txt_file_words_number(file, encodings)
            # 生成书籍信息 书籍名;文件路径;文件大小;章节数;总字数;创建时间;修改时间
            book_message_map = {
                "书籍名称": self.book_filename,
                "文件大小": book_size,
                "章节数量": str(len(self.book_chapters)) + "章",
                "总字符数": book_total_words,
                "创建时间": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getctime(file))),
                "修改时间": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(file))),
                "访问时间": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getatime(file))),
                "文件路径": file,
            }
            line_start = '<p style="line-height:150%">'
            style_start = '<font color="#2d76b6">'
            style_end = "</font>"
            line_end = "</p>"
            book_info_str = ""
            for key, value in book_message_map.items():
                book_info_str += line_start + style_start + key + "： " + style_end + str(value) + line_end
            self.text_label_book_browser.setText(book_info_str)
        else:  # 文件为空，说明没有选择文件
            print('您没有选择文件！')

    def matching_chapter_name(self):
        # 一种匹配章节目录的规则
        pattern = r"(第)([\u4e00-\u9fa5a-zA-Z0-9\s]{1,7})[章|节][^\n]{0,35}()?(|\n)"
        last_index = 0
        for i in range(len(self.book_lines)):
            line = self.book_lines[i].strip()
            if line != "" and re.search(pattern, line):
                line = re.search(pattern, line).group()
                line = line.replace("\n", "").replace("=", "")
                if len(line) < 30:  # 标题30字以内
                    if last_index != 0 and (i - last_index) < 30:  # 章节最小间隔
                        continue
                    self.book_chapters.append({line: i})
                    last_index = i

    # 设置章节目录
    def set_chapters(self):
        # 每次绘制目录时先清除一下
        self.book_tree_widget.clear()
        _translate = QtCore.QCoreApplication.translate
        __sortingEnabled = self.book_tree_widget.isSortingEnabled()
        for i, value in enumerate(self.book_chapters):
            item = QTreeWidgetItem(self.book_tree_widget)
            item.setText(0, _translate("MyMainWindow", list(value.keys())[0]))
            self.book_tree_widget.addTopLevelItem(item)
        self.book_tree_widget.setSortingEnabled(__sortingEnabled)
        self.book_tree_widget.clicked.connect(self.onTreeClicked)
        # 当前章节
        self.book_tree_widget.setCurrentItem(self.book_tree_widget.topLevelItem(self.current_chapter), 0)
        # 为当前章节设置背景色
        self.book_tree_widget.topLevelItem(self.current_chapter).setBackground(0, QColor(15, 136, 235))
        # 隐藏标题栏
        self.book_tree_widget.header().setVisible(False)

    # 设置文本浏览器的内容
    def show_content(self):
        if len(self.book_chapters) == 0:
            return
        # 设置字体
        font = QFont()
        font.setPointSize(int(self.font_size))
        self.text_browser_book.setFont(font)
        # 将文件内容添加到文本浏览器中
        self.text_browser_book.setText(self.to_browser_content(self.get_content()))
        # 展示章节名
        self.book_chapter_title.setText(list(self.book_chapters[self.current_chapter].keys())[0])
        # 更新滚动条范围
        self.update_scrollbar_range()

    # 更新滚动条范围
    def update_scrollbar_range(self):
        # 获取文本浏览器的垂直滚动条
        v_scrollbar = self.text_browser_book.verticalScrollBar()
        # 设置外部滚动条的范围与文本浏览器的滚动条一致
        if self.external_scrollbar.minimum() != v_scrollbar.minimum():
            self.external_scrollbar.setMinimum(v_scrollbar.minimum())
        if self.external_scrollbar.maximum() != v_scrollbar.maximum():
            self.external_scrollbar.setMaximum(v_scrollbar.maximum())
        if self.external_scrollbar.pageStep() != v_scrollbar.pageStep():
            self.external_scrollbar.setPageStep(v_scrollbar.pageStep())
        if self.external_scrollbar.singleStep() != v_scrollbar.singleStep():
            self.external_scrollbar.setSingleStep(v_scrollbar.singleStep())

    # 获取章节内容
    def get_content(self):
        index = self.current_chapter
        # 起始行
        start = list(self.book_chapters[index].values())[0]
        # 如果是终章
        if index == self.book_tree_widget.topLevelItemCount() - 1:
            content_text = "".join(self.book_lines[start:-1])
        else:
            # 终止行
            end = list(self.book_chapters[index + 1].values())[0]
            content_text = "".join(self.book_lines[start:end])
        # 去除部分小说广告
        if self.text_filtration is None:
            self.text_filtration = ""
        advertisement_list = self.text_filtration.split("\n")
        for advertisement in advertisement_list:
            if advertisement == "":
                continue
            content_text = re.sub(advertisement, "", content_text)
        # 将三个及以上连着的换行符替换为两个换行符
        content_text = re.sub(r"(\n){3,}", r"\n\n", content_text)
        # 将最后的空行和换行符都去掉
        content_text = re.sub(r"(\n){2,}$", "\n", content_text)
        return content_text

    def to_browser_content(self, content_text):
        content_html = ""
        content_list = content_text.split("\n")
        line_height = str(int(float(self.line_spacing) * 20))
        for content in content_list:
            content_html += "<p style='line-height:" + str(line_height) + "px;width:100%;'>" + content + "</p>"
        return content_html

    # 点击目录跳转到章节
    def onTreeClicked(self, index):
        # 恢复原来章节的背景色(设置透明度为0)，为新章节设置背景色
        self.book_tree_widget.topLevelItem(self.current_chapter).setBackground(0, QColor(0, 0, 0, 0))
        # 获取点击的项目下标
        self.current_chapter = int(index.row())
        self.book_tree_widget.topLevelItem(self.current_chapter).setBackground(0, QColor(15, 136, 235))
        self.show_content()
        self.book_tab_widget.setCurrentIndex(2)
        self.save_info()

    # 展示上一章
    def show_last(self):
        if self.current_chapter <= 0 or self.book_tree_widget.topLevelItem(self.current_chapter - 1) is None:
            message_box_util.box_information(self.main_object, "提醒", "已经到第一章了哦~")
            return
        # 更改目录背景色
        self.book_tree_widget.topLevelItem(self.current_chapter).setBackground(0, QColor(0, 0, 0, 0))
        self.current_chapter = self.current_chapter - 1
        self.show_content()  # 显示内容
        self.book_tree_widget.topLevelItem(self.current_chapter).setBackground(0, QColor(15, 136, 235))
        self.save_info()

    # 展示下一章
    def show_next(self):
        if (self.current_chapter + 1) >= len(self.book_chapters):
            message_box_util.box_information(self.main_object, "提醒", "已经到最后一章了哦~")
            return
        # 更改目录背景色
        self.book_tree_widget.topLevelItem(self.current_chapter).setBackground(0, QColor(0, 0, 0, 0))
        self.current_chapter = self.current_chapter + 1
        self.show_content()  # 显示内容
        self.book_tree_widget.topLevelItem(self.current_chapter).setBackground(0, QColor(15, 136, 235))
        self.save_info()

    def font_size_add(self):
        font_size = self.text_label_setting_font_size_minus.text()
        font_size = int(font_size) + 1
        if font_size > 30:
            message_box_util.box_information(self.main_object, "失败", "抱歉，最大只能设置到30哦~")
            return
        self.text_label_setting_font_size_minus.setText(str(font_size))

    def font_size_minus(self):
        font_size = self.text_label_setting_font_size_minus.text()
        font_size = int(font_size) - 1
        if font_size < 8:
            message_box_util.box_information(self.main_object, "失败", "抱歉，最小只能设置到8哦~")
            return
        self.text_label_setting_font_size_minus.setText(str(font_size))

    def refresh_theme(self):
        if not super().refresh_theme():
            return False
        # 调整tab_widget样式
        style_util.set_tab_widget_style(self.book_tab_widget, self.is_dark())
        # 调整按钮样式
        is_dark = self.is_dark()
        style_util.set_button_style(self.push_button_book_select, is_dark)
        style_util.set_button_style(self.text_push_button_setting_sure, is_dark)
        style_util.set_button_style(self.text_push_button_setting_font_size_minus, is_dark)
        style_util.set_button_style(self.text_push_button_setting_font_size_add, is_dark)
        style_util.set_combo_box_style(self.text_interval_combo_box, is_dark)
        # 调整横线样式
        if is_dark:
            line_style = "border: 1px solid white;"
        else:
            line_style = "border: 1px solid black;"
        self.text_line_select_title.setStyleSheet(line_style)
        self.text_line_content_title.setStyleSheet(line_style)
        # 调整翻页按钮样式
        push_button_style = "QPushButton { background: transparent; border: none; } QPushButton:hover { background: {}; }"
        if is_dark:
            self.push_button_book_chapter_last.setStyleSheet(push_button_style.replace("{}",
                                                                                       "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop: 0 rgba(200, 200, 200, 100), stop:1 rgba(0, 0, 0, 0))"))
            self.push_button_book_chapter_next.setStyleSheet(push_button_style.replace("{}",
                                                                                       "qlineargradient(x1:1, y1:0, x2:0, y2:0, stop: 0 rgba(200, 200, 200, 100), stop:1 rgba(0, 0, 0, 0))"))
        else:
            self.push_button_book_chapter_last.setStyleSheet(push_button_style.replace("{}",
                                                                                       "qlineargradient(x1:1, y1:0, x2:0, y2:0, stop: 0 rgba(0, 0, 0, 0), stop:1 rgba(0, 0, 0, 100))"))
            self.push_button_book_chapter_next.setStyleSheet(push_button_style.replace("{}",
                                                                                       "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop: 0 rgba(0, 0, 0, 0), stop:1 rgba(0, 0, 0, 100))"))
        # 字符串过滤区域样式调整
        if is_dark:
            self.text_setting_edit_filtration.setStyleSheet("""
            QPlainTextEdit {
                border-radius: 10px;
                border: 1px solid white;
                background: transparent;
            }""" + style_util.scroll_bar_style)
        else:
            self.text_setting_edit_filtration.setStyleSheet("""
            QPlainTextEdit {
                border-radius: 10px;
                border: 1px solid black;
                background: transparent;
            }""" + style_util.scroll_bar_style)
        # 书籍目录区域
        if is_dark:
            self.book_tree_widget.setStyleSheet(tree_widget_dark_style)
        else:
            self.book_tree_widget.setStyleSheet(tree_widget_light_style)
        # 外部滚动条样式
        if is_dark:
            self.external_scrollbar.setStyleSheet(style_util.scroll_bar_style)
        else:
            self.external_scrollbar.setStyleSheet(style_util.scroll_bar_style)
        # 更新滚动条范围
        self.update_scrollbar_range()


# 书籍目录样式
tree_widget_dark_style = """
QTreeWidget {
  border-radius: 10px;
  border: none;
  background: transparent;
}
QTreeWidget::item {
  padding-left: 10px;
}
QTreeWidget::item:click {
  background: transparent;
}
QTreeWidget::item:hover {
  background-color: rgba(255, 255, 255, 80);
  border-radius: 10px;
}
QTreeWidget::item:selected {
  background-color: #4d4d4d;
  color: rgb(255, 255, 255);
  border-radius: 10px;
}
QTreeWidget::item:!alternate:!selected {
  background-color: rgba(100, 100, 100, 0.1);
  border-radius: 10px;
}""" + style_util.scroll_bar_style

tree_widget_light_style = """
QTreeWidget {
  border-radius: 10px;
  border: none;
  background: transparent;
}
QTreeWidget::item {
  padding-left: 10px;
}
QTreeWidget::item:click {
  background: transparent;
}
QTreeWidget::item:hover {
  background-color: rgba(0, 0, 0, 80);
  border-radius: 10px;
}
QTreeWidget::item:selected {
  background-color: #4d4d4d;
  color: rgb(255, 255, 255);
  border-radius: 10px;
}
QTreeWidget::item:!alternate:!selected {
  background-color: rgba(100, 100, 100, 0.1);
  border-radius: 10px;
}""" + style_util.scroll_bar_style