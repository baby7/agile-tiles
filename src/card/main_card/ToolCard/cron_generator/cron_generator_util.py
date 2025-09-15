import traceback
from datetime import datetime
from croniter import croniter

from PySide6.QtGui import QTextOption
from PySide6.QtWidgets import (QLabel, QLineEdit, QPushButton, QVBoxLayout,
                               QWidget, QHBoxLayout, QSpinBox, QCheckBox,
                               QTextEdit, QComboBox, QApplication, QRadioButton,
                               QGridLayout, QGroupBox, QTabWidget)
from src.module import dialog_module
from src.ui import style_util


class CronGeneratorPopup(QWidget):

    def __init__(self, parent=None, main_object=None, is_dark=None):
        super().__init__(parent=parent)
        # 初始化
        self.parent = parent
        self.use_parent = main_object
        # 初始化界面
        self.init_ui()
        # 设置样式
        self.setStyleSheet("background: transparent; border: none; padding: 3px;")
        style_util.set_dialog_control_style(self, is_dark)
        # 生成初始Cron表达式
        self.generate_cron()

    def refresh_theme(self, main_object):
        """刷新主题"""
        style_util.set_dialog_control_style(self, main_object.is_dark)

    def init_ui(self):
        # 主部件和布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(0, 10, 0, 10)

        # 创建选项卡
        self.tab_widget = QTabWidget()

        # 秒选项卡
        # self.second_tab = self.create_time_tab("秒", 0, 59)
        # self.tab_widget.addTab(self.second_tab, "秒")

        # 分选项卡
        self.minute_tab = self.create_time_tab("分", 0, 59)
        self.tab_widget.addTab(self.minute_tab, "分")

        # 时选项卡
        self.hour_tab = self.create_time_tab("时", 0, 23)
        self.tab_widget.addTab(self.hour_tab, "时")

        # 日选项卡
        self.day_tab = self.create_day_tab()
        self.tab_widget.addTab(self.day_tab, "日")

        # 月选项卡
        self.month_tab = self.create_time_tab("月", 1, 12)
        self.tab_widget.addTab(self.month_tab, "月")

        # 周选项卡
        self.week_tab = self.create_week_tab()
        self.tab_widget.addTab(self.week_tab, "周")

        main_layout.addWidget(self.tab_widget)

        # 按钮布局
        button_layout = QHBoxLayout()

        # 生成按钮
        generate_button = QPushButton("生成 Cron")
        generate_button.setMinimumHeight(30)
        generate_button.clicked.connect(self.generate_cron)
        button_layout.addWidget(generate_button)

        # 复制按钮
        copy_button = QPushButton("复制 Cron")
        copy_button.setMinimumHeight(30)
        copy_button.clicked.connect(self.copy_cron)
        button_layout.addWidget(copy_button)

        # 清空按钮
        clear_button = QPushButton("清空")
        clear_button.setMinimumHeight(30)
        clear_button.clicked.connect(self.clear_cron)
        button_layout.addWidget(clear_button)

        # 运行按钮
        run_button = QPushButton("运行")
        run_button.setMinimumHeight(30)
        run_button.clicked.connect(self.run_cron)
        button_layout.addWidget(run_button)

        main_layout.addLayout(button_layout)

        # Cron显示区域
        self.cron_display = QTextEdit()
        self.cron_display.setReadOnly(True)
        self.cron_display.setWordWrapMode(QTextOption.WrapMode.WrapAnywhere)
        main_layout.addWidget(self.cron_display)

    def create_time_tab(self, unit, min_val, max_val):
        """创建时间选项卡的通用方法"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)

        # 单选按钮组
        group_box = QGroupBox(f"{unit}设置")
        group_box.setStyleSheet("""QGroupBox{
            border: 1px solid rgba(125, 125, 125, 125);
            padding-top: 8px;
            padding-left: 0px;
            padding-right: 0px;
            padding-bottom: 0px;
            margin-left: 0px;
            margin-right: 0px;
        }""")
        group_layout = QVBoxLayout()

        # 每选项
        self_per = QRadioButton(f"每{unit}")
        self_per.setChecked(True)
        group_layout.addWidget(self_per)

        # 周期选项
        period_layout = QHBoxLayout()
        period_layout.setSpacing(0)
        period_layout.setContentsMargins(0, 0, 0, 0)
        period_radio = QRadioButton("周期 从")
        period_input1 = QSpinBox()
        period_input1.setMinimumWidth(68)
        period_input1.setMaximumHeight(20)
        period_input1.setRange(min_val, max_val)
        period_label2 = QLabel("到")
        period_input2 = QSpinBox()
        period_input2.setMinimumWidth(68)
        period_input2.setMaximumHeight(20)
        period_input2.setRange(min_val, max_val)
        period_input2.setValue(max_val)
        period_layout.addWidget(period_radio)
        period_layout.addWidget(period_input1)
        period_layout.addWidget(period_label2)
        period_layout.addWidget(period_input2)
        period_layout.addStretch()
        group_layout.addLayout(period_layout)

        # 循环选项
        loop_layout = QHBoxLayout()
        loop_layout.setSpacing(0)
        loop_layout.setContentsMargins(0, 0, 0, 0)
        period_layout.setSpacing(0)
        loop_radio = QRadioButton("循环 从")
        loop_input1 = QSpinBox()
        loop_input1.setMinimumWidth(68)
        loop_input1.setMaximumHeight(20)
        loop_input1.setRange(min_val, max_val)
        loop_label2 = QLabel(f"{unit}开始,每")
        loop_input2 = QSpinBox()
        loop_input2.setMinimumWidth(68)
        loop_input2.setMaximumHeight(20)
        loop_input2.setRange(1, max_val)
        loop_input2.setValue(1)
        loop_label3 = QLabel(f"{unit}执行一次")
        loop_layout.addWidget(loop_radio)
        loop_layout.addWidget(loop_input1)
        loop_layout.addWidget(loop_label2)
        loop_layout.addWidget(loop_input2)
        loop_layout.addWidget(loop_label3)
        loop_layout.addStretch()
        group_layout.addLayout(loop_layout)

        # 指定选项
        specify_radio = QRadioButton("指定")
        group_layout.addWidget(specify_radio)

        # 复选框网格
        grid_layout = QGridLayout()
        checkboxes = []
        for i in range(min_val, max_val + 1):
            checkbox = QCheckBox(str(i))
            checkboxes.append(checkbox)
            row = (i - min_val) // 6
            col = (i - min_val) % 6
            grid_layout.addWidget(checkbox, row, col)

        group_layout.addLayout(grid_layout)
        group_box.setLayout(group_layout)
        layout.addWidget(group_box)
        layout.addStretch()

        # 存储控件引用
        setattr(self, f"{unit}_per", self_per)
        setattr(self, f"{unit}_period_radio", period_radio)
        setattr(self, f"{unit}_period_input1", period_input1)
        setattr(self, f"{unit}_period_input2", period_input2)
        setattr(self, f"{unit}_loop_radio", loop_radio)
        setattr(self, f"{unit}_loop_input1", loop_input1)
        setattr(self, f"{unit}_loop_input2", loop_input2)
        setattr(self, f"{unit}_specify_radio", specify_radio)
        setattr(self, f"{unit}_checkboxes", checkboxes)

        return tab

    def create_day_tab(self):
        """创建日选项卡"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)

        # 单选按钮组
        group_box = QGroupBox("日设置")
        group_box.setStyleSheet("""QGroupBox{
            border: 1px solid rgba(125, 125, 125, 125);
            padding-top: 8px;
            padding-left: 0px;
            padding-right: 0px;
            padding-bottom: 0px;
            margin-left: 0px;
            margin-right: 0px;
        }""")
        group_layout = QVBoxLayout()

        # 每选项
        day_per = QRadioButton("每日")
        day_per.setChecked(True)
        group_layout.addWidget(day_per)

        # 周期选项
        period_layout = QHBoxLayout()
        period_layout.setSpacing(0)
        period_layout.setContentsMargins(0, 0, 0, 0)
        period_radio = QRadioButton("周期")
        period_input1 = QSpinBox()
        period_input1.setMinimumWidth(68)
        period_input1.setMaximumHeight(20)
        period_input1.setRange(1, 31)
        period_label2 = QLabel("到")
        period_input2 = QSpinBox()
        period_input2.setMinimumWidth(68)
        period_input2.setMaximumHeight(20)
        period_input2.setRange(1, 31)
        period_input2.setValue(31)
        period_layout.addWidget(period_radio)
        period_layout.addWidget(period_input1)
        period_layout.addWidget(period_label2)
        period_layout.addWidget(period_input2)
        period_layout.addStretch()
        group_layout.addLayout(period_layout)

        # 循环选项
        loop_layout = QHBoxLayout()
        loop_layout.setSpacing(0)
        loop_layout.setContentsMargins(0, 0, 0, 0)
        loop_radio = QRadioButton("循环 从")
        loop_input1 = QSpinBox()
        loop_input1.setMinimumWidth(68)
        loop_input1.setMaximumHeight(20)
        loop_input1.setRange(1, 31)
        loop_label2 = QLabel("日开始,每")
        loop_input2 = QSpinBox()
        loop_input2.setMinimumWidth(68)
        loop_input2.setMaximumHeight(20)
        loop_input2.setRange(1, 31)
        loop_input2.setValue(1)
        loop_label3 = QLabel("日执行一次")
        loop_layout.addWidget(loop_radio)
        loop_layout.addWidget(loop_input1)
        loop_layout.addWidget(loop_label2)
        loop_layout.addWidget(loop_input2)
        loop_layout.addWidget(loop_label3)
        loop_layout.addStretch()
        group_layout.addLayout(loop_layout)

        # 最近工作日选项
        workday_radio = QRadioButton("最近的工作日")
        group_layout.addWidget(workday_radio)

        # 本月最后一天选项
        lastday_radio = QRadioButton("本月最后一天")
        group_layout.addWidget(lastday_radio)

        # 指定选项
        specify_radio = QRadioButton("指定")
        group_layout.addWidget(specify_radio)

        # 复选框网格
        grid_layout = QGridLayout()
        checkboxes = []
        for i in range(1, 32):
            checkbox = QCheckBox(str(i))
            checkboxes.append(checkbox)
            row = (i - 1) // 6
            col = (i - 1) % 6
            grid_layout.addWidget(checkbox, row, col)

        group_layout.addLayout(grid_layout)
        group_box.setLayout(group_layout)
        layout.addWidget(group_box)
        layout.addStretch()

        # 存储控件引用
        self.day_per = day_per
        self.day_period_radio = period_radio
        self.day_period_input1 = period_input1
        self.day_period_input2 = period_input2
        self.day_loop_radio = loop_radio
        self.day_loop_input1 = loop_input1
        self.day_loop_input2 = loop_input2
        self.day_workday_radio = workday_radio
        self.day_lastday_radio = lastday_radio
        self.day_specify_radio = specify_radio
        self.day_checkboxes = checkboxes

        return tab

    def create_week_tab(self):
        """创建周选项卡"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)

        # 单选按钮组
        group_box = QGroupBox("周设置")
        group_box.setStyleSheet("""QGroupBox{
            border: 1px solid rgba(125, 125, 125, 125);
            padding-top: 8px;
            padding-left: 0px;
            padding-right: 0px;
            padding-bottom: 0px;
            margin-left: 0px;
            margin-right: 0px;
        }""")
        group_layout = QVBoxLayout()

        # 每选项
        week_per = QRadioButton("每周")
        week_per.setChecked(True)
        group_layout.addWidget(week_per)

        # 周期选项
        period_layout = QHBoxLayout()
        period_layout.setSpacing(0)
        period_layout.setContentsMargins(0, 0, 0, 0)
        period_radio = QRadioButton("周期 从")
        period_combo1 = QComboBox()
        period_combo1.addItems(["周日", "周一", "周二", "周三", "周四", "周五", "周六"])
        period_label2 = QLabel("到")
        period_combo2 = QComboBox()
        period_combo2.addItems(["周日", "周一", "周二", "周三", "周四", "周五", "周六"])
        period_combo2.setCurrentIndex(6)
        period_layout.addWidget(period_radio)
        period_layout.addWidget(period_combo1)
        period_layout.addWidget(period_label2)
        period_layout.addWidget(period_combo2)
        period_layout.addStretch()
        group_layout.addLayout(period_layout)

        # 第几个周几选项
        nth_layout = QHBoxLayout()
        nth_layout.setSpacing(0)
        nth_radio = QRadioButton("第")
        nth_combo1 = QComboBox()
        nth_combo1.addItems(["1", "2", "3", "4", "5", "最后"])
        nth_label = QLabel("个")
        nth_combo2 = QComboBox()
        nth_combo2.addItems(["周日", "周一", "周二", "周三", "周四", "周五", "周六"])
        nth_layout.addWidget(nth_radio)
        nth_layout.addWidget(nth_combo1)
        nth_layout.addWidget(nth_label)
        nth_layout.addWidget(nth_combo2)
        nth_layout.addStretch()
        group_layout.addLayout(nth_layout)

        # 指定选项
        specify_radio = QRadioButton("指定")
        group_layout.addWidget(specify_radio)

        # 复选框网格
        grid_layout = QGridLayout()
        week_days = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"]
        checkboxes = []
        for i, day in enumerate(week_days):
            checkbox = QCheckBox(day)
            checkboxes.append(checkbox)
            row = i // 4
            col = i % 4
            grid_layout.addWidget(checkbox, row, col)

        group_layout.addLayout(grid_layout)
        group_box.setLayout(group_layout)
        layout.addWidget(group_box)
        layout.addStretch()

        # 存储控件引用
        self.week_per = week_per
        self.week_period_radio = period_radio
        self.week_period_combo1 = period_combo1
        self.week_period_combo2 = period_combo2
        self.week_nth_radio = nth_radio
        self.week_nth_combo1 = nth_combo1
        self.week_nth_combo2 = nth_combo2
        self.week_specify_radio = specify_radio
        self.week_checkboxes = checkboxes

        return tab

    def generate_cron(self):
        """生成Cron表达式并显示"""
        try:
            # 获取各字段的Cron表达式部分
            # second = self.get_field_expression("秒", 0, 59)
            minute = self.get_field_expression("分", 0, 59)
            hour = self.get_field_expression("时", 0, 23)
            day = self.get_day_expression()
            month = self.get_field_expression("月", 1, 12)
            week = self.get_week_expression()

            # 组合成完整的Cron表达式
            # cron_expression = f"{second} {minute} {hour} {day} {month} {week}"
            cron_expression = f"{minute} {hour} {day} {month} {week}"

            # 显示结果
            self.cron_display.setPlainText(cron_expression)

        except Exception as e:
            dialog_module.box_information(self.use_parent, "错误", f"生成Cron表达式时出错: {str(e)}")

    def get_field_expression(self, field, min_val, max_val):
        """获取字段的Cron表达式部分"""
        per = getattr(self, f"{field}_per")
        period_radio = getattr(self, f"{field}_period_radio")
        period_input1 = getattr(self, f"{field}_period_input1")
        period_input2 = getattr(self, f"{field}_period_input2")
        loop_radio = getattr(self, f"{field}_loop_radio")
        loop_input1 = getattr(self, f"{field}_loop_input1")
        loop_input2 = getattr(self, f"{field}_loop_input2")
        specify_radio = getattr(self, f"{field}_specify_radio")
        checkboxes = getattr(self, f"{field}_checkboxes")

        if per.isChecked():
            return "*"
        elif period_radio.isChecked():
            return f"{period_input1.value()}-{period_input2.value()}"
        elif loop_radio.isChecked():
            return f"{loop_input1.value()}/{loop_input2.value()}"
        elif specify_radio.isChecked():
            selected = []
            for i, checkbox in enumerate(checkboxes):
                if checkbox.isChecked():
                    selected.append(str(i + min_val))
            if not selected:
                return "*"
            return ",".join(selected)
        return "*"

    def get_day_expression(self):
        """获取日的Cron表达式部分"""
        if self.day_per.isChecked():
            return "*"
        elif self.day_period_radio.isChecked():
            return f"{self.day_period_input1.value()}-{self.day_period_input2.value()}"
        elif self.day_loop_radio.isChecked():
            return f"{self.day_loop_input1.value()}/{self.day_loop_input2.value()}"
        elif self.day_workday_radio.isChecked():
            return "W"
        elif self.day_lastday_radio.isChecked():
            return "L"
        elif self.day_specify_radio.isChecked():
            selected = []
            for i, checkbox in enumerate(self.day_checkboxes):
                if checkbox.isChecked():
                    selected.append(str(i + 1))
            if not selected:
                return "*"
            return ",".join(selected)
        return "*"

    def get_week_expression(self):
        """获取周的Cron表达式部分"""
        if self.week_per.isChecked():
            return "?"
        elif self.week_period_radio.isChecked():
            start = self.week_period_combo1.currentIndex()
            end = self.week_period_combo2.currentIndex()
            return f"{start}-{end}"
        elif self.week_nth_radio.isChecked():
            nth = self.week_nth_combo1.currentIndex() + 1
            if nth == 6:  # 最后
                nth = "L"
            day = self.week_nth_combo2.currentIndex()
            return f"{day}#{nth}"
        elif self.week_specify_radio.isChecked():
            selected = []
            for i, checkbox in enumerate(self.week_checkboxes):
                if checkbox.isChecked():
                    selected.append(str(i))
            if not selected:
                return "?"
            return ",".join(selected)
        return "?"

    def copy_cron(self):
        """复制Cron表达式到剪贴板"""
        if not self.cron_display.toPlainText().strip():
            dialog_module.box_information(self.use_parent, "提示", "没有Cron表达式可复制")
            return
        QApplication.clipboard().setText(self.cron_display.toPlainText())
        dialog_module.box_information(self.use_parent, "复制成功", "Cron表达式已复制到剪贴板")

    def clear_cron(self):
        """清空Cron显示区域"""
        self.cron_display.clear()

    # 新增运行测试方法
    def run_cron(self):
        """运行Cron表达式，显示最近十次运行时间"""
        try:
            cron_expression = self.cron_display.toPlainText().strip()
            if not cron_expression:
                dialog_module.box_information(self.use_parent, "提示", "请先生成Cron表达式")
                return
            # 获取当前时间作为起始点
            now = datetime.now()
            # 使用croniter计算最近十次运行时间
            iter = croniter(cron_expression, now)
            next_times = []
            for i in range(10):
                next_time = iter.get_next(datetime)
                next_times.append(next_time)
            # 格式化输出
            title = "最近十次运行时间"
            result = ""
            for i, time in enumerate(next_times):
                result += f"{time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            # 显示结果
            dialog_module.box_information(self.use_parent, title, result)
        except Exception as e:
            traceback.print_exc()
            dialog_module.box_information(self.use_parent, "错误", f"计算运行时间时出错: {str(e)}")