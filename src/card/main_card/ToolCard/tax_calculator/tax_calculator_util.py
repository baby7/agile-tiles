from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QDoubleSpinBox,
                               QTabWidget, QTableWidget, QTableWidgetItem, QGroupBox, QScrollArea, QFrame)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QFont

from src.module import dialog_module
from src.ui import style_util


class TaxResultDialog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        # 主布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # 结果容器
        self.result_frame = QFrame()
        self.result_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 12px;
            }
        """)

        frame_layout = QVBoxLayout(self.result_frame)

        # 标题
        title_label = QLabel("个人所得税计算结果")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("padding: 5px;")
        frame_layout.addWidget(title_label)

        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        frame_layout.addWidget(line)

        # 结果内容
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setStyleSheet("""
            QTextEdit {
                border: none;
                background: transparent;
                font-size: 14px;
                padding: 10px;
            }
        """)
        frame_layout.addWidget(self.result_text)

        # 返回按钮
        back_button = QPushButton("返回计算器")
        back_button.clicked.connect(self.close_result)
        frame_layout.addWidget(back_button)

        layout.addWidget(self.result_frame)

        # 设置动画
        self.animation = QPropertyAnimation(self.result_frame, b"geometry")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.OutBack)

        # 修复：添加关闭动画
        self.close_animation = QPropertyAnimation(self.result_frame, b"geometry")
        self.close_animation.setDuration(300)
        self.close_animation.setEasingCurve(QEasingCurve.InBack)

        # 修复：添加标志位防止重复触发
        self.is_showing = False
        self.is_closing = False

    def show_result(self, use_parent, result_text):
        # 修复：防止重复显示
        if self.is_showing or self.is_closing:
            return
        self.is_showing = True
        self.result_text.setPlainText(result_text)
        self.show()

        start_rect = QRect(
            0,
            0,
            use_parent.width(),
            use_parent.height()
        )

        # 修复：设置正确的初始位置
        self.setGeometry(start_rect)
        self.result_frame.setGeometry(start_rect)

        # 修复：简化动画，直接显示而不使用动画
        self.is_showing = False

    def close_result(self):
        # 修复：防止重复关闭
        if self.is_closing:
            return

        self.is_closing = True
        self.hide()
        self.is_closing = False

    # 修复：重写关闭事件
    def closeEvent(self, event):
        self.close_result()
        event.accept()


class TaxCalculatorPopup(QWidget):
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

    def init_ui(self):
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 创建标签页
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # 计算器标签页
        self.calculator_tab = self.create_calculator_tab()
        self.tab_widget.addTab(self.calculator_tab, "💰 计算器")

        # 税率表标签页
        self.tax_rate_tab = self.create_tax_rate_tab()
        self.tab_widget.addTab(self.tax_rate_tab, "📊 税率表")

        # 专项附加扣除标签页
        self.deduction_tab = self.create_deduction_tab()
        self.tab_widget.addTab(self.deduction_tab, "📋 专项扣除")

        # 按钮区域
        self.create_button_area(main_layout)

        # 初始化结果对话框
        self.result_dialog = TaxResultDialog(self)
        self.result_dialog.hide()

    def create_calculator_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)

        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet("QScrollArea { border: none; }")
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # 收入信息组
        income_group = QGroupBox("📈 收入信息")
        income_group.setStyleSheet(self.get_groupbox_style())
        income_layout = QVBoxLayout(income_group)

        self.add_input_row(income_layout, "年收入（元）：", "annual_income", 0, 99999999)
        scroll_layout.addWidget(income_group)

        # 基本减除费用组
        basic_group = QGroupBox("📉 基本减除费用")
        basic_group.setStyleSheet(self.get_groupbox_style())
        basic_layout = QVBoxLayout(basic_group)

        basic_row = QVBoxLayout()
        basic_label = QLabel("基本减除费用（元/年）：")
        self.basic_deduction_input = QDoubleSpinBox()
        self.basic_deduction_input.setRange(0, 999999)
        self.basic_deduction_input.setValue(60000)
        self.basic_deduction_input.setDecimals(2)
        self.basic_deduction_input.setSuffix(" 元/年")
        self.basic_deduction_input.setReadOnly(True)
        basic_row.addWidget(basic_label)
        basic_row.addWidget(self.basic_deduction_input)
        basic_layout.addLayout(basic_row)

        scroll_layout.addWidget(basic_group)

        # 专项扣除组
        special_group = QGroupBox("🛡️ 专项扣除（年）")
        special_group.setStyleSheet(self.get_groupbox_style())
        special_layout = QVBoxLayout(special_group)

        self.add_input_row(special_layout, "社会保险（五险一金）（元/年）：", "social_insurance", 0, 999999)
        scroll_layout.addWidget(special_group)

        # 专项附加扣除组
        additional_group = QGroupBox("🎯 专项附加扣除（年）")
        additional_group.setStyleSheet(self.get_groupbox_style())
        additional_layout = QVBoxLayout(additional_group)

        self.add_input_row(additional_layout, "子女教育（2000元/月/子女）：", "child_education", 0, 999999)
        self.add_input_row(additional_layout, "继续教育（学历400元/月，职业证书3600元）：", "continuing_education", 0, 999999)
        self.add_input_row(additional_layout, "住房贷款利息（1000元/月）：", "housing_loan", 0, 999999)
        self.add_input_row(additional_layout, "住房租金（800-1500元/月）：", "housing_rent", 0, 999999)
        self.add_input_row(additional_layout, "赡养老人（3000元/月）：", "elder_support", 0, 999999)
        self.add_input_row(additional_layout, "三岁以下婴幼儿照护（2000元/月/幼儿）：", "child_care", 0, 999999)
        self.add_input_row(additional_layout, "大病医疗（80000元以内据实扣除）：", "medical_expense", 0, 80000)
        self.add_input_row(additional_layout, "个人养老金（12000元/年）：", "personal_pension", 0, 12000)
        self.add_input_row(additional_layout, "税优健康险（2400元/年）：", "health_insurance", 0, 2400)
        self.add_input_row(additional_layout, "其他扣除：", "other_deduction", 0, 999999)

        scroll_layout.addWidget(additional_group)

        # 已预缴税额组
        prepaid_group = QGroupBox("🧾 已预缴税额")
        prepaid_group.setStyleSheet(self.get_groupbox_style())
        prepaid_layout = QVBoxLayout(prepaid_group)

        self.add_input_row(prepaid_layout, "已预缴税额：", "prepaid_tax", 0, 999999)

        scroll_layout.addWidget(prepaid_group)

        scroll_area.setWidget(scroll_content)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        return tab

    def add_input_row(self, layout, label_text, input_name, min_val, max_val):
        row = QVBoxLayout()
        label = QLabel(label_text)
        input_field = QDoubleSpinBox()
        input_field.setRange(min_val, max_val)
        input_field.setDecimals(2)
        input_field.setSuffix(" 元")

        # 保存到实例变量
        setattr(self, f"{input_name}_input", input_field)

        row.addWidget(label)
        row.addWidget(input_field)
        layout.addLayout(row)

    def get_groupbox_style(self):
        return "QGroupBox{border: 1px solid rgba(125, 125, 125, 125); padding-top: 8px;}"

    def create_tax_rate_tab(self):
        tab = QWidget()
        tab.setStyleSheet("background: transparent; border: none;")
        layout = QVBoxLayout(tab)

        # 税率表标题
        rate_title = QLabel("个人所得税税率表（工资、薪金所得适用）")
        rate_title_font = QFont()
        rate_title_font.setBold(True)
        rate_title.setFont(rate_title_font)
        rate_title.setAlignment(Qt.AlignCenter)
        rate_title.setStyleSheet("color: #1565c0; padding: 10px;")
        layout.addWidget(rate_title)

        # 创建税率表
        self.tax_rate_table = QTableWidget()
        self.tax_rate_table.setColumnCount(4)
        self.tax_rate_table.setHorizontalHeaderLabels(["级数", "应纳税所得额", "税率", "速算扣除"])
        self.tax_rate_table.setStyleSheet("""
            QTableWidget {
                background: transparent;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QHeaderView::section {
                background: transparent;
                padding: 8px;
                border: 1px solid #90caf9;
                font-weight: bold;
            }
        """)

        # 税率数据
        tax_rates = [
            ("1", "不超过36000元", "3%", "0"),
            ("2", "36000-144000元", "10%", "2520"),
            ("3", "144000-300000元", "20%", "16920"),
            ("4", "300000-420000元", "25%", "31920"),
            ("5", "420000-660000元", "30%", "52920"),
            ("6", "660000-960000元", "35%", "85920"),
            ("7", "超过960000元", "45%", "181920")
        ]

        self.tax_rate_table.setRowCount(len(tax_rates))
        for row, data in enumerate(tax_rates):
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignCenter)
                self.tax_rate_table.setItem(row, col, item)

        self.tax_rate_table.resizeColumnsToContents()
        self.tax_rate_table.setColumnWidth(1, 150)
        layout.addWidget(self.tax_rate_table)

        return tab

    def create_deduction_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # 专项附加扣除说明
        deduction_title = QLabel("专项附加扣除明细")
        deduction_title_font = QFont()
        deduction_title_font.setBold(True)
        deduction_title.setFont(deduction_title_font)
        deduction_title.setAlignment(Qt.AlignCenter)
        deduction_title.setStyleSheet("color: #1565c0; padding: 10px;")
        layout.addWidget(deduction_title)

        # 扣除说明文本
        deduction_text = QTextEdit()
        deduction_text.setReadOnly(True)
        deduction_text.setStyleSheet("""
            QTextEdit {
                background: transparent;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 10px;
                font-size: 14px;
            }
        """)
        deduction_text.setPlainText("""
专项附加扣除项目明细：

🎯 三岁以下婴幼儿照护：2000元/月/幼儿
📚 子女教育：2000元/月/子女
🎓 继续教育：
    • 学历教育：400元/月
    • 职业资格证书：3600元/年
🏠 住房租金（根据城市不同）：
    • 直辖市、省会城市等：1500元/月
    • 市辖区户籍人口超过100万的城市：1100元/月
    • 其他城市：800元/月
🏡 住房贷款利息：1000元/月
👵 赡养老人：3000元/月
🏥 大病医疗：80000元以内据实扣除
💰 个人养老金：12000元/年
❤️ 税优健康险：2400元/年或200元/月

注：专项附加扣除需要符合相关条件，请根据实际情况填写。
        """)
        layout.addWidget(deduction_text)

        return tab

    def create_button_area(self, main_layout):
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(10, 0, 10, 10)

        # 计算按钮
        self.calculate_button = QPushButton("🧮 计算个人所得税")
        self.calculate_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: linear-gradient(45deg, #0d47a1, #1565c0);
            }
            QPushButton:pressed {
                background: linear-gradient(45deg, #08306b, #0d47a1);
            }
        """)
        self.calculate_button.clicked.connect(self.calculate_tax)
        button_layout.addWidget(self.calculate_button)

        # 重置按钮
        self.reset_button = QPushButton("🔄 重置")
        self.reset_button.setStyleSheet("""
            QPushButton {
                background: linear-gradient(45deg, #757575, #9e9e9e);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: linear-gradient(45deg, #616161, #757575);
            }
        """)
        self.reset_button.clicked.connect(self.reset_inputs)
        button_layout.addWidget(self.reset_button)

        main_layout.addLayout(button_layout)

    def calculate_tax(self):
        try:
            # 获取输入值
            annual_income = self.annual_income_input.value()
            if annual_income <= 0:
                self.show_error("请输入年收入")
                return

            basic_deduction = self.basic_deduction_input.value()
            social_insurance = self.social_insurance_input.value()

            # 专项附加扣除
            child_education = self.child_education_input.value()
            continuing_education = self.continuing_education_input.value()
            housing_loan = self.housing_loan_input.value()
            housing_rent = self.housing_rent_input.value()
            elder_support = self.elder_support_input.value()
            child_care = self.child_care_input.value()
            medical_expense = self.medical_expense_input.value()
            personal_pension = self.personal_pension_input.value()
            health_insurance = self.health_insurance_input.value()
            other_deduction = self.other_deduction_input.value()

            prepaid_tax = self.prepaid_tax_input.value()

            # 计算专项扣除总额
            special_deduction = social_insurance

            # 计算专项附加扣除总额
            additional_deduction = (child_education + continuing_education + housing_loan +
                                    housing_rent + elder_support + child_care +
                                    medical_expense + personal_pension + health_insurance)

            # 计算应纳税所得额
            taxable_income = max(0, annual_income - basic_deduction - special_deduction -
                                 additional_deduction - other_deduction)

            # 根据税率表计算税额
            tax_amount = self.calculate_tax_amount(taxable_income)

            # 计算应退税额（负数表示需要补税）
            tax_refund = prepaid_tax - tax_amount

            # 格式化结果显示
            result_text = f"""
📊 个人所得税计算结果

💰 收入与扣除明细：
    年收入总额：{annual_income:,.2f} 元
    基本减除费用：{basic_deduction:,.2f} 元
    专项扣除：{special_deduction:,.2f} 元
    专项附加扣除：{additional_deduction:,.2f} 元
    其他扣除：{other_deduction:,.2f} 元

🎯 计税基础：
    应纳税所得额：{taxable_income:,.2f} 元

🧮 税额计算：
    应缴税额：{tax_amount:,.2f} 元
    已预缴税额：{prepaid_tax:,.2f} 元

💡  最终结果：
    应退税额（负数为补税）：{tax_refund:,.2f} 元
            """

            # 添加状态标记
            if tax_refund < 0:
                result_text += f"\n⚠️  需要补缴税款：{abs(tax_refund):,.2f} 元"
            elif tax_refund > 0:
                result_text += f"\n✅  可以申请退税：{tax_refund:,.2f} 元"
            else:
                result_text += "\nℹ️  无需补税或退税"

            # 显示结果对话框
            self.result_dialog.show_result(use_parent=self, result_text=result_text)

        except Exception as e:
            self.show_error(f"计算错误：{str(e)}")

    def show_error(self, message):
        dialog_module.box_information(self.use_parent, "计算错误", message)

    def calculate_tax_amount(self, taxable_income):
        """根据应纳税所得额计算税额"""
        if taxable_income <= 0:
            return 0

        # 2025年个人所得税税率表
        tax_brackets = [
            (36000, 0.03, 0),
            (144000, 0.10, 2520),
            (300000, 0.20, 16920),
            (420000, 0.25, 31920),
            (660000, 0.30, 52920),
            (960000, 0.35, 85920),
            (float('inf'), 0.45, 181920)
        ]

        for limit, rate, deduction in tax_brackets:
            if taxable_income <= limit:
                return taxable_income * rate - deduction

        return 0

    def reset_inputs(self):
        """重置所有输入框"""
        self.annual_income_input.setValue(0)
        self.basic_deduction_input.setValue(60000)
        self.social_insurance_input.setValue(0)
        self.child_education_input.setValue(0)
        self.continuing_education_input.setValue(0)
        self.housing_loan_input.setValue(0)
        self.housing_rent_input.setValue(0)
        self.elder_support_input.setValue(0)
        self.child_care_input.setValue(0)
        self.medical_expense_input.setValue(0)
        self.personal_pension_input.setValue(0)
        self.health_insurance_input.setValue(0)
        self.other_deduction_input.setValue(0)
        self.prepaid_tax_input.setValue(0)

    def refresh_theme(self, main_object):
        """刷新主题"""
        style_util.set_dialog_control_style(self, main_object.is_dark)