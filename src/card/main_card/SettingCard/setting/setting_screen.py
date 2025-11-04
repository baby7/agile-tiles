# coding:utf-8
from PySide6.QtCore import Signal

from src.constant import data_save_constant
from src.card.main_card.SettingCard.setting.setting_screen_form import Ui_Form
from src.my_component.AgileTilesAcrylicWindow.AgileTilesAcrylicWindow import AgileTilesAcrylicWindow
import src.ui.style_util as style_util
from src.module.Box import message_box_util


class SettingScreenWindow(AgileTilesAcrylicWindow, Ui_Form):

    parent = None
    use_parent = None
    setting_config = None
    setting_signal = Signal(str)

    def __init__(self, parent=None, use_parent=None, setting_config=None):
        super(SettingScreenWindow, self).__init__(is_dark=use_parent.is_dark, form_theme_mode=use_parent.form_theme_mode,
                                                 form_theme_transparency=use_parent.form_theme_transparency)
        # 初始化UI
        self.setupUi(self)
        # 初始化
        self.parent = parent
        self.use_parent = use_parent
        self.setting_config = setting_config
        # 布局初始化
        self.widget_base.setLayout(self.gridLayout_2)
        self.gridLayout_2.setContentsMargins(10, 10, 10, 10)
        # 设置标题栏
        self.setWindowTitle("灵卡面板 - 界面设置")
        self.titleBar.minBtn.close()
        self.titleBar.maxBtn.close()
        # 加载数据
        self.load_date()
        # 点击事件
        self.push_button_ok.clicked.connect(self.push_button_submit_clicked)
        # 设置样式
        style_util.set_dialog_control_style(self, self.is_dark)

    def load_date(self):
        """
        加载数据到界面
        """
        try:
            # 窗口弹出动画类型
            if self.setting_config['formAnimationType'] == "Line":
                self.radio_button_form_animation_line.setChecked(True)
            else:
                self.radio_button_form_animation_elastic.setChecked(True)
            # 窗口弹出动画时间
            self.spin_box_form_animation_time.setValue(self.setting_config['formAnimationTime'])
            # 是否启用侧边弹出功能
            if self.setting_config["wakeUpByMouse"]:
                self.check_box_side_popup.setChecked(True)
            else:
                self.check_box_side_popup.setChecked(False)
            # 侧边弹出动画时间
            self.spin_box_side_popup_animation_time.setValue(self.setting_config["wakeUpByMouseTime"])
            # 鼠标离开隐藏窗口
            if self.setting_config["wakeUpByMouseHide"] == "Forever":
                self.radio_button_form_hide_by_mouse_forever.setChecked(True)
            else:
                self.radio_button_form_hide_by_mouse_only_mouse.setChecked(True)
            # 字体
            self.font_combo_box.setCurrentText(self.setting_config['fontName'])
        except Exception as e:
            print(f"setting_screen load_date 2 error: {str(e)}")


    def push_button_submit_clicked(self):
        confirm = message_box_util.box_acknowledgement(self.use_parent, "注意", "确定要保存界面设置吗？")
        if confirm:
            try:
                # 窗口弹出动画类型
                if self.radio_button_form_animation_line.isChecked():
                    self.setting_config['formAnimationType'] = "Line"
                else:
                    self.setting_config['formAnimationType'] = "Elastic"
                # 窗口弹出动画时间
                self.setting_config['formAnimationTime'] = self.spin_box_form_animation_time.value()
                # 是否启用侧边弹出功能
                if self.check_box_side_popup.isChecked():
                    self.setting_config["wakeUpByMouse"] = True
                else:
                    self.setting_config["wakeUpByMouse"] = False
                # 侧边弹出动画时间
                self.setting_config["wakeUpByMouseTime"] = self.spin_box_side_popup_animation_time.value()
                # 鼠标离开隐藏窗口
                if self.radio_button_form_hide_by_mouse_forever.isChecked():
                    self.setting_config["wakeUpByMouseHide"] = "Forever"
                else:
                    self.setting_config["wakeUpByMouseHide"] = "OnlyMouse"
                # 字体
                self.setting_config['fontName'] = self.font_combo_box.currentText()
                # 保存数据
                self.parent.save_setting_to_main(trigger_type=data_save_constant.TRIGGER_TYPE_SETTING_SCREEN, in_data=self.setting_config)
                self.close()
            except Exception as e:
                print(f"setting_screen push_button_submit_clicked 1 error: {str(e)}")
            return
        else:
            return

    def closeEvent(self, event):
        """重写关闭事件，确保下拉框弹出菜单关闭"""
        # 关闭字体下拉框
        if self.font_combo_box.view().isVisible():
            self.font_combo_box.hidePopup()
        # 继续正常的关闭流程
        super().closeEvent(event)
