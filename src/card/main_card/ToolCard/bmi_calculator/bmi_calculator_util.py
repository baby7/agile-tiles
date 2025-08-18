from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PySide6.QtCore import Qt
from src.component.AgileTilesAcrylicWindow.AgileTilesAcrylicWindow import AgileTilesAcrylicWindow
from src.ui import style_util


class BMICalculatorPopup(AgileTilesAcrylicWindow):
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
        self.setMinimumSize(400, 300)
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

        # 输入身高
        height_label = QLabel("请输入身高（厘米）：")
        height_label.setStyleSheet("background: transparent;")
        main_layout.addWidget(height_label)

        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText("例如：170")
        main_layout.addWidget(self.height_input)

        # 输入体重
        weight_label = QLabel("请输入体重（千克）：")
        weight_label.setStyleSheet("background: transparent;")
        main_layout.addWidget(weight_label)

        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText("例如：65")
        main_layout.addWidget(self.weight_input)

        # 计算按钮
        calculate_button = QPushButton("计算 BMI")
        calculate_button.clicked.connect(self.calculate_bmi)
        calculate_button.setMinimumSize(120, 30)
        main_layout.addWidget(calculate_button, alignment=Qt.AlignCenter)

        # 结果显示
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(self.result_label)

    def calculate_bmi(self):
        """计算 BMI 并显示结果"""
        try:
            # 获取输入值
            height = float(self.height_input.text())
            weight = float(self.weight_input.text())

            if height <= 0 or weight <= 0:
                raise ValueError("身高和体重必须为正数")

            # 转换身高为米
            height_m = height / 100

            # 计算 BMI
            bmi = weight / (height_m ** 2)

            # 判断健康状态
            if bmi < 18.5:
                status = "偏瘦"
            elif 18.5 <= bmi < 24:
                status = "正常"
            elif 24 <= bmi < 28:
                status = "超重"
            else:
                status = "肥胖"

            # 显示结果
            self.result_label.setText(f"BMI: {bmi:.2f}\n健康状态: {status}")

        except ValueError as e:
            # 错误提示
            QMessageBox.warning(self, "输入错误", str(e))
            self.result_label.setText("")


def show_bmi_calculator_dialog(main_object, title, content):
    """显示 BMI 计算器对话框"""
    dialog = BMICalculatorPopup(None, main_object, title, content)
    dialog.refresh_geometry(main_object.toolkit.resolution_util.get_screen(main_object))
    dialog.show()
    return dialog
