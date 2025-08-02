from PySide6.QtCore import QSettings, QTimer
from PySide6.QtWidgets import QLineEdit, QPushButton, QWidget, QHBoxLayout, QLabel, QVBoxLayout, QDialog, QProgressBar
import src.ui.style_util as style_util

from src.component.AgileTilesFramelessDialog.AgileTilesFramelessDialog import AgileTilesFramelessDialog


def box_information(widget, title, content, button_ok_text="确定", close_seconds=None):
    """
    消息通知弹窗
    :param widget: 需要绑定的widget
    :param title: 标题
    :param content: 内容
    :param button_ok_text: 确认按钮文本
    :param close_seconds: 自动关闭的时间（秒），传入 None 则不自动关闭
    """
    # 获取窗口构建信息
    is_dark = None
    form_theme_mode = None
    form_theme_transparency = None
    if hasattr(widget, "is_dark"):
        is_dark = widget.is_dark
        form_theme_mode = widget.form_theme_mode
        form_theme_transparency = widget.form_theme_transparency
    elif hasattr(widget, "ui_setting"):
        is_dark = widget.ui_setting.is_dark()
    if is_dark is None:
        app_name = "AgileTiles"
        settings = QSettings(app_name, "Theme")
        is_dark = settings.value("IsDark", False, type=bool)
    # 构建窗口
    dialog = AgileTilesFramelessDialog(is_dark=is_dark, form_theme_mode=form_theme_mode,
                                       form_theme_transparency=form_theme_transparency)
    dialog.setWindowTitle(title)  # 设置到标题栏

    layout = QVBoxLayout(dialog.widget_base)
    layout.setContentsMargins(20, 15, 20, 15)  # 调整顶部边距
    layout.setSpacing(15)

    # 内容部分
    content_label = QLabel(content)
    content_label.setWordWrap(True)
    content_label.setStyleSheet("""QLabel {
        font-size: 14px;
        background-color: transparent;
    }""")
    layout.addWidget(content_label)

    # 按钮部分
    button = QPushButton(button_ok_text)
    style_util.set_button_style(button, is_dark)
    button.setFixedSize(80, 32)
    button.clicked.connect(dialog.accept)

    # 按钮居中布局
    btn_container = QWidget()
    btn_container.setStyleSheet("background-color: transparent;")
    btn_layout = QHBoxLayout(btn_container)
    btn_layout.addStretch()
    btn_layout.addWidget(button)
    btn_layout.addStretch()

    layout.addWidget(btn_container)

    # 尺寸优化
    dialog.setMinimumSize(280, 140)
    dialog.resize(360, 160)  # 更紧凑的默认尺寸
    if hasattr(widget, "toolkit"):
        dialog.refresh_geometry(widget.toolkit.resolution_util.get_screen(widget))

    # 如果传入了秒参数，则设置定时器
    if close_seconds is not None and close_seconds > 0:
        timer = QTimer(dialog)
        timer.setSingleShot(True)  # 单次触发
        timer.timeout.connect(dialog.accept)  # 定时器触发后关闭窗口
        timer.start(int(close_seconds * 1000))  # 转换为毫秒

    dialog.exec()


def box_acknowledgement(widget, title, content, button_ok_text="确定", button_no_text="取消"):
    """
    消息确认弹窗
    :param widget: 需要绑定的widget
    :param title: 标题
    :param content: 内容
    :param button_ok_text: 确认按钮文本
    :param button_no_text:  取消按钮文本
    :return: 是否按了确定
    """
    # 获取窗口构建信息
    is_dark = None
    form_theme_mode = None
    form_theme_transparency = None
    if hasattr(widget, "is_dark"):
        is_dark = widget.is_dark
        form_theme_mode = widget.form_theme_mode
        form_theme_transparency = widget.form_theme_transparency
    elif hasattr(widget, "ui_setting"):
        is_dark = widget.ui_setting.is_dark()
    if is_dark is None:
        app_name = "AgileTiles"
        settings = QSettings(app_name, "Theme")
        is_dark = settings.value("IsDark", False, type=bool)
    # 构建窗口
    dialog = AgileTilesFramelessDialog(is_dark=is_dark, form_theme_mode=form_theme_mode,
                                       form_theme_transparency=form_theme_transparency)
    dialog.setWindowTitle(title)

    layout = QVBoxLayout(dialog.widget_base)
    layout.setContentsMargins(20, 15, 20, 15)
    layout.setSpacing(15)

    # 内容标签
    content_label = QLabel(content)
    content_label.setWordWrap(True)
    content_label.setStyleSheet("""QLabel {
        font-size: 14px;
        background-color: transparent;
    }""")
    layout.addWidget(content_label)

    # 双按钮布局
    btn_container = QWidget()
    btn_container.setStyleSheet("background-color: transparent;")
    btn_layout = QHBoxLayout(btn_container)
    btn_layout.addStretch()

    # 取消按钮
    btn_cancel = QPushButton(button_no_text)
    style_util.set_button_style(btn_cancel, is_dark)
    btn_cancel.setFixedSize(80, 32)
    btn_cancel.clicked.connect(dialog.reject)

    # 确定按钮
    btn_confirm = QPushButton(button_ok_text)
    style_util.set_button_style(btn_confirm, is_dark)
    btn_confirm.setFixedSize(80, 32)
    btn_confirm.clicked.connect(dialog.accept)

    btn_layout.addWidget(btn_cancel)
    btn_layout.addWidget(btn_confirm)
    layout.addWidget(btn_container)

    # 尺寸设置
    dialog.setMinimumSize(300, 200)
    dialog.resize(360, 200)
    dialog.refresh_geometry(widget.toolkit.resolution_util.get_screen(widget))

    return dialog.exec() == QDialog.Accepted


def box_input(widget, title, content, button_ok_text="确定", button_no_text="取消", old_text=None):
    """
    输入弹窗
    :param widget: 需要绑定的widget
    :param title: 标题
    :param content: 内容
    :param button_ok_text: 确认按钮文本
    :param button_no_text:  取消按钮文本
    :return: 是否按了确定
    :return:
    """
    # 获取窗口构建信息
    is_dark = None
    form_theme_mode = None
    form_theme_transparency = None
    if hasattr(widget, "is_dark"):
        is_dark = widget.is_dark
        form_theme_mode = widget.form_theme_mode
        form_theme_transparency = widget.form_theme_transparency
    elif hasattr(widget, "ui_setting"):
        is_dark = widget.ui_setting.is_dark()
    if is_dark is None:
        app_name = "AgileTiles"
        settings = QSettings(app_name, "Theme")
        is_dark = settings.value("IsDark", False, type=bool)
    # 构建窗口
    dialog = AgileTilesFramelessDialog(is_dark=is_dark, form_theme_mode=form_theme_mode,
                                       form_theme_transparency=form_theme_transparency)
    dialog.setWindowTitle(title)

    layout = QVBoxLayout(dialog.widget_base)
    layout.setContentsMargins(20, 15, 20, 15)
    layout.setSpacing(15)

    # 内容标签
    content_label = QLabel(content)
    content_label.setStyleSheet("""QLabel {
        font-size: 14px;
        background-color: transparent;
    }""")
    layout.addWidget(content_label)

    # 输入框
    input_field = QLineEdit()
    style_util.set_line_edit_style(input_field, is_dark)
    input_field.setMinimumWidth(260)
    input_field.setMinimumHeight(22)
    if old_text:
        input_field.setText(old_text)
    layout.addWidget(input_field)

    # 双按钮布局
    btn_container = QWidget()
    btn_container.setStyleSheet("background-color: transparent;")
    btn_layout = QHBoxLayout(btn_container)
    btn_layout.addStretch()

    btn_cancel = QPushButton(button_no_text)
    style_util.set_button_style(btn_cancel, is_dark)
    btn_cancel.setFixedSize(80, 32)
    btn_cancel.clicked.connect(dialog.reject)

    btn_confirm = QPushButton(button_ok_text)
    style_util.set_button_style(btn_confirm, is_dark)
    btn_confirm.setFixedSize(80, 32)
    btn_confirm.clicked.connect(dialog.accept)

    btn_layout.addWidget(btn_cancel)
    btn_layout.addWidget(btn_confirm)
    layout.addWidget(btn_container)

    # 尺寸设置
    dialog.setMinimumSize(320, 200)
    dialog.resize(400, 200)
    dialog.refresh_geometry(widget.toolkit.resolution_util.get_screen(widget))

    # 设置输入焦点
    input_field.setFocus()

    if dialog.exec() == QDialog.Accepted:
        return input_field.text()
    return None


def box_progress(widget, title, label_text="正在下载更新...", cancel_text="取消"):
    """
    进度条弹窗
    :param widget: 需要绑定的widget
    :param title: 标题
    :param label_text: 进度标签文本
    :param cancel_text: 取消按钮文本
    :return: 对话框实例和进度条对象
    """
    is_dark = widget.is_dark
    if is_dark is None:
        app_name = "AgileTiles"
        settings = QSettings(app_name, "Theme")
        is_dark = settings.value("IsDark", False, type=bool)
    form_theme_mode = widget.form_theme_mode
    form_theme_transparency = widget.form_theme_transparency
    dialog = AgileTilesFramelessDialog(
        is_dark=is_dark,
        form_theme_mode=form_theme_mode,
        form_theme_transparency=form_theme_transparency
    )
    dialog.setWindowTitle(title)

    layout = QVBoxLayout(dialog.widget_base)
    layout.setContentsMargins(20, 15, 20, 15)
    layout.setSpacing(15)

    # 进度标签
    label = QLabel(label_text)
    label.setStyleSheet("""
        QLabel {
            font-size: 14px;
            background-color: transparent;
        }
    """)
    layout.addWidget(label)

    # 进度条
    progress_bar = QProgressBar()
    progress_bar.setRange(0, 100)
    progress_bar.setValue(0)
    style_util.set_progress_bar_style(progress_bar, is_dark)  # 添加进度条样式
    layout.addWidget(progress_bar)

    # 取消按钮
    cancel_button = QPushButton(cancel_text)
    style_util.set_button_style(cancel_button, is_dark)
    cancel_button.setFixedSize(80, 32)

    # 按钮布局
    btn_container = QWidget()
    btn_container.setStyleSheet("background-color: transparent;")
    btn_layout = QHBoxLayout(btn_container)
    btn_layout.addStretch()
    btn_layout.addWidget(cancel_button)
    btn_layout.addStretch()

    layout.addWidget(btn_container)

    # 尺寸设置
    dialog.setMinimumSize(400, 180)
    dialog.resize(450, 200)
    if hasattr(widget, "toolkit"):
        dialog.refresh_geometry(widget.toolkit.resolution_util.get_screen(widget))

    return dialog, progress_bar, cancel_button

