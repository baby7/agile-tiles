import math

from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QHBoxLayout, QFileDialog, QApplication
from PySide6.QtGui import QPainter, QColor, QPen, QGuiApplication, QPixmap, QFont
from PySide6.QtCore import Qt, QRect, QPoint, Signal, QSize

from src.ui import style_util


def get_virtual_geo():
    # 获取所有屏幕计算最大的宽度和高度
    screens = QGuiApplication.screens()
    desktop_width = 0
    desktop_height = 0
    for screen in screens:
        # 获取屏幕的几何信息（逻辑像素）
        geometry = screen.geometry()
        # 获取设备像素比（缩放因子）
        device_pixel_ratio = screen.devicePixelRatio()
        # 计算物理分辨率
        physical_x = round(geometry.x() * device_pixel_ratio)
        physical_y = round(geometry.y() * device_pixel_ratio)
        physical_width = round(geometry.width() * device_pixel_ratio)
        physical_height = round(geometry.height() * device_pixel_ratio)
        # 计算相对于0坐标的顶点坐标
        screen_width = physical_x + physical_width
        screen_height = physical_y + physical_height
        # 更新最大宽高
        if screen_width > desktop_width:
            desktop_width = screen_width
        if screen_height > desktop_height:
            desktop_height = screen_height
    return QRect(0, 0, desktop_width, desktop_height)


def grab_screens():
    """截取所有屏幕，并拼接成一张大图"""
    screens = QGuiApplication.screens()
    virtual_geo = get_virtual_geo()
    result = QPixmap(virtual_geo.size())
    result.fill(Qt.GlobalColor.transparent)

    painter = QPainter(result)
    for screen in screens:
        # 获取屏幕的几何信息（逻辑像素）
        geometry = screen.geometry()
        # 获取设备像素比（缩放因子）
        device_pixel_ratio = screen.devicePixelRatio()
        # 计算物理分辨率
        physical_x = round(geometry.x() * device_pixel_ratio)
        physical_y = round(geometry.y() * device_pixel_ratio)
        physical_width = round(geometry.width() * device_pixel_ratio)
        physical_height = round(geometry.height() * device_pixel_ratio)
        physical_geometry = QRect(physical_x, physical_y, physical_width, physical_height)
        # 获取屏幕的像素
        pix = screen.grabWindow(0)
        pix.setDevicePixelRatio(1)
        # pix 已经是逻辑大小（Qt 会自动考虑 DPR）
        target_rect = physical_geometry.topLeft() - virtual_geo.topLeft()
        painter.drawPixmap(target_rect, pix)
    painter.end()
    return result, virtual_geo

# def pixmap_device_pixel_ratio_change(pixmap: QPixmap):
#     width = int(pixmap.width() / pixmap.devicePixelRatio())
#     height = int(pixmap.height() / pixmap.devicePixelRatio())
#     result = QPixmap(QSize(width, height))
#     result.fill(Qt.GlobalColor.transparent)
#     painter = QPainter(result)
#     painter.drawPixmap(QPoint(0, 0), pixmap)
#     return result



class Rectangle:
    """矩形类，存储矩形信息和绘制属性"""

    def __init__(self, rect, pen):
        self.rect = rect
        self.pen = QPen(pen)  # 复制画笔属性
        self.type = "rectangle"  # 图形类型


class Ellipse:
    """椭圆类，存储椭圆信息和绘制属性"""

    def __init__(self, rect, pen):
        self.rect = rect
        self.pen = QPen(pen)  # 复制画笔属性
        self.type = "ellipse"  # 图形类型


class Line:
    """直线类，存储直线信息和绘制属性"""

    def __init__(self, start_point, end_point, pen):
        self.start_point = start_point
        self.end_point = end_point
        self.pen = QPen(pen)  # 复制画笔属性
        self.type = "line"  # 图形类型


class Arrow:
    """箭头类，存储箭头信息和绘制属性"""

    def __init__(self, start_point, end_point, pen):
        self.start_point = start_point
        self.end_point = end_point
        self.pen = QPen(pen)  # 复制画笔属性
        self.type = "arrow"  # 图形类型


class ScreenshotWidget(QWidget):
    """截图组件，整合了遮罩层和工具栏"""
    close_signal = Signal(str)

    def __init__(self, parent=None, main_object=None):
        super().__init__(parent=None)
        self.main_object = main_object
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)  # 允许接收键盘事件
        self.setMouseTracking(True)

        self.screen_count = len(QGuiApplication.screens())
        if self.screen_count == 1:
            # 截取整个屏幕作为背景
            self.fullscreen_pixmap = QGuiApplication.primaryScreen().grabWindow(0)
            screen_geometry = QGuiApplication.primaryScreen().virtualGeometry()
            self.dpr = self.devicePixelRatioF()  # 获取设备像素比
        else:
            # 获取所有屏幕的总体矩形 + 截图
            self.fullscreen_pixmap, screen_geometry = grab_screens()
            self.dpr = 1
        self.setGeometry(screen_geometry)

        # 截图相关变量
        self.start_point = QPoint()
        self.end_point = QPoint()
        self.dragging = False
        self.captured_pixmap = None
        self.screenshot_rect = None
        self.is_captured = False  # 标记是否已完成截图

        # 区域调整相关变量
        self.resizing = False  # 是否正在调整区域
        self.resize_handle = None  # 当前调整的把手位置
        self.resize_start_rect = None  # 调整开始时的矩形
        self.resize_start_point = None  # 调整开始的鼠标位置
        self.handle_size = 8  # 调整把手的大小
        self.moving = False  # 是否正在移动截图区域
        self.move_start_point = None  # 移动开始时的鼠标位置
        self.move_start_rect = None  # 移动开始时的矩形位置

        # 图形绘制相关变量
        self.drawing = False  # 是否正在绘制图形
        self.draw_start = QPoint()  # 绘制起始点
        self.draw_end = QPoint()  # 绘制结束点
        self.shapes = []  # 存储所有绘制的图形
        self.undo_stack = []  # 撤销栈
        self.redo_stack = []  # 重做栈
        self.current_pen = QPen(QColor(255, 0, 0), 3)  # 当前画笔设置
        self.current_tool = None  # 当前选中的工具
        self.last_tool = None  # 上一次选中的工具

        # 提示文本
        self.tip_label = QLabel("拖动鼠标选择区域 | ESC取消", self)
        self.tip_label.setStyleSheet(
            "background-color: rgba(0, 0, 0, 120); "
            "color: white; "
            "padding: 5px; "
            "border-radius: 5px;"
        )
        self.tip_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tip_label.setGeometry(
            screen_geometry.width() // 2 - int(0.07968 * screen_geometry.width()),
            int(0.027778 * screen_geometry.height()),
            int(0.15625 * screen_geometry.width()),
            int(0.027778 * screen_geometry.height())
        )
        font = QFont()
        font.setPointSize(int(10 * 0.00052 * screen_geometry.width()))
        self.tip_label.setFont(font)

        # 尺寸信息显示
        self.size_label = QLabel("", self)
        self.size_label.setStyleSheet(
            "background-color: rgba(0, 0, 0, 150); "
            "color: white; "
            "padding: 3px;"
        )
        self.size_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.size_label.setFixedSize(int(0.052083 * screen_geometry.width()), int(0.022222 * screen_geometry.height()))
        self.size_label.setFont(font)
        self.size_label.hide()

        # 创建工具栏
        self.toolbar = QWidget(self)
        self.toolbar.setStyleSheet("""
            QWidget {
                background-color: rgb(255, 255, 255);
                border-radius: 5px;
            }
            QPushButton {
                background-color: rgba(70, 70, 70, 50);
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: rgba(90, 90, 90, 50);
            }
            QPushButton:pressed {
                background-color: rgba(110, 110, 110, 50);
            }
            QPushButton:checked {
                background-color: rgba(130, 130, 130, 50);
            }
            QPushButton:disabled {
                background-color: rgba(50, 50, 50, 30);
                color: rgba(255, 255, 255, 100);
            }
        """)
        self.toolbar.hide()

        # 创建图形工具子工具栏
        self.draw_toolbar = QWidget(self)
        self.draw_toolbar.setStyleSheet("""
            QWidget {
                background-color: rgb(240, 240, 240);
                border-radius: 5px;
            }
            QPushButton {
                background-color: rgba(70, 70, 70, 50);
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: rgba(90, 90, 90, 50);
            }
            QPushButton:pressed {
                background-color: rgba(110, 110, 110, 50);
            }
            QPushButton:checked {
                background-color: rgba(130, 130, 130, 50);
            }
            QPushButton:disabled {
                background-color: rgba(50, 50, 50, 30);
                color: rgba(255, 255, 255, 100);
            }
        """)
        self.draw_toolbar.hide()

        # 创建粗细选择按钮 - 使用圆形代替文本
        self.thin_btn = QPushButton("", self.draw_toolbar)
        self.thin_btn.setCheckable(True)
        self.thin_btn.setFixedSize(16, 16)
        self.thin_btn.setStyleSheet("""
            QPushButton {
                background-color: black;
                border-radius: 8px;
            }
            QPushButton:checked {
                background-color: rgba(138, 162, 210, 125);
            }
        """)
        self.thin_btn.clicked.connect(lambda: self.set_pen_width(1))

        self.medium_btn = QPushButton("", self.draw_toolbar)
        self.medium_btn.setCheckable(True)
        self.medium_btn.setFixedSize(20, 20)
        self.medium_btn.setStyleSheet("""
            QPushButton {
                background-color: black;
                border-radius: 10px;
            }
            QPushButton:checked {
                background-color: rgba(138, 162, 210, 125);
            }
        """)
        self.medium_btn.clicked.connect(lambda: self.set_pen_width(3))
        self.medium_btn.setChecked(True)  # 默认选中中等粗细

        self.thick_btn = QPushButton("", self.draw_toolbar)
        self.thick_btn.setCheckable(True)
        self.thick_btn.setFixedSize(24, 24)
        self.thick_btn.setStyleSheet("""
            QPushButton {
                background-color: black;
                border-radius: 12px;
            }
            QPushButton:checked {
                background-color: rgba(138, 162, 210, 125);
            }
        """)
        self.thick_btn.clicked.connect(lambda: self.set_pen_width(5))

        # 创建颜色选择按钮
        self.red_btn = QPushButton("", self.draw_toolbar)
        self.red_btn.setCheckable(True)
        self.red_btn.setFixedSize(24, 24)
        self.red_btn.setStyleSheet("""
            QPushButton {
                background-color: red;
                border-radius: 12px;
            }
            QPushButton:checked {
                border: 4px solid rgb(125, 125, 125);
            }
        """)
        self.red_btn.clicked.connect(lambda: self.set_pen_color(QColor(255, 0, 0)))
        self.red_btn.setChecked(True)  # 默认选中红色

        self.green_btn = QPushButton("", self.draw_toolbar)
        self.green_btn.setCheckable(True)
        self.green_btn.setFixedSize(24, 24)
        self.green_btn.setStyleSheet("""
            QPushButton {
                background-color: green;
                border-radius: 12px;
            }
            QPushButton:checked {
                border: 4px solid rgb(125, 125, 125);
            }
        """)
        self.green_btn.clicked.connect(lambda: self.set_pen_color(QColor(0, 255, 0)))

        self.blue_btn = QPushButton("", self.draw_toolbar)
        self.blue_btn.setCheckable(True)
        self.blue_btn.setFixedSize(24, 24)
        self.blue_btn.setStyleSheet("""
            QPushButton {
                background-color: blue;
                border-radius: 12px;
            }
            QPushButton:checked {
                border: 4px solid rgb(125, 125, 125);
            }
        """)
        self.blue_btn.clicked.connect(lambda: self.set_pen_color(QColor(0, 0, 255)))

        self.yellow_btn = QPushButton("", self.draw_toolbar)
        self.yellow_btn.setCheckable(True)
        self.yellow_btn.setFixedSize(24, 24)
        self.yellow_btn.setStyleSheet("""
            QPushButton {
                background-color: yellow;
                border-radius: 12px;
            }
            QPushButton:checked {
                border: 4px solid rgb(125, 125, 125);
            }
        """)
        self.yellow_btn.clicked.connect(lambda: self.set_pen_color(QColor(255, 255, 0)))

        self.white_btn = QPushButton("", self.draw_toolbar)
        self.white_btn.setCheckable(True)
        self.white_btn.setFixedSize(24, 24)
        self.white_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border-radius: 12px;
            }
            QPushButton:checked {
                border: 4px solid rgb(125, 125, 125);
            }
        """)
        self.white_btn.clicked.connect(lambda: self.set_pen_color(QColor(255, 255, 255)))

        self.black_btn = QPushButton("", self.draw_toolbar)
        self.black_btn.setCheckable(True)
        self.black_btn.setFixedSize(24, 24)
        self.black_btn.setStyleSheet("""
            QPushButton {
                background-color: black;
                border-radius: 12px;
            }
            QPushButton:checked {
                border: 4px solid rgb(125, 125, 125);
            }
        """)
        self.black_btn.clicked.connect(lambda: self.set_pen_color(QColor(0, 0, 0)))

        self.toolbar_title = QLabel("【】", self.draw_toolbar)

        # 图形工具栏布局
        draw_toolbar_layout = QHBoxLayout(self.draw_toolbar)
        draw_toolbar_layout.addStretch()
        draw_toolbar_layout.addWidget(self.toolbar_title)
        draw_toolbar_layout.addWidget(QLabel("粗细:"))
        draw_toolbar_layout.addWidget(self.thin_btn)
        draw_toolbar_layout.addWidget(self.medium_btn)
        draw_toolbar_layout.addWidget(self.thick_btn)
        draw_toolbar_layout.addSpacing(10)
        draw_toolbar_layout.addWidget(QLabel("颜色:"))
        draw_toolbar_layout.addWidget(self.red_btn)
        draw_toolbar_layout.addWidget(self.green_btn)
        draw_toolbar_layout.addWidget(self.blue_btn)
        draw_toolbar_layout.addWidget(self.yellow_btn)
        draw_toolbar_layout.addWidget(self.white_btn)
        draw_toolbar_layout.addWidget(self.black_btn)
        draw_toolbar_layout.addStretch()
        draw_toolbar_layout.setContentsMargins(5, 5, 5, 5)

        # 创建按钮
        self.rect_btn = QPushButton("", self.toolbar)
        self.rect_btn.setToolTip("绘制矩形")
        self.rect_btn.setCheckable(True)  # 设置为可选中状态
        style_util.set_card_button_style(self.rect_btn, "Graphics/rectangle-one", is_dark=False)

        self.ellipse_btn = QPushButton("", self.toolbar)
        self.ellipse_btn.setToolTip("绘制椭圆")
        self.ellipse_btn.setCheckable(True)
        style_util.set_card_button_style(self.ellipse_btn, "Graphics/round", is_dark=False)

        self.line_btn = QPushButton("", self.toolbar)
        self.line_btn.setToolTip("绘制直线")
        self.line_btn.setCheckable(True)
        style_util.set_card_button_style(self.line_btn, "Character/minus", is_dark=False)

        self.arrow_btn = QPushButton("", self.toolbar)
        self.arrow_btn.setToolTip("绘制箭头")
        self.arrow_btn.setCheckable(True)
        style_util.set_card_button_style(self.arrow_btn, "Arrows/arrow-left-up", is_dark=False)

        # 添加撤销和重做按钮
        self.undo_btn = QPushButton("", self.toolbar)
        self.undo_btn.setToolTip("撤销")
        style_util.set_card_button_style(self.undo_btn, "Edit/back", is_dark=False)
        self.undo_btn.clicked.connect(self.undo)
        self.undo_btn.setEnabled(False)  # 初始状态禁用

        self.redo_btn = QPushButton("", self.toolbar)
        self.redo_btn.setToolTip("重做")
        style_util.set_card_button_style(self.redo_btn, "Edit/next", is_dark=False)
        self.redo_btn.clicked.connect(self.redo)
        self.redo_btn.setEnabled(False)  # 初始状态禁用

        self.translate_btn = QPushButton("", self.toolbar)
        self.translate_btn.setToolTip("识别文字并翻译")
        style_util.set_card_button_style(self.translate_btn, "Base/translate", is_dark=False)
        self.ocr_to_excel_btn = QPushButton("", self.toolbar)
        self.ocr_to_excel_btn.setToolTip("图片转表格")
        style_util.set_card_button_style(self.ocr_to_excel_btn, "Office/excel", is_dark=False)
        self.ocr_btn = QPushButton("", self.toolbar)
        self.ocr_btn.setToolTip("识别文字")
        style_util.set_card_button_style(self.ocr_btn, "Office/text-recognition", is_dark=False)
        self.save_btn = QPushButton("", self.toolbar)
        self.save_btn.setToolTip("另存为图片")
        style_util.set_card_button_style(self.save_btn, "Hardware/memory-card-one", is_dark=False)
        self.see_btn = QPushButton("", self.toolbar)
        self.see_btn.setToolTip("查看截图")
        style_util.set_card_button_style(self.see_btn, "Base/preview-open", is_dark=False)
        self.top_btn = QPushButton("", self.toolbar)
        self.top_btn.setToolTip("置顶/钉住")
        style_util.set_card_button_style(self.top_btn, "Edit/pin", is_dark=False)
        self.copy_btn = QPushButton("", self.toolbar)
        self.copy_btn.setToolTip("复制截图到剪贴板")
        style_util.set_card_button_style(self.copy_btn, "Edit/copy", is_dark=False)
        self.close_btn = QPushButton("", self.toolbar)
        self.close_btn.setToolTip("关闭")
        style_util.set_card_button_style(self.close_btn, "Character/close", is_dark=False)

        # 连接信号
        self.rect_btn.clicked.connect(lambda: self.toggle_drawing_mode("rectangle"))
        self.ellipse_btn.clicked.connect(lambda: self.toggle_drawing_mode("ellipse"))
        self.line_btn.clicked.connect(lambda: self.toggle_drawing_mode("line"))
        self.arrow_btn.clicked.connect(lambda: self.toggle_drawing_mode("arrow"))
        self.translate_btn.clicked.connect(self.translate_screenshot)
        self.ocr_to_excel_btn.clicked.connect(self.ocr_to_excel_screenshot)
        self.ocr_btn.clicked.connect(self.ocr_screenshot)
        self.save_btn.clicked.connect(self.save_screenshot)
        self.see_btn.clicked.connect(self.see_screenshot)
        self.top_btn.clicked.connect(self.see_top_screenshot)
        self.copy_btn.clicked.connect(self.copy_screenshot)
        self.close_btn.clicked.connect(self.close_screenshot)

        # 连接鼠标悬停事件
        self.close_btn.installEventFilter(self)
        self.translate_btn.installEventFilter(self)
        self.ocr_to_excel_btn.installEventFilter(self)
        self.ocr_btn.installEventFilter(self)
        self.save_btn.installEventFilter(self)
        self.see_btn.installEventFilter(self)
        self.top_btn.installEventFilter(self)
        self.copy_btn.installEventFilter(self)
        self.rect_btn.installEventFilter(self)
        self.ellipse_btn.installEventFilter(self)
        self.line_btn.installEventFilter(self)
        self.arrow_btn.installEventFilter(self)
        self.undo_btn.installEventFilter(self)
        self.redo_btn.installEventFilter(self)

        # 工具栏布局
        toolbar_layout = QHBoxLayout(self.toolbar)
        toolbar_layout.addWidget(self.rect_btn)
        toolbar_layout.addWidget(self.ellipse_btn)
        toolbar_layout.addWidget(self.line_btn)
        toolbar_layout.addWidget(self.arrow_btn)
        toolbar_layout.addWidget(self.undo_btn)
        toolbar_layout.addWidget(self.redo_btn)
        toolbar_layout.addWidget(self.translate_btn)
        toolbar_layout.addWidget(self.ocr_to_excel_btn)
        toolbar_layout.addWidget(self.ocr_btn)
        toolbar_layout.addWidget(self.save_btn)
        toolbar_layout.addWidget(self.see_btn)
        toolbar_layout.addWidget(self.top_btn)
        toolbar_layout.addWidget(self.copy_btn)
        toolbar_layout.addWidget(self.close_btn)
        toolbar_layout.setContentsMargins(5, 5, 5, 5)

    def get_resize_handle_at(self, pos):
        """获取指定位置上的调整把手"""
        if not self.screenshot_rect:
            return None

        rect = self.screenshot_rect
        handle_size = self.handle_size

        # 定义把手的矩形区域
        handles = {
            'top_left': QRect(rect.left() - handle_size // 2, rect.top() - handle_size // 2, handle_size, handle_size),
            'top_right': QRect(rect.right() - handle_size // 2, rect.top() - handle_size // 2, handle_size,
                               handle_size),
            'bottom_left': QRect(rect.left() - handle_size // 2, rect.bottom() - handle_size // 2, handle_size,
                                 handle_size),
            'bottom_right': QRect(rect.right() - handle_size // 2, rect.bottom() - handle_size // 2, handle_size,
                                  handle_size),
            'top': QRect(rect.center().x() - handle_size // 2, rect.top() - handle_size // 2, handle_size, handle_size),
            'bottom': QRect(rect.center().x() - handle_size // 2, rect.bottom() - handle_size // 2, handle_size,
                            handle_size),
            'left': QRect(rect.left() - handle_size // 2, rect.center().y() - handle_size // 2, handle_size,
                          handle_size),
            'right': QRect(rect.right() - handle_size // 2, rect.center().y() - handle_size // 2, handle_size,
                           handle_size),
        }

        # 检查鼠标是否在任何把手上
        for handle_name, handle_rect in handles.items():
            if handle_rect.contains(pos):
                return handle_name

        # 检查是否在截图区域内（用于移动）
        if rect.contains(pos):
            return 'move'

        return None

    def update_cursor(self, pos):
        """根据鼠标位置更新光标"""
        if not self.is_captured or not self.screenshot_rect:
            self.setCursor(Qt.CursorShape.CrossCursor)
            return

        handle = self.get_resize_handle_at(pos)

        if handle == 'top_left' or handle == 'bottom_right':
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
        elif handle == 'top_right' or handle == 'bottom_left':
            self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        elif handle == 'top' or handle == 'bottom':
            self.setCursor(Qt.CursorShape.SizeVerCursor)
        elif handle == 'left' or handle == 'right':
            self.setCursor(Qt.CursorShape.SizeHorCursor)
        elif handle == 'move' and not self.current_tool:  # 只有在非绘图模式下才显示移动光标
            self.setCursor(Qt.CursorShape.SizeAllCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def add_to_history(self):
        """将当前图形状态添加到历史记录"""
        # 深拷贝当前图形列表
        shapes_copy = []
        for shape in self.shapes:
            if shape.type == "rectangle":
                shapes_copy.append(Rectangle(shape.rect, shape.pen))
            elif shape.type == "ellipse":
                shapes_copy.append(Ellipse(shape.rect, shape.pen))
            elif shape.type == "line":
                shapes_copy.append(Line(shape.start_point, shape.end_point, shape.pen))
            elif shape.type == "arrow":
                shapes_copy.append(Arrow(shape.start_point, shape.end_point, shape.pen))

        # 添加到撤销栈
        self.undo_stack.append(shapes_copy)
        # 清空重做栈
        self.redo_stack = []

        # 更新按钮状态
        self.undo_btn.setEnabled(len(self.undo_stack) > 0)
        self.redo_btn.setEnabled(len(self.redo_stack) > 0)

    def undo(self):
        # 隐藏绘图工具栏
        self.draw_toolbar.hide()
        """撤销操作"""
        if not self.undo_stack:
            return

        # 将当前状态保存到重做栈
        shapes_copy = []
        for shape in self.shapes:
            if shape.type == "rectangle":
                shapes_copy.append(Rectangle(shape.rect, shape.pen))
            elif shape.type == "ellipse":
                shapes_copy.append(Ellipse(shape.rect, shape.pen))
            elif shape.type == "line":
                shapes_copy.append(Line(shape.start_point, shape.end_point, shape.pen))
            elif shape.type == "arrow":
                shapes_copy.append(Arrow(shape.start_point, shape.end_point, shape.pen))
        self.redo_stack.append(shapes_copy)

        # 恢复上一个状态
        self.shapes = self.undo_stack.pop()

        # 更新按钮状态
        self.undo_btn.setEnabled(len(self.undo_stack) > 0)
        self.redo_btn.setEnabled(len(self.redo_stack) > 0)

        self.update()

    def redo(self):
        # 隐藏绘图工具栏
        self.draw_toolbar.hide()
        """重做操作"""
        if not self.redo_stack:
            return

        # 将当前状态保存到撤销栈
        shapes_copy = []
        for shape in self.shapes:
            if shape.type == "rectangle":
                shapes_copy.append(Rectangle(shape.rect, shape.pen))
            elif shape.type == "ellipse":
                shapes_copy.append(Ellipse(shape.rect, shape.pen))
            elif shape.type == "line":
                shapes_copy.append(Line(shape.start_point, shape.end_point, shape.pen))
            elif shape.type == "arrow":
                shapes_copy.append(Arrow(shape.start_point, shape.end_point, shape.pen))
        self.undo_stack.append(shapes_copy)

        # 恢复下一个状态
        self.shapes = self.redo_stack.pop()

        # 更新按钮状态
        self.undo_btn.setEnabled(len(self.undo_stack) > 0)
        self.redo_btn.setEnabled(len(self.redo_stack) > 0)

        self.update()

    def set_pen_width(self, width):
        """设置画笔粗细"""
        self.current_pen.setWidth(width)
        # 更新按钮选中状态
        self.thin_btn.setChecked(width == 1)
        self.medium_btn.setChecked(width == 3)
        self.thick_btn.setChecked(width == 5)

    def set_pen_color(self, color):
        """设置画笔颜色"""
        self.current_pen.setColor(color)
        # 更新按钮选中状态
        self.red_btn.setChecked(self.compare_colors(color, QColor(255, 0, 0)))
        self.green_btn.setChecked(self.compare_colors(color, QColor(0, 255, 0)))
        self.blue_btn.setChecked(self.compare_colors(color, QColor(0, 0, 255)))
        self.yellow_btn.setChecked(self.compare_colors(color, QColor(255, 255, 0)))
        self.white_btn.setChecked(self.compare_colors(color, QColor(255, 255, 255)))
        self.black_btn.setChecked(self.compare_colors(color, QColor(0, 0, 0)))

    def compare_colors(self, color1, color2):
        if color1.red() == color2.red() and color1.green() == color2.green() and color1.blue() == color2.blue():
            return True
        else:
            return False

    def toggle_drawing_mode(self, tool):
        """切换绘图模式"""
        # 取消之前选中的工具
        if self.current_tool:
            if self.current_tool == "rectangle":
                self.toolbar_title.setText("【矩形】")
                self.rect_btn.setChecked(False)
            elif self.current_tool == "ellipse":
                self.toolbar_title.setText("【椭圆】")
                self.ellipse_btn.setChecked(False)
            elif self.current_tool == "line":
                self.toolbar_title.setText("【直线】")
                self.line_btn.setChecked(False)
            elif self.current_tool == "arrow":
                self.toolbar_title.setText("【箭头】")
                self.arrow_btn.setChecked(False)

        # 切换文字
        if tool == "rectangle":
            self.toolbar_title.setText("【矩形】")
        elif tool == "ellipse":
            self.toolbar_title.setText("【椭圆】")
        elif tool == "line":
            self.toolbar_title.setText("【直线】")
        elif tool == "arrow":
            self.toolbar_title.setText("【箭头】")

        # 设置新的工具
        if self.current_tool == tool:
            # 如果点击的是当前已选中的工具，则取消选择
            self.current_tool = None
            self.drawing = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
            # 隐藏绘图工具栏
            self.draw_toolbar.hide()
        else:
            # 选择新的工具
            self.current_tool = tool
            self.drawing = False
            self.setCursor(Qt.CursorShape.CrossCursor)
            # 显示绘图工具栏
            self.show_draw_toolbar()

        self.update()

    def show_draw_toolbar(self):
        """显示绘图工具栏"""
        if self.screenshot_rect:
            # 定位绘图工具栏在主工具栏下方
            toolbar_rect = self.toolbar.geometry()
            self.draw_toolbar.setFixedSize(self.toolbar.width(), 50)  # 增加高度以适应圆形按钮
            self.draw_toolbar.move(toolbar_rect.x(), toolbar_rect.bottom() + 5)
            self.draw_toolbar.show()

    def paintEvent(self, event):
        painter = QPainter(self)

        if not self.is_captured:
            # 截图模式
            if self.screen_count > 1:
                self.paint_more_screen(painter)
            else:
                self.paint_one_screen(painter)
        else:
            # 编辑模式 - 只显示截图区域，其他区域半透明
            painter.drawPixmap(0, 0, self.fullscreen_pixmap)
            painter.fillRect(self.rect(), QColor(0, 0, 0, 120))

            # 绘制截图区域
            if self.screenshot_rect:
                painter.drawPixmap(self.screenshot_rect.topLeft(), self.captured_pixmap)
                painter.setPen(QPen(QColor(100, 150, 243), 2))
                painter.drawRect(self.screenshot_rect)

                # 绘制调整把手
                if not self.drawing and not self.resizing and not self.moving:  # 不在绘图或调整时才绘制把手
                    self.draw_resize_handles(painter)

            # 绘制所有已保存的图形
            for shape in self.shapes:
                painter.setPen(shape.pen)
                if shape.type == "rectangle":
                    painter.drawRect(shape.rect)
                elif shape.type == "ellipse":
                    painter.drawEllipse(shape.rect)
                elif shape.type == "line":
                    painter.drawLine(shape.start_point, shape.end_point)
                elif shape.type == "arrow":
                    self.draw_arrow(painter, shape.start_point, shape.end_point, shape.pen)

            # 绘制当前正在绘制的图形
            if self.drawing and self.draw_start and self.draw_end:
                rect = QRect(self.draw_start, self.draw_end).normalized()
                painter.setPen(self.current_pen)
                painter.setBrush(Qt.BrushStyle.NoBrush)  # 确保没有填充

                if self.current_tool == "rectangle":
                    painter.drawRect(rect)
                elif self.current_tool == "ellipse":
                    painter.drawEllipse(rect)
                elif self.current_tool == "line":
                    painter.drawLine(self.draw_start, self.draw_end)
                elif self.current_tool == "arrow":
                    self.draw_arrow(painter, self.draw_start, self.draw_end, self.current_pen)

    def draw_resize_handles(self, painter):
        """绘制调整把手"""
        if not self.screenshot_rect:
            return

        rect = self.screenshot_rect
        handle_size = self.handle_size

        # 保存原始画笔和画刷
        original_pen = painter.pen()
        original_brush = painter.brush()

        # 设置把手颜色
        painter.setPen(QPen(QColor(255, 255, 255), 1))
        painter.setBrush(QColor(100, 150, 243))

        # 绘制四个角把手
        handles = [
            QRect(rect.left() - handle_size // 2, rect.top() - handle_size // 2, handle_size, handle_size),  # 左上
            QRect(rect.right() - handle_size // 2, rect.top() - handle_size // 2, handle_size, handle_size),  # 右上
            QRect(rect.left() - handle_size // 2, rect.bottom() - handle_size // 2, handle_size, handle_size),  # 左下
            QRect(rect.right() - handle_size // 2, rect.bottom() - handle_size // 2, handle_size, handle_size),  # 右下
        ]

        for handle in handles:
            painter.drawRect(handle)

        # 绘制四条边中间的把手
        side_handles = [
            QRect(rect.center().x() - handle_size // 2, rect.top() - handle_size // 2, handle_size, handle_size),  # 上
            QRect(rect.center().x() - handle_size // 2, rect.bottom() - handle_size // 2, handle_size, handle_size),
            # 下
            QRect(rect.left() - handle_size // 2, rect.center().y() - handle_size // 2, handle_size, handle_size),  # 左
            QRect(rect.right() - handle_size // 2, rect.center().y() - handle_size // 2, handle_size, handle_size),  # 右
        ]

        for handle in side_handles:
            painter.drawRect(handle)

        # 恢复原始画笔和画刷
        painter.setPen(original_pen)
        painter.setBrush(original_brush)

    def draw_arrow(self, painter, start_point, end_point, pen):
        """绘制箭头 - 修复版本"""
        # 绘制直线
        painter.setPen(pen)
        painter.drawLine(start_point, end_point)

        # 计算箭头的方向向量
        dx = end_point.x() - start_point.x()
        dy = end_point.y() - start_point.y()

        # 计算箭头的角度（注意Qt的y轴是向下的）
        angle = math.atan2(dy, dx)

        # 箭头长度
        arrow_length = 15
        # 箭头角度
        arrow_angle = math.pi / 6  # 30度

        # 计算箭头两个点的坐标
        x1 = end_point.x() - arrow_length * math.cos(angle - arrow_angle)
        y1 = end_point.y() - arrow_length * math.sin(angle - arrow_angle)
        x2 = end_point.x() - arrow_length * math.cos(angle + arrow_angle)
        y2 = end_point.y() - arrow_length * math.sin(angle + arrow_angle)

        # 绘制箭头
        painter.drawLine(end_point, QPoint(int(x1), int(y1)))
        painter.drawLine(end_point, QPoint(int(x2), int(y2)))

    def paint_more_screen(self, painter):
        painter.drawPixmap(0, 0, self.fullscreen_pixmap)  # 背景

        # 半透明遮罩
        painter.fillRect(self.rect(), QColor(0, 0, 0, 120))

        if self.dragging:
            # 计算选区矩形
            rect = QRect(self.start_point, self.end_point).normalized()

            # 从截图中裁剪区域
            selected_pix = self.fullscreen_pixmap.copy(rect)

            # 绘制选区
            painter.drawPixmap(rect.topLeft(), selected_pix)

            # 绘制选区边框
            painter.setPen(QPen(QColor(100, 150, 243), 2))
            painter.drawRect(rect)

            # 更新尺寸标签
            self.size_label.setText(f"{rect.width()} x {rect.height()}")
            self.size_label.move(rect.bottomRight().x() - 50, rect.bottomRight().y() + 10)
            self.size_label.show()
        else:
            self.size_label.hide()

    def paint_one_screen(self, painter):
        """绘制遮罩层和选区 - 修复模糊问题"""
        # 获取窗口大小
        win_size = self.size()
        # 绘制屏幕截图背景（考虑DPI缩放")
        scaled_pixmap = self.fullscreen_pixmap.scaled(
            win_size * self.dpr,
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        painter.drawPixmap(0, 0, win_size.width(), win_size.height(), scaled_pixmap)
        # 绘制半透明遮罩层
        painter.fillRect(self.rect(), QColor(0, 0, 0, 120))
        if self.dragging:
            # 计算选区矩形
            rect = QRect(self.start_point, self.end_point).normalized()
            # 修复：从原始图像中拷贝区域（不缩放）
            dpr_rect = QRect(
                rect.topLeft() * self.dpr,
                rect.size() * self.dpr
            )
            selected_pix = self.fullscreen_pixmap.copy(dpr_rect)
            # 绘制选区
            painter.drawPixmap(rect.topLeft(), selected_pix)
            # 绘制选区边框
            painter.setPen(QPen(QColor(100, 150, 243), 2))
            painter.drawRect(rect)
            # 更新尺寸标签
            self.size_label.setText(f"{rect.width()} x {rect.height()}")
            self.size_label.move(rect.bottomRight().x() - 50, rect.bottomRight().y() + 10)
            self.size_label.show()
        else:
            self.size_label.hide()

    def mousePressEvent(self, event):
        """鼠标按下事件处理"""
        if event.button() == Qt.MouseButton.LeftButton:
            # 使用原始坐标
            pos = event.position().toPoint()

            if self.is_captured and self.screenshot_rect:
                print("点击了截图区域")
                # 检查是否点击了调整把手
                handle = self.get_resize_handle_at(pos)
                if handle and handle != "move":
                    print("点击了调整把手")
                    # 如果点击了把手，无论是否在绘图模式下都允许调整
                    self.resizing = True
                    self.resize_handle = handle
                    self.resize_start_rect = QRect(self.screenshot_rect)
                    self.resize_start_point = pos
                    return

                # 检查是否在截图区域内
                if self.screenshot_rect.contains(pos):
                    print("在截图区域内")
                    if self.current_tool:
                        print("在绘图模式下")
                        # 绘图模式下，记录起始点
                        self.draw_start = pos
                        self.draw_end = self.draw_start
                        self.drawing = True
                    else:
                        print("非绘图模式下")
                        # 非绘图模式下，开始移动截图区域
                        # self.moving = True
                        # self.move_start_point = pos
                        # self.move_start_rect = QRect(self.screenshot_rect)
                        self.resizing = True
                        self.resize_handle = handle
                        self.resize_start_rect = QRect(self.screenshot_rect)
                        self.resize_start_point = pos
                    return

            # 如果不在截图区域内，开始选择区域
            if not self.is_captured:
                print("开始选择区域")
                self.start_point = pos
                self.end_point = self.start_point
                self.dragging = True
                self.tip_label.show()
                self.update()

            # 明确接受事件，防止继续传递
            event.accept()
        else:
            # 对于非左键事件，调用父类处理
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """鼠标移动事件处理"""
        # 更新光标形状
        self.update_cursor(event.position().toPoint())

        if self.drawing and self.is_captured:
            # 绘图模式下，更新结束点
            self.draw_end = event.pos()
            self.update()
            return

        if self.resizing and self.screenshot_rect:
            # 调整区域大小
            pos = event.position().toPoint()
            dx = pos.x() - self.resize_start_point.x()
            dy = pos.y() - self.resize_start_point.y()

            new_rect = QRect(self.resize_start_rect)

            if self.resize_handle == 'move':
                # 移动整个区域
                new_rect.translate(dx, dy)
            elif self.resize_handle == 'top_left':
                new_rect.setTopLeft(self.resize_start_rect.topLeft() + QPoint(dx, dy))
            elif self.resize_handle == 'top_right':
                new_rect.setTopRight(self.resize_start_rect.topRight() + QPoint(dx, dy))
            elif self.resize_handle == 'bottom_left':
                new_rect.setBottomLeft(self.resize_start_rect.bottomLeft() + QPoint(dx, dy))
            elif self.resize_handle == 'bottom_right':
                new_rect.setBottomRight(self.resize_start_rect.bottomRight() + QPoint(dx, dy))
            elif self.resize_handle == 'top':
                new_rect.setTop(self.resize_start_rect.top() + dy)
            elif self.resize_handle == 'bottom':
                new_rect.setBottom(self.resize_start_rect.bottom() + dy)
            elif self.resize_handle == 'left':
                new_rect.setLeft(self.resize_start_rect.left() + dx)
            elif self.resize_handle == 'right':
                new_rect.setRight(self.resize_start_rect.right() + dx)

            # 确保矩形有效（宽度和高度为正）
            if new_rect.width() > 10 and new_rect.height() > 10:
                self.screenshot_rect = new_rect.normalized()

                # 更新截图内容
                if self.screen_count > 1:
                    self.captured_pixmap = self.fullscreen_pixmap.copy(self.screenshot_rect)
                else:
                    dpr_rect = QRect(
                        self.screenshot_rect.topLeft() * self.dpr,
                        self.screenshot_rect.size() * self.dpr
                    )
                    self.captured_pixmap = self.fullscreen_pixmap.copy(dpr_rect)

                # 重新定位工具栏
                self.position_toolbar(self.screenshot_rect)

                self.update()
            return

        if self.moving and self.screenshot_rect:
            # 移动截图区域
            pos = event.position().toPoint()
            dx = pos.x() - self.move_start_point.x()
            dy = pos.y() - self.move_start_point.y()

            new_rect = QRect(self.move_start_rect)
            new_rect.translate(dx, dy)

            # 确保矩形在屏幕范围内
            screen_geometry = self.rect()
            if (new_rect.left() >= 0 and new_rect.right() <= screen_geometry.width() and
                    new_rect.top() >= 0 and new_rect.bottom() <= screen_geometry.height()):
                self.screenshot_rect = new_rect

                # 重新定位工具栏
                self.position_toolbar(self.screenshot_rect)

                self.update()
            return

        if self.dragging:
            # 使用原始坐标
            self.end_point = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event):
        """鼠标释放事件处理"""
        if self.drawing and self.is_captured:
            # 绘图模式下，完成图形绘制
            if event.button() == Qt.MouseButton.LeftButton:
                # 确保释放点在截图区域内
                if self.screenshot_rect.contains(event.pos()):
                    self.draw_end = event.pos()

                    # 保存图形前先添加历史记录
                    self.add_to_history()

                    # 保存图形
                    if self.current_tool == "rectangle":
                        rect = QRect(self.draw_start, self.draw_end).normalized()
                        # 确保矩形在截图区域内
                        rect = rect.intersected(self.screenshot_rect)
                        if rect.width() > 5 and rect.height() > 5:  # 避免太小的矩形
                            shape = Rectangle(rect, self.current_pen)
                            self.shapes.append(shape)

                    elif self.current_tool == "ellipse":
                        rect = QRect(self.draw_start, self.draw_end).normalized()
                        # 确保椭圆在截图区域内
                        rect = rect.intersected(self.screenshot_rect)
                        if rect.width() > 5 and rect.height() > 5:  # 避免太小的椭圆
                            shape = Ellipse(rect, self.current_pen)
                            self.shapes.append(shape)

                    elif self.current_tool == "line":
                        # 确保线段在截图区域内
                        if self.screenshot_rect.contains(self.draw_start) and self.screenshot_rect.contains(
                                self.draw_end):
                            # 计算线段长度
                            length = math.sqrt((self.draw_end.x() - self.draw_start.x()) ** 2 +
                                               (self.draw_end.y() - self.draw_start.y()) ** 2)
                            if length > 5:  # 避免太短的线段
                                shape = Line(self.draw_start, self.draw_end, self.current_pen)
                                self.shapes.append(shape)

                    elif self.current_tool == "arrow":
                        # 确保箭头在截图区域内
                        if self.screenshot_rect.contains(self.draw_start) and self.screenshot_rect.contains(
                                self.draw_end):
                            # 计算箭头长度
                            length = math.sqrt((self.draw_end.x() - self.draw_start.x()) ** 2 +
                                               (self.draw_end.y() - self.draw_start.y()) ** 2)
                            if length > 5:  # 避免太短的箭头
                                shape = Arrow(self.draw_start, self.draw_end, self.current_pen)
                                self.shapes.append(shape)

                    # 重置绘图状态，但保持绘图模式激活
                    self.draw_start = QPoint()
                    self.draw_end = QPoint()
                    self.drawing = False
                self.update()
            return

        if self.resizing:
            # 结束调整
            self.resizing = False
            self.resize_handle = None
            self.resize_start_rect = None
            self.resize_start_point = None
            self.update()  # 添加这行，确保调整结束后重绘把手
            return

        if self.moving:
            # 结束移动
            self.moving = False
            self.move_start_point = None
            self.move_start_rect = None
            self.update()
            return

        if self.is_captured:
            return

        if self.screen_count > 1:
            self.more_screen_mouse_release_event(event)
        else:
            self.one_screen_mouse_release_event(event)

    def more_screen_mouse_release_event(self, event):
        """鼠标释放事件处理"""
        if event.button() == Qt.MouseButton.LeftButton and self.dragging:
            # 使用原始坐标
            self.end_point = event.position().toPoint()
            self.dragging = False

            # 获取选区矩形
            rect = QRect(self.start_point, self.end_point).normalized()

            # 确保选区有效
            if rect.width() > 10 and rect.height() > 10:
                self.captured_pixmap = self.fullscreen_pixmap.copy(rect)
                self.screenshot_rect = rect
                self.show_toolbar(rect)
            else:
                self.close_trigger()

    def one_screen_mouse_release_event(self, event):
        """鼠标释放事件处理"""
        if event.button() == Qt.MouseButton.LeftButton and self.dragging:
            # 使用原始坐标
            self.end_point = event.position().toPoint()
            self.dragging = False

            # 获取选区矩形
            rect = QRect(self.start_point, self.end_point).normalized()

            # 确保选区有效
            if rect.width() > 10 and rect.height() > 10:
                # 考虑设备像素比调整选区
                dpr_rect = QRect(
                    rect.topLeft() * self.dpr,
                    rect.size() * self.dpr
                )

                # 从全屏截图中裁剪选区
                self.captured_pixmap = self.fullscreen_pixmap.copy(dpr_rect)
                self.screenshot_rect = rect
                self.show_toolbar(rect)
            else:
                self.close_trigger()

        # 右键完成截图
        elif event.button() == Qt.MouseButton.RightButton and self.dragging:
            self.end_point = event.position().toPoint()
            self.dragging = False

            rect = QRect(self.start_point, self.end_point).normalized()
            if rect.width() > 10 and rect.height() > 10:
                dpr_rect = QRect(
                    rect.topLeft() * self.dpr,
                    rect.size() * self.dpr
                )
                self.captured_pixmap = self.fullscreen_pixmap.copy(dpr_rect)
                self.screenshot_rect = rect
                self.show_toolbar(rect)

    def show_toolbar(self, rect):
        """显示工具栏"""
        self.is_captured = True
        self.tip_label.hide()
        self.size_label.hide()

        # 清空历史记录
        self.undo_stack = []
        self.redo_stack = []
        self.undo_btn.setEnabled(False)
        self.redo_btn.setEnabled(False)

        # 定位工具栏
        self.position_toolbar(rect)
        self.toolbar.show()
        self.update()

    def position_toolbar(self, rect):
        if self.screen_count > 1:
            screen_geometry = QGuiApplication.primaryScreen().virtualGeometry()
        else:
            screen_geometry = QGuiApplication.primaryScreen().geometry()

        # 计算工具栏位置
        x = rect.x()
        y = rect.bottom() + 10

        # 如果下方空间不足，则显示在区域上方
        if y + self.toolbar.height() > screen_geometry.bottom():
            y = rect.top() - self.toolbar.height() - 10
        # 如果右边空间不足，则显示在区域左边
        if x + self.toolbar.width() > screen_geometry.right():
            x = rect.left() - self.toolbar.width() - 10

        if self.screen_count > 1:
            x = max(screen_geometry.left(), min(x, screen_geometry.right() - self.toolbar.width()))
            y = max(screen_geometry.top(), min(y, screen_geometry.bottom() - self.toolbar.height()))
        else:
            x = max(0, min(x, screen_geometry.width() - self.toolbar.width()))
            y = max(0, min(y, screen_geometry.height() - self.toolbar.height()))

        # 移动主工具栏
        self.toolbar.move(x, y)
        # 如果绘图子工具栏正在显示，也移动它
        if self.draw_toolbar.isVisible():
            self.draw_toolbar.move(x, y + self.toolbar.height() + 5)

    def save_screenshot(self):
        """保存截图到文件"""
        try:
            # 创建一个临时副本，用于绘制图形
            temp_pixmap = self.captured_pixmap.copy()
            painter = QPainter(temp_pixmap)

            # 将所有图形绘制到截图上
            for shape in self.shapes:
                # 将屏幕坐标转换为截图内的相对坐标
                if shape.type == "rectangle":
                    relative_rect = QRect(
                        shape.rect.x() - self.screenshot_rect.x(),
                        shape.rect.y() - self.screenshot_rect.y(),
                        shape.rect.width(),
                        shape.rect.height()
                    )
                    painter.setPen(shape.pen)
                    painter.drawRect(relative_rect)
                elif shape.type == "ellipse":
                    relative_rect = QRect(
                        shape.rect.x() - self.screenshot_rect.x(),
                        shape.rect.y() - self.screenshot_rect.y(),
                        shape.rect.width(),
                        shape.rect.height()
                    )
                    painter.setPen(shape.pen)
                    painter.drawEllipse(relative_rect)
                elif shape.type == "line":
                    relative_start = QPoint(
                        shape.start_point.x() - self.screenshot_rect.x(),
                        shape.start_point.y() - self.screenshot_rect.y()
                    )
                    relative_end = QPoint(
                        shape.end_point.x() - self.screenshot_rect.x(),
                        shape.end_point.y() - self.screenshot_rect.y()
                    )
                    painter.setPen(shape.pen)
                    painter.drawLine(relative_start, relative_end)
                elif shape.type == "arrow":
                    relative_start = QPoint(
                        shape.start_point.x() - self.screenshot_rect.x(),
                        shape.start_point.y() - self.screenshot_rect.y()
                    )
                    relative_end = QPoint(
                        shape.end_point.x() - self.screenshot_rect.x(),
                        shape.end_point.y() - self.screenshot_rect.y()
                    )
                    painter.setPen(shape.pen)
                    self.draw_arrow(painter, relative_start, relative_end, shape.pen)

            painter.end()

            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "保存截图",
                "屏幕截图.png",
                "PNG 图片 (*.png);;JPEG 图片 (*.jpg *.jpeg)"
            )
            if file_path:
                temp_pixmap.save(file_path)
        except Exception:
            pass
        self.close_trigger("")

    def translate_screenshot(self):
        """翻译截图"""
        self.main_object.screenshot_captured_to_translate(self.captured_pixmap)
        self.close_trigger("")

    def ocr_screenshot(self):
        """识别截图"""
        self.main_object.screenshot_captured_to_ocr(self.captured_pixmap)
        self.close_trigger("")

    def ocr_to_excel_screenshot(self):
        """截图转excel"""
        self.main_object.start_single_image_to_excel_converter(self.captured_pixmap)
        self.close_trigger("")

    def see_screenshot(self):
        """查看截图"""
        self.main_object.start_image_show(self.get_end_captured_pixmap())
        self.close_trigger("")

    def see_top_screenshot(self):
        """查看置顶"""
        self.main_object.start_top_image_show(self.get_end_captured_pixmap())
        self.close_trigger("")

    def copy_screenshot(self):
        """复制截图到剪贴板"""
        # 获取绘制后的截图
        temp_pixmap = self.get_end_captured_pixmap()
        # 将图片复制到剪贴板
        QApplication.clipboard().setPixmap(temp_pixmap)
        self.close_trigger("")

    def get_end_captured_pixmap(self):
        # 创建一个临时副本，用于绘制图形
        temp_pixmap = self.captured_pixmap.copy()
        painter = QPainter(temp_pixmap)
        # 将所有图形绘制到截图上
        for shape in self.shapes:
            # 将屏幕坐标转换为截图内的相对坐标
            if shape.type == "rectangle":
                relative_rect = QRect(
                    shape.rect.x() - self.screenshot_rect.x(),
                    shape.rect.y() - self.screenshot_rect.y(),
                    shape.rect.width(),
                    shape.rect.height()
                )
                painter.setPen(shape.pen)
                painter.drawRect(relative_rect)
            elif shape.type == "ellipse":
                relative_rect = QRect(
                    shape.rect.x() - self.screenshot_rect.x(),
                    shape.rect.y() - self.screenshot_rect.y(),
                    shape.rect.width(),
                    shape.rect.height()
                )
                painter.setPen(shape.pen)
                painter.drawEllipse(relative_rect)
            elif shape.type == "line":
                relative_start = QPoint(
                    shape.start_point.x() - self.screenshot_rect.x(),
                    shape.start_point.y() - self.screenshot_rect.y()
                )
                relative_end = QPoint(
                    shape.end_point.x() - self.screenshot_rect.x(),
                    shape.end_point.y() - self.screenshot_rect.y()
                )
                painter.setPen(shape.pen)
                painter.drawLine(relative_start, relative_end)
            elif shape.type == "arrow":
                relative_start = QPoint(
                    shape.start_point.x() - self.screenshot_rect.x(),
                    shape.start_point.y() - self.screenshot_rect.y()
                )
                relative_end = QPoint(
                    shape.end_point.x() - self.screenshot_rect.x(),
                    shape.end_point.y() - self.screenshot_rect.y()
                )
                painter.setPen(shape.pen)
                self.draw_arrow(painter, relative_start, relative_end, shape.pen)

        painter.end()
        return temp_pixmap

    def close_screenshot(self):
        """关闭"""
        self.close_trigger("")

    def close_trigger(self, text=None):
        try:
            self.main_object.cancel_screenshot()
        except Exception:
            pass
        try:
            self.close()
        except Exception:
            pass

    def keyPressEvent(self, event):
        """键盘事件处理"""
        if event.key() == Qt.Key.Key_Escape:
            if self.current_tool:
                # 退出绘图模式
                if self.current_tool == "rectangle":
                    self.rect_btn.setChecked(False)
                elif self.current_tool == "ellipse":
                    self.ellipse_btn.setChecked(False)
                elif self.current_tool == "line":
                    self.line_btn.setChecked(False)
                elif self.current_tool == "arrow":
                    self.arrow_btn.setChecked(False)

                self.current_tool = None
                self.drawing = False
                self.setCursor(Qt.CursorShape.ArrowCursor)
                # 隐藏绘图工具栏
                self.draw_toolbar.hide()
                self.update()
            else:
                self.close_trigger()
        elif event.key() == Qt.Key.Key_Z and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            # Ctrl+Z 撤销
            self.undo()
        elif event.key() == Qt.Key.Key_Y and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            # Ctrl+Y 重做
            self.redo()