from PySide6.QtCore import Qt, QByteArray, QSize
from PySide6.QtGui import QFont, QPixmap, QPainter, QIcon
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QComboBox, QPushButton, QCheckBox, QLineEdit, QSpinBox, QTextEdit, QRadioButton, \
    QFontComboBox, QFrame, QBoxLayout, QWidget, QDateEdit, QTabWidget, QTableWidget, QDoubleSpinBox, \
    QPlainTextEdit, QToolButton
from qframelesswindow import TitleBar
from qframelesswindow.titlebar import MinimizeButton, MaximizeButton, CloseButton

from src.card.main_card.ChatCard.chat_component.EnterTextEdit.EnterTextEdit import EnterTextEdit
from src.ui.svg_dict import svg_dict

'''
**********************************svg工具 · 开始***************************************
↓                                                                                 ↓
'''
def get_icon_by_path(icon_path: str, size=None, is_dark=False, custom_color=None):
    icon_type = icon_path.split("/")[0]
    icon_name = icon_path.split("/")[1]
    svg_data = svg_dict[icon_type][icon_name]
    return get_icon_by_svg(svg_data=svg_data, size=size, is_dark=is_dark, custom_color=custom_color)

def get_icon_by_svg(svg_data: str, size=None, is_dark=False, custom_color=None):
    """根据svg获取QIcon"""
    return QIcon(get_pixmap_by_svg(svg_data=svg_data, size=size, is_dark=is_dark, custom_color=custom_color))

def get_svg_by_path(icon_path: str, is_dark=False):
    icon_type = icon_path.split("/")[0]
    icon_name = icon_path.split("/")[1]
    svg_data = svg_dict[icon_type][icon_name]
    if is_dark:
        svg_data = svg_data.replace("black", "white")
    return svg_data

def get_pixmap_by_path(icon_path: str, size=None, is_dark=False, custom_color=None):
    icon_type = icon_path.split("/")[0]
    icon_name = icon_path.split("/")[1]
    svg_data = svg_dict[icon_type][icon_name]
    return get_pixmap_by_svg(svg_data=svg_data, size=size, is_dark=is_dark, custom_color=custom_color)

def get_pixmap_by_svg(svg_data: str, size=None, is_dark=False, custom_color=None):
    """根据svg获取QPixmap"""
    if custom_color is not None:
        svg_data = svg_data.replace("black", custom_color)
    else:
        if is_dark:
            svg_data = svg_data.replace("black", "white")
    renderer = QSvgRenderer(QByteArray(svg_data.encode()))
    if size is not None:
        pixmap_size = QSize(size, size)
    else:
        pixmap_size = renderer.defaultSize()
    pixmap = QPixmap(pixmap_size)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return pixmap
'''
↑                                                                                ↑
**********************************svg工具 · 结束***************************************
'''

'''
**********************************通用 · 开始***************************************
↓                                                                                 ↓
'''
transparent_style = "background: transparent; border: none;"

scroll_bar_style = """
/******** 滚动条  *********/
/* 垂直滚动条 */
QScrollBar:vertical {
    border-width: 0px;
    border: none;
    width: 10px;
    border-radius: 5px;
    background-color: transparent;
}
QScrollBar::handle:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop: 0 rgba(179, 179, 179, 125), stop: 0.5 rgba(179, 179, 179, 125), stop:1 rgba(179, 179, 179, 125));
    min-height: 20px;
    max-height: 20px;
    margin: 0px 0px 0px 0px;
    border-radius: 5px;
}
QScrollBar::add-line:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
    stop: 0 rgba(179, 179, 179, 0), stop: 0.5 rgba(179, 179, 179, 0),  stop:1 rgba(179, 179, 179, 0));
    height: 0px;
    border: none;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
    stop: 0  rgba(179, 179, 179, 0), stop: 0.5 rgba(179, 179, 179, 0),  stop:1 rgba(179, 179, 179, 0));
    height: 0 px;
    border: none;
    subcontrol-position: top;
    subcontrol-origin: margin;
}
QScrollBar::sub-page:vertical {
    background: rgba(179, 179, 179, 0);
}
QScrollBar::add-page:vertical {
    background: rgba(179, 179, 179, 0);
}

/* 水平滚动条 */
QScrollBar:horizontal {
    border-width: 0px;
    border: none;
    height: 10px;
    border-radius: 5px;
    background-color: transparent;
}
QScrollBar::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop: 0 rgba(179, 179, 179, 125), stop: 0.5 rgba(179, 179, 179, 125), stop:1 rgba(179, 179, 179, 125));
    min-width: 20px;
    max-width: 20px;
    margin: 0px 0px 0px 0px;
    border-radius: 5px;
}
QScrollBar::add-line:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
    stop: 0 rgba(179, 179, 179, 0), stop: 0.5 rgba(179, 179, 179, 0),  stop:1 rgba(179, 179, 179, 0));
    width: 0px;
    border: none;
    subcontrol-position: right;
    subcontrol-origin: margin;
}
QScrollBar::sub-line:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
    stop: 0  rgba(179, 179, 179, 0), stop: 0.5 rgba(179, 179, 179, 0),  stop:1 rgba(179, 179, 179, 0));
    width: 0px;
    border: none;
    subcontrol-position: left;
    subcontrol-origin: margin;
}
QScrollBar::sub-page:horizontal {
    background: rgba(179, 179, 179, 0);
}
QScrollBar::add-page:horizontal {
    background: rgba(179, 179, 179, 0);
}
"""

'''
↑                                                                                ↑
**********************************通用 · 结束***************************************
'''

'''
**********************************卡片 · 开始***************************************
↓                                                                                 ↓
'''
card_style = """
QScrollArea {
    border: 1px solid rgba(255, 255, 255, 170);
}
border-style: solid;
border-radius: 15px;
background-color:rgba(255, 255, 255, 100);
"""
card_dark_style = """
QScrollArea {
    border: 1px solid #2C2E39;
}
border-style: solid;
border-radius: 15px;
background-color:rgba(34, 34, 34, 255);
"""
'''
↑                                                                                ↑
**********************************卡片 · 结束***************************************
'''
'''
**********************************导航栏 · 开始***************************************
↓                                                                                 ↓
'''
header_button_style = """
QPushButton {
    border-radius: none;
    background-color: transparent;
}
QPushButton:hover {
    border-radius: 10px;
    border: 0px solid rgba(255, 255, 255, 170);
    background-color:rgba(255, 255, 255, 100);
}
"""
header_button_dark_style = """
QPushButton {
    border-radius: none;
    background-color: transparent;
}
QPushButton:hover {
    border:0px solid #2C2E39;
    border-radius: 10px;
    background-color:rgba(34, 34, 34, 255);
}
"""
'''
↑                                                                                ↑
**********************************导航栏 · 结束***************************************
'''
'''
**********************************菜单 · 开始***************************************
↓                                                                                 ↓
'''
menu_button_on = """QPushButton {
    border: none;
    background: transparent;
}
"""
menu_button_off = """QPushButton {
    border-radius: 10px;
    border: none;
    background-color: transparent;
}
QPushButton:hover {
    background-color: rgba(125, 125, 125, 0.2);
}
QPushButton:pressed {
    background-color: rgba(125, 125, 125, 0.4);
}
"""
def get_menu_button_style(state):
    if state:
        return menu_button_on
    else:
        return menu_button_off
'''
↑                                                                                ↑
**********************************菜单 · 结束***************************************
'''

'''
**********************************按钮 · 开始***************************************
↓                                                                                 ↓
'''
# 普通按钮
button_light_style = """
QPushButton {
    padding-left: 10px;
    padding-right: 10px;
    border-radius: 10px;
    border: 1px solid black;
    background-color: rgba(230, 231, 232, 200);
}
QPushButton:hover {
    background: rgba(0, 0, 0, 0.3);
    color: rgb(255, 255, 255);
    border: none;
}
QPushButton:disabled {
    background: rgba(125, 125, 125, 125);
    color: rgba(125, 125, 125, 125);
    border: none;
}"""
button_dark_style = """
QPushButton {
    padding-left: 10px;
    padding-right: 10px;
    border-radius: 10px;
    border: 1px solid white;
    background-color: rgba(20, 21, 22, 200);
}
QPushButton:hover {
    background: rgba(255, 255, 255, 0.3);
    color: rgb(0, 0, 0);
    border: none;
}
QPushButton:disabled {
    background: rgba(125, 125, 125, 125);
    color: rgba(125, 125, 125, 125);
    border: none;
}"""
box_button_style = """
QPushButton {
    padding-left: 10px;
    padding-right: 10px;
    padding-top: 5px;
    padding-bottom: 5px;
    border-radius: 10px;
    border: 1px solid black;
    color: rgb(0, 0, 0);
    background-color: rgb(230, 231, 232);
}
QPushButton:hover {
    background: rgba(0, 0, 0, 0.3);
    color: rgb(255, 255, 255);
    border: 0px solid black;
}
QPushButton:disabled {
    background: rgba(125, 125, 125, 125);
    color: rgba(125, 125, 125, 125);
    border: none;
}
"""
card_button_style = """
QPushButton {
    background: transparent;
    color: rgb(0, 0, 0);
    border:0px solid rgb(0,0,0);
    border-radius: 16px;
    padding: 7px;
}
QPushButton:hover {
    background: rgba(0, 0, 0, 0.3);
    color: #FFFFFF;
    border: 0px solid black;
}
QPushButton:disabled {
    background: rgba(125, 125, 125, 125);
    color: rgba(125, 125, 125, 125);
    border: none;
}
"""
card_button_dark_style = """
QPushButton {
    background: transparent;
    color: rgb(0, 0, 0);
    border:0px solid rgb(0,0,0);
    border-radius: 16px;
    padding: 7px;
}
QPushButton:hover {
    background: rgba(125, 125, 125, 30);
    color: #FFFFFF;
    border: 0px solid black;
}
QPushButton:disabled {
    background: rgba(125, 125, 125, 125);
    color: rgba(125, 125, 125, 125);
    border: none;
}
"""
normal_light_button_style = """
QPushButton {
    border-radius: 10px;
    border: 1px solid white;
    background-color:rgba(230, 231, 232, 200);
}
QPushButton:hover {
    background: rgba(0, 0, 0, 0.3);
    color: rgb(255, 255, 255);
    border: none;
}
QPushButton:disabled {
    background: rgba(125, 125, 125, 125);
    color: rgba(125, 125, 125, 125);
    border: none;
}
"""
normal_dark_button_style = """
QPushButton {
    border-radius: 10px;
    border: 1px solid black;
    background-color:rgba(20, 21, 22, 200);
}
QPushButton:hover {
    background: rgba(230, 231, 232, 0.3);
    color: rgb(0, 0, 0);
    border: none;
}
QPushButton:disabled {
    background: rgba(125, 125, 125, 125);
    color: rgba(125, 125, 125, 125);
    border: none;
}
"""
def set_button_style(button, is_dark=False, icon_path=None, size=None, style_change=True):
    if style_change:
        if is_dark:
            button.setStyleSheet(button_dark_style)
        else:
            button.setStyleSheet(button_light_style)
    if icon_path is not None and icon_path != "":
        button.setIcon(get_icon_by_path(icon_path=icon_path, size=size, is_dark=is_dark))
    button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    # 最小高度
    if button.minimumHeight() == 0:
        button.setMinimumHeight(25)
    # 鼠标手型
    if button.cursor() != Qt.CursorShape.PointingHandCursor:
        button.setCursor(Qt.CursorShape.PointingHandCursor)

def set_card_button_style(button: QPushButton, icon_path: str, size=None, is_dark=False, style_change=True):
    if style_change:
        if is_dark:
            button.setStyleSheet(card_button_dark_style)
        else:
            button.setStyleSheet(card_button_style)
    button.setIcon(get_icon_by_path(icon_path=icon_path, size=size, is_dark=is_dark))
    button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    # 鼠标手型
    if button.cursor() != Qt.CursorShape.PointingHandCursor:
        button.setCursor(Qt.CursorShape.PointingHandCursor)
'''
↑                                                                                ↑
**********************************按钮 · 结束***************************************
'''

'''
**********************************复选框 · 开始***************************************
↓                                                                                 ↓
'''
radio_button_style = """
QRadioButton {
    border: none;/*最外层边框*/
    background-color: transparent;
}
QRadioButton::indicator{/*选择框尺寸*/
    background-color: transparent;
    border: none;
    width: 20px;
    height: 20px;
    margin-left: 0px;
}
QRadioButton::indicator:unchecked {
    image: url(:static/img/IconPark/dark/Graphics/round.png);
}
QRadioButton::indicator:unchecked:hover {
    image: url(:static/img/IconPark/dark/Graphics/round.png);
}
QRadioButton::indicator:unchecked:pressed {
    image: url(:static/img/IconPark/dark/Graphics/round.png);
}
QRadioButton::indicator:checked {
    image: url(:static/img/IconPark/dark/Edit/radio-two.png);
}
QRadioButton::indicator:checked:hover {
    image: url(:static/img/IconPark/dark/Edit/radio-two.png);
}
QRadioButton::indicator:checked:pressed {
    image: url(:static/img/IconPark/dark/Edit/radio-two.png);
}
"""
check_box_style = """
QCheckBox{
    border: none;/*最外层边框*/
    background-color: transparent;
}
QCheckBox::indicator{/*选择框尺寸*/
    background-color: transparent;
    border: none;
    width: 20px;
    height: 20px;
}
QCheckBox::indicator:unchecked {            /* 未选中时状态 */
    image: url(:static/img/IconPark/dark/Graphics/round.png);
}
QCheckBox::indicator:unchecked:hover {      /* 未选中时，鼠标悬停时的状态 */
    image: url(:static/img/IconPark/dark/Graphics/round.png);
}
QCheckBox::indicator:unchecked:pressed {    /* 未选中时，按钮下按时的状态 */
    image: url(:static/img/IconPark/dark/Graphics/round.png);
}
QCheckBox::indicator:checked {              /* 按钮选中时的状态 */
    image: url(:static/img/IconPark/dark/Character/check-one.png);
}
QCheckBox::indicator:checked:hover {        /* 按钮选中时，鼠标悬停状态 */
    image: url(:static/img/IconPark/dark/Character/check-one.png);
}
QCheckBox::indicator:checked:pressed {      /* 按钮选中时，鼠标下按时的状态 */
    image: url(:static/img/IconPark/dark/Character/check-one.png);
}
"""
def set_radio_button_style(radio_button, is_dark=False):
    if is_dark:
        radio_button.setStyleSheet(radio_button_style.replace("IconPark/dark", "IconPark/light")
                                .replace("rgba(0, 0, 0, 0.3);", "rgba(255, 255, 255, 0.3);"))
    else:
        radio_button.setStyleSheet(radio_button_style)
    # 根据弧度设置最小高度
    if radio_button.minimumHeight() == 0:
        radio_button.setMinimumHeight(20)
    # 鼠标手型
    if radio_button.cursor() != Qt.CursorShape.PointingHandCursor:
        radio_button.setCursor(Qt.CursorShape.PointingHandCursor)

def set_check_box_style(check_box, is_dark=False):
    if is_dark:
        check_box.setStyleSheet(check_box_style.replace("IconPark/dark", "IconPark/light")
                                .replace("rgba(0, 0, 0, 0.3);", "rgba(255, 255, 255, 0.3);"))
    else:
        check_box.setStyleSheet(check_box_style)
    # 根据弧度设置最小高度
    if check_box.minimumHeight() == 0:
        check_box.setMinimumHeight(20)
    # 鼠标手型
    if check_box.cursor() != Qt.CursorShape.PointingHandCursor:
        check_box.setCursor(Qt.CursorShape.PointingHandCursor)
'''
↑                                                                                ↑
**********************************复选框 · 结束***************************************
'''

'''
**********************************输入框 · 开始**************************************
↓                                                                                 ↓
'''
line_edit_style = """
QLineEdit {
    border-radius: 10px;
    border: 1px solid black;
    background-color: transparent;
    padding-left: 5px;
}
"""
line_edit_dark_style = """
QLineEdit {
    border-radius: 10px;
    border: 1px solid white;
    background-color: transparent;
    padding-left: 5px;
}
"""
box_line_edit_style = """
QLineEdit {
    border: 1px solid black;
    background-color: transparent;
    padding: 5px; 
}
"""
text_edit_style = """
QTextEdit {
    border-radius: 10px;
    border: 1px solid black;
    background-color: transparent;
}
"""
text_edit_dark_style = """
QTextEdit {
    border-radius: 10px;
    border: 1px solid white;
    background-color: transparent;
}
"""
spin_box_style = """
QSpinBox {
    border-radius: 10px;
    border: 1px solid black;
    color: rgb(0, 0, 0);
    background-color: transparent;
    padding: 0px;
}
QSpinBox:hover { }
QSpinBox:up-button {
    subcontrol-origin:border;
    subcontrol-position:right;
    image: url(:static/img/IconPark/dark/Arrows/right-one.png);
    width: 20px;
    height: 20px;
}
QSpinBox:up-button:hover {
	subcontrol-origin:border;
    subcontrol-position:right;
    image: url(:static/img/IconPark/dark/Arrows/right-one.png);
}
QSpinBox:up-button:pressed {
	subcontrol-origin:border;
    subcontrol-position:right;
    image: url(:static/img/IconPark/dark/Arrows/right-one.png);
}
QSpinBox:down-button {
    subcontrol-origin:border;
    subcontrol-position:left;
    image: url(:static/img/IconPark/dark/Arrows/left-one.png);
    width: 20px;
    height: 20px;
}
QSpinBox:down-button:hover {
    subcontrol-position:left;
    image: url(:static/img/IconPark/dark/Arrows/left-one.png);
}
QSpinBox:down-button:pressed {
    subcontrol-position:left;
    image: url(:static/img/IconPark/dark/Arrows/left-one.png);
}
"""
double_spin_box_style = """
QDoubleSpinBox {
    border-radius: 10px;
    border: 1px solid black;
    color: rgb(0, 0, 0);
    background-color: transparent;
    padding: 0px;
}
QDoubleSpinBox:hover { }
QDoubleSpinBox:up-button {
    subcontrol-origin:border;
    subcontrol-position:right;
    image: url(:static/img/IconPark/dark/Arrows/right-one.png);
    width: 20px;
    height: 20px;
}
QDoubleSpinBox:up-button:hover {
	subcontrol-origin:border;
    subcontrol-position:right;
    image: url(:static/img/IconPark/dark/Arrows/right-one.png);
}
QDoubleSpinBox:up-button:pressed {
	subcontrol-origin:border;
    subcontrol-position:right;
    image: url(:static/img/IconPark/dark/Arrows/right-one.png);
}
QDoubleSpinBox:down-button {
    subcontrol-origin:border;
    subcontrol-position:left;
    image: url(:static/img/IconPark/dark/Arrows/left-one.png);
    width: 20px;
    height: 20px;
}
QDoubleSpinBox:down-button:hover {
    subcontrol-position:left;
    image: url(:static/img/IconPark/dark/Arrows/left-one.png);
}
QDoubleSpinBox:down-button:pressed {
    subcontrol-position:left;
    image: url(:static/img/IconPark/dark/Arrows/left-one.png);
}
"""
def set_line_edit_style(line_edit, is_dark=False):
    if is_dark:
        line_edit.setStyleSheet(line_edit_dark_style)
    else:
        line_edit.setStyleSheet(line_edit_style)
    # 根据弧度设置最小高度
    if line_edit.minimumHeight() == 0:
        line_edit.setMinimumHeight(20)

def set_text_edit_style(text_edit, is_dark=False):
    if is_dark:
        text_edit.setStyleSheet(text_edit_dark_style + scroll_bar_style)
    else:
        text_edit.setStyleSheet(text_edit_style + scroll_bar_style)

def set_spin_box_style(spin_box, is_dark=False):
    if is_dark:
        spin_box.setStyleSheet(spin_box_style
                               .replace("black", "white")
                               .replace("dark", "light")
                               .replace("rgb(0, 0, 0)", "rgb(255, 255, 255)"))
        spin_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
    else:
        spin_box.setStyleSheet(spin_box_style)
        spin_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
    spin_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
    # 根据弧度设置最小高度
    if spin_box.minimumHeight() == 0:
        spin_box.setMinimumHeight(20)

def set_double_spin_box_style(spin_box, is_dark=False):
    if is_dark:
        spin_box.setStyleSheet(double_spin_box_style
                               .replace("black", "white")
                               .replace("dark", "light")
                               .replace("rgb(0, 0, 0)", "rgb(255, 255, 255)"))
        spin_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
    else:
        spin_box.setStyleSheet(double_spin_box_style)
        spin_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
    # 根据弧度设置最小高度
    if spin_box.minimumHeight() == 0:
        spin_box.setMinimumHeight(20)
'''
↑                                                                                ↑
**********************************输入框 · 结束**************************************
'''

'''
**********************************日期框 · 开始**************************************
↓                                                                                 ↓
'''
date_edit_style = """
QDateEdit {
    border-radius: 10px;
    border: 1px solid black;
    color: rgb(0, 0, 0);
    background-color: transparent;
}
QDateEdit:hover { }
QDateEdit:up-button {
    subcontrol-origin:border;
    subcontrol-position:right;
    image: url(:static/img/IconPark/dark/Arrows/right-one.png);
    width: 20px;
    height: 20px;
}
QDateEdit:up-button:hover {
	subcontrol-origin:border;
    subcontrol-position:right;
    image: url(:static/img/IconPark/dark/Arrows/right-one.png);
}
QDateEdit:up-button:pressed {
	subcontrol-origin:border;
    subcontrol-position:right;
    image: url(:static/img/IconPark/dark/Arrows/right-one.png);
}
QDateEdit:down-button {
    subcontrol-origin:border;
    subcontrol-position:left;
    image: url(:static/img/IconPark/dark/Arrows/left-one.png);
    width: 20px;
    height: 20px;
}
QDateEdit:down-button:hover {
    subcontrol-position:left;
    image: url(:static/img/IconPark/dark/Arrows/left-one.png);
}
QDateEdit:down-button:pressed {
    subcontrol-position:left;
    image: url(:static/img/IconPark/dark/Arrows/left-one.png);
}
"""

def set_date_edit_style(date_edit, is_dark=False):
    if is_dark:
        date_edit.setStyleSheet(date_edit_style
                               .replace("black", "white")
                               .replace("dark", "light")
                               .replace("rgb(0, 0, 0)", "rgb(255, 255, 255)"))
        date_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
    else:
        date_edit.setStyleSheet(date_edit_style)
        date_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
    date_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
    # 根据弧度设置最小高度
    if date_edit.minimumHeight() == 0:
        date_edit.setMinimumHeight(20)
'''
↑                                                                                ↑
**********************************日期框 · 结束***************************************
'''

'''
**********************************下拉框 · 开始***************************************
↓                                                                                 ↓
'''
combo_box_style = """
/*下拉框*/
QComboBox {
    border-radius: 10px;
    border: 1px solid black;
    color: rgb(0, 0, 0);
    background: transparent;
    padding-left: 10px;
}
QComboBox:disabled {
    color: black;
}
/*点击combox的样式*/
QComboBox:on {
    color: rgb(0, 0, 0);
    background: transparent;
    border: 1px solid black;
    border-radius: 10px;
    padding-left: 10px;
}
/*下拉框的样式*/
QComboBox QAbstractItemView {
    margin-top: 4px;
    padding: 5px 5px 5px 5px;
    height: 21px;
    outline: 0px solid gray;    /*取消选中虚线*/
    border: 1px solid rgb(66, 66, 66);
    color: rgb(0, 0, 0);
    background-color: rgb(255, 255, 255);
}
/*选中每一项高度*/
QComboBox QAbstractItemView::item {
    color: rgb(100, 100, 100);
    background-color: rgb(255, 255, 255);
    border-radius: 10px;
}
/*选中每一项的字体颜色和背景颜色*/
QComboBox QAbstractItemView::item:selected {
    color: rgba(75, 175, 255, 1);
    background-color: rgb(255, 255, 255);
    border-radius: 10px;
}
/*下拉箭头的边框*/
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 20px;
    border-left-width: 0px;
    border-left-color: darkgray;
    border-left-style: solid; /* just a single line */
    border-top-right-radius: 3px; /* same radius as the QComboBox */
    border-bottom-right-radius: 3px;
}
/*下拉箭头样式*/
QComboBox::down-arrow {
    image: url(:static/img/IconPark/dark/Arrows/down-one.png);
    padding-right: 2px;
    width: 20px;
    height: 20px;
}
/*下拉箭头点击样式*/
QComboBox::down-arrow:on {
    image: url(:static/img/IconPark/dark/Arrows/down-one.png);
    padding-right: 2px;
    width: 20px;
    height: 20px;
}
"""
def set_combo_box_style(combo_box, is_dark=False):
    style = combo_box_style + scroll_bar_style
    if is_dark:
        style = style.replace("black", "white")
        style = style.replace('color: rgb(0, 0, 0);', 'color: rgb(239, 240, 241);')
        style = style.replace('color: rgb(255, 255, 255);', 'color: rgb(0, 0, 0);')
        style = style.replace('IconPark/dark', 'IconPark/light')
    combo_box.setStyleSheet(style)
    # 不设置Popup则列表不能弹出；不设置FramelessWindowHint则不能无边框；不设置NoDropShadowWindowHint则右下角有默认三角形阴影。
    combo_box.view().parentWidget().setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint | Qt.WindowType.NoDropShadowWindowHint)
    # 设置背景透明，否则qss透明度不生效
    combo_box.view().parentWidget().setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    # 根据弧度设置最小高度
    if combo_box.minimumHeight() == 0:
        combo_box.setMinimumHeight(20)
'''
↑                                                                                ↑
**********************************下拉框 · 结束***************************************
'''

'''
**********************************选项卡 · 开始***************************************
↓                                                                                 ↓
'''
tab_widget_style = """
QWidget {
    background: transparent;
}
QTabWidget::pane {
    margin: 10px;
    background: transparent;
    color: rgb(0, 0, 0);
    border-radius: 12px;
    border: 1px solid white;
}
QTabBar::tab {
    height:24px; 
    min-width: 40px;
    background: transparent;
    border-radius: 12px;
    margin-top: 10px;
    margin-left: 10px;
	padding-left: 5px;
	padding-right: 5px;
}
QTabBar::tab:selected {
    background: rgba(255, 255, 255, 180);
    border: 1px solid rgb(120, 120, 120);
}
QTabBar::tab:!selected {
    background: rgba(255, 255, 255, 100);
}
"""
tab_widget_dark_style = """
QWidget {
    background:transparent
}
QTabWidget::pane {
    margin: 10px;
    background: rgba(0, 0, 0, 150);
    color: rgb(255, 255, 255);
    border: none;
    border-radius: 12px;
}
QTabBar::tab {
    height:24px; 
    min-width: 40px;
    background: transparent;
    border-radius: 12px;
    margin-top: 10px;
    margin-left: 10px;
	padding-left: 5px;
	padding-right: 5px;
}
QTabBar::tab:selected {
    background: rgba(0, 0, 0, 180);
    border: 1px solid rgb(120, 120, 120);
}
QTabBar::tab:!selected {
    background: rgba(0, 0, 0, 100);
}
"""
def set_tab_widget_style(tab_widget, is_dark=False):
    if is_dark:
        tab_widget.setStyleSheet(tab_widget_dark_style)
    else:
        tab_widget.setStyleSheet(tab_widget_style)
    tab_widget.setStyleSheet(tab_widget.styleSheet() + scroll_bar_style)
    tab_bar = tab_widget.tabBar()
    tab_bar.setCursor(Qt.PointingHandCursor)

'''
↑                                                                                ↑
**********************************选项卡 · 结束***************************************
'''

'''
**********************************进度条 · 开始***************************************
↓                                                                                 ↓
'''
def set_progress_bar_style(progress_bar, is_dark):
    if is_dark:
        progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #555;
                border-radius: 5px;
                background-color: #333;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 4px;
            }
        """)
    else:
        progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #f0f0f0;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #2196F3;
                border-radius: 4px;
            }
        """)

'''
↑                                                                                ↑
**********************************进度条 · 结束***************************************
'''

'''
**********************************表格 · 开始***************************************
↓                                                                                 ↓
'''
table_widget_style = """
/* 表格整体样式 */
QTableWidget {
    gridline-color: #E0E0E0;
    background-color: #FFFFFF;
    color: #333333;
    border: 1px solid #E1E1E1;
    border-radius: 4px;
}

/* 表头样式 */
QHeaderView::section {
    background-color: #F5F5F5;
    color: #444444;
    padding: 4px;
    border: none;
    border-bottom: 2px solid #0078D7;
    font-weight: bold;
}

QHeaderView {
    background-color: #F0F0F0;
}

/* 行样式 */
QTableWidget::item {
    padding: 6px;
    border-bottom: 1px solid #EEEEEE;
}

QTableWidget::item:selected {
    background-color: #E3F2FD;
    color: #0066CC;
}

/* 交替行颜色 */
QTableWidget::item:nth-child(even) {
    background-color: #FAFAFA;
}

QTableWidget::item:nth-child(odd) {
    background-color: #FFFFFF;
}

/* 滚动条样式 */
QScrollBar:vertical {
    background: #F8F8F8;
    width: 12px;
}

QScrollBar::handle:vertical {
    background: #D0D0D0;
    min-height: 20px;
    border-radius: 4px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    background: none;
}
"""

table_widget_dark_style = """
/* 表格整体样式 */
QTableWidget {
    gridline-color: #444;
    background-color: #2D2D30;
    color: #E0E0E0;
    border: 1px solid #3F3F46;
    border-radius: 4px;
}

/* 表头样式 */
QHeaderView::section {
    background-color: #252526;
    color: #D4D4D4;
    padding: 4px;
    border: none;
    border-bottom: 2px solid #0078D7;
    font-weight: bold;
}

QHeaderView {
    background-color: #1E1E1E;
}

/* 行样式 */
QTableWidget::item {
    padding: 6px;
    border-bottom: 1px solid #3F3F46;
}

QTableWidget::item:selected {
    background-color: #3E3E40;
    color: #FFFFFF;
}

/* 交替行颜色 */
QTableWidget::item:nth-child(even) {
    background-color: #2D2D30;
}

QTableWidget::item:nth-child(odd) {
    background-color: #252526;
}

/* 滚动条样式 */
QScrollBar:vertical {
    background: #1E1E1E;
    width: 12px;
}

QScrollBar::handle:vertical {
    background: #5A5A5A;
    min-height: 20px;
    border-radius: 4px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    background: none;
}
"""
def set_table_widget_style(table_widget, is_dark=False):
    if is_dark:
        table_widget.setStyleSheet(table_widget_dark_style)
    else:
        table_widget.setStyleSheet(table_widget_style)
    # 隐藏列标
    table_widget.verticalHeader().hide()

'''
↑                                                                                ↑
**********************************表格 · 结束***************************************
'''

'''
**********************************总体调整 · 开始***************************************
↓                                                                                 ↓
'''
frame_style = "QFrame { background-color: transparent; }"
def find_all_widgets(widget, widget_list=None):
    """
    使用迭代方式查找所有子控件，避免递归深度超限
    """
    widget_list = []
    stack = [widget]
    while stack:
        current_widget = stack.pop()
        widget_list.append(current_widget)
        # 使用 children() 获取直接子控件，并添加到栈中
        stack.extend(current_widget.children())
    return widget_list

def set_dialog_control_style(widget, is_dark=False):
    # 查询所有控件
    all_widgets = find_all_widgets(widget)
    for widget_item in all_widgets:
        if isinstance(widget_item, QWidget):
            if not isinstance(widget, QPlainTextEdit):
                widget_item.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)     # 右键禁止
        if isinstance(widget_item, QComboBox) or isinstance(widget_item, QFontComboBox):
            set_combo_box_style(widget_item, is_dark)
            continue
        elif isinstance(widget_item, QToolButton):
            # 鼠标手型
            if widget_item.cursor() != Qt.CursorShape.PointingHandCursor:
                widget_item.setCursor(Qt.CursorShape.PointingHandCursor)
            continue
        elif isinstance(widget_item, QPushButton):
            if widget_item.objectName() in [
                "AgileTilesTitleBarTitlePushButton",
                "AgileTilesTitleBarQuestionPushButton",
                "push_button_importance_exigency",
                "push_button_no_importance_exigency",
                "push_button_importance_no_exigency",
                "push_button_no_importance_no_exigency",
            ]:
                # 鼠标手型
                if widget_item.cursor() != Qt.CursorShape.PointingHandCursor:
                    widget_item.setCursor(Qt.CursorShape.PointingHandCursor)
                continue
            set_button_style(widget_item, is_dark)
            continue
        elif isinstance(widget_item, QRadioButton):
            set_radio_button_style(widget_item, is_dark)
            continue
        elif isinstance(widget_item, QTabWidget):
            set_tab_widget_style(widget_item, is_dark)
            continue
        elif isinstance(widget_item, QTableWidget):
            set_table_widget_style(widget_item, is_dark)
            continue
        elif isinstance(widget_item, QCheckBox):
            set_check_box_style(widget_item, is_dark)
            continue
        elif isinstance(widget_item, QSpinBox):
            set_spin_box_style(widget_item, is_dark)
            continue
        elif isinstance(widget_item, QDoubleSpinBox):
            set_double_spin_box_style(widget_item, is_dark)
            continue
        elif isinstance(widget_item, QDateEdit):
            set_date_edit_style(widget_item, is_dark)
            continue
        elif isinstance(widget_item, QLineEdit):
            set_line_edit_style(widget_item, is_dark)
            continue
        elif isinstance(widget_item, QTextEdit) or isinstance(widget_item, EnterTextEdit):
            set_text_edit_style(widget_item, is_dark)
            continue
        elif isinstance(widget_item, QFrame) and "frame" in widget_item.objectName():
            widget_item.setStyleSheet(frame_style)
            continue
    # 设置字体
    set_font_and_right_click_style(widget, widget)

def set_font_and_right_click_style(main_window, widget):
    """
    设置字体和右键禁止
    """
    # 查询所有控件
    all_widgets = find_all_widgets(widget)
    for widget in all_widgets:
        if isinstance(widget, QWidget):
            if not isinstance(widget, QPlainTextEdit):
                widget.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)     # 右键禁止
        if isinstance(widget, QBoxLayout):
            continue
        if isinstance(widget, TitleBar):
            continue
        if isinstance(widget, MinimizeButton) or isinstance(widget, MaximizeButton) or isinstance(widget, CloseButton):
            continue
        if not hasattr(widget, 'font'):
            continue
        if not 'setFont' in dir(widget):
            continue
        if widget == main_window:
            continue
        try:
            widget.setFont(QFont(main_window.form_font_name, widget.font().pointSize()))
        except Exception as e:
            if not hasattr(main_window, 'use_parent') or not hasattr(main_window.use_parent, 'form_font_name'):
                continue
            try:
                widget.setFont(QFont(main_window.use_parent.form_font_name, widget.font().pointSize()))
            except Exception as e:
                print(f"set_font_and_right_click_style error: {str(e)}")


def set_all_theme(main_object):
    if main_object.is_dark:
        main_object.setStyleSheet("*{ outline: none; background:rgba(24, 24, 24, 255); color:rgb(239, 240, 241) };")
    else:
        main_object.setStyleSheet("*{ outline: none; background:rgba(0, 115, 255, 15); color:rgb(0, 0, 0) };")

'''
↑                                                                                ↑
**********************************总体调整 · 结束***************************************
'''
def set_card_shadow_effect(widget):
    if widget.graphicsEffect():
        widget.graphicsEffect().deleteLater()
    # 添加外部阴影效果（暂不启用，启用会导致其下的按钮的图标和文字中间有间隔，例如音乐卡片上面的两个按钮）
    # shadow_effect = QGraphicsDropShadowEffect(widget)
    # shadow_effect.setColor(QColor(150, 150, 150, 50))  # rgba(150, 150, 150, 40)
    # shadow_effect.setOffset(0, 0)  # 偏移量
    # shadow_effect.setBlurRadius(15)  # 模糊半径
    # widget.setGraphicsEffect(shadow_effect)

def remove_card_shadow_effect(widget):
    if widget.graphicsEffect():
        widget.graphicsEffect().deleteLater()
