# coding:utf-8
from PySide6.QtGui import QPixmap

from src.component.AgileTilesAcrylicWindow.AgileTilesAcrylicWindow import AgileTilesAcrylicWindow
import src.ui.style_util as style_util
from src.constant import version_constant
from src.module.About.about_us_form import Ui_Form


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
        self.label_title.setText("灵卡面板 " + str(version_constant.get_current_version()))

    def _init_ui(self):
        # 设置背景色
        background = "background-color: transparent;"
        self.label_icon.setStyleSheet(background)
        self.label_title.setStyleSheet(background)
        self.label_copyright.setStyleSheet(background)
        self.label_framework.setStyleSheet(background)
        # 设置图标
        if self.is_dark:
            self.label_icon.setPixmap(QPixmap("./static/img/icon/dark/icon.png"))
        else:
            self.label_icon.setPixmap(QPixmap("./static/img/icon/light/icon.png"))
        self.label_icon.setScaledContents(True)
