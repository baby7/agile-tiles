from PySide6.QtCore import QEventLoop
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QVBoxLayout, QLabel, QLineEdit

from src.ui import style_util

dialog_close_button_style = """
QPushButton {
    background: transparent;
    border: none;
}
"""

def set_dialog(main_object):
    # 基础弹窗背景
    main_object.widget_dialog_base.raise_()
    main_object.widget_dialog_base.resize(main_object.width(), main_object.height())
    main_object.widget_dialog_base.move(0, 0)
    main_object.widget_dialog_base.hide()
    # 弹窗图标
    icon_path = ":static/img/icon/icon.ico"
    main_object.label_dialog_icon.setPixmap(QPixmap(icon_path))
    main_object.label_dialog_icon.setFixedSize(20, 20)
    main_object.label_dialog_icon.setScaledContents(True)
    # 弹窗标题
    main_object.label_dialog_title.setText(main_object.app_title)
    # 弹窗关闭按钮
    main_object.push_button_dialog_close.setStyleSheet(dialog_close_button_style)
    main_object.push_button_dialog_close.setIcon(style_util.get_icon_by_path("Character/close-one", custom_color="#FF0000"))
    # 关闭事件
    main_object.push_button_dialog_close.clicked.connect(lambda: dialog_close_click(main_object))


def refresh_theme(main_object):
    if main_object.is_dark:
        main_object.widget_dialog_base.setStyleSheet("background-color: rgb(24, 24, 24); border-radius: 10px; border: none;")
    else:
        main_object.widget_dialog_base.setStyleSheet(f"background-color: rgb(200, 200, 200); border-radius: 10px; border: none;")
    # 弹窗背景
    if main_object.is_dark:
        main_object.widget_dialog_entity.setStyleSheet("background-color: rgb(10, 11, 12); border-radius: 10px; border: none;")
    else:
        main_object.widget_dialog_entity.setStyleSheet(f"background-color: rgb(220, 221, 222); border-radius: 10px; border: none;")
    # 弹窗背景边框
    if main_object.is_dark:
        main_object.widget_dialog_content.setStyleSheet("background-color: rgb(24, 24, 24); border-radius: 10px; border: none;")
    else:
        main_object.widget_dialog_content.setStyleSheet(f"background-color: rgb(200, 200, 200); border-radius: 10px; border: none;")
    # 按钮样式
    style_util.set_button_style(main_object.push_button_dialog_cancel, main_object.is_dark)
    style_util.set_button_style(main_object.push_button_dialog_confirm, main_object.is_dark)


def dialog_close_click(main_object):
    # 隐藏弹窗
    main_object.widget_dialog_base.hide()
    # 清空控件
    clear_widget(main_object)

def clear_widget(main_object):
    # 删除子控件
    layout = main_object.widget_dialog_content.layout()
    if layout is not None:
        # 递归删除所有子控件
        _clear_layout(layout)
        # 删除布局本身
        layout.deleteLater()
        # 从widget中移除布局引用
        main_object.widget_dialog_content.setLayout(None)

def _clear_layout(layout):
    """递归清除布局中的所有控件"""
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            # 删除控件
            widget.deleteLater()
        else:
            # 如果是子布局，递归清除
            child_layout = item.layout()
            if child_layout is not None:
                _clear_layout(child_layout)

def box_information(main_object, title, content, button_ok_text="确定"):
    """
    消息通知弹窗
    :param main_object: 主窗口
    :param title: 标题
    :param content: 内容
    :param button_ok_text: 确认按钮文本
    """
    # 清空控件
    clear_widget(main_object)
    # 创建一个事件循环
    loop = QEventLoop()
    # 确定按钮事件
    def accept():
        nonlocal loop
        main_object.widget_dialog_base.hide()
        if loop and loop.isRunning():
            loop.quit()
    # 设置弹窗标题
    main_object.label_dialog_title.setText(title)
    # 设置按钮显示
    main_object.push_button_dialog_confirm.setText(button_ok_text)
    main_object.push_button_dialog_cancel.hide()
    main_object.push_button_dialog_confirm.show()
    # 构建布局
    layout = QVBoxLayout()
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
    # 将布局添加到弹窗内容中
    main_object.widget_dialog_content.setLayout(layout)
    # 按钮事件
    main_object.push_button_dialog_confirm.clicked.connect(accept)
    # 展示
    main_object.widget_dialog_base.show()
    # 创建一个局部事件循环实现阻塞效果
    loop.exec()
    # 断开按钮的点击事件
    main_object.push_button_dialog_confirm.clicked.disconnect(accept)
    # 清空控件
    clear_widget(main_object)
    # 隐藏弹窗
    main_object.widget_dialog_base.hide()


def box_acknowledgement(main_object, title, content, button_ok_text="确定", button_no_text="取消"):
    """
    消息确认弹窗
    :param main_object: 主窗口
    :param title: 标题
    :param content: 内容
    :param button_ok_text: 确认按钮文本
    :param button_no_text:  取消按钮文本
    :return: 是否按了确定
    """
    # 清空控件
    clear_widget(main_object)
    # 创建一个事件循环
    loop = QEventLoop()
    # 结果变量
    result = None
    # 确定按钮事件
    def accept():
        nonlocal result, loop
        result = True
        main_object.widget_dialog_base.hide()
        if loop and loop.isRunning():
            loop.quit()
    # 取消按钮事件
    def reject():
        nonlocal result, loop
        result = False
        main_object.widget_dialog_base.hide()
        if loop and loop.isRunning():
            loop.quit()
    # 设置弹窗标题
    main_object.label_dialog_title.setText(title)
    # 设置按钮显示
    main_object.push_button_dialog_cancel.setText(button_no_text)
    main_object.push_button_dialog_confirm.setText(button_ok_text)
    main_object.push_button_dialog_cancel.show()
    main_object.push_button_dialog_confirm.show()
    # 构建布局
    layout = QVBoxLayout()
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
    # 将布局添加到弹窗内容中
    main_object.widget_dialog_content.setLayout(layout)
    # 按钮事件
    main_object.push_button_dialog_cancel.clicked.connect(reject)
    main_object.push_button_dialog_confirm.clicked.connect(accept)
    # 展示
    main_object.widget_dialog_base.show()
    # 创建一个局部事件循环实现阻塞效果
    loop.exec()
    # 断开按钮的点击事件
    main_object.push_button_dialog_cancel.clicked.disconnect(reject)
    main_object.push_button_dialog_confirm.clicked.disconnect(accept)
    # 清空控件
    clear_widget(main_object)
    # 隐藏弹窗
    main_object.widget_dialog_base.hide()
    # 返回结果
    return result

def box_input(main_object, title, content, button_ok_text="确定", button_no_text="取消", old_text=None):
    """
    输入弹窗
    :param main_object: 主窗口
    :param title: 标题
    :param content: 内容
    :param button_ok_text: 确认按钮文本
    :param button_no_text:  取消按钮文本
    :param old_text:  默认展示的文本
    :return: 是否按了确定
    :return:
    """
    # 清空控件
    clear_widget(main_object)
    # 创建一个事件循环
    loop = QEventLoop()
    # 结果变量
    result = None
    # 确定按钮事件
    def accept():
        nonlocal result, loop
        result = True
        main_object.widget_dialog_base.hide()
        if loop and loop.isRunning():
            loop.quit()
    # 取消按钮事件
    def reject():
        nonlocal result, loop
        result = False
        main_object.widget_dialog_base.hide()
        if loop and loop.isRunning():
            loop.quit()
    # 设置弹窗标题
    main_object.label_dialog_title.setText(title)
    # 设置按钮显示
    main_object.push_button_dialog_cancel.setText(button_no_text)
    main_object.push_button_dialog_confirm.setText(button_ok_text)
    main_object.push_button_dialog_cancel.show()
    main_object.push_button_dialog_confirm.show()
    # 构建布局
    layout = QVBoxLayout()
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
    style_util.set_line_edit_style(input_field, main_object.is_dark)
    input_field.setMinimumWidth(260)
    input_field.setMinimumHeight(22)
    if old_text:
        input_field.setText(old_text)
    layout.addWidget(input_field)
    # 将布局添加到弹窗内容中
    main_object.widget_dialog_content.setLayout(layout)
    # 按钮事件
    main_object.push_button_dialog_cancel.clicked.connect(reject)
    main_object.push_button_dialog_confirm.clicked.connect(accept)
    # 设置输入焦点
    input_field.setFocus()
    # 展示
    main_object.widget_dialog_base.show()
    # 创建一个局部事件循环实现阻塞效果
    loop.exec()
    # 获取要返回的结果
    if result:
        result_text = input_field.text()
    else:
        result_text = None
    # 断开按钮的点击事件
    main_object.push_button_dialog_cancel.clicked.disconnect(reject)
    main_object.push_button_dialog_confirm.clicked.disconnect(accept)
    # 清空控件
    clear_widget(main_object)
    # 隐藏弹窗
    main_object.widget_dialog_base.hide()
    # 返回结果
    return result_text