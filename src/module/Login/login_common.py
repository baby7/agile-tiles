# coding:utf-8
# 基础包
from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QPixmap, QIcon
import src.ui.style_util as style_util


def refresh_theme(main_object, is_dark=False):
    # 按钮样式
    button_list = [
        main_object.push_button_user_login, # 登录
        main_object.push_button_user_register, main_object.push_button_register_validator_code, # 注册
        main_object.push_button_user_forget, main_object.push_button_forget_validator_code, # 忘记密码
    ]
    for button in button_list:
        style_util.set_button_style(button, is_dark)
    # 输入框样式
    line_edit_list = [
        main_object.line_edit_user_login_username, main_object.line_edit_user_login_password,       # 登录
        main_object.line_edit_user_register_nickname, main_object.line_edit_user_register_username,
        main_object.line_edit_register_validator_code, main_object.line_edit_user_register_password,
        main_object.line_edit_user_register_password_check,   # 注册
        main_object.line_edit_user_forget_username, main_object.line_edit_forget_validator_code,
        main_object.line_edit_user_forget_password, main_object.line_edit_user_forget_password_check    # 忘记密码
    ]
    for line_edit in line_edit_list:
        style_util.set_line_edit_style(line_edit, is_dark)
    # 选项卡样式
    style_util.set_tab_widget_style(main_object.tab_widget_login, is_dark)
    if is_dark:
        icon = "./static/img/icon/dark/icon.png"
    else:
        icon = "./static/img/icon/light/icon.png"
    # 复选框
    style_util.set_check_box_style(main_object.check_box_user_area_agree_protocol, is_dark)
    # logo
    main_object.label_user_login_logo.setPixmap(QPixmap(icon))
    main_object.label_user_register_logo.setPixmap(QPixmap(icon))
    main_object.label_user_forget_logo.setPixmap(QPixmap(icon))

def get_icon_park_path(icon_position, is_dark):
    icon_theme_folder = "light" if is_dark else "dark"
    return QIcon("./static/img/IconPark/" + icon_theme_folder + "/" + icon_position + ".png")

def get_pixmap_park_path(icon_position, is_dark, is_yellow=False):
    icon_theme_folder = "light" if is_dark else "dark"
    if is_yellow:
        icon_theme_folder = "yellow"
    return QPixmap("./static/img/IconPark/" + icon_theme_folder + "/" + icon_position + ".png")

def validate_phone(line_edit, label_prompt):
    """
    校验国内手机号格式
    规则：1开头，第二位3-9，总长度11位数字
    """
    text = line_edit.text()
    # 使用正则表达式校验
    pattern = QRegularExpression("^1[3-9]\\d{9}$")
    if not pattern.match(text).hasMatch():
        label_prompt.setText("<font color='red'>手机号格式不正确</font>")
        return False
    label_prompt.setText("")
    return True

def validate_nickname(line_edit, label_prompt):
    """
    校验昵称
    规则：2-20位，不能包含非法字符
    """
    text = line_edit.text()
    length = len(text)
    if length < 2:
        label_prompt.setText("<font color='red'>昵称太短（至少2位）</font>")
        return False
    elif length > 20:
        label_prompt.setText("<font color='red'>昵称过长（最多20位）</font>")
        return False
    elif not line_edit.hasAcceptableInput():
        label_prompt.setText("<font color='red'>不能包含非法字符</font>")
        return False
    elif " " in text or "\r" in text or "\n" in text:
        label_prompt.setText("<font color='red'>不能包含特殊字符</font>")
        return False
    else:
        label_prompt.setText("")
        return True


def validate_password(line_edit, label_prompt):
    """
    校验密码（简化版）
    规则：10-20位，必须同时包含字母（不区分大小写）和数字
    """
    text = line_edit.text()
    has_letter = any(c.isalpha() for c in text)  # 检查任意字母（不区分大小写）
    has_digit = any(c.isdigit() for c in text)  # 检查数字

    if len(text) < 10:
        label_prompt.setText("<font color='red'>密码太短（至少10位）</font>")
        return False
    elif len(text) > 20:
        label_prompt.setText("<font color='red'>密码太长（至多20位）</font>")
        return False
    elif not (has_letter and has_digit):
        label_prompt.setText("<font color='red'>需包含字母和数字</font>")
        return False
    else:
        label_prompt.setText("")
        return True


def validate_password_check(line_edit=None, line_edit_check=None, label_prompt_check=None):
    """
    校验重复密码
    规则：两次密码需要相同
    """
    if line_edit.text() != line_edit_check.text():
        label_prompt_check.setText("<font color='red'>两次密码不一致</font>")
        return False
    label_prompt_check.setText("")
    return True

def validate_validator_code(line_edit, label_prompt):
    """
    校验验证码格式
    规则：6位数字（常见验证码格式）
    """
    text = line_edit.text()
    # 使用正则表达式校验6位纯数字
    pattern = QRegularExpression("^\\d{6}$")
    if not pattern.match(text).hasMatch():
        label_prompt.setText("<font color='red'>验证码必须是6位数字</font>")
        return False
    label_prompt.setText("")
    return True

def validate_invite_code(line_edit, label_prompt):
    """
    校验邀请码格式
    规则：6位数字或字母（常见邀请码格式）可为空
    """
    text = line_edit.text()
    if text == "":
        label_prompt.setText("")
        return True
    # 使用正则表达式校验6位数字或字母
    pattern = QRegularExpression("^[A-Za-z0-9]{6}$")
    if not pattern.match(text).hasMatch():
        label_prompt.setText("<font color='red'>邀请码必须是6位数字或字母</font>")
        return False
    label_prompt.setText("")
    return True
