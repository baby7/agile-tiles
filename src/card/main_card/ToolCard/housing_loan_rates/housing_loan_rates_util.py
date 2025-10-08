import math
from PySide6.QtWidgets import (QWidget, QTabWidget, QVBoxLayout,
                               QGroupBox, QFormLayout, QComboBox, QPushButton, QTableWidget,
                               QTableWidgetItem, QLabel, QHeaderView, QDoubleSpinBox, QSpinBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor, QBrush

from src.my_component.AgileTilesAcrylicWindow.AgileTilesAcrylicWindow import AgileTilesAcrylicWindow
from src.ui import style_util


class MortgageCalculator(AgileTilesAcrylicWindow):
    def __init__(self, parent=None, use_parent=None, title=None, content=None):
        super().__init__(parent=parent, is_dark=use_parent.is_dark, form_theme_mode=use_parent.form_theme_mode,
                         form_theme_transparency=use_parent.form_theme_transparency)
        # 初始化
        self.parent = parent
        self.use_parent = use_parent
        # 设置标题栏
        self.setWindowTitle(title)  # 设置到标题栏
        self.titleBar.minBtn.close()
        self.titleBar.maxBtn.close()
        self.setMinimumSize(700, 900)
        # 初始化界面
        self.init_ui()
        # 设置样式
        style_util.set_dialog_control_style(self, self.is_dark)

    def init_ui(self):
        # 主部件和布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        self.widget_base.setLayout(main_layout)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # 创建标签页
        self.tab_widget = QTabWidget()
        self.tab_widget.setFont(QFont("", 10))

        # 添加标签页
        self.combined_tab = self.create_combined_tab()
        self.commercial_tab = self.create_commercial_tab()
        self.provident_tab = self.create_provident_tab()

        self.tab_widget.addTab(self.combined_tab, "组合贷款")
        self.tab_widget.addTab(self.commercial_tab, "商业贷款")
        self.tab_widget.addTab(self.provident_tab, "公积金贷款")

        main_layout.addWidget(self.tab_widget)

        # 创建还款明细表格
        self.create_payment_table(main_layout)

        # 添加底部信息
        footer_label = QLabel("中国房贷计算器 | 数据仅供参考，实际以银行计算结果为准")
        footer_label.setFont(QFont("", 8))
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_label.setStyleSheet("background: transparent; color: #7f8c8d; margin-top: 10px;")
        main_layout.addWidget(footer_label)

    def create_combined_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)

        # 贷款信息组
        loan_group = QGroupBox("贷款信息")
        loan_group.setStyleSheet("QGroupBox{border: 1px solid rgba(125, 125, 125, 125); padding-top: 8px;}")
        loan_layout = QFormLayout()
        loan_layout.setSpacing(10)

        self.combined_total_loan = QDoubleSpinBox()
        self.combined_total_loan.setRange(1, 10000000)
        self.combined_total_loan.setValue(2000000)
        self.combined_total_loan.setPrefix("¥ ")
        self.combined_total_loan.setSingleStep(10000)

        self.combined_commercial_loan = QDoubleSpinBox()
        self.combined_commercial_loan.setRange(1, 10000000)
        self.combined_commercial_loan.setValue(1000000)
        self.combined_commercial_loan.setPrefix("¥ ")
        self.combined_commercial_loan.setSingleStep(10000)

        self.combined_commercial_rate = QDoubleSpinBox()
        self.combined_commercial_rate.setRange(1, 15)
        self.combined_commercial_rate.setValue(4.3)
        self.combined_commercial_rate.setSuffix(" %")
        self.combined_commercial_rate.setSingleStep(0.1)

        self.combined_provident_loan = QDoubleSpinBox()
        self.combined_provident_loan.setRange(1, 10000000)
        self.combined_provident_loan.setValue(1000000)
        self.combined_provident_loan.setPrefix("¥ ")
        self.combined_provident_loan.setSingleStep(10000)

        self.combined_provident_rate = QDoubleSpinBox()
        self.combined_provident_rate.setRange(1, 15)
        self.combined_provident_rate.setValue(3.1)
        self.combined_provident_rate.setSuffix(" %")
        self.combined_provident_rate.setSingleStep(0.1)

        self.combined_term = QSpinBox()
        self.combined_term.setRange(1, 30)
        self.combined_term.setValue(30)
        self.combined_term.setSuffix(" 年")

        self.combined_type = QComboBox()
        self.combined_type.addItem("等额本息")
        self.combined_type.addItem("等额本金")

        loan_layout.addRow("贷款总额:", self.combined_total_loan)
        loan_layout.addRow("商业贷款金额:", self.combined_commercial_loan)
        loan_layout.addRow("商业贷款利率:", self.combined_commercial_rate)
        loan_layout.addRow("公积金贷款金额:", self.combined_provident_loan)
        loan_layout.addRow("公积金贷款利率:", self.combined_provident_rate)
        loan_layout.addRow("贷款期限:", self.combined_term)
        loan_layout.addRow("还款方式:", self.combined_type)

        loan_group.setLayout(loan_layout)
        layout.addWidget(loan_group)

        # 计算按钮
        self.combined_calculate_btn = QPushButton("计算还款计划")
        self.combined_calculate_btn.clicked.connect(lambda: self.calculate_combined())
        self.combined_calculate_btn.setMinimumHeight(30)
        layout.addWidget(self.combined_calculate_btn)

        # 结果摘要
        self.combined_result_label = QLabel()
        self.combined_result_label.setFont(QFont("", 10))
        self.combined_result_label.setStyleSheet("color: #2c3e50;")
        self.combined_result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.combined_result_label)

        return tab

    def create_commercial_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)

        # 贷款信息组
        loan_group = QGroupBox("贷款信息")
        loan_group.setStyleSheet("QGroupBox{border: 1px solid rgba(125, 125, 125, 125); padding-top: 8px;}")
        loan_layout = QFormLayout()
        loan_layout.setSpacing(10)

        self.commercial_loan = QDoubleSpinBox()
        self.commercial_loan.setRange(1, 10000000)
        self.commercial_loan.setValue(1000000)
        self.commercial_loan.setPrefix("¥ ")
        self.commercial_loan.setSingleStep(10000)

        self.commercial_rate = QDoubleSpinBox()
        self.commercial_rate.setRange(1, 15)
        self.commercial_rate.setValue(4.3)
        self.commercial_rate.setSuffix(" %")
        self.commercial_rate.setSingleStep(0.1)

        self.commercial_term = QSpinBox()
        self.commercial_term.setRange(1, 30)
        self.commercial_term.setValue(30)
        self.commercial_term.setSuffix(" 年")

        self.commercial_type = QComboBox()
        self.commercial_type.addItem("等额本息")
        self.commercial_type.addItem("等额本金")

        loan_layout.addRow("贷款金额:", self.commercial_loan)
        loan_layout.addRow("贷款利率:", self.commercial_rate)
        loan_layout.addRow("贷款期限:", self.commercial_term)
        loan_layout.addRow("还款方式:", self.commercial_type)

        loan_group.setLayout(loan_layout)
        layout.addWidget(loan_group)

        # 计算按钮
        self.commercial_calculate_btn = QPushButton("计算还款计划")
        self.commercial_calculate_btn.clicked.connect(lambda: self.calculate_commercial())
        self.commercial_calculate_btn.setMinimumHeight(30)
        layout.addWidget(self.commercial_calculate_btn)

        # 结果摘要
        self.commercial_result_label = QLabel()
        self.commercial_result_label.setFont(QFont("", 10))
        self.commercial_result_label.setStyleSheet("color: #2c3e50;")
        self.commercial_result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.commercial_result_label)

        return tab

    def create_provident_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)

        # 贷款信息组
        loan_group = QGroupBox("贷款信息")
        loan_group.setStyleSheet("QGroupBox{border: 1px solid rgba(125, 125, 125, 125); padding-top: 8px;}")
        loan_layout = QFormLayout()
        loan_layout.setSpacing(10)

        self.provident_loan = QDoubleSpinBox()
        self.provident_loan.setRange(1, 10000000)
        self.provident_loan.setValue(800000)
        self.provident_loan.setPrefix("¥ ")
        self.provident_loan.setSingleStep(10000)

        self.provident_rate = QDoubleSpinBox()
        self.provident_rate.setRange(1, 15)
        self.provident_rate.setValue(3.1)
        self.provident_rate.setSuffix(" %")
        self.provident_rate.setSingleStep(0.1)

        self.provident_term = QSpinBox()
        self.provident_term.setRange(1, 30)
        self.provident_term.setValue(25)
        self.provident_term.setSuffix(" 年")

        self.provident_type = QComboBox()
        self.provident_type.addItem("等额本息")
        self.provident_type.addItem("等额本金")

        loan_layout.addRow("贷款金额:", self.provident_loan)
        loan_layout.addRow("贷款利率:", self.provident_rate)
        loan_layout.addRow("贷款期限:", self.provident_term)
        loan_layout.addRow("还款方式:", self.provident_type)

        loan_group.setLayout(loan_layout)
        layout.addWidget(loan_group)

        # 计算按钮
        self.provident_calculate_btn = QPushButton("计算还款计划")
        self.provident_calculate_btn.clicked.connect(lambda: self.calculate_provident())
        self.provident_calculate_btn.setMinimumHeight(30)
        layout.addWidget(self.provident_calculate_btn)

        # 结果摘要
        self.provident_result_label = QLabel()
        self.provident_result_label.setFont(QFont("", 10))
        self.provident_result_label.setStyleSheet("color: #2c3e50;")
        self.provident_result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.provident_result_label)

        return tab

    def create_payment_table(self, layout):
        # 创建还款明细表格
        table_group = QGroupBox("还款明细")
        table_group.setStyleSheet("QGroupBox{border: 1px solid rgba(125, 125, 125, 125); padding-top: 8px;}")
        table_layout = QVBoxLayout()

        self.payment_table = QTableWidget()
        self.payment_table.setColumnCount(6)
        self.payment_table.setHorizontalHeaderLabels(
            ["期数", "月供总额", "商业贷款月供", "公积金贷款月供", "总利息", "剩余本金"])
        self.payment_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.payment_table.verticalHeader().setVisible(False)
        self.payment_table.setFont(QFont("", 9))
        self.payment_table.setEditTriggers(QTableWidget.NoEditTriggers)

        # 初始隐藏商业和公积金贷款月供列
        self.payment_table.setColumnHidden(2, True)
        self.payment_table.setColumnHidden(3, True)

        table_layout.addWidget(self.payment_table)
        table_group.setLayout(table_layout)
        layout.addWidget(table_group)

    def calculate_combined(self):
        # 获取组合贷款参数
        commercial_loan = self.combined_commercial_loan.value()
        commercial_rate = self.combined_commercial_rate.value() / 100 / 12  # 月利率
        provident_loan = self.combined_provident_loan.value()
        provident_rate = self.combined_provident_rate.value() / 100 / 12  # 月利率
        term = self.combined_term.value() * 12  # 月数
        loan_type = self.combined_type.currentText()

        # 显示商业和公积金贷款月供列
        self.payment_table.setColumnHidden(2, False)
        self.payment_table.setColumnHidden(3, False)

        # 计算商业贷款部分
        if loan_type == "等额本息":
            commercial_monthly_payment = self.calculate_equal_payment(commercial_loan, commercial_rate, term)
        else:
            commercial_monthly_payment = self.calculate_decreasing_payment(commercial_loan, commercial_rate, term)

        # 计算公积金贷款部分
        if loan_type == "等额本息":
            provident_monthly_payment = self.calculate_equal_payment(provident_loan, provident_rate, term)
        else:
            provident_monthly_payment = self.calculate_decreasing_payment(provident_loan, provident_rate, term)

        # 合并还款计划
        combined_payment = []
        total_interest = 0
        total_principal = commercial_loan + provident_loan

        for i in range(term):
            month = i + 1
            comm_payment = commercial_monthly_payment[i]
            prov_payment = provident_monthly_payment[i]

            # 合并数据
            total_payment = comm_payment["payment"] + prov_payment["payment"]
            interest = comm_payment["interest"] + prov_payment["interest"]
            principal = comm_payment["principal"] + prov_payment["principal"]
            remaining = comm_payment["remaining"] + prov_payment["remaining"]

            total_interest += interest

            combined_payment.append({
                "month": month,
                "payment": total_payment,
                "commercial_payment": comm_payment["payment"],
                "provident_payment": prov_payment["payment"],
                "interest": interest,
                "principal": principal,
                "remaining": remaining
            })

        # 显示结果摘要
        total_payment = total_principal + total_interest
        summary = f"贷款总额: ¥{total_principal:,.2f} | 支付利息: ¥{total_interest:,.2f} | 还款总额: ¥{total_payment:,.2f} | 月均还款: ¥{(total_payment / term):,.2f}"
        self.combined_result_label.setText(summary)
        self.combined_result_label.setStyleSheet("background: transparent;")

        # 更新表格
        self.update_payment_table(combined_payment)

    def calculate_commercial(self):
        # 获取商业贷款参数
        loan = self.commercial_loan.value()
        rate = self.commercial_rate.value() / 100 / 12  # 月利率
        term = self.commercial_term.value() * 12  # 月数
        loan_type = self.commercial_type.currentText()

        # 隐藏商业和公积金贷款月供列
        self.payment_table.setColumnHidden(2, True)
        self.payment_table.setColumnHidden(3, True)

        # 计算还款计划
        if loan_type == "等额本息":
            payments = self.calculate_equal_payment(loan, rate, term)
        else:
            payments = self.calculate_decreasing_payment(loan, rate, term)

        # 显示结果摘要
        total_principal = loan
        total_interest = sum(p["interest"] for p in payments)
        total_payment = total_principal + total_interest

        # 根据还款方式显示不同的月供信息
        if loan_type == "等额本息":
            monthly_payment = payments[0]["payment"] if payments else 0
            summary = f"贷款总额: ¥{total_principal:,.2f} | 支付利息: ¥{total_interest:,.2f} | 还款总额: ¥{total_payment:,.2f} | 每月还款: ¥{monthly_payment:,.2f}"
        else:
            first_payment = payments[0]["payment"] if payments else 0
            last_payment = payments[-1]["payment"] if payments else 0
            summary = f"贷款总额: ¥{total_principal:,.2f} | 支付利息: ¥{total_interest:,.2f} | 还款总额: ¥{total_payment:,.2f} | 首月还款: ¥{first_payment:,.2f} | 末月还款: ¥{last_payment:,.2f}"

        self.commercial_result_label.setText(summary)

        # 更新表格
        self.update_payment_table(payments)

    def calculate_provident(self):
        # 获取公积金贷款参数
        loan = self.provident_loan.value()
        rate = self.provident_rate.value() / 100 / 12  # 月利率
        term = self.provident_term.value() * 12  # 月数
        loan_type = self.provident_type.currentText()

        # 隐藏商业和公积金贷款月供列
        self.payment_table.setColumnHidden(2, True)
        self.payment_table.setColumnHidden(3, True)

        # 计算还款计划
        if loan_type == "等额本息":
            payments = self.calculate_equal_payment(loan, rate, term)
        else:
            payments = self.calculate_decreasing_payment(loan, rate, term)

        # 显示结果摘要
        total_principal = loan
        total_interest = sum(p["interest"] for p in payments)
        total_payment = total_principal + total_interest

        # 根据还款方式显示不同的月供信息
        if loan_type == "等额本息":
            monthly_payment = payments[0]["payment"] if payments else 0
            summary = f"贷款总额: ¥{total_principal:,.2f} | 支付利息: ¥{total_interest:,.2f} | 还款总额: ¥{total_payment:,.2f} | 每月还款: ¥{monthly_payment:,.2f}"
        else:
            first_payment = payments[0]["payment"] if payments else 0
            last_payment = payments[-1]["payment"] if payments else 0
            summary = f"贷款总额: ¥{total_principal:,.2f} | 支付利息: ¥{total_interest:,.2f} | 还款总额: ¥{total_payment:,.2f} | 首月还款: ¥{first_payment:,.2f} | 末月还款: ¥{last_payment:,.2f}"

        self.provident_result_label.setText(summary)

        # 更新表格
        self.update_payment_table(payments)

    def calculate_equal_payment(self, loan, monthly_rate, term):
        """计算等额本息还款计划"""
        # 每月还款金额 = [贷款本金×月利率×(1+月利率)^还款月数]÷[(1+月利率)^还款月数-1]
        if monthly_rate == 0:  # 避免除以零
            monthly_payment = loan / term
        else:
            monthly_payment = loan * monthly_rate * math.pow(1 + monthly_rate, term) / (
                        math.pow(1 + monthly_rate, term) - 1)

        payments = []
        remaining = loan

        for month in range(1, term + 1):
            # 每月利息 = 剩余本金 × 月利率
            interest = remaining * monthly_rate
            # 每月本金 = 月供 - 月利息
            principal = monthly_payment - interest
            remaining -= principal

            # 最后一个月调整剩余本金为零
            if month == term:
                principal += remaining
                monthly_payment += remaining
                remaining = 0

            payments.append({
                "month": month,
                "payment": monthly_payment,
                "principal": principal,
                "interest": interest,
                "remaining": remaining
            })

        return payments

    def calculate_decreasing_payment(self, loan, monthly_rate, term):
        """计算等额本金还款计划"""
        # 每月本金 = 贷款总额 / 贷款月数
        monthly_principal = loan / term
        payments = []
        remaining = loan

        for month in range(1, term + 1):
            # 每月利息 = 剩余本金 × 月利率
            interest = remaining * monthly_rate
            # 月供 = 每月本金 + 每月利息
            monthly_payment = monthly_principal + interest
            remaining -= monthly_principal

            # 最后一个月调整剩余本金为零
            if month == term:
                monthly_payment += remaining
                remaining = 0

            payments.append({
                "month": month,
                "payment": monthly_payment,
                "principal": monthly_principal,
                "interest": interest,
                "remaining": remaining
            })

        return payments

    def update_payment_table(self, payments):
        """更新还款明细表格"""
        self.payment_table.setRowCount(len(payments))

        for i, payment in enumerate(payments):
            # 期数
            month_item = QTableWidgetItem(str(payment["month"]))
            month_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.payment_table.setItem(i, 0, month_item)

            # 月供总额
            total_payment = payment["payment"]
            total_item = QTableWidgetItem(f"¥{total_payment:,.2f}")
            total_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.payment_table.setItem(i, 1, total_item)

            # 商业贷款月供
            if "commercial_payment" in payment:  # 组合贷款
                comm_payment = payment["commercial_payment"]
                comm_item = QTableWidgetItem(f"¥{comm_payment:,.2f}")
            else:  # 单一贷款
                comm_item = QTableWidgetItem("")
            comm_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.payment_table.setItem(i, 2, comm_item)

            # 公积金贷款月供
            if "provident_payment" in payment:  # 组合贷款
                prov_payment = payment["provident_payment"]
                prov_item = QTableWidgetItem(f"¥{prov_payment:,.2f}")
            else:  # 单一贷款
                prov_item = QTableWidgetItem("")
            prov_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.payment_table.setItem(i, 3, prov_item)

            # 利息
            interest_item = QTableWidgetItem(f"¥{payment['interest']:,.2f}")
            interest_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.payment_table.setItem(i, 4, interest_item)

            # 剩余本金
            remaining_item = QTableWidgetItem(f"¥{payment['remaining']:,.2f}")
            remaining_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.payment_table.setItem(i, 5, remaining_item)

            # 设置颜色
            if i % 2 == 0:
                for col in range(6):
                    item = self.payment_table.item(i, col)
                    if item:
                        item.setBackground(QBrush(QColor(245, 245, 245)))


def show_housing_loan_rates_dialog(main_object, title, content):
    """显示房贷计算器对话框"""
    dialog = MortgageCalculator(None, main_object, title, content)
    dialog.refresh_geometry(main_object.toolkit.resolution_util.get_screen(main_object))
    dialog.show()
    return dialog