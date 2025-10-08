# coding:utf-8
import traceback

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QListView

from src.card.main_card.SettingCard.setting.setting_theme_form import Ui_Form
from src.my_component.AgileTilesAcrylicWindow.AgileTilesAcrylicWindow import AgileTilesAcrylicWindow
import src.ui.style_util as style_util
from src.constant import data_save_constant
from src.module.Box import message_box_util


class SettingThemeWindow(AgileTilesAcrylicWindow, Ui_Form):

    use_parent = None
    setting_config = None
    setting_signal = Signal(str)
    mode_list = None

    def __init__(self, parent=None, use_parent=None, setting_config=None):
        super(SettingThemeWindow, self).__init__(is_dark=use_parent.is_dark, form_theme_mode=use_parent.form_theme_mode,
                                                 form_theme_transparency=use_parent.form_theme_transparency)
        self.setupUi(self)
        # 初始化
        self.parent = parent
        self.use_parent = use_parent
        self.setting_config = setting_config
        # 布局初始化
        self.widget_base.setLayout(self.gridLayout_3)
        self.gridLayout_3.setContentsMargins(10, 10, 10, 10)
        # 设置标题栏
        self.setWindowTitle("灵卡面板 - 主题设置")
        self.titleBar.minBtn.close()
        self.titleBar.maxBtn.close()
        # 设置样式
        style_util.set_dialog_control_style(self, self.is_dark)
        self.horizontal_slider_transparency.setStyleSheet(theme_progress_style)
        self.horizontal_slider_transparency.setMinimumHeight(20)
        # 添加滑块值变化信号连接
        self.horizontal_slider_transparency.valueChanged.connect(self.on_slider_changed)
        # 重新设置QListView,否则qss QComboBox QAbstractItemView不生效
        self.combo_box_mode.setView(QListView())
        self.set_mode_list()
        # 事件
        self.push_button_ok.clicked.connect(self.push_button_submit_clicked)
        # 加载数据
        self.load_date()

    def set_mode_list(self):
        self.mode_list = ["亚克力", "半透明"]
        self.combo_box_mode.addItems(self.mode_list)

    def load_date(self):
        """
        加载数据到界面
        """
        # 设置主题
        if self.setting_config["theme"] == "Light":
            self.radio_button_color_light.setChecked(True)
        else:
            self.radio_button_color_dark.setChecked(True)
        # 设置主题模式
        if self.setting_config["themeMode"] is not None:
            if self.setting_config["themeMode"] == "Acrylic":
                self.combo_box_mode.setCurrentText("亚克力")
            else:
                self.combo_box_mode.setCurrentText("半透明")
        # 设置透明度
        if self.setting_config["themeTransparency"] is not None:
            value = int(self.setting_config["themeTransparency"])
            self.horizontal_slider_transparency.setValue(value)
            self.label_transparency.setText(f"{value}%")

    def on_slider_changed(self, value):
        """ 处理滑块值变化事件 """
        self.label_transparency.setText(f"{value}%")

    def push_button_submit_clicked(self):
        confirm = message_box_util.box_acknowledgement(self.use_parent, "注意", "确定要保存主题设置吗？")
        if confirm:
            try:
                # 主题
                if self.radio_button_color_light.isChecked():
                    self.setting_config["theme"] = "Light"
                else:
                    self.setting_config["theme"] = "Dark"
                # 主题模式
                if self.combo_box_mode.currentText() == "亚克力":
                    self.setting_config["themeMode"] = "Acrylic"
                else:
                    self.setting_config["themeMode"] = "Translucence"
                # 透明度
                self.setting_config["themeTransparency"] = int(self.horizontal_slider_transparency.value())
                # 保存数据
                self.parent.save_setting_to_main(trigger_type=data_save_constant.TRIGGER_TYPE_SETTING_THEME, in_data=self.setting_config)
                self.close()
            except Exception as e:
                traceback.print_exc()
                print(f"setting_theme push_button_submit_clicked 1 error: {str(e)}")
            return
        else:
            return

    def closeEvent(self, event):
        """重写关闭事件，确保下拉框弹出菜单关闭"""
        # 关闭主题模式下拉框
        if self.combo_box_mode.view().isVisible():
            self.combo_box_mode.hidePopup()

        # 继续正常的关闭流程
        super().closeEvent(event)


theme_progress_style = """
QSlider {
    background-color: transparent;
}
QSlider::groove:horizontal {
    background-color: #444444;
    height: 4px;
    border-radius: 2px;
}
QSlider::sub-page:horizontal {
    background-color: #666666;
    border-radius: 2px;
}
QSlider::add-page:horizontal {
    background-color: #333333;
    border-radius: 2px;
}
QSlider::handle:horizontal {
    background: #666666;
    width: 8px;      /* 竖条宽度 */
    height: 8px;    /* 竖条高度 */
    margin: -4px 0;  /* 垂直居中 */
    border-radius: 5px;
    border: 1px solid #888888;  /* 添加边框 */
}
"""