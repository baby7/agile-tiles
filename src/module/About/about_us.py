# coding:utf-8
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QCursor

from src.client import common
from src.my_component.AgileTilesAcrylicWindow.AgileTilesAcrylicWindow import AgileTilesAcrylicWindow
import src.ui.style_util as style_util
from src.constant import version_constant
from src.module.About.about_us_form import Ui_Form
from src.util import browser_util


class AboutUsWindow(AgileTilesAcrylicWindow, Ui_Form):

    use_parent = None

    def __init__(self, parent=None, use_parent=None):
        super(AboutUsWindow, self).__init__(is_dark=use_parent.is_dark, form_theme_mode=use_parent.form_theme_mode,
                                                 form_theme_transparency=use_parent.form_theme_transparency)
        self.setupUi(self)
        # 初始化
        self.use_parent = use_parent
        # 布局初始化
        self.widget_base.setLayout(self.gridLayout)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        # 设置标题栏
        self.setWindowTitle("灵卡面板 - 关于我们")
        self.titleBar.minBtn.close()
        self.titleBar.maxBtn.close()
        # 初始化界面布局
        self._init_ui()
        # 设置样式
        style_util.set_dialog_control_style(self, self.is_dark)
        # 设置文字
        self.label_title.setText(str(version_constant.get_current_version()))
        # 设置按钮
        self.push_button_link.setText(common.index_url)
        # 按钮点击事件
        self.push_button_link.clicked.connect(self.push_button_link_click)
        # 设置按钮样式
        background = "background-color: transparent; color: rgb(20, 161, 248);"
        self.push_button_link.setStyleSheet(background)
        self.push_button_link.setCursor(QCursor(Qt.PointingHandCursor))     # 鼠标手形

    def _init_ui(self):
        # 设置背景色
        background = "background-color: transparent;"
        self.label_icon.setStyleSheet(background)
        self.label_title.setStyleSheet(background)
        self.label_copyright.setStyleSheet(background)
        self.label_company.setStyleSheet(background)
        # 设置图标
        self.label_icon.setPixmap(QPixmap(":static/img/icon/icon_title.png"))
        self.label_icon.setFixedSize(128, 165)
        self.label_icon.setScaledContents(True)

    def push_button_link_click(self):
        # 用户协议
        browser_util.open_url(common.index_url)
        self.close()
