import os
import subprocess
import tempfile

from PySide6.QtWidgets import QApplication, QVBoxLayout, QPushButton, QHBoxLayout, \
    QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
from PySide6.QtGui import Qt, QColor, QBrush
from PySide6.QtCore import Slot, QDateTime
from lxml import html

from src.component.AgileTilesAcrylicWindow.AgileTilesAcrylicWindow import AgileTilesAcrylicWindow
from src.component.ChartWidget.DateTimeChartWidget import DateTimeChartWidget
from src.module.Box import message_box_util
from src.ui import style_util


class BatteryTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["日期", "最大容量 (mWh)", "设计容量 (mWh)", "健康度 (%)"])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setAlternatingRowColors(True)

    def set_data(self, data):
        """填充表格数据"""
        self.setRowCount(len(data))

        for row, (date, max_charge, nominal_charge, health) in enumerate(data):
            # 日期
            self.setItem(row, 0, QTableWidgetItem(date))

            # 最大容量
            self.setItem(row, 1, QTableWidgetItem(f"{max_charge:,.0f}"))

            # 设计容量
            self.setItem(row, 2, QTableWidgetItem(f"{nominal_charge:,.0f}"))

            # 健康度
            health_item = QTableWidgetItem(f"{health:.1f}%")

            # 根据健康度设置颜色
            if health > 80:
                health_item.setForeground(QBrush(QColor(0, 128, 0)))  # 绿色
            elif health > 60:
                health_item.setForeground(QBrush(QColor(200, 150, 0)))  # 橙色
            else:
                health_item.setForeground(QBrush(QColor(200, 0, 0)))  # 红色
                health_item.setBackground(QBrush(QColor(255, 230, 230)))  # 浅红色背景

            self.setItem(row, 3, health_item)

        # 按日期排序（最新的在最上面）
        self.sortItems(0, Qt.DescendingOrder)


class NotebookBatteryGraph(AgileTilesAcrylicWindow):
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
        self.setMinimumSize(450, 900)
        # 初始化界面
        self.init_ui()
        # 设置样式
        style_util.set_dialog_control_style(self, self.is_dark)
        # 窗口显示后自动生成并加载电池报告
        QApplication.processEvents()
        self.generate_and_load_report()

    def init_ui(self):
        # 主部件和布局
        layout = QVBoxLayout()
        layout.setSpacing(15)
        self.widget_base.setLayout(layout)
        layout.setContentsMargins(10, 10, 10, 10)

        # 提示按钮
        report_btn = QPushButton('如何生成html电池健康报告？', self)
        report_btn.clicked.connect(self.show_report_generation_instructions)
        report_btn.setMinimumHeight(30)
        layout.addWidget(report_btn)

        # 状态标签
        self.status_label = QLabel("正在生成电池报告...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("background-color: transparent;")
        layout.addWidget(self.status_label)

        # 创建电池健康曲线图
        self.graph_widget = DateTimeChartWidget()
        layout.addWidget(self.graph_widget)

        # 创建数据表格
        self.table_widget = BatteryTableWidget()
        layout.addWidget(self.table_widget)

        # 底部信息
        bottom_layout = QHBoxLayout()
        self.info_label = QLabel("")
        self.info_label.setStyleSheet("background-color: transparent;")
        bottom_layout.addWidget(self.info_label)

        refresh_btn = QPushButton('重新生成报告', self)
        refresh_btn.setStyleSheet("padding: 6px;")
        refresh_btn.setMinimumHeight(30)
        refresh_btn.clicked.connect(self.generate_and_load_report)
        bottom_layout.addWidget(refresh_btn)

        layout.addLayout(bottom_layout)

        self.setLayout(layout)

        # 设置窗口大小
        self.resize(900, 700)

        # 设置窗口的位置居中
        screen = QApplication.primaryScreen().size()
        self.move((screen.width() - self.width()) // 2,
                  (screen.height() - self.height()) // 2)

    def generate_and_load_report(self):
        """生成电池报告并加载数据"""
        self.status_label.setText("正在生成电池报告...")
        QApplication.processEvents()  # 更新UI

        try:
            # 创建临时文件
            with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as temp_file:
                temp_path = temp_file.name

            # 执行命令生成电池报告
            result = subprocess.run(
                ['powercfg', '/batteryreport', '/output', temp_path],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            if result.returncode != 0:
                raise Exception(f"命令执行失败: {result.stderr}")

            # temp_path = "dev_util/battery-report.html"

            self.status_label.setText(f"报告已生成: {temp_path}")

            # 读取HTML文件内容
            with open(temp_path, 'r', encoding='utf-8') as file:
                html_content = file.read()

            # 解析HTML内容
            data = self.parse_html(html_content)

            if not data:
                self.status_label.setText("未找到电池数据，请检查报告内容")
                return

            chart_data = []
            for data_item in data:
                chart_data.append([QDateTime.fromString(data_item[0], "yyyy-MM-dd"), data_item[3]])

            # 更新图表和表格
            self.graph_widget.set_data(chart_data)
            self.graph_widget.set_title("电池健康曲线")
            self.graph_widget.set_x_axis_title("日期")
            self.graph_widget.set_y_axis_title("健康度(%)")
            self.table_widget.set_data(data)

            # 更新底部信息
            start_date = data[0][0]
            start_health = data[0][3]
            end_date = data[-1][0]
            end_health = data[-1][3]

            self.info_label.setText(
                f"电池健康变化: {start_date} ({start_health:.1f}%) → {end_date} ({end_health:.1f}%) | "
                f"数据点: {len(data)} | 最低健康度: {min(d[3] for d in data):.1f}%"
            )

        except Exception as e:
            self.status_label.setText(f"错误: {str(e)}")
            message_box_util.box_information(self.use_parent, "错误", f"生成或加载电池报告时出错:\n{str(e)}")
        finally:
            # 删除临时文件
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def parse_html(self, html_content):
        """解析HTML内容提取电池数据"""
        root = html.fromstring(html_content)
        table = root.xpath('/html/body/table[6]')
        if not table:
            return []

        data = []
        for row in table[0].xpath('.//tr'):
            # 跳过表头
            if row.getparent().tag == 'thead':
                continue

            cols = row.xpath('.//td')
            if len(cols) >= 3 and cols[0] is not None and cols[1] is not None and cols[2] is not None:
                # 提取和清理数据
                date_content = cols[0].text_content().replace('\n', '').replace('\r', '')
                max_charge_content = cols[1].text_content().replace('\n', '').replace('\r', '')
                nominal_charge_content = cols[2].text_content().replace('\n', '').replace('\r', '')

                if "," not in max_charge_content:
                    return []

                date = date_content.strip()[0:10].strip()
                if not date:
                    continue

                max_charge = max_charge_content.strip().replace(',', '').replace(' mWh', '')
                if not max_charge:
                    continue
                max_charge = float(max_charge)

                nominal_charge = nominal_charge_content.strip().replace(',', '').replace(' mWh', '')
                if not nominal_charge:
                    continue
                nominal_charge = float(nominal_charge)

                health = (max_charge / nominal_charge) * 100
                data.append((date, max_charge, nominal_charge, health))

        return data

    @Slot()
    def show_report_generation_instructions(self):
        """显示生成电池健康报告的指令"""
        message_box_util.box_information(self.use_parent, "生成电池健康报告", "在命令提示符（CMD）中输入以下命令来生成电池健康报告：\n\npowercfg /batteryreport")


def show_notebook_battery_graph_dialog(main_object, title, content):
    """显示笔记本电池健康对话框"""
    dialog = NotebookBatteryGraph(None, main_object, title, content)
    dialog.refresh_geometry(main_object.toolkit.resolution_util.get_screen(main_object))
    dialog.show()
    return dialog