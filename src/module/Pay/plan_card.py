from PySide6.QtGui import Qt, QFont
from PySide6.QtWidgets import QVBoxLayout, QLabel, QFrame, QSizePolicy


class PlanCard(QFrame):
    """自定义订阅计划卡片"""

    def __init__(self, title, base_price, discount_price, plan_code, is_dark=False, parent=None):
        super().__init__(parent)
        self.setObjectName("planCard")
        self.is_dark = is_dark
        self.plan_code = plan_code
        self.setup_ui(title, base_price, discount_price)

    def setup_ui(self, title, base_price, discount_price):
        # 设置卡片样式
        self.setMinimumSize(120, 150)
        self.setMaximumSize(180, 200)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        # 根据主题设置样式
        if self.is_dark:
            self.setStyleSheet("""
                QFrame#planCard {
                    background-color: #2a2a2a;
                    border-radius: 10px;
                    border: 1px solid #444;
                }
                QFrame#planCard:hover {
                    background-color: #3a3a3a;
                    border: 1px solid #666;
                }
                QFrame#planCard[selected="true"] {
                    background-color: #3a3a3a;
                    border: 2px solid #4d90fe;
                }
                QLabel {
                    color: #ddd;
                }
            """)
        else:
            self.setStyleSheet("""
                QFrame#planCard {
                    background-color: #f8f9fa;
                    border-radius: 10px;
                    border: 1px solid #ddd;
                }
                QFrame#planCard:hover {
                    background-color: #e9ecef;
                    border: 1px solid #ccc;
                }
                QFrame#planCard[selected="true"] {
                    background-color: #e9ecef;
                    border: 2px solid #4d90fe;
                }
                QLabel {
                    color: #333;
                }
            """)

        # 卡片布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # 标题
        title_label = QLabel(title)
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("background: transparent;")

        # 价格
        price_layout = QVBoxLayout()
        price_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        price_layout.setSpacing(2)

        # 如果有折扣价，显示原价和折扣价
        if discount_price != base_price:
            # 显示划掉的原价
            original_price_label = QLabel(f"<s>¥{int(base_price)}</s>")  # 显示整数，想显示小数用QLabel(f"¥{base_price:.2f}")
            original_price_font = QFont()
            original_price_font.setPointSize(12)
            original_price_label.setFont(original_price_font)
            original_price_label.setStyleSheet("color: #999;" if not self.is_dark else "color: #777;")
            original_price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            original_price_label.setStyleSheet("background: transparent;")
            price_layout.addWidget(original_price_label)

            # 显示折扣价
            discount_price_label = QLabel(f"¥{int(discount_price)}")   # 显示整数，想显示小数用QLabel(f"¥{discount_price:.2f}")
            discount_price_font = QFont()
            discount_price_font.setPointSize(18)
            discount_price_font.setBold(True)
            discount_price_label.setFont(discount_price_font)
            discount_price_label.setStyleSheet("color: #e74c3c;" if not self.is_dark else "color: #ef9a9a;")
            discount_price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            discount_price_label.setStyleSheet("background: transparent;")
            price_layout.addWidget(discount_price_label)
        else:
            # 没有折扣，只显示一个价格
            price_label = QLabel(f"¥{int(base_price)}")  # 显示整数，想显示小数用QLabel(f"¥{base_price:.2f}")
            price_font = QFont()
            price_font.setPointSize(18)
            price_font.setBold(True)
            price_label.setFont(price_font)
            price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            price_label.setStyleSheet("background: transparent;")
            price_layout.addWidget(price_label)

        # 添加到布局
        layout.addStretch(1)
        layout.addWidget(title_label)
        layout.addLayout(price_layout)
        layout.addStretch(1)

        # 点击事件
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def set_selected(self, selected):
        """设置选中状态"""
        self.setProperty("selected", selected)
        self.style().unpolish(self)
        self.style().polish(self)