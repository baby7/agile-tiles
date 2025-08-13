# coding:utf-8
import sys
import traceback

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QListView

from src.card.main_card.SettingCard.setting.setting_system_form import Ui_Form
import src.ui.style_util as style_util
import src.constant.data_save_constant as data_save_constant
from src.component.AgileTilesAcrylicWindow.AgileTilesAcrylicWindow import AgileTilesAcrylicWindow
from src.component.GlobalHotkeyManager.GlobalHotkeyManager import GlobalHotkeyManager
from src.util import winreg_util
from src.module.Box import message_box_util


class SettingSystemWindow(AgileTilesAcrylicWindow, Ui_Form):

    use_parent = None
    setting_config = None
    setting_signal = Signal(str)
    old_wake_up_keyboard = None
    old_translate_keyboard = None

    def __init__(self, parent=None, use_parent=None, setting_config=None):
        super(SettingSystemWindow, self).__init__(is_dark=use_parent.is_dark, form_theme_mode=use_parent.form_theme_mode,
                                                  form_theme_transparency=use_parent.form_theme_transparency)
        self.setupUi(self)
        # 初始化
        self.parent = parent
        self.use_parent = use_parent
        self.setting_config = setting_config
        # 初始化布局
        self.widget_base.setLayout(self.gridLayout_4)
        self.gridLayout_4.setContentsMargins(10, 10, 10, 10)
        # 设置标题栏
        self.setWindowTitle("灵卡面板 - 系统设置")
        self.titleBar.minBtn.close()
        self.titleBar.maxBtn.close()
        # 重新设置QListView,否则qss QComboBox QAbstractItemView不生效
        self.combo_box_wake_up_main_keyboard.setView(QListView())
        self.combo_box_wake_up_vice_keyboard.setView(QListView())
        self.combo_box_translate_main_keyboard.setView(QListView())
        self.combo_box_translate_vice_keyboard.setView(QListView())
        self.set_main_keyboard_list()
        self.set_vice_keyboard_list()
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
        # 开机自启动
        if winreg_util.is_auto_start_enabled():
            self.check_box_self_starting.setChecked(True)
        else:
            self.check_box_self_starting.setChecked(False)
        # 键盘唤醒是否启用
        if "wakeUpByKeyboard" in self.setting_config and self.setting_config["wakeUpByKeyboard"]:
            self.check_box_wake_up_keyboard.setChecked(True)
        else:
            self.check_box_wake_up_keyboard.setChecked(False)
        # 截图翻译是否启用
        if "translateByKeyboard" in self.setting_config and self.setting_config["translateByKeyboard"]:
            self.check_box_translate_keyboard.setChecked(True)
        else:
            self.check_box_translate_keyboard.setChecked(False)
        # 快捷键
        if "wakeUpByKeyboardType" in self.setting_config and self.setting_config["wakeUpByKeyboardType"] is not None:
            self.combo_box_wake_up_main_keyboard.setCurrentText(self.setting_config["wakeUpByKeyboardType"].split("+")[0])
            self.combo_box_wake_up_vice_keyboard.setCurrentText(self.setting_config["wakeUpByKeyboardType"].split("+")[1])
        else:
            self.combo_box_wake_up_main_keyboard.setCurrentText("Ctrl")
            self.combo_box_wake_up_vice_keyboard.setCurrentText("1")
        if "translateByKeyboardType" in self.setting_config and self.setting_config["translateByKeyboardType"] is not None:
            self.combo_box_translate_main_keyboard.setCurrentText(self.setting_config["translateByKeyboardType"].split("+")[0])
            self.combo_box_translate_vice_keyboard.setCurrentText(self.setting_config["translateByKeyboardType"].split("+")[1])
        else:
            self.combo_box_translate_main_keyboard.setCurrentText("Ctrl")
            self.combo_box_translate_vice_keyboard.setCurrentText("2")
        # 保存旧快捷键
        if "wakeUpByKeyboard" in self.setting_config and self.setting_config["wakeUpByKeyboard"]:
            if "wakeUpByKeyboardType" in self.setting_config and self.setting_config["wakeUpByKeyboardType"] is not None:
                self.old_wake_up_keyboard = self.setting_config["wakeUpByKeyboardType"]
        if "translateByKeyboard" in self.setting_config and self.setting_config["translateByKeyboard"]:
            if "translateByKeyboardType" in self.setting_config and self.setting_config["translateByKeyboardType"] is not None:
                self.old_translate_keyboard = self.setting_config["translateByKeyboardType"]

    def set_main_keyboard_list(self):
        main_keyboard_list = ["Ctrl", "Shift", "Alt", "Win"]
        self.combo_box_wake_up_main_keyboard.addItems(main_keyboard_list)
        self.combo_box_translate_main_keyboard.addItems(main_keyboard_list)

    def set_vice_keyboard_list(self):
        vice_keyboard_list = ["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12",
                "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        self.combo_box_wake_up_vice_keyboard.addItems(vice_keyboard_list)
        self.combo_box_translate_vice_keyboard.addItems(vice_keyboard_list)

    def push_button_submit_clicked(self):
        # 检测特殊快捷键
        special_key_list = [
            ("Alt", "f4"),  # 关闭程序
            ("Win", "r"),   # 运行程序
            ("Win", "d"),   # 显示桌面
            ("Win", "m"),   # 最小化
            ("Win", "e"),   # 打开文件管理器
            ("Win", "x"),   # 运行程序
            ("Win", "s"),   # 显示系统设置
            ("Win", "l"),   # 锁屏
        ]
        # 检测快捷键
        if self.check_box_wake_up_keyboard.isChecked():
            for special_key in special_key_list:
                if (self.combo_box_wake_up_main_keyboard.currentText() == special_key[0]
                        and self.combo_box_wake_up_vice_keyboard.currentText() == special_key[1]):
                    message_box_util.box_information(self.use_parent, "错误", "不可设置的快捷键" + special_key[0] + "+" + special_key[1])
                    return
            # 首先检测快捷键是否是之前设置的快捷键
            if (self.old_wake_up_keyboard != self.combo_box_wake_up_main_keyboard.currentText() + "+" + self.combo_box_wake_up_vice_keyboard.currentText()
            and self.old_wake_up_keyboard != self.combo_box_translate_main_keyboard.currentText() + "+" + self.combo_box_translate_vice_keyboard.currentText()):
                # 再检测快捷键是否被其他程序占用
                hotkey = self.combo_box_wake_up_main_keyboard.currentText() + "+" + self.combo_box_wake_up_vice_keyboard.currentText()
                if GlobalHotkeyManager.is_hotkey_occupied(win_id=self.use_parent.winId(), key_combination=hotkey):
                    message_box_util.box_information(self.use_parent, "错误", "界面展示/隐藏快捷键已被占用")
                    return
        if self.check_box_translate_keyboard.isChecked():
            for special_key in special_key_list:
                if (self.combo_box_translate_main_keyboard.currentText() == special_key[0]
                        and self.combo_box_translate_vice_keyboard.currentText() == special_key[1]):
                    message_box_util.box_information(self.use_parent, "错误", "不可设置的快捷键" + special_key[0] + "+" + special_key[1])
                    return
            # 首先检测快捷键是否是之前设置的快捷键
            if (self.old_translate_keyboard != self.combo_box_wake_up_main_keyboard.currentText() + "+" + self.combo_box_wake_up_vice_keyboard.currentText()
            and self.old_translate_keyboard != self.combo_box_translate_main_keyboard.currentText() + "+" + self.combo_box_translate_vice_keyboard.currentText()):
                # 检测快捷键是否被占用
                hotkey = self.combo_box_translate_main_keyboard.currentText() + "+" + self.combo_box_translate_vice_keyboard.currentText()
                if GlobalHotkeyManager.is_hotkey_occupied(win_id=self.use_parent.winId(), key_combination=hotkey):
                    message_box_util.box_information(self.use_parent, "错误", "截图翻译快捷键已被占用")
                    return
        # 是否相同
        if self.check_box_wake_up_keyboard.isChecked() and self.check_box_translate_keyboard.isChecked():
            if (self.combo_box_wake_up_main_keyboard.currentText() == self.combo_box_translate_main_keyboard.currentText()
                    and self.combo_box_wake_up_vice_keyboard.currentText() == self.combo_box_translate_vice_keyboard.currentText()):
                message_box_util.box_information(self.use_parent, "错误", "两个快捷键不能相同")
                return
        # 确认
        confirm = message_box_util.box_acknowledgement(self.use_parent, "注意", "确定要保存快捷键吗？")
        if confirm:
            # 开机自启动
            try:
                if self.check_box_self_starting.isChecked():
                    winreg_util.set_auto_start(True)
                else:
                    winreg_util.set_auto_start(False)
            except Exception as e:
                traceback.print_exc()
                print(f"设置开机自启动失败: {e}", file=sys.stderr)
                message_box_util.box_information(self.use_parent, "错误", "设置开机自启动失败")
            # 键盘唤醒
            if self.check_box_wake_up_keyboard.isChecked():
                self.setting_config["wakeUpByKeyboard"] = True
            else:
                self.setting_config["wakeUpByKeyboard"] = False
            # 截图翻译
            if self.check_box_translate_keyboard.isChecked():
                self.setting_config["translateByKeyboard"] = True
            else:
                self.setting_config["translateByKeyboard"] = False
            # 快捷键
            self.setting_config["wakeUpByKeyboardType"] = (self.combo_box_wake_up_main_keyboard.currentText()
                                                           + "+" + self.combo_box_wake_up_vice_keyboard.currentText())
            self.setting_config["translateByKeyboardType"] = (self.combo_box_translate_main_keyboard.currentText()
                                                              + "+" + self.combo_box_translate_vice_keyboard.currentText())
            self.parent.save_setting_to_main(trigger_type=data_save_constant.TRIGGER_TYPE_SETTING_SYSTEM, in_data=self.setting_config)
            self.close()
            return
        else:
            return

    def closeEvent(self, event):
        """重写关闭事件，确保下拉框弹出菜单关闭"""
        # 关闭主键盘下拉框
        if self.combo_box_wake_up_main_keyboard.view().isVisible():
            self.combo_box_wake_up_main_keyboard.hidePopup()
        if self.combo_box_translate_main_keyboard.view().isVisible():
            self.combo_box_translate_main_keyboard.hidePopup()
        # 关闭副键盘下拉框
        if self.combo_box_wake_up_vice_keyboard.view().isVisible():
            self.combo_box_wake_up_vice_keyboard.hidePopup()
        if self.combo_box_translate_vice_keyboard.view().isVisible():
            self.combo_box_translate_vice_keyboard.hidePopup()

        # 继续正常的关闭流程
        super().closeEvent(event)
