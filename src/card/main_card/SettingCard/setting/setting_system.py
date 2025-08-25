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
    old_screenshot_keyboard = None
    old_search_keyboard = None

    def __init__(self, parent=None, use_parent=None, setting_config=None):
        super(SettingSystemWindow, self).__init__(is_dark=use_parent.is_dark, form_theme_mode=use_parent.form_theme_mode,
                                                  form_theme_transparency=use_parent.form_theme_transparency)
        self.setupUi(self)
        # 初始化
        self.parent = parent
        self.use_parent = use_parent
        self.setting_config = setting_config
        # 初始化布局
        self.widget_base.setLayout(self.gridLayout_5)
        self.gridLayout_5.setContentsMargins(10, 10, 10, 10)
        # 设置标题栏
        self.setWindowTitle("灵卡面板 - 系统设置")
        self.titleBar.minBtn.close()
        self.titleBar.maxBtn.close()
        # 重新设置QListView,否则qss QComboBox QAbstractItemView不生效
        self.combo_box_wake_up_main_keyboard.setView(QListView())
        self.combo_box_wake_up_vice_keyboard.setView(QListView())
        self.combo_box_screenshot_main_keyboard.setView(QListView())
        self.combo_box_screenshot_vice_keyboard.setView(QListView())
        self.combo_box_search_main_keyboard.setView(QListView())
        self.combo_box_search_vice_keyboard.setView(QListView())
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
        if "screenshotByKeyboard" in self.setting_config and self.setting_config["screenshotByKeyboard"]:
            self.check_box_screenshot_keyboard.setChecked(True)
        else:
            self.check_box_screenshot_keyboard.setChecked(False)
        # 快捷键
        if "wakeUpByKeyboardType" in self.setting_config and self.setting_config["wakeUpByKeyboardType"] is not None:
            self.combo_box_wake_up_main_keyboard.setCurrentText(self.setting_config["wakeUpByKeyboardType"].split("+")[0])
            self.combo_box_wake_up_vice_keyboard.setCurrentText(self.setting_config["wakeUpByKeyboardType"].split("+")[1])
        else:
            self.combo_box_wake_up_main_keyboard.setCurrentText("Alt")
            self.combo_box_wake_up_vice_keyboard.setCurrentText("1")
        if "screenshotByKeyboardType" in self.setting_config and self.setting_config["screenshotByKeyboardType"] is not None:
            self.combo_box_screenshot_main_keyboard.setCurrentText(self.setting_config["screenshotByKeyboardType"].split("+")[0])
            self.combo_box_screenshot_vice_keyboard.setCurrentText(self.setting_config["screenshotByKeyboardType"].split("+")[1])
        else:
            self.combo_box_screenshot_main_keyboard.setCurrentText("Alt")
            self.combo_box_screenshot_vice_keyboard.setCurrentText("2")
        if "searchByKeyboardType" in self.setting_config and self.setting_config["searchByKeyboardType"] is not None:
            self.combo_box_search_main_keyboard.setCurrentText(self.setting_config["searchByKeyboardType"].split("+")[0])
            self.combo_box_search_vice_keyboard.setCurrentText(self.setting_config["searchByKeyboardType"].split("+")[1])
        else:
            self.combo_box_search_main_keyboard.setCurrentText("Alt")
            self.combo_box_search_vice_keyboard.setCurrentText("3")
        # 保存旧快捷键
        if "wakeUpByKeyboard" in self.setting_config and self.setting_config["wakeUpByKeyboard"]:
            if "wakeUpByKeyboardType" in self.setting_config and self.setting_config["wakeUpByKeyboardType"] is not None:
                self.old_wake_up_keyboard = self.setting_config["wakeUpByKeyboardType"]
        if "screenshotByKeyboard" in self.setting_config and self.setting_config["screenshotByKeyboard"]:
            if "screenshotByKeyboardType" in self.setting_config and self.setting_config["screenshotByKeyboardType"] is not None:
                self.old_screenshot_keyboard = self.setting_config["screenshotByKeyboardType"]
        if "searchByKeyboard" in self.setting_config and self.setting_config["searchByKeyboard"]:
            if "searchByKeyboardType" in self.setting_config and self.setting_config["searchByKeyboardType"] is not None:
                self.old_search_keyboard = self.setting_config["searchByKeyboardType"]

    def set_main_keyboard_list(self):
        main_keyboard_list = ["Ctrl", "Shift", "Alt", "Win"]
        self.combo_box_wake_up_main_keyboard.addItems(main_keyboard_list)
        self.combo_box_screenshot_main_keyboard.addItems(main_keyboard_list)
        self.combo_box_search_main_keyboard.addItems(main_keyboard_list)

    def set_vice_keyboard_list(self):
        vice_keyboard_list = ["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12",
                "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        self.combo_box_wake_up_vice_keyboard.addItems(vice_keyboard_list)
        self.combo_box_screenshot_vice_keyboard.addItems(vice_keyboard_list)
        self.combo_box_search_vice_keyboard.addItems(vice_keyboard_list)

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
        old_search_keyboard_list = [
            self.old_wake_up_keyboard,
            self.old_screenshot_keyboard,
            self.old_search_keyboard
        ]
        # 检测快捷键
        if not self.check_keyboard_success(title="界面展示/隐藏",
                                           check_keyboard=self.check_box_wake_up_keyboard,
                                           main_keyboard=self.combo_box_wake_up_main_keyboard,
                                           vice_keyboard=self.combo_box_wake_up_vice_keyboard,
                                           old_search_keyboard_list=old_search_keyboard_list):
            return
        if not self.check_keyboard_success(title="截图",
                                           check_keyboard=self.check_box_screenshot_keyboard,
                                           main_keyboard=self.combo_box_screenshot_main_keyboard,
                                           vice_keyboard=self.combo_box_screenshot_vice_keyboard,
                                           old_search_keyboard_list=old_search_keyboard_list):
            return
        if not self.check_keyboard_success(title="本地搜索",
                                           check_keyboard=self.check_box_search_keyboard,
                                           main_keyboard=self.combo_box_search_main_keyboard,
                                           vice_keyboard=self.combo_box_search_vice_keyboard,
                                           old_search_keyboard_list=old_search_keyboard_list):
            return
        # 是否相同
        if self.check_keyboard_same(self.check_box_wake_up_keyboard, self.check_box_screenshot_keyboard,
                                    self.combo_box_wake_up_main_keyboard, self.combo_box_screenshot_main_keyboard,
                                    self.combo_box_wake_up_vice_keyboard, self.combo_box_screenshot_vice_keyboard):
            return
        if self.check_keyboard_same(self.check_box_wake_up_keyboard, self.check_box_search_keyboard,
                                    self.combo_box_wake_up_main_keyboard, self.combo_box_search_main_keyboard,
                                    self.combo_box_wake_up_vice_keyboard, self.combo_box_search_vice_keyboard):
            return
        if self.check_keyboard_same(self.check_box_search_keyboard, self.check_box_screenshot_keyboard,
                                    self.combo_box_search_main_keyboard, self.combo_box_screenshot_main_keyboard,
                                    self.combo_box_search_vice_keyboard, self.combo_box_screenshot_vice_keyboard):
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
            # 截图
            if self.check_box_screenshot_keyboard.isChecked():
                self.setting_config["screenshotByKeyboard"] = True
            else:
                self.setting_config["screenshotByKeyboard"] = False
            # 本地搜索
            if self.check_box_search_keyboard.isChecked():
                self.setting_config["searchByKeyboard"] = True
            else:
                self.setting_config["searchByKeyboard"] = False
            # 快捷键
            self.setting_config["wakeUpByKeyboardType"] = (self.combo_box_wake_up_main_keyboard.currentText()
                                                           + "+" + self.combo_box_wake_up_vice_keyboard.currentText())
            self.setting_config["screenshotByKeyboardType"] = (self.combo_box_screenshot_main_keyboard.currentText()
                                                              + "+" + self.combo_box_screenshot_vice_keyboard.currentText())
            self.setting_config["searchByKeyboardType"] = (self.combo_box_search_main_keyboard.currentText()
                                                              + "+" + self.combo_box_search_vice_keyboard.currentText())
            self.parent.save_setting_to_main(trigger_type=data_save_constant.TRIGGER_TYPE_SETTING_SYSTEM, in_data=self.setting_config)
            self.close()
            return
        else:
            return

    def check_keyboard_success(self, title, check_keyboard, main_keyboard, vice_keyboard, old_search_keyboard_list):
        if not check_keyboard.isChecked():
            return True
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
        for special_key in special_key_list:
            if main_keyboard.currentText() == special_key[0] and vice_keyboard.currentText() == special_key[1]:
                message_box_util.box_information(self.use_parent, "错误", "不可设置的快捷键" + special_key[0] + "+" + special_key[1])
                return False
        # 首先检测快捷键是否是之前设置的快捷键
        is_old_keyboard = False
        for old_search_keyboard in old_search_keyboard_list:
            if old_search_keyboard is None:
                continue
            if old_search_keyboard == self.combo_box_wake_up_main_keyboard.currentText() + "+" + self.combo_box_wake_up_vice_keyboard.currentText():
                is_old_keyboard = True
            if old_search_keyboard == self.combo_box_wake_up_vice_keyboard.currentText() + "+" + self.combo_box_wake_up_main_keyboard.currentText():
                is_old_keyboard = True
        if is_old_keyboard:
            return True
        # 检测快捷键是否被占用
        hotkey = main_keyboard.currentText() + "+" + vice_keyboard.currentText()
        if GlobalHotkeyManager.is_hotkey_occupied(win_id=self.use_parent.winId(), key_combination=hotkey):
            message_box_util.box_information(self.use_parent, "错误", f"{title}快捷键已被占用")
            return False
        # 返回正常
        return True

    # 检测两个快捷键是否相同
    def check_keyboard_same(self, check_keyboard_1, check_keyboard_2, main_keyboard_1, main_keyboard_2, vice_keyboard_1, vice_keyboard_2):
        if check_keyboard_1.isChecked() and check_keyboard_2.isChecked():
            if (main_keyboard_1.currentText() == main_keyboard_2.currentText()
                    and vice_keyboard_1.currentText() == vice_keyboard_2.currentText()):
                message_box_util.box_information(self.use_parent, "错误", "快捷键不能相同")
                return True
            else:
                return False
        else:
            return False

    def closeEvent(self, event):
        """重写关闭事件，确保下拉框弹出菜单关闭"""
        # 关闭主键盘下拉框
        if self.combo_box_wake_up_main_keyboard.view().isVisible():
            self.combo_box_wake_up_main_keyboard.hidePopup()
        if self.combo_box_screenshot_main_keyboard.view().isVisible():
            self.combo_box_screenshot_main_keyboard.hidePopup()
        if self.combo_box_search_main_keyboard.view().isVisible():
            self.combo_box_search_main_keyboard.hidePopup()
        # 关闭副键盘下拉框
        if self.combo_box_wake_up_vice_keyboard.view().isVisible():
            self.combo_box_wake_up_vice_keyboard.hidePopup()
        if self.combo_box_screenshot_vice_keyboard.view().isVisible():
            self.combo_box_screenshot_vice_keyboard.hidePopup()
        if self.combo_box_search_vice_keyboard.view().isVisible():
            self.combo_box_search_vice_keyboard.hidePopup()

        # 继续正常的关闭流程
        super().closeEvent(event)
