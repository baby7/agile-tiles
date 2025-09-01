from PySide6.QtCore import QSettings
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from src.component.AgileTilesTitleBar.AgileTilesTitleBar import AgileTilesTitleBar
from src.component.BaseAcrylicWindow.BaseAcrylicWindow import BaseAcrylicWindow
from src.module import init_module
from src.ui import style_util
from src.module.Box import message_box_util


class AgileTilesAcrylicWindow(BaseAcrylicWindow):
    """ A frameless window with acrylic effect """

    label_background = None
    base_layout = None
    widget_base = None

    def __init__(self, parent=None, is_dark=None, form_theme_mode="Acrylic", form_theme_transparency=50):
        super().__init__(parent=parent)
        if is_dark is None:
            app_name = "AgileTiles"
            settings = QSettings(app_name, "Theme")
            self.is_dark = settings.value("IsDark", False, type=bool)
        else:
            self.is_dark = is_dark
        self.form_theme_mode = form_theme_mode
        self.form_theme_transparency = form_theme_transparency
        try:
            # 窗口设置
            self.message_box_util = message_box_util
            self.standard_title_bar = AgileTilesTitleBar(self, self.is_dark)
            self.setTitleBar(self.standard_title_bar)
            self.setWindowIcon(QIcon(":static/img/icon/icon.png"))
            self.titleBar.raise_()
            # 布局设置
            self.widget_base = None
            self.init_base_ui()
            self.setMinimumWidth(300)
            # 主题设置
            init_module.set_theme(self)
        except Exception as e:
            print(e)
        # 设置滚动条
        self.setStyleSheet(self.styleSheet() + style_util.scroll_bar_style)

    def init_base_ui(self):
        # 背景
        self.label_background = QLabel(self)
        self.label_background.hide()
        # 基础布局
        self.base_layout = QVBoxLayout(self)
        self.base_layout.setContentsMargins(10, 32, 10, 10)
        self.base_layout.setSpacing(0)
        self.widget_base = QWidget(self)
        self.widget_base.setObjectName(u"widget")
        if self.is_dark:
            self.widget_base.setStyleSheet("""
            QWidget {
                border-radius: 10px;
                border: none;
                background-color: rgba(34, 34, 34, 255);
                color: rgba(255, 255, 255, 200);
            }
            QTextBrowser {
                background-color: transparent;
            }""" + style_util.scroll_bar_style)
        else:
            self.widget_base.setStyleSheet("""
            QWidget {
                border-radius: 10px;
                border: none;
                background-color: rgba(255, 255, 255, 160);
                color: #000000;
            }
            QTextBrowser {
                background-color: transparent;
            }""" + style_util.scroll_bar_style)
        self.base_layout.addWidget(self.widget_base)
        print("初始化布局完成")

    def refresh_geometry(self, desktop):
        """设置窗口居中"""
        window_x, window_y = desktop.geometry().x(), desktop.geometry().y()
        window_width, window_height = desktop.size().width(), desktop.size().height()
        self.move(int((window_width - self.width()) / 2) + window_x, int((window_height - self.height()) / 2) + window_y)

    def resizeEvent(self, event):
        """ 重写窗口大小改变事件 """
        super().resizeEvent(event)
        # 同步更新背景标签尺寸
        if self.label_background:
            self.label_background.resize(self.width(), self.height())
