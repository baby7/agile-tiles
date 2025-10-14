from PySide6.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

from src.ui import style_util


class CalorieCalculatorPopup(QWidget):

    def __init__(self, parent=None, main_object=None, is_dark=None):
        super().__init__(parent=parent)
        # 初始化
        self.parent = parent
        self.use_parent = main_object
        self.updating = False  # 防止循环更新
        # 初始化界面
        self.init_ui()
        # 设置样式
        style_util.set_dialog_control_style(self, is_dark)

    def init_ui(self):
        # 主部件和布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # 千焦输入
        kj_label = QLabel("千焦 (kJ):")
        kj_label.setStyleSheet("background: transparent;")
        main_layout.addWidget(kj_label)

        self.kj_input = QLineEdit()
        self.kj_input.setPlaceholderText("输入千焦值")
        self.kj_input.textChanged.connect(self.on_kj_changed)
        main_layout.addWidget(self.kj_input)

        # 卡路里输入
        cal_label = QLabel("卡路里 (cal):")
        cal_label.setStyleSheet("background: transparent;")
        main_layout.addWidget(cal_label)

        self.cal_input = QLineEdit()
        self.cal_input.setPlaceholderText("输入卡路里值")
        self.cal_input.textChanged.connect(self.on_cal_changed)
        main_layout.addWidget(self.cal_input)

        # 大卡输入
        kcal_label = QLabel("大卡 (kcal):")
        kcal_label.setStyleSheet("background: transparent;")
        main_layout.addWidget(kcal_label)

        self.kcal_input = QLineEdit()
        self.kcal_input.setPlaceholderText("输入大卡值")
        self.kcal_input.textChanged.connect(self.on_kcal_changed)
        main_layout.addWidget(self.kcal_input)

        # 说明标签
        note_label = QLabel("提示: 1大卡 = 1000卡路里 = 4.184千焦")
        note_label.setStyleSheet("font-size: 12px; color: #666; background: transparent;")
        note_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(note_label)

    def on_kj_changed(self, text):
        """千焦输入框改变时的处理"""
        if self.updating or not text:
            return

        try:
            self.updating = True
            kj_value = float(text)
            # 千焦转大卡: 1大卡 = 4.184千焦
            kcal_value = kj_value / 4.184
            # 大卡转卡路里: 1大卡 = 1000卡路里
            cal_value = kcal_value * 1000

            self.kcal_input.setText(f"{kcal_value:.2f}")
            self.cal_input.setText(f"{cal_value:.2f}")

        except ValueError:
            # 输入无效时清空其他框
            self.kcal_input.clear()
            self.cal_input.clear()
        finally:
            self.updating = False

    def on_cal_changed(self, text):
        """卡路里输入框改变时的处理"""
        if self.updating or not text:
            return

        try:
            self.updating = True
            cal_value = float(text)
            # 卡路里转大卡: 1大卡 = 1000卡路里
            kcal_value = cal_value / 1000
            # 大卡转千焦: 1大卡 = 4.184千焦
            kj_value = kcal_value * 4.184

            self.kcal_input.setText(f"{kcal_value:.2f}")
            self.kj_input.setText(f"{kj_value:.2f}")

        except ValueError:
            # 输入无效时清空其他框
            self.kcal_input.clear()
            self.kj_input.clear()
        finally:
            self.updating = False

    def on_kcal_changed(self, text):
        """大卡输入框改变时的处理"""
        if self.updating or not text:
            return

        try:
            self.updating = True
            kcal_value = float(text)
            # 大卡转千焦: 1大卡 = 4.184千焦
            kj_value = kcal_value * 4.184
            # 大卡转卡路里: 1大卡 = 1000卡路里
            cal_value = kcal_value * 1000

            self.kj_input.setText(f"{kj_value:.2f}")
            self.cal_input.setText(f"{cal_value:.2f}")

        except ValueError:
            # 输入无效时清空其他框
            self.kj_input.clear()
            self.cal_input.clear()
        finally:
            self.updating = False

    def refresh_theme(self, main_object):
        # 设置样式
        style_util.set_dialog_control_style(self, main_object.is_dark)
