from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QApplication, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap


class TutorialWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.steps = []
        self.current_step = 0
        self.init_ui()
        self.init_styles()

    def init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 主内容容器
        self.main_widget = QWidget(self)
        self.main_widget.setObjectName("mainWidget")

        # 错误信息显示
        self.error_label = QLabel("图片加载失败\n请检查文件路径", self.main_widget)
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setWordWrap(True)
        self.error_label.hide()

        # 图片显示
        self.image_label = QLabel(self.main_widget)
        self.image_label.setAlignment(Qt.AlignCenter)

        # 按钮布局
        self.close_btn = QPushButton("×", self.main_widget)
        self.prev_btn = QPushButton("← 上一步", self.main_widget)
        self.next_btn = QPushButton("下一步 →", self.main_widget)
        self.final_btn = QPushButton("开始使用", self.main_widget)
        self.final_btn.hide()

        # 布局设置
        v_layout = QVBoxLayout(self.main_widget)
        v_layout.addWidget(self.image_label)
        v_layout.addWidget(self.error_label)

        # 底部按钮布局
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.prev_btn, 0, Qt.AlignLeft)
        btn_layout.addStretch()
        btn_layout.addWidget(self.final_btn, 0, Qt.AlignCenter)
        btn_layout.addStretch()
        btn_layout.addWidget(self.next_btn, 0, Qt.AlignRight)
        v_layout.addLayout(btn_layout)

        # 信号连接
        self.close_btn.clicked.connect(self.close)
        self.prev_btn.clicked.connect(self.prev_step)
        self.next_btn.clicked.connect(self.next_step)
        self.final_btn.clicked.connect(self.close)

    def init_styles(self):
        style = """
        #mainWidget {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop:0 #a1c4fd,stop:1 #c2e9fb);
            border-radius: 15px;
            padding: 20px;
        }
        QLabel#error_label {
            font-size: 24px;
            color: #666666;
            margin: 50px;
        }
        QPushButton {
            min-width: 120px;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 8px;
            border: 1px solid #cccccc;
            background-color: #f8f9fa;
        }
        QPushButton:hover {
            background-color: #e9ecef;
        }
        QPushButton:disabled {
            color: #999999;
            background-color: #f8f9fa;
        }
        #close_btn {
            min-width: 40px;
            max-width: 40px;
            border-radius: 20px;
            font-size: 20px;
        }
        #final_btn {
            background-color: #007bff;
            color: white;
            min-width: 160px;
        }
        """
        self.setStyleSheet(style)
        self.error_label.setObjectName("error_label")
        self.close_btn.setObjectName("close_btn")
        self.final_btn.setObjectName("final_btn")

    def resizeEvent(self, event):
        # 主容器居中显示
        container_size = QSize(800, 600)
        if self.width() < 850 or self.height() < 650:
            container_size = QSize(600, 450)

        self.main_widget.setFixedSize(container_size)
        self.main_widget.move(
            (self.width() - container_size.width()) // 2,
            (self.height() - container_size.height()) // 2
        )
        self.close_btn.move(
            self.main_widget.x() + container_size.width() - 50,
            self.main_widget.y() + 10
        )

    def add_step(self, image_path):
        self.steps.append(image_path)

    def start(self):
        if self.steps:
            self.showFullScreen()
            self.update_step()

    def update_step(self):
        # 重置显示状态
        self.error_label.hide()
        self.image_label.show()
        self.image_label.setScaledContents(True)

        # 尝试加载图片
        pixmap = QPixmap(self.steps[self.current_step])
        if pixmap.isNull():
            self.handle_image_error()
        else:
            self.image_label.setPixmap(pixmap)

        # 更新按钮状态
        is_last_step = self.current_step == len(self.steps) - 1
        self.prev_btn.setDisabled(self.current_step == 0)
        self.next_btn.setDisabled(is_last_step)
        self.final_btn.setVisible(is_last_step)

    def handle_image_error(self):
        self.image_label.hide()
        self.error_label.show()
        self.error_label.setText(
            f"无法加载第 {self.current_step + 1} 步引导图片\n"
            f"文件路径: {self.steps[self.current_step]}"
        )

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.update_step()

    def next_step(self):
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.update_step()
