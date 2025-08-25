from PySide6.QtWidgets import (QWidget, QLabel, QLineEdit,
                               QPushButton, QVBoxLayout, QTextEdit, QFileDialog,
                               QScrollArea, QHBoxLayout)
from PySide6.QtGui import QPixmap, QPainter, QFont, QFontMetrics, QImage, QColor
from PySide6.QtCore import Qt, QDate, QSize
from src.ui import style_util


class HoldGrudgesGenPopup(QWidget):
    def __init__(self, parent=None, main_object=None, is_dark=None):
        super().__init__(parent=parent)
        # 初始化
        self.parent = parent
        self.use_parent = main_object
        self.setStyleSheet("background: transparent; border: none; padding: 0px;")
        # 初始化界面
        self.init_ui()
        # 设置样式
        style_util.set_dialog_control_style(self, is_dark)

    def init_ui(self):
        # 主部件和布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(3)

        # 输入时间
        time_layout = QHBoxLayout(self)
        time_layout.setSpacing(5)
        time_label = QLabel("输入时间：")
        time_label.setStyleSheet("background: transparent;")
        time_layout.addWidget(time_label)

        self.time_input = QLineEdit()
        today = QDate.currentDate().toString("yyyy年M月d日")
        self.time_input.setText(today + "，")
        time_layout.addWidget(self.time_input)
        main_layout.addLayout(time_layout)

        # 输入天气
        weather_layout = QHBoxLayout(self)
        weather_layout.setSpacing(5)
        weather_label = QLabel("输入天气：")
        weather_label.setStyleSheet("background: transparent;")
        weather_layout.addWidget(weather_label)

        self.weather_input = QLineEdit()
        self.weather_input.setText("晴天，")
        weather_layout.addWidget(self.weather_input)
        main_layout.addLayout(weather_layout)

        # 输入内容
        content_label = QLabel("输入内容：")
        content_label.setStyleSheet("background: transparent;")
        main_layout.addWidget(content_label)

        self.content_input = QTextEdit()
        self.content_input.setText("群主拒绝了女装，")
        self.content_input.setMaximumHeight(80)
        main_layout.addWidget(self.content_input)

        # 结束语
        end_layout = QHBoxLayout(self)
        end_layout.setSpacing(5)
        end_label = QLabel("输入结束语：")
        end_label.setStyleSheet("background: transparent;")
        end_layout.addWidget(end_label)

        self.end_input = QLineEdit()
        self.end_input.setText("这个仇，我先记下了")
        end_layout.addWidget(self.end_input)
        main_layout.addLayout(end_layout)

        # 生成按钮
        button_layout = QHBoxLayout(self)
        button_layout.setSpacing(5)
        generate_button = QPushButton("生成图片")
        generate_button.clicked.connect(self.generate_image)
        generate_button.setMinimumSize(QSize(80, 30))
        button_layout.addWidget(generate_button)

        # 保存按钮
        save_button = QPushButton("保存图片")
        save_button.clicked.connect(self.save_image)
        save_button.setMinimumSize(QSize(80, 30))
        button_layout.addWidget(save_button)
        main_layout.addLayout(button_layout)

        # 创建滚动区域用于显示图片
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumHeight(300)
        main_layout.addWidget(scroll_area)

        # 图片显示容器
        image_container = QWidget()
        scroll_area.setWidget(image_container)
        container_layout = QVBoxLayout(image_container)

        # 图片显示标签
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(300, 300)
        self.image_label.setStyleSheet("background-color: #f0f0f0; border: none;")
        container_layout.addWidget(self.image_label, 0, Qt.AlignCenter)

        # 加载顶部图片
        self.top_image = QPixmap("./static/img/card/ToolCard/HoldGrudges/HoldGrudges.jpg")
        if self.top_image.isNull():
            print("警告：无法加载HoldGrudges.jpg图片！")
            # 创建默认图片
            self.top_image = QPixmap(264, 254)
            self.top_image.fill(QColor("#e0e0e0"))
            painter = QPainter(self.top_image)
            painter.setFont(QFont("", 16))
            painter.drawText(self.top_image.rect(), Qt.AlignCenter, "记仇图片")
            painter.end()

        # 初始图片
        self.original_image = None
        self.generate_image()

    def generate_image(self):
        """生成记仇图片，高度根据内容自动调整"""
        # 获取输入内容
        date = self.time_input.text() or ""
        weather = self.weather_input.text() or ""
        content = self.content_input.toPlainText() or ""
        end = self.end_input.text() or ""

        # 组合文本
        text = f"{date}{weather}{content}{end}"

        # 设置图片宽度：比加载的图片稍宽
        width = self.top_image.width() + 50  # 264 + 50 = 314px
        margin = 20

        # 创建字体
        text_font = QFont("", 14)
        text_font.setBold(True)

        # 计算文本高度
        metrics = QFontMetrics(text_font)
        text_width = width - 2 * margin
        text_height = metrics.boundingRect(
            0, 0, text_width, 0,
            Qt.TextWordWrap | Qt.AlignCenter,
            text
        ).height()

        # 计算总高度：顶部图片高度 + 文本高度 + 边距
        top_image_height = self.top_image.height()
        height = top_image_height + text_height + 80  # 添加边距

        # 创建图片
        image = QImage(width, height, QImage.Format_ARGB32)
        image.fill(Qt.white)

        # 绘制
        painter = QPainter(image)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制顶部图片（居中）
        top_image_x = (width - self.top_image.width()) // 2
        painter.drawPixmap(top_image_x, 10, self.top_image)

        # 绘制文本内容
        painter.setFont(text_font)
        painter.setPen(Qt.black)

        # 计算文本位置（在图片下方）
        text_rect = painter.boundingRect(
            margin, top_image_height + 30,
                    width - 2 * margin, text_height,
                    Qt.TextWordWrap | Qt.AlignCenter,
            text
        )
        painter.drawText(text_rect, Qt.TextWordWrap | Qt.AlignCenter, text)

        painter.end()

        # 保存原始图片用于保存
        self.original_image = QPixmap.fromImage(image)

        # 创建预览图片（缩小显示）
        preview_width = 300  # 固定预览宽度
        preview_height = int(height * (preview_width / width))
        preview_pixmap = self.original_image.scaled(
            preview_width, preview_height,
            Qt.KeepAspectRatio, Qt.SmoothTransformation
        )

        # 显示预览图片
        self.image_label.setPixmap(preview_pixmap)

    def save_image(self):
        """保存生成的图片"""
        if self.original_image is None:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存图片", "记仇图片.png", "PNG图像 (*.png);;所有文件 (*)"
        )

        if file_path:
            if not file_path.endswith(".png"):
                file_path += ".png"
            self.original_image.save(file_path, "PNG")

    def refresh_theme(self, main_object):
        # 设置样式
        style_util.set_dialog_control_style(self, main_object.is_dark)
