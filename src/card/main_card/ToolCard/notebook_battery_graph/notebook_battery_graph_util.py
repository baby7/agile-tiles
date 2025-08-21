import os
import subprocess
import tempfile
from datetime import timedelta

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox, QHBoxLayout, \
    QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
from PySide6.QtGui import Qt, QColor, QBrush, QPainter, QPen
from PySide6.QtCore import Slot, QPointF
from lxml import html
from dateutil import parser

from src.component.AgileTilesAcrylicWindow.AgileTilesAcrylicWindow import AgileTilesAcrylicWindow
from src.ui import style_util


class BatteryGraphWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.points = []
        self.min_date = None
        self.max_date = None
        self.min_health = 100
        self.max_health = 100
        self.setMinimumHeight(300)

    def set_data(self, data):
        """设置要绘制的数据"""
        self.points = []
        if not data:
            return

        # 转换日期和健康值
        for date_str, _, _, health in data:
            try:
                date = parser.parse(date_str)
                self.points.append((date, health))
            except:
                continue

        if self.points:
            # 计算最小/最大日期和健康值
            self.min_date = min(p[0] for p in self.points)
            self.max_date = max(p[0] for p in self.points)
            self.min_health = min(p[1] for p in self.points)
            self.max_health = max(p[1] for p in self.points)

            # 确保最小健康值不低于0，最大不超过100
            self.min_health = max(0, self.min_health - 5)
            self.max_health = min(100, self.max_health + 5)

        self.update()

    def paintEvent(self, event):
        """绘制电池健康曲线"""
        if not self.points:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 设置边距
        margin = 40
        width = self.width() - 2 * margin
        height = self.height() - 2 * margin

        # 绘制背景
        painter.fillRect(self.rect(), QColor(240, 240, 240))

        # 绘制坐标轴
        painter.setPen(QPen(Qt.black, 2))
        painter.drawLine(margin, margin, margin, margin + height)  # Y轴
        painter.drawLine(margin, margin + height, margin + width, margin + height)  # X轴

        # 绘制Y轴刻度和标签
        painter.setPen(QPen(Qt.darkGray, 1))
        for i in range(0, 101, 20):
            y = margin + height - (i / 100.0) * height
            painter.drawLine(margin - 5, y, margin + width, y)
            painter.drawText(5, y + 5, f"{i}%")

        # 绘制X轴刻度和标签
        date_range = (self.max_date - self.min_date).days
        if date_range < 1:
            date_range = 1

        # 每隔一定时间点绘制一个刻度
        num_ticks = min(8, date_range)
        interval = max(1, date_range // num_ticks)

        for i in range(0, date_range + 1, interval):
            date = self.min_date + timedelta(days=i)
            x = margin + (i / date_range) * width
            painter.drawLine(x, margin + height, x, margin + height + 5)

            # 格式化日期
            date_str = date.strftime("%Y-%m-%d")
            painter.drawText(x - 20, margin + height + 20, date_str)

        # 绘制曲线
        if len(self.points) > 1:
            path = []
            for i, (date, health) in enumerate(self.points):
                days = (date - self.min_date).days
                x = margin + (days / date_range) * width
                y = margin + height - (health / 100.0) * height

                if i == 0:
                    path.append(QPointF(x, y))
                else:
                    # 使用贝塞尔曲线平滑连接点
                    prev_x, prev_y = path[-1].x(), path[-1].y()
                    ctrl_x1 = prev_x + (x - prev_x) * 0.5
                    ctrl_y1 = prev_y
                    ctrl_x2 = prev_x + (x - prev_x) * 0.5
                    ctrl_y2 = y

                    path.append(QPointF(ctrl_x1, ctrl_y1))
                    path.append(QPointF(ctrl_x2, ctrl_y2))
                    path.append(QPointF(x, y))

            # 绘制曲线
            painter.setPen(QPen(QColor(0, 100, 200), 3))
            painter.drawPolyline(path)

            # 绘制数据点
            painter.setPen(QPen(Qt.darkBlue, 1))
            painter.setBrush(QBrush(QColor(100, 180, 255)))
            for point in path:
                if point in [path[0], path[-1]] or len(path) < 10:  # 只绘制首尾点或当点数少时绘制所有点
                    painter.drawEllipse(point, 5, 5)

        # 绘制标题
        painter.setPen(Qt.darkBlue)
        painter.setFont(self.font())
        painter.drawText(margin, 20, "电池健康曲线")


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
        self.graph_widget = BatteryGraphWidget()
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

            # temp_path = "battery-report.html"

            self.status_label.setText(f"报告已生成: {temp_path}")

            # 读取HTML文件内容
            with open(temp_path, 'r', encoding='utf-8') as file:
                html_content = file.read()

            # 解析HTML内容
            data = self.parse_html(html_content)

            if not data:
                self.status_label.setText("未找到电池数据，请检查报告内容")
                return

            # 更新图表和表格
            self.graph_widget.set_data(data)
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
            QMessageBox.critical(self, "错误", f"生成或加载电池报告时出错:\n{str(e)}")
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
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("生成电池健康报告")
        msg_box.setText("在命令提示符（CMD）中输入以下命令来生成电池健康报告：\n\npowercfg /batteryreport")
        msg_box.setInformativeText("本功能会在窗口打开时自动执行此命令并加载生成的报告")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()


def show_notebook_battery_graph_dialog(main_object, title, content):
    """显示笔记本电池健康对话框"""
    dialog = NotebookBatteryGraph(None, main_object, title, content)
    dialog.refresh_geometry(main_object.toolkit.resolution_util.get_screen(main_object))
    dialog.show()
    return dialog