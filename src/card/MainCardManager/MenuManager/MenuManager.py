import time

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QFont, QEnterEvent
from PySide6.QtWidgets import QLabel, QPushButton, QHBoxLayout

from src.card.card_component.ThemeSwitchButton.ThemeSwitchButton import ThemeSwitchButton
from src.constant import card_constant

# 菜单常量
MENU_DEFAULT_WIDTH = 38     # 菜单默认宽度
MENU_SPREAD_WIDTH = 100     # 菜单展开宽度
MENU_MARGIN_WIDTH = 4       # 菜单按钮外间距
MENU_PADDING_WIDTH = 4      # 菜单按钮内间距
MENU_BUTTON_HEIGHT = 34     # 菜单按钮高度
MENU_BUTTON_ICON_SIZE = 22  # 菜单按钮图标大小



class MenuCard(QLabel):

    animation_run_time = 0  # 动画执行时间
    last_animation_time = 0   # 上次动画执行时间
    is_dark = None
    dark_style_sheet = "border-radius: 15px; border: 1px solid #2C2E39; background-color: rgba(34, 34, 34, 254);"
    light_min_style_sheet = "border-radius: 15px; border: 1px solid rgba(255, 255, 255, 170); background-color: rgba(255, 255, 255, 160);"
    light_max_style_sheet = "border-radius: 15px; border: 1px solid rgba(255, 255, 255, 170); background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgb(220, 245, 255), stop:1 rgb(250, 215, 254));"

    def __init__(self, parent, main_object, is_dark):
        super(MenuCard, self).__init__(parent)
        self.main_object = main_object
        self.is_dark = is_dark

    def enterEvent(self, event: QEnterEvent):
        """重写鼠标进入事件"""
        self.show_menu()
        super().enterEvent(event)

    def show_menu(self):
        self.last_animation_time = int(time.time() * 1000)
        if not self.is_dark:
            print(f"切换到浅色模式,current_status:{self.get_current_status()}")
            self.setStyleSheet(self.light_max_style_sheet if self.get_current_status() else self.light_min_style_sheet)
        self.main_object.main_card_manager.change_menu_label_width(enter=True)

    def leaveEvent(self, event: QEnterEvent):
        """重写鼠标离开事件"""
        self.hide_menu()
        super().leaveEvent(event)

    def hide_menu(self):
        self.last_animation_time = int(time.time() * 1000)
        if not self.is_dark:
            print(f"切换到浅色模式,current_status:{self.get_current_status()}")
            self.setStyleSheet(self.light_max_style_sheet if self.get_current_status() else self.light_min_style_sheet)
        self.main_object.main_card_manager.change_menu_label_width(enter=False)

    def set_theme(self, is_dark: bool):
        self.is_dark = is_dark
        if self.is_dark:
            self.setStyleSheet(self.dark_style_sheet)
        else:
            print(f"切换到浅色模式,current_status:{self.get_current_status()}")
            self.setStyleSheet(self.light_min_style_sheet if self.get_current_status() else self.light_max_style_sheet)

    def get_current_status(self):
        return self.width() == MENU_DEFAULT_WIDTH


class MenuNormalButton(QPushButton):

    menu_button_width = MENU_SPREAD_WIDTH - MENU_MARGIN_WIDTH * 2     # 菜单按钮宽度
    menu_button_height = 34     # 菜单按钮高度
    menu_button_icon_size = 22  # 菜单按钮图标大小
    menu_layout = None          # 菜单布局
    menu_icon = None            # 菜单按钮图标
    menu_text = None            # 菜单按钮文字
    current_menu_location = None

    def __init__(self, parent, main_object, name, title, menu_location, is_dark):
        super(MenuNormalButton, self).__init__(parent)
        self.main_object = main_object
        self.is_dark = is_dark
        self.current_menu_location = menu_location
        setattr(self.main_object, f'push_button_{name}', self)
        self.init_ui(name, title)

    def init_ui(self, name, title):
        # 设置按钮属性
        self.setFixedSize(self.menu_button_width, self.menu_button_height)
        self.setObjectName(f'push_button_{name}')
        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setKerning(True)
        # 创建图标
        self.menu_icon = QLabel()
        self.menu_icon.setStyleSheet("background-color: transparent; border: none;")
        self.menu_icon.setFont(font)
        self.menu_icon.setFixedSize(QSize(self.menu_button_icon_size, self.menu_button_icon_size))
        # 创建文字
        self.menu_text = QLabel()
        self.menu_text.setStyleSheet("background-color: transparent; border: none;")
        self.menu_text.setFont(font)
        self.menu_text.setText(title)
        self.menu_text.setFixedSize(QSize(50, self.menu_button_icon_size))
        # 创建布局
        self.menu_layout = QHBoxLayout()
        self.menu_layout.setContentsMargins(MENU_PADDING_WIDTH, 0, MENU_PADDING_WIDTH, 0)
        self.menu_layout.setSpacing(0)
        # 根据菜单位置进行布局
        if self.current_menu_location == card_constant.MENU_POSITION_RIGHT:
            self.menu_layout.addWidget(self.menu_text)
            self.menu_layout.addStretch()
            self.menu_layout.addWidget(self.menu_icon)
            # 文字排列从右
            self.menu_text.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        else:
            self.menu_layout.addWidget(self.menu_icon)
            self.menu_layout.addStretch()
            self.menu_layout.addWidget(self.menu_text)
            # 文字排列从左
            self.menu_text.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        # 设置布局
        self.setLayout(self.menu_layout)

    def refresh_ui(self, menu_location):
        if self.current_menu_location == menu_location:
            return
        self.current_menu_location = menu_location
        # 先移除所有控件和伸缩条
        while self.menu_layout.count():
            item = self.menu_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
        # 按新顺序重新添加
        if self.current_menu_location == card_constant.MENU_POSITION_RIGHT:
            self.menu_layout.addWidget(self.menu_text)
            self.menu_layout.addStretch()
            self.menu_layout.addWidget(self.menu_icon)
            # 文字排列从右
            self.menu_text.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        else:
            self.menu_layout.addWidget(self.menu_icon)
            self.menu_layout.addStretch()
            self.menu_layout.addWidget(self.menu_text)
            # 文字排列从左
            self.menu_text.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

    def setIcon(self, icon: QIcon):
        self.menu_icon.setPixmap(icon.pixmap(self.menu_button_icon_size, self.menu_button_icon_size))


class MenuThemeButton(QPushButton):

    menu_button_width = MENU_SPREAD_WIDTH - MENU_MARGIN_WIDTH * 2     # 菜单按钮宽度
    menu_button_height = 52     # 菜单按钮高度
    menu_layout = None          # 菜单布局
    menu_switch = None          # 菜单按钮图标
    menu_text = None            # 菜单按钮文字

    def __init__(self, parent, main_object, menu_location, is_dark):
        super(MenuThemeButton, self).__init__(parent)
        self.main_object = main_object
        self.is_dark = is_dark
        self.current_menu_location = menu_location
        setattr(self.main_object, f'theme_switch_button', self)
        self.init_ui()

    def init_ui(self):
        title = "主题切换"
        # 设置按钮属性
        self.setFixedSize(self.menu_button_width, self.menu_button_height)
        self.setObjectName(f'theme_switch_button')
        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setKerning(True)
        # 创建切换按钮
        self.menu_switch = ThemeSwitchButton(default_theme=not self.main_object.is_dark)
        self.menu_switch.setFixedSize(QSize(30, self.menu_button_height))
        self.menu_switch.resize(self.menu_switch.size())
        # self.menu_switch.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))  # 鼠标手形
        # 创建文字
        self.menu_text = QLabel()
        self.menu_text.setStyleSheet("background-color: transparent; border: none;")
        self.menu_text.setFont(font)
        self.menu_text.setText(title)
        self.menu_text.setFixedSize(QSize(50, self.menu_button_height))
        # 创建布局
        self.menu_layout = QHBoxLayout()
        self.menu_layout.setContentsMargins(0, 0, 0, 0)
        self.menu_layout.setSpacing(0)
        # 根据菜单位置进行布局
        if self.current_menu_location == card_constant.MENU_POSITION_RIGHT:
            self.menu_layout.addWidget(self.menu_text)
            self.menu_layout.addStretch()
            self.menu_layout.addWidget(self.menu_switch)
            # 文字排列从右
            self.menu_text.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        else:
            self.menu_layout.addWidget(self.menu_switch)
            self.menu_layout.addStretch()
            self.menu_layout.addWidget(self.menu_text)
            # 文字排列从左
            self.menu_text.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        # 设置布局
        self.setLayout(self.menu_layout)

    def refresh_ui(self, menu_location):
        if self.current_menu_location == menu_location:
            return
        self.current_menu_location = menu_location
        # 先移除所有控件和伸缩条
        while self.menu_layout.count():
            item = self.menu_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
        # 按新顺序重新添加
        if self.current_menu_location == card_constant.MENU_POSITION_RIGHT:
            self.menu_layout.addWidget(self.menu_text)
            self.menu_layout.addStretch()
            self.menu_layout.addWidget(self.menu_switch)
            # 文字排列从右
            self.menu_text.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        else:
            self.menu_layout.addWidget(self.menu_switch)
            self.menu_layout.addStretch()
            self.menu_layout.addWidget(self.menu_text)
            # 文字排列从左
            self.menu_text.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

    def setIcon(self, icon: QIcon):
        pass

    def mousePressEvent(self, event):
        self.menu_switch.mouse_press_event()
        super().mousePressEvent(event)
