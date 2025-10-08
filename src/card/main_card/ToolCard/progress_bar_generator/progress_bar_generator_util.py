import json

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSpinBox, QDoubleSpinBox,
    QListWidget, QColorDialog, QFileDialog, QGroupBox,
    QFormLayout, QSizePolicy, QScrollArea, QListWidgetItem, QDialog,
    QGridLayout, QFontComboBox
)
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont, QImage, QFontMetrics, QMouseEvent, QWheelEvent
from PySide6.QtCore import Qt, QRectF, QPoint, QPointF, QSettings

from src.my_component.AgileTilesAcrylicWindow.AgileTilesAcrylicWindow import AgileTilesAcrylicWindow
from src.my_component.AgileTilesFramelessDialog.AgileTilesFramelessDialog import AgileTilesFramelessDialog
from src.module.Box import message_box_util
from src.ui import style_util

# 默认颜色列表
DEFAULT_COLORS = [
    "#FF9999", "#99FF99", "#9999FF", "#FFFF99",
    "#FF99FF", "#99FFFF", "#FFCC99", "#CC99FF",
    "#FF6666", "#66FF66", "#6666FF", "#FFFF66"
]


class ZoomableImageView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.original_pixmap = None
        self.scaled_pixmap = None
        self.scale_factor = 1.0
        self.min_scale = 0.1
        self.max_scale = 10.0
        self.pan_start = QPoint()
        self.pan_offset = QPointF(0, 0)
        self.setMouseTracking(True)
        self.setStyleSheet("background-color: #f0f0f0;")

    def set_pixmap(self, pixmap):
        self.original_pixmap = pixmap
        self.scale_factor = 1.0
        self.pan_offset = QPointF(0, 0)

        # 计算适合视图的缩放比例
        if pixmap and not pixmap.isNull():
            view_width = self.width()
            view_height = self.height()
            img_width = pixmap.width()
            img_height = pixmap.height()

            # 计算缩放比例，使图像适应视图
            scale_x = view_width / img_width if img_width > 0 else 1.0
            scale_y = view_height / img_height if img_height > 0 else 1.0
            self.scale_factor = min(scale_x, scale_y, 1.0)  # 不超过原始大小

            # 创建缩放后的图像
            new_width = int(img_width * self.scale_factor)
            new_height = int(img_height * self.scale_factor)
            self.scaled_pixmap = pixmap.scaled(
                new_width, new_height,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        else:
            self.scaled_pixmap = pixmap

        self.update()

    def paintEvent(self, event):
        if not self.scaled_pixmap or self.scaled_pixmap.isNull():
            # 绘制占位文本
            painter = QPainter(self)
            painter.setPen(Qt.gray)
            painter.drawText(self.rect(), Qt.AlignCenter, "预览区域 - 生成后将显示进度条")
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        painter.setRenderHint(QPainter.Antialiasing)

        # 计算绘制位置
        img_width = self.scaled_pixmap.width()
        img_height = self.scaled_pixmap.height()

        x_offset = (self.width() - img_width) / 2 + self.pan_offset.x()
        y_offset = (self.height() - img_height) / 2 + self.pan_offset.y()

        painter.drawPixmap(int(x_offset), int(y_offset), self.scaled_pixmap)

    def wheelEvent(self, event: QWheelEvent):
        # 计算缩放因子
        zoom_in = event.angleDelta().y() > 0
        zoom_factor = 1.25 if zoom_in else 0.8

        # 计算新的缩放比例
        new_scale = self.scale_factor * zoom_factor
        new_scale = max(self.min_scale, min(self.max_scale, new_scale))

        if new_scale == self.scale_factor:
            return

        # 获取鼠标在图像上的位置
        mouse_pos = event.position()
        img_pos = self._map_to_image(mouse_pos)

        # 更新缩放比例
        old_scale = self.scale_factor
        self.scale_factor = new_scale

        # 计算新的偏移量，使缩放以鼠标位置为中心
        if self.original_pixmap:
            img_width = self.original_pixmap.width() * self.scale_factor
            img_height = self.original_pixmap.height() * self.scale_factor

            # 计算鼠标位置在缩放前后的图像坐标变化
            scale_change = self.scale_factor / old_scale
            self.pan_offset = QPointF(
                (self.pan_offset.x() + img_pos.x()) * scale_change - img_pos.x(),
                (self.pan_offset.y() + img_pos.y()) * scale_change - img_pos.y()
            )

            # 更新缩放后的图像 - 使用高质量缩放
            new_width = int(self.original_pixmap.width() * self.scale_factor)
            new_height = int(self.original_pixmap.height() * self.scale_factor)
            self.scaled_pixmap = self.original_pixmap.scaled(
                new_width, new_height,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.pan_start = event.position().toPoint()
            self.setCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() & Qt.LeftButton:
            # 计算拖动距离并更新偏移量
            delta = event.position().toPoint() - self.pan_start
            self.pan_offset += delta
            self.pan_start = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.ArrowCursor)

    def _map_to_image(self, pos):
        """将窗口坐标映射到原始图像坐标"""
        if not self.original_pixmap:
            return QPointF(0, 0)

        img_width = self.scaled_pixmap.width()
        img_height = self.scaled_pixmap.height()

        x_offset = (self.width() - img_width) / 2 + self.pan_offset.x()
        y_offset = (self.height() - img_height) / 2 + self.pan_offset.y()

        # 计算相对于图像的位置
        x_in_img = (pos.x() - x_offset) / self.scale_factor
        y_in_img = (pos.y() - y_offset) / self.scale_factor

        return QPointF(x_in_img, y_in_img)

    def reset_view(self):
        """重置视图到初始状态"""
        self.scale_factor = 1.0
        self.pan_offset = QPointF(0, 0)
        if self.original_pixmap:
            # 计算适合视图的缩放比例
            view_width = self.width()
            view_height = self.height()
            img_width = self.original_pixmap.width()
            img_height = self.original_pixmap.height()

            # 计算缩放比例，使图像适应视图
            scale_x = view_width / img_width if img_width > 0 else 1.0
            scale_y = view_height / img_height if img_height > 0 else 1.0
            self.scale_factor = min(scale_x, scale_y, 1.0)  # 不超过原始大小

            # 创建缩放后的图像
            new_width = int(img_width * self.scale_factor)
            new_height = int(img_height * self.scale_factor)
            self.scaled_pixmap = self.original_pixmap.scaled(
                new_width, new_height,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        self.update()


class VideoSegmentDialog(AgileTilesFramelessDialog):
    def __init__(self, parent=None, is_dark=None, form_theme_mode="Acrylic", form_theme_transparency=50, used_colors=None, start_time=0.0):
        super().__init__(parent, is_dark=is_dark, form_theme_mode=form_theme_mode, form_theme_transparency=form_theme_transparency)

        self.setWindowTitle("添加视频片段")
        self.setFixedSize(400, 350)

        self.start_time = start_time
        # 获取已使用的颜色，避免重复
        self.used_colors = used_colors if used_colors else []
        # 初始化UI
        self.init_ui()
        # 设置样式
        style_util.set_dialog_control_style(self, self.is_dark)

    def init_ui(self):
        # 主部件和布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        self.widget_base.setLayout(main_layout)
        main_layout.setContentsMargins(10, 10, 10, 10)

        form_layout = QFormLayout()

        self.start_time_input = QDoubleSpinBox()
        self.start_time_input.setRange(0, 9999.99)
        self.start_time_input.setDecimals(2)
        self.start_time_input.setSuffix(" 秒")
        self.start_time_input.setValue(self.start_time)  # 设置默认开始时间

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("输入片段标题")

        self.text_color_btn = QPushButton("选择文字颜色")
        self.text_color_btn.setMinimumHeight(27)
        self.text_color_btn.setMinimumWidth(140)
        self.text_color_btn.clicked.connect(self.choose_text_color)
        self.text_color = QColor(Qt.black)
        self.text_color_preview = QLabel()
        self.text_color_preview.setFixedSize(20, 20)
        self.text_color_preview.setStyleSheet(f"background-color: {self.text_color.name()}; border: 1px solid #ccc;")

        self.bg_color_btn = QPushButton("选择背景颜色")
        self.bg_color_btn.setMinimumHeight(27)
        self.bg_color_btn.setMinimumWidth(140)
        self.bg_color_btn.clicked.connect(self.choose_bg_color)

        # 选择第一个未使用的颜色
        self.bg_color = self.get_next_available_color()
        self.bg_color_preview = QLabel()
        self.bg_color_preview.setFixedSize(20, 20)
        self.bg_color_preview.setStyleSheet(f"background-color: {self.bg_color.name()}; border: 1px solid #ccc;")

        # 颜色预览布局
        text_color_layout = QHBoxLayout()
        text_color_layout.addWidget(self.text_color_btn)
        text_color_layout.addWidget(self.text_color_preview)
        text_color_layout.addStretch()

        bg_color_layout = QHBoxLayout()
        bg_color_layout.addWidget(self.bg_color_btn)
        bg_color_layout.addWidget(self.bg_color_preview)
        bg_color_layout.addStretch()

        form_layout.addRow("开始时间:", self.start_time_input)
        form_layout.addRow("标题:", self.title_input)
        form_layout.addRow("文字颜色:", text_color_layout)
        form_layout.addRow("背景颜色:", bg_color_layout)

        button_layout = QHBoxLayout()
        self.ok_btn = QPushButton("确定")
        self.ok_btn.setMinimumHeight(30)
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.setMinimumHeight(30)
        self.cancel_btn.clicked.connect(self.reject)

        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.ok_btn)

        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

    def get_next_available_color(self):
        # 获取第一个未使用的颜色
        for color_hex in DEFAULT_COLORS:
            color = QColor(color_hex)
            if color not in self.used_colors:
                return color

        # 如果所有颜色都已使用，返回第一个颜色
        return QColor(DEFAULT_COLORS[0])

    def choose_text_color(self):
        # 临时保存当前样式表
        current_style = self.styleSheet()
        self.setStyleSheet("")  # 清除样式表
        color = QColorDialog.getColor(self.text_color, self, "选择文字颜色")
        # 恢复样式表
        self.setStyleSheet(current_style)
        if color.isValid():
            self.text_color = color
            self.text_color_preview.setStyleSheet(
                f"background-color: {self.text_color.name()}; border: 1px solid #ccc;")

    def choose_bg_color(self):
        # 临时保存当前样式表
        current_style = self.styleSheet()
        self.setStyleSheet("")  # 清除样式表
        color = QColorDialog.getColor(self.bg_color, self, "选择背景颜色")
        # 恢复样式表
        self.setStyleSheet(current_style)
        if color.isValid():
            self.bg_color = color
            self.bg_color_preview.setStyleSheet(f"background-color: {self.bg_color.name()}; border: 1px solid #ccc;")

    def get_segment_data(self):
        return {
            'start_time': self.start_time_input.value(),
            'title': self.title_input.text(),
            'text_color': self.text_color,
            'bg_color': self.bg_color
        }


class ProgressBarGenerator(AgileTilesAcrylicWindow):
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
        self.setMinimumSize(1200, 800)
        # 初始化设置
        self.total_duration = 0.0
        self.segments = []
        self.progress_bar_image = None
        self.selected_font = "Arial"  # 默认字体
        self.font_size = 24  # 默认字体大小
        # 初始化 QSettings [工具模块 - 视频进度条生成器]
        self.settings = QSettings(self.use_parent.app_name, "Tool" + "ProgressBarGenerator")
        # 初始化UI
        self.init_ui()
        # 设置样式
        style_util.set_dialog_control_style(self, self.is_dark)

    def init_ui(self):
        # 主部件和布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        self.widget_base.setLayout(main_layout)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # 顶部导入导出按钮组
        io_group = QGroupBox("数据管理")
        io_group.setStyleSheet("QGroupBox{border: 1px solid rgba(125, 125, 125, 125); padding-top: 8px;}")
        io_layout = QHBoxLayout()

        self.import_btn = QPushButton("导入进度条数据")
        self.import_btn.setMinimumHeight(30)
        self.export_btn = QPushButton("导出进度条数据")
        self.export_btn.setMinimumHeight(30)

        io_layout.addWidget(self.import_btn)
        io_layout.addWidget(self.export_btn)
        io_group.setLayout(io_layout)

        main_layout.addWidget(io_group)

        # 上部控制面板
        top_panel = QWidget()
        top_layout = QHBoxLayout()

        # 左侧设置面板
        left_panel = QGroupBox("设置")
        left_panel.setStyleSheet("QGroupBox{border: 1px solid rgba(125, 125, 125, 125); padding-top: 8px;}")
        left_layout = QVBoxLayout()

        # 进度条尺寸设置
        size_group = QGroupBox("进度条尺寸")
        size_group.setStyleSheet("QGroupBox{border: 1px solid rgba(125, 125, 125, 125); padding-top: 8px;}")
        size_layout = QGridLayout()

        self.width_spin = QSpinBox()
        self.width_spin.setRange(100, 7680)  # 增加最大宽度以支持更高分辨率
        self.width_spin.setValue(3840)
        self.width_spin.setSuffix(" px")

        self.height_spin = QSpinBox()
        self.height_spin.setRange(10, 400)  # 增加最大高度
        self.height_spin.setValue(96)
        self.height_spin.setSuffix(" px")

        size_layout.addWidget(QLabel("宽度:"), 0, 0)
        size_layout.addWidget(self.width_spin, 0, 1)
        size_layout.addWidget(QLabel("高度:"), 1, 0)
        size_layout.addWidget(self.height_spin, 1, 1)
        size_group.setLayout(size_layout)

        # 总时长设置
        duration_group = QGroupBox("总视频时长")
        duration_group.setStyleSheet("QGroupBox{border: 1px solid rgba(125, 125, 125, 125); padding-top: 8px;}")
        duration_layout = QHBoxLayout()

        self.duration_input = QDoubleSpinBox()
        self.duration_input.setRange(0.1, 9999.99)
        self.duration_input.setValue(300.0)
        self.duration_input.setDecimals(2)
        self.duration_input.setSuffix(" 秒")

        duration_layout.addWidget(QLabel("时长:"))
        duration_layout.addWidget(self.duration_input)
        duration_group.setLayout(duration_layout)

        # 字体选择设置
        font_group = QGroupBox("字体设置")
        font_group.setStyleSheet("QGroupBox{border: 1px solid rgba(125, 125, 125, 125); padding-top: 8px;}")
        font_layout = QFormLayout()

        self.font_combo = QFontComboBox()
        self.font_combo.setEditable(False)
        self.font_combo.setCurrentFont(QFont("Arial"))
        self.selected_font = "Arial"

        # 添加字体大小设置
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 72)  # 设置字体大小范围
        self.font_size_spin.setValue(24)  # 默认字体大小
        self.font_size_spin.setSuffix(" px")

        font_layout.addRow("选择字体:", self.font_combo)
        font_layout.addRow("字体大小:", self.font_size_spin)
        font_group.setLayout(font_layout)

        # 添加到左侧布局
        left_layout.addWidget(size_group)
        left_layout.addWidget(duration_group)
        left_layout.addWidget(font_group)
        left_layout.addStretch()
        left_panel.setLayout(left_layout)

        # 右侧片段编辑面板
        right_panel = QGroupBox("片段编辑")
        right_panel.setStyleSheet("QGroupBox{border: 1px solid rgba(125, 125, 125, 125); padding-top: 8px;}")
        right_layout = QVBoxLayout()

        # 添加片段按钮
        self.add_segment_btn = QPushButton("添加视频片段")
        self.add_segment_btn.setMinimumHeight(30)

        # 编辑和删除按钮
        edit_delete_layout = QHBoxLayout()
        self.edit_segment_btn = QPushButton("编辑选中片段")
        self.edit_segment_btn.setMinimumHeight(30)
        self.edit_segment_btn.setEnabled(False)

        self.delete_segment_btn = QPushButton("删除选中片段")
        self.delete_segment_btn.setMinimumHeight(30)
        self.delete_segment_btn.setEnabled(False)

        edit_delete_layout.addWidget(self.edit_segment_btn)
        edit_delete_layout.addWidget(self.delete_segment_btn)

        # 片段列表
        self.segments_list = QListWidget()
        self.segments_list.setStyleSheet(style_util.scroll_bar_style)

        # 添加到右侧布局
        right_layout.addWidget(self.add_segment_btn)
        right_layout.addLayout(edit_delete_layout)
        right_layout.addWidget(QLabel("片段列表:"))
        right_layout.addWidget(self.segments_list)
        right_panel.setLayout(right_layout)

        # 添加到顶部布局
        top_layout.addWidget(left_panel)
        top_layout.addWidget(right_panel)
        top_panel.setLayout(top_layout)

        # 下部预览区域
        bottom_panel = QGroupBox("预览(预览时可能模糊，导出是正常的)")
        bottom_panel.setStyleSheet("QGroupBox{border: 1px solid rgba(125, 125, 125, 125); padding-top: 8px;}")
        bottom_layout = QVBoxLayout()

        # 创建滚动区域用于预览长条形的进度条
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # 使用自定义的可缩放图像视图
        self.image_view = ZoomableImageView()
        self.image_view.setMinimumSize(600, 150)
        self.image_view.setStyleSheet("border: 1px solid gray; background-color: #f8f8f8;")
        self.image_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.scroll_area.setWidget(self.image_view)
        bottom_layout.addWidget(self.scroll_area)

        # 控制按钮
        control_layout = QHBoxLayout()

        self.reset_view_btn = QPushButton("重置视图")
        self.reset_view_btn.setMinimumHeight(30)
        self.reset_view_btn.setMinimumWidth(80)
        control_layout.addWidget(self.reset_view_btn)

        control_layout.addStretch()

        self.generate_btn = QPushButton("生成进度条")
        self.generate_btn.setMinimumHeight(30)
        self.generate_btn.setMinimumWidth(100)
        control_layout.addWidget(self.generate_btn)

        self.save_btn = QPushButton("导出进度条图片")
        self.save_btn.setMinimumHeight(30)
        self.save_btn.setMinimumWidth(100)
        self.save_btn.setEnabled(False)
        control_layout.addWidget(self.save_btn)

        bottom_layout.addLayout(control_layout)
        bottom_panel.setLayout(bottom_layout)

        # 添加到主布局
        main_layout.addWidget(top_panel)
        main_layout.addWidget(bottom_panel)

        # 事件
        self.import_btn.clicked.connect(self.import_data)
        self.export_btn.clicked.connect(self.export_data)
        self.font_combo.currentFontChanged.connect(self.update_font)
        self.font_size_spin.valueChanged.connect(self.update_font_size)
        self.add_segment_btn.clicked.connect(self.show_add_segment_dialog)
        self.edit_segment_btn.clicked.connect(self.edit_segment)
        self.delete_segment_btn.clicked.connect(self.delete_segment)
        self.segments_list.itemSelectionChanged.connect(self.toggle_edit_delete_buttons)
        self.reset_view_btn.clicked.connect(self.reset_preview_view)
        self.generate_btn.clicked.connect(self.generate_progress_bar)
        self.save_btn.clicked.connect(self.save_progress_bar)

    def update_font(self, font):
        """更新选择的字体"""
        self.selected_font = font.family()

    def update_font_size(self, size):
        """更新字体大小"""
        self.font_size = size

    def get_used_colors(self):
        """获取已使用的颜色列表"""
        return [segment['bg_color'] for segment in self.segments]

    def get_next_start_time(self):
        """计算下一个片段的开始时间（比上一个多30%的总时长）"""
        if not self.segments:
            return 0.0

        # 获取最后一个片段的开始时间
        last_start_time = self.segments[-1]['start_time']
        total_duration = self.duration_input.value()

        # 计算下一个开始时间（增加30%的总时长）
        next_start_time = last_start_time + (total_duration * 0.3)

        # 确保不超过总时长
        if next_start_time >= total_duration:
            next_start_time = total_duration * 0.9  # 如果超过，设置为总时长的90%

        return next_start_time

    def show_add_segment_dialog(self):
        # 计算下一个片段的开始时间
        next_start_time = self.get_next_start_time()

        dialog = VideoSegmentDialog(None, is_dark=self.is_dark, used_colors=self.get_used_colors(), start_time=next_start_time)
        if dialog.exec() == QDialog.Accepted:
            segment_data = dialog.get_segment_data()
            self.add_segment(segment_data)

    def add_segment(self, segment_data):
        start_time = segment_data['start_time']
        title = segment_data['title']
        text_color = segment_data['text_color']
        bg_color = segment_data['bg_color']

        # 检查时间是否有效
        if start_time >= self.duration_input.value():
            message_box_util.box_information(self.use_parent, "警告", "开始时间不能超过总视频时长")
            return

        # 检查时间是否与现有片段重叠
        for segment in self.segments:
            if abs(segment['start_time'] - start_time) < 0.1:
                message_box_util.box_information(self.use_parent, "警告", "开始时间与现有片段太接近")
                return

        segment = {
            'start_time': start_time,
            'title': title,
            'text_color': text_color,
            'bg_color': bg_color
        }

        self.segments.append(segment)
        self.segments.sort(key=lambda x: x['start_time'])
        self.update_segments_list()

    def update_segments_list(self):
        self.segments_list.clear()
        for i, segment in enumerate(self.segments):
            item = QListWidgetItem(f"{segment['start_time']}s: {segment['title']}")
            item.setBackground(segment['bg_color'])
            item.setForeground(segment['text_color'])
            self.segments_list.addItem(item)

    def toggle_edit_delete_buttons(self):
        has_selection = len(self.segments_list.selectedItems()) > 0
        self.edit_segment_btn.setEnabled(has_selection)
        self.delete_segment_btn.setEnabled(has_selection)

    def edit_segment(self):
        selected_items = self.segments_list.selectedItems()
        if not selected_items:
            return

        index = self.segments_list.row(selected_items[0])
        segment = self.segments[index]

        # 创建已使用颜色列表（排除当前片段的颜色）
        used_colors = [s['bg_color'] for i, s in enumerate(self.segments) if i != index]

        dialog = VideoSegmentDialog(None, is_dark=self.is_dark, used_colors=used_colors)
        dialog.start_time_input.setValue(segment['start_time'])
        dialog.title_input.setText(segment['title'])
        dialog.text_color = segment['text_color']
        dialog.bg_color = segment['bg_color']
        dialog.text_color_preview.setStyleSheet(
            f"background-color: {dialog.text_color.name()}; border: 1px solid #ccc;")
        dialog.bg_color_preview.setStyleSheet(f"background-color: {dialog.bg_color.name()}; border: 1px solid #ccc;")

        if dialog.exec() == QDialog.Accepted:
            # 删除旧片段，添加新片段
            self.segments.pop(index)
            self.add_segment(dialog.get_segment_data())

    def delete_segment(self):
        selected_items = self.segments_list.selectedItems()
        if not selected_items:
            return

        index = self.segments_list.row(selected_items[0])
        self.segments.pop(index)
        self.update_segments_list()

    def generate_progress_bar(self):
        if not self.segments:
            message_box_util.box_information(self.use_parent, "警告", "请至少添加一个视频片段")
            return

        total_duration = self.duration_input.value()
        width = self.width_spin.value()
        height = self.height_spin.value()

        # 创建图像 - 使用更高的分辨率
        image = QImage(width, height, QImage.Format_ARGB32)
        image.fill(Qt.white)

        painter = QPainter(image)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        # 绘制背景
        painter.fillRect(0, 0, width, height, Qt.white)

        # 绘制片段
        # 使用用户设置的字体和大小
        font = QFont(self.selected_font)
        font_size = self.font_size
        font.setPointSize(font_size)
        font.setWeight(QFont.Bold)  # 使用粗体提高可读性
        painter.setFont(font)

        for i, segment in enumerate(self.segments):
            start_x = (segment['start_time'] / total_duration) * width

            # 计算结束时间（下一个片段的开始时间或视频结束）
            if i < len(self.segments) - 1:
                end_time = self.segments[i + 1]['start_time']
            else:
                end_time = total_duration

            end_x = (end_time / total_duration) * width
            segment_width = end_x - start_x

            # 只绘制宽度大于5像素的片段，避免太窄无法显示
            if segment_width < 5:
                continue

            # 绘制背景色
            painter.fillRect(int(start_x), 0, int(segment_width), height, segment['bg_color'])

            # 绘制标题（只在宽度足够时显示）
            if segment_width > 50:
                painter.setPen(segment['text_color'])
                text_rect = QRectF(start_x + 5, 0, segment_width - 10, height)

                # 计算文本宽度，如果文本太长则省略
                title = segment['title']
                metrics = QFontMetrics(font)
                elided_title = metrics.elidedText(title, Qt.ElideRight, int(segment_width - 20))

                painter.drawText(text_rect, Qt.AlignCenter, elided_title)

        painter.end()

        # 保存图像并更新预览
        self.progress_bar_image = image
        self.update_preview()
        self.save_btn.setEnabled(True)

        message_box_util.box_information(self.use_parent, "成功", "进度条生成成功！")

    def update_preview(self):
        if not self.progress_bar_image:
            return

        # 将QImage转换为QPixmap
        pixmap = QPixmap.fromImage(self.progress_bar_image)

        # 设置到图像视图
        self.image_view.set_pixmap(pixmap)

    def reset_preview_view(self):
        """重置预览视图"""
        if self.image_view:
            self.image_view.reset_view()

    def save_progress_bar(self):
        if not self.progress_bar_image:
            return

        last_image_path = self.settings.value("lastImagePath", "")
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存进度条图像",
            last_image_path or "video_progress_bar.png",
            "PNG 图片 (*.png);;JPEG 图片 (*.jpg *.jpeg)"
        )

        if file_path:
            if self.progress_bar_image.save(file_path):
                # 保存本次路径到 QSettings
                self.settings.setValue("lastImagePath", file_path)
                message_box_util.box_information(self.use_parent, "成功", f"图像已保存到: {file_path}")
            else:
                message_box_util.box_information(self.use_parent, "错误", "图像保存失败！")

    def export_data(self):
        """导出进度条数据到JSON文件"""
        if not self.segments:
            message_box_util.box_information(self.use_parent, "警告", "没有数据可导出")
            return

        # 准备导出数据
        data = {
            "width": self.width_spin.value(),
            "height": self.height_spin.value(),
            "duration": self.duration_input.value(),
            "font": self.selected_font,
            "font_size": self.font_size,  # 添加字体大小
            "segments": []
        }

        # 转换片段数据为可序列化的格式
        for segment in self.segments:
            data["segments"].append({
                "start_time": segment["start_time"],
                "title": segment["title"],
                "text_color": segment["text_color"].name(),
                "bg_color": segment["bg_color"].name()
            })

        # 从 QSettings 中读取上次路径
        last_file_path = self.settings.value("lastFilePath", "")
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "导出进度条数据",
            last_file_path or "progress_bar_data.json",
            "*.json"
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                # 保存本次路径到 QSettings
                self.settings.setValue("lastFilePath", file_path)
                message_box_util.box_information(self.use_parent, "成功", "数据导出成功！")
            except Exception as e:
                message_box_util.box_information(self.use_parent, "错误", f"导出失败: {str(e)}")

    def import_data(self):
        """从JSON文件导入进度条数据"""
        # 从 QSettings 中读取上次路径
        last_file_path = self.settings.value("lastFilePath", "")
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "导入进度条数据",
            last_file_path or "",
            "JSON文件 (*.json);;所有文件 (*)"
        )

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # 验证数据格式
                if not all(key in data for key in ["width", "height", "duration", "font", "segments"]):
                    message_box_util.box_information(self.use_parent, "错误", "无效的数据格式")
                    return

                # 更新界面设置
                self.width_spin.setValue(data["width"])
                self.height_spin.setValue(data["height"])
                self.duration_input.setValue(data["duration"])

                # 设置字体
                font_index = self.font_combo.findText(data["font"], Qt.MatchFixedString)
                if font_index >= 0:
                    self.font_combo.setCurrentIndex(font_index)
                    self.selected_font = data["font"]

                # 设置字体大小（如果存在）
                if "font_size" in data:
                    self.font_size_spin.setValue(data["font_size"])
                    self.font_size = data["font_size"]

                # 清空现有片段
                self.segments.clear()

                # 添加新片段
                for segment_data in data["segments"]:
                    segment = {
                        "start_time": segment_data["start_time"],
                        "title": segment_data["title"],
                        "text_color": QColor(segment_data["text_color"]),
                        "bg_color": QColor(segment_data["bg_color"])
                    }
                    self.segments.append(segment)

                # 更新片段列表
                self.update_segments_list()

                # 保存本次路径到 QSettings
                self.settings.setValue("lastFilePath", file_path)
                message_box_util.box_information(self.use_parent, "成功", "数据导入成功！")

            except Exception as e:
                message_box_util.box_information(self.use_parent, "错误", f"导入失败: {str(e)}")

    def closeEvent(self, event):
        confirm = message_box_util.box_acknowledgement(self.use_parent, "注意", "该工具不保存数据到面板，如要后续使用请保存到本地！是否不保存继续退出？")
        if confirm:
            event.accept() # 接受关闭事件
        else:
            event.ignore()  # 忽略关闭事件


def show_progress_bar_generator_dialog(main_object, title, content):
    """显示进度条生成器对话框"""
    dialog = ProgressBarGenerator(None, main_object, title, content)
    dialog.refresh_geometry(main_object.toolkit.resolution_util.get_screen(main_object))
    dialog.show()
    return dialog