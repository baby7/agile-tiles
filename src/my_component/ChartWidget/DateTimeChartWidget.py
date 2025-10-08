import math

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCharts import QChart, QChartView, QSplineSeries, QDateTimeAxis, QValueAxis, QLineSeries
from PySide6.QtCore import Qt, QDateTime, QPointF
from PySide6.QtGui import QMouseEvent, QPainter, QPen, QFont, QColor


class CrosshairChartView(QChartView):
    def __init__(self, chart, parent=None):
        super().__init__(chart, parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setMouseTracking(True)

        # 存储数据系列
        self.series = None

        # 创建十字线系列
        self.v_line = QLineSeries()
        self.v_line.setPen(QPen(QColor(125, 125, 125), 0.5, Qt.DashLine))
        self.h_line = QLineSeries()
        self.h_line.setPen(QPen(QColor(125, 125, 125), 0.5, Qt.DashLine))

        # 先创建系列但不添加到图表，等坐标轴准备好后再添加
        self.crosshair_added = False

        # 信息标签
        self.info_label = QLabel()
        self.info_label.setStyleSheet("background-color: white; border: 1px solid gray; padding: 2px;")
        self.info_label.setFont(QFont("Arial", 8))
        self.info_label.hide()
        self.info_label.setParent(self)
        self.info_label.resize(150, 40)

    def set_series(self, series):
        """设置数据系列"""
        self.series = series

    def ensure_crosshair_added(self):
        """确保十字线已添加到图表并附加到坐标轴"""
        if not self.crosshair_added and self.chart().axes():
            # 添加十字线到图表
            self.chart().addSeries(self.v_line)
            self.chart().addSeries(self.h_line)

            # 附加到坐标轴
            axis_x = self.chart().axes(Qt.Horizontal)[0]
            axis_y = self.chart().axes(Qt.Vertical)[0]
            self.v_line.attachAxis(axis_x)
            self.v_line.attachAxis(axis_y)
            self.h_line.attachAxis(axis_x)
            self.h_line.attachAxis(axis_y)

            self.crosshair_added = True

    def mouseMoveEvent(self, event: QMouseEvent):
        """处理鼠标移动事件"""
        if not self.series:
            return

        # 确保十字线已添加
        self.ensure_crosshair_added()

        # 获取鼠标位置对应的图表值
        mouse_pos = event.position()
        chart_value = self.chart().mapToValue(QPointF(mouse_pos))
        x_val = chart_value.x()

        # 查找最近的数据点
        closest_point, min_x_diff = self.find_closest_point(x_val)

        if closest_point:
            # 更新十字线位置
            self.update_crosshair(closest_point)

            # 更新信息标签
            self.update_info_label(closest_point, mouse_pos)

        super().mouseMoveEvent(event)

    def find_closest_point(self, x_val):
        """查找x值最接近的数据点"""
        points = self.series.points()
        if not points:
            return None, float('inf')

        closest_point = None
        min_x_diff = float('inf')

        for point in points:
            x_diff = abs(point.x() - x_val)
            if x_diff < min_x_diff:
                min_x_diff = x_diff
                closest_point = point

        return closest_point, min_x_diff

    def update_crosshair(self, point):
        """更新十字线位置"""
        # 获取坐标轴范围
        axis_x = self.chart().axes(Qt.Horizontal)[0]
        axis_y = self.chart().axes(Qt.Vertical)[0]

        # 获取坐标轴范围值
        x_min = axis_x.min().toMSecsSinceEpoch() if hasattr(axis_x.min(), 'toMSecsSinceEpoch') else axis_x.min()
        x_max = axis_x.max().toMSecsSinceEpoch() if hasattr(axis_x.max(), 'toMSecsSinceEpoch') else axis_x.max()
        y_min = axis_y.min()
        y_max = axis_y.max()

        # 更新垂直线 (x固定，y从最小到最大)
        self.v_line.clear()
        self.v_line.append(point.x(), y_min)
        self.v_line.append(point.x(), y_max)

        # 更新水平线 (y固定，x从最小到最大)
        self.h_line.clear()
        self.h_line.append(x_min, point.y())
        self.h_line.append(x_max, point.y())

    def update_info_label(self, point, mouse_pos):
        """更新信息标签内容和位置"""
        # 转换日期格式
        x_dt = QDateTime.fromMSecsSinceEpoch(int(point.x()))
        x_str = x_dt.toString("yyyy-MM-dd HH:mm")
        y_value = point.y()

        # 设置标签文本
        self.info_label.setText(f"时间: {x_str}\n数值: {y_value:.2f}")

        # 调整标签位置（避免超出视图边界）
        label_width = self.info_label.width()
        label_height = self.info_label.height()

        chart_rect = self.rect()
        pos_x = mouse_pos.x() + 10
        pos_y = mouse_pos.y() + 10

        # 确保标签不会超出视图右边界
        if pos_x + label_width > chart_rect.width():
            pos_x = mouse_pos.x() - label_width - 10

        # 确保标签不会超出视图下边界
        if pos_y + label_height > chart_rect.height():
            pos_y = mouse_pos.y() - label_height - 10

        # 移动标签到新位置
        self.info_label.move(int(pos_x), int(pos_y))
        self.info_label.show()

    def leaveEvent(self, event):
        """鼠标离开图表区域时隐藏十字线和标签"""
        self.v_line.clear()
        self.h_line.clear()
        self.info_label.hide()
        super().leaveEvent(event)


class DateTimeChartWidget(QWidget):
    """日期曲线图表组件"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        # 创建图表
        self.chart = QChart()
        self.chart.setTitle("日期曲线图")
        self.chart.legend().setVisible(False)

        # 创建数据系列
        self.series = QSplineSeries()

        # 创建坐标轴
        self.axis_x = QDateTimeAxis()
        self.axis_x.setTitleText("日期")
        self.axis_x.setGridLineVisible(False)

        self.axis_y = QValueAxis()
        self.axis_y.setTitleText("数值")
        self.axis_y.setGridLineVisible(False)

        # 创建图表视图
        self.chart_view = CrosshairChartView(self.chart)

        # 设置布局
        self.layout.addWidget(self.chart_view)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def set_data(self, data):
        """
        设置图表数据

        参数:
            data: 包含日期和数值的列表，格式为 [(datetime1, value1), (datetime2, value2), ...]
                  其中datetime可以是QDateTime对象或时间戳(毫秒)
        """
        # 清空现有数据
        self.series.clear()

        # 添加新数据
        for dt, value in data:
            if isinstance(dt, QDateTime):
                x_value = dt.toMSecsSinceEpoch()
            else:
                x_value = dt  # 假设已经是时间戳

            self.series.append(x_value, value)

        # 更新图表
        self.update_chart()

    def update_chart(self):
        """更新图表显示"""
        # 移除现有系列
        for series in self.chart.series():
            self.chart.removeSeries(series)

        # 移除现有坐标轴
        for axis in self.chart.axes():
            self.chart.removeAxis(axis)

        # 添加数据系列
        self.chart.addSeries(self.series)

        # 获取数据点
        points = self.series.points()
        if not points:
            return

        # 计算日期范围
        x_values = [point.x() for point in points]
        min_x = min(x_values)
        max_x = max(x_values)

        min_date = QDateTime.fromMSecsSinceEpoch(int(min_x))
        max_date = QDateTime.fromMSecsSinceEpoch(int(max_x))

        # 计算数值范围
        y_values = [point.y() for point in points]
        y_min = min(y_values)
        y_max = max(y_values)

        # 添加填充
        x_padding = (max_x - min_x) * 0.05  # 5%的填充
        y_padding = (y_max - y_min) * 0.1  # 10%的填充

        # 设置X轴范围和格式
        self.axis_x.setFormat("yyyy-MM-dd")

        self.axis_x.setRange(
            QDateTime.fromMSecsSinceEpoch(int(min_x - x_padding)),
            QDateTime.fromMSecsSinceEpoch(int(max_x + x_padding))
        )
        self.axis_x.setLabelsAngle(45)

        # 设置Y轴范围为整数，最小值为0
        # 计算合适的Y轴最大值（向上取整）
        y_max_ceil = math.ceil(y_max + y_padding)
        if y_max_ceil <= 0:
            y_max_ceil = 1  # 确保最大值至少为1

        # 设置Y轴范围和刻度
        self.axis_y.setRange(0, y_max_ceil)
        self.axis_y.setTickCount(min(10, y_max_ceil + 1))  # 设置刻度数量
        self.axis_y.setLabelFormat("%.0f")  # 只显示整数

        # 添加坐标轴
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)

        # 附加系列到坐标轴
        self.series.attachAxis(self.axis_x)
        self.series.attachAxis(self.axis_y)

        # 设置十字线视图的数据系列
        self.chart_view.set_series(self.series)
        # 重置十字线添加状态，确保下次鼠标移动时会重新添加
        self.chart_view.crosshair_added = False

    def set_title(self, title):
        """设置图表标题"""
        self.chart.setTitle(title)

    def set_x_axis_title(self, title):
        """设置X轴标题"""
        self.axis_x.setTitleText(title)

    def set_y_axis_title(self, title):
        """设置Y轴标题"""
        self.axis_y.setTitleText(title)
