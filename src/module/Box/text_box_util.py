import json
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QVBoxLayout, QLabel, QPushButton, QApplication,
                               QHBoxLayout, QTextBrowser, QSizePolicy)
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

from src.component.AgileTilesAcrylicWindow.AgileTilesAcrylicWindow import AgileTilesAcrylicWindow
from src.constant import dialog_constant
from src.module.Box import message_box_util
from src.ui import style_util


class TextPopup(AgileTilesAcrylicWindow):
    def __init__(self, parent=None, use_parent=None, title=None, content=None):
        super().__init__(parent=parent, is_dark=use_parent.is_dark, form_theme_mode=use_parent.form_theme_mode,
                         form_theme_transparency=use_parent.form_theme_transparency)
        self.use_parent = use_parent
        self.content = content or {}
        self._init_components()
        self._setup_initial_config(title)
        self._handle_content_type()
        self.center_on_screen()

    def _init_components(self):
        """初始化基础组件"""
        self.network_manager = QNetworkAccessManager(self)
        self.loading_label = QLabel("内容加载中...", self)
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.error_label = None
        self.content_widget = None
        self.copy_button = None
        self.refresh_button = None  # 新增刷新按钮引用

    def _setup_initial_config(self, title):
        """窗口基础配置"""
        self.setWindowTitle(title or "内容查看")
        self.setMinimumSize(400, 300)
        self.resize(*self.content.get('size', (500, 400)))

    def _handle_content_type(self):
        """内容类型路由"""
        if 'url' in self.content:
            self._init_ui_with_loading()
            self._fetch_remote_content()
        else:
            self.loading_label.deleteLater()
            self._init_ui_with_content()

    def _init_ui_with_loading(self):
        """初始化加载状态UI"""
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.loading_label)
        self._create_buttons(is_url_content=True)  # 新增参数表示是URL内容
        main_layout.addLayout(self._create_button_layout())
        self.widget_base.setLayout(main_layout)

    def _init_ui_with_content(self):
        """初始化本地内容UI"""
        main_layout = QVBoxLayout()
        self.content_widget = self._create_content_widget()
        main_layout.addWidget(self.content_widget)
        self._create_buttons()  # 创建常规按钮
        main_layout.addLayout(self._create_button_layout())
        self.widget_base.setLayout(main_layout)

    # 新增统一按钮创建方法
    def _create_buttons(self, is_url_content=False):
        """创建操作按钮"""
        self._create_copy_button(disabled=is_url_content)
        if is_url_content:
            self._create_refresh_button()

    def _create_refresh_button(self):
        """创建刷新按钮"""
        self.refresh_button = QPushButton("刷新", self)
        self.refresh_button.setMinimumSize(100, 30)
        self._set_button_style(self.refresh_button)
        self.refresh_button.clicked.connect(self._on_refresh_clicked)

    def _on_refresh_clicked(self):
        """处理刷新点击事件"""
        # 清除旧内容
        if self.content_widget:
            self.content_widget.deleteLater()
            self.content_widget = None

        # 显示加载状态
        self.loading_label = QLabel("重新加载中...", self)
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.widget_base.layout().insertWidget(0, self.loading_label)

        # 禁用按钮防止重复点击
        self.refresh_button.setEnabled(False)
        self.copy_button.setEnabled(False)

        # 重新发起请求
        self._fetch_remote_content()

    def _fetch_remote_content(self):
        try:
            url = QUrl(self.content['url'])
            if not url.isValid():
                raise ValueError("无效的URL地址")

            request = QNetworkRequest(url)
            request.setRawHeader(b"Authorization", bytes(self.use_parent.access_token, "utf-8"))
            reply = self.network_manager.get(request)  # 获取reply对象
            reply.finished.connect(lambda: self._handle_response(reply))  # 显式传递参数
        except Exception as e:
            self._show_error(str(e))

    def _handle_response(self, reply):
        """处理网络响应"""
        reply.deleteLater()

        print("处理网络响应")

        # 恢复按钮状态
        if self.refresh_button:
            self.refresh_button.setEnabled(True)
        self.copy_button.setEnabled(True)

        if reply.error() != QNetworkReply.NoError:
            self._show_error(f"请求失败: {reply.errorString()}")
            return

        try:
            data = json.loads(bytes(reply.readAll()).decode())
            content = data.get('data', '')
            if not content:
                raise ValueError("返回数据中缺少data字段")
        except Exception as e:
            self._show_error(f"数据解析失败: {str(e)}")
            return

        self._update_content_display(content)

    def _update_content_display(self, content):
        """更新内容显示"""
        # 移除加载状态
        self.loading_label.deleteLater()

        # 创建实际内容组件
        self.content["content"] = content["content"]
        self.content_widget = self._create_content_widget()
        self.widget_base.layout().insertWidget(0, self.content_widget)

        # 更新复制功能
        if self.copy_button:
            self.copy_button.setEnabled(True)

    def _create_content_widget(self):
        """创建内容显示组件"""
        content_type = self._detect_content_type()

        if content_type in (
        dialog_constant.DIALOG_TEXT_HTML, dialog_constant.DIALOG_TEXT_MARKDOWN, dialog_constant.DIALOG_TEXT_LONG_TEXT):
            return self._create_browser(content_type)
        return self._create_label()

    def _detect_content_type(self):
        """内容类型检测"""
        if self.content.get(dialog_constant.DIALOG_TEXT_HTML):          # HTML
            return dialog_constant.DIALOG_TEXT_HTML
        if self.content.get(dialog_constant.DIALOG_TEXT_MARKDOWN):      # Markdown
            return dialog_constant.DIALOG_TEXT_MARKDOWN
        if self.content.get(dialog_constant.DIALOG_TEXT_LONG_TEXT):     # 长文本
            return dialog_constant.DIALOG_TEXT_LONG_TEXT
        if len(str(self.content.get('content', ''))) > 200:              # 长文本
            return dialog_constant.DIALOG_TEXT_LONG_TEXT
        return dialog_constant.DIALOG_TEXT_SHORT_TEXT                   # 短文本

    def _create_browser(self, content_type):
        """创建富文本浏览器"""
        browser = QTextBrowser()
        browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        browser.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self._setup_browser_font(browser)
        content = str(self.content.get('content', ''))
        {
            dialog_constant.DIALOG_TEXT_HTML: lambda: browser.setHtml(content),
            dialog_constant.DIALOG_TEXT_MARKDOWN: lambda: browser.setMarkdown(content),
            dialog_constant.DIALOG_TEXT_LONG_TEXT: lambda: browser.setPlainText(content)
        }[content_type]()

        return browser

    def _create_label(self):
        """创建普通文本标签"""
        label = QLabel(str(self.content.get('content', '')))
        label.setWordWrap(True)
        label.setStyleSheet(style_util.transparent_style)
        return label

    def _create_copy_button(self, disabled=False):
        """创建复制按钮"""
        self.copy_button = QPushButton("复制", self)
        self.copy_button.setMinimumSize(100, 30)
        self.copy_button.setEnabled(not disabled)
        self._set_button_style(self.copy_button)
        self.copy_button.clicked.connect(self._copy_content)

    def _create_button_layout(self):
        """创建按钮布局（支持刷新按钮）"""
        layout = QHBoxLayout()
        layout.addStretch()

        # 添加操作按钮
        if self.copy_button:
            layout.addWidget(self.copy_button)
        if self.refresh_button:  # 只在有刷新按钮时显示
            layout.addWidget(self.refresh_button)

        layout.addStretch()
        return layout

    def _show_error(self, message):
        """显示错误信息（增加按钮状态处理）"""
        self.loading_label.deleteLater()
        self.error_label = QLabel(f"⚠️ {message}", self)
        self.error_label.setStyleSheet("color: red; font-weight: bold;")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.widget_base.layout().insertWidget(0, self.error_label)

        # 恢复按钮状态
        if self.refresh_button:
            self.refresh_button.setEnabled(True)
        if self.copy_button:
            self.copy_button.setEnabled(False)

    def _setup_browser_font(self, browser):
        """设置浏览器字体"""
        font = QFont()
        font.setPointSize(10)
        browser.setFont(font)

    def _set_button_style(self, button):
        """设置按钮样式"""
        style = style_util.normal_dark_button_style if self.is_dark else style_util.normal_light_button_style
        button.setStyleSheet(style)

    def center_on_screen(self):
        """窗口居中显示"""
        qr = self.frameGeometry()
        cp = QApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _copy_content(self):
        """复制当前内容"""
        content = str(self.content.get('content', ''))
        QApplication.clipboard().setText(content)
        # 弹窗提醒
        message_box_util.box_information(self, "提醒", f"复制内容成功，您现在可以粘贴了~")


def show_text_dialog(main_object, title, content):
    """显示内容对话框"""
    dialog = TextPopup(None, main_object, title, content)
    dialog.refresh_geometry(main_object.toolkit.resolution_util.get_screen(main_object))
    dialog.show()
    return dialog