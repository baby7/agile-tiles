#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
    name:       动画和分辨率工具
    by:         baby7
    blog:       https://www.baby7blog.com
    annotation: 分辨率参数初始化和动画执行
"""
import time
from functools import partial

from PySide6 import QtCore, QtGui
from win32api import GetMonitorInfo, MonitorFromPoint
from PySide6.QtCore import QSequentialAnimationGroup, QPropertyAnimation, QRect, QEasingCurve
from PySide6.QtWidgets import QApplication


def get_windows_width_and_height(main_window):
    desktop = get_screen(main_window)
    return desktop.size().width(), desktop.size().height()

def get_screen(main_window):
    desktop = QApplication.screens()[0]
    for screen in QApplication.screens():
        if not hasattr(main_window, 'form_screen_name'):
            break
        if screen.name() == main_window.form_screen_name:
            return screen
    return desktop


def init_resolution(main_window, is_first=True):
    """
    初始化分辨率参数
    :param main_window: 主窗口
    :param is_first: 是否第一次初始化
    """
    # 初始化界面和固定大小
    if is_first:
        main_window.setupUi(main_window)
    # 先加载初始值
    load_data(main_window)
    # 显示屏幕
    screen_name = main_window.form_screen_name
    desktop_size = QApplication.screens()[0].size()
    desktop_geometry = QApplication.screens()[0].geometry()
    if screen_name is not None:
        for screen in QApplication.screens():
            if screen.name() == screen_name:
                print(f"显示器信息：{screen.name()}")
                desktop_size = screen.size()
                desktop_geometry = screen.geometry()
    main_window.desktop_width = desktop_size.width()
    main_window.desktop_height = desktop_size.height()
    # 屏幕信息
    monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
    monitor = monitor_info.get('Monitor')  # 屏幕分辨率
    work = monitor_info.get('Work')  # 工作区间
    # 缩放比例
    scaling = monitor[2] / main_window.desktop_width
    # 任务栏高度
    main_window.taskbar_height = int(int(monitor[3] - work[3]) / scaling)
    # 初始化位置
    main_window.screen_x = desktop_geometry.x()
    main_window.screen_y = desktop_geometry.y()
    print(f"显示器位置：{desktop_geometry}")
    if main_window.form_locate == "Right":
        main_window.move(main_window.screen_x + main_window.desktop_width - main_window.width(), main_window.screen_y)
    else:
        main_window.move(main_window.screen_x, main_window.screen_y)
    # 初始化大小
    new_width = main_window.CARD_WIDTH * main_window.form_width + main_window.CARD_INTERVAL * (main_window.form_width + 1)
    main_window.resize(new_width, main_window.desktop_height - main_window.taskbar_height)
    # 退出
    out_animation(main_window)


def load_data(main_window):
    """
    加载初始值
    :param main_window: 主窗口
    """
    if (main_window.main_data is None or main_window.main_data["data"] is None
            or main_window.main_data["data"]["SettingCard"] is None
            or main_window.main_data["data"]["SettingCard"][main_window.hardware_id] is None):
        return
    setting_data = main_window.main_data["data"]["SettingCard"][main_window.hardware_id]
    # 选择的屏幕
    main_window.form_screen_name = setting_data['screenName']
    # 窗口位置
    main_window.form_locate = setting_data['windowPosition']
    # 窗口弹出动画类型
    main_window.form_animation_type = setting_data['formAnimationType']
    # 窗口弹出动画时间
    main_window.form_animation_time = setting_data['formAnimationTime']
    # 是否启用侧边弹出功能
    main_window.form_enable_sidebar = setting_data["wakeUpByMouse"]
    # 侧边弹出动画时间
    main_window.form_enable_sidebar_time = setting_data["wakeUpByMouseTime"]
    # 鼠标离开隐藏窗口
    main_window.form_hide_type = setting_data["wakeUpByMouseHide"]
    # 菜单栏位置
    main_window.form_menu_locate = setting_data['menuPosition']
    # 字体
    main_window.form_font_name = setting_data['fontName']
    # 大小
    main_window.form_width = setting_data["width"]
    main_window.form_height = setting_data["height"]


def in_animation(main_window):
    """
    进入动画
    :param main_window: 主窗口
    :return:
    """
    # print("进入动画")
    # 当前时间戳
    current_time = int(round(time.time() * 1000))
    # 上次时间戳
    last_time = main_window.animation_time
    # 相隔0.35秒内不进行动画
    if current_time - last_time < main_window.form_animation_time:
        return
    # 记录动画时间戳
    main_window.animation_time = current_time
    main_window.show_form = True
    # 加载动画类型
    if main_window.form_animation_type == "Line":
        animation_type = QEasingCurve.Linear
    else:
        animation_type = QEasingCurve.OutBack
    if main_window.form_locate == "Right":
        # 右侧从右到左
        start_animation(
            main_window,
            main_window.desktop_width,
            0,
            main_window.desktop_width - main_window.width(),
            0,
            animation_type
        )
    else:
        # 左侧从左到右
        start_animation(
            main_window,
            0 - main_window.width(),
            0,
            0,
            0,
            animation_type
        )
    # 通知卡片退出动画
    main_window.notify_card_show_form()


def out_animation(main_window):
    """
    退出动画
    :param main_window: 主窗口
    :return:
    """
    # print("退出动画")
    # 当前时间戳
    current_time = int(round(time.time() * 1000))
    # 上次时间戳
    last_time = main_window.animation_time
    # 相隔0.35秒内不进行动画
    if current_time - last_time < main_window.form_animation_time:
        return
    # 记录动画时间戳
    main_window.animation_time = current_time
    main_window.show_form = False
    # 加载动画类型
    if main_window.form_animation_type == "Line":
        animation_type = QEasingCurve.Linear
    else:
        animation_type = QEasingCurve.InBack
    if main_window.form_locate == "Right":
        # 右侧从左到右
        start_animation(
            main_window,
            main_window.desktop_width - main_window.width(),
            0,
            main_window.desktop_width,
            0,
            animation_type
        )
    else:
        # 左侧从右到左·
        start_animation(
            main_window,
            0,
            0,
            0 - main_window.width(),
            0,
            animation_type
        )
    # 通知卡片退出动画
    main_window.notify_card_hide_form()


def start_animation(main_window, start_x, start_y, end_x, end_y, animation_type=None):
    """
    动画执行
    :param main_window: 主窗口
    :param start_x: 初始点x
    :param start_y: 初始点y
    :param end_x: 结束点x
    :param end_y: 结束点y
    :param animation_type: 动画类型
    :return:
    """
    main_window.group = QSequentialAnimationGroup()
    animation = QPropertyAnimation(main_window, b'geometry')
    animation.setDuration(main_window.form_animation_time)  # 持续时间
    animation.setStartValue(QRect(main_window.screen_x + start_x, main_window.screen_y + start_y, main_window.width(), main_window.height()))
    animation.setEndValue(QRect(main_window.screen_x + end_x, main_window.screen_y + end_y, main_window.width(), main_window.height()))
    animation.setEasingCurve(animation_type)
    main_window.group.addAnimation(animation)
    main_window.group.start()

"""-------------------------------------------鼠标检测窗口开始--------------------------------------------------"""
def init_mouse_detect_window(main_window):
    # 鼠标追踪
    main_window.setMouseTracking(True)
    # 鼠标检测定时器
    main_window.mouse_check_timer = QtCore.QTimer(main_window)
    main_window.mouse_check_timer.timeout.connect(partial(check_mouse_position, main_window))
    main_window.mouse_check_timer.start(50)  # 每100ms检测一次
    # 隐藏窗口的延迟定时器
    main_window.hide_timer = QtCore.QTimer(main_window)
    main_window.hide_timer.setSingleShot(True)
    main_window.hide_timer.timeout.connect(partial(check_hide_window, main_window))

def check_mouse_position(main_window):
    if not main_window.form_enable_sidebar:
        return
    """ 检测鼠标位置并触发窗口显示/隐藏 """
    if not main_window.isVisible():
        return
    cursor_pos = QtGui.QCursor.pos()
    x = cursor_pos.x()
    y = cursor_pos.y()
    screen_width = main_window.desktop_width
    edge_margin = 5  # 右侧边缘检测区域宽度
    # 判断是否在右侧边缘区域中央
    in_edge = False
    if main_window.form_locate == "Right":
        if x >= (screen_width - edge_margin + main_window.screen_x) and (100 + main_window.screen_y) <= y <= (main_window.desktop_height - 100 + main_window.screen_y):
            in_edge = True
    else:
        if x <= (edge_margin + main_window.screen_x) and (100 + main_window.screen_y) <= y <= (main_window.desktop_height - 100 + main_window.screen_y):
            in_edge = True
    current_time = int(round(time.time() * 1000))
    try:
        # 窗口未显示时检测边缘区域
        if not main_window.show_form and in_edge:
            if main_window.last_time_in_edge is None:
                main_window.last_time_in_edge = current_time
            if current_time - main_window.last_time_in_edge > main_window.form_enable_sidebar_time:
                trigger_show_animation(main_window)
                main_window.last_time_in_edge = current_time
            else:
                return
        # 窗口已显示时检测是否离开
        elif main_window.show_form:
            window_pos = main_window.mapFromGlobal(cursor_pos)
            in_window = main_window.rect().contains(window_pos)
            if not in_window and not in_edge:
                main_window.hide_timer.start(50)  # 延迟500ms隐藏
        main_window.last_time_in_edge = current_time
    except Exception as e:
        print(f"check_mouse_position error: {str(e)}")

def check_hide_window(main_window):
    if not main_window.form_enable_sidebar:
        return
    """ 延迟隐藏窗口的最终检查 """
    cursor_pos = QtGui.QCursor.pos()
    x = cursor_pos.x()
    y = cursor_pos.y()
    screen_width = main_window.desktop_width
    edge_margin = 5
    # 判断是否在右侧边缘区域中央
    in_edge = False
    if main_window.form_locate == "Right":
        if x >= (screen_width - edge_margin + main_window.screen_x) and (100 + main_window.screen_y) <= y <= (main_window.desktop_height - 100 + main_window.screen_y):
            in_edge = True
    else:
        if x <= (edge_margin + main_window.screen_x) and (100 + main_window.screen_y) <= y <= (main_window.desktop_height - 100 + main_window.screen_y):
            in_edge = True
    window_pos = main_window.mapFromGlobal(cursor_pos)
    in_window = main_window.rect().contains(window_pos)
    if main_window.form_hide_type == "Forever":
        main_window.is_mouse_trigger = True
    if main_window.show_form and not in_window and not in_edge and main_window.is_mouse_trigger:
        trigger_hide_animation(main_window)

def trigger_show_animation(main_window):
    """ 触发显示动画 """
    # 如果登录窗口展示则不处理动画
    if main_window.start_login_view:
        return
    if not main_window.show_form:
        # print("鼠标触发,显示窗口")
        main_window.toolkit.resolution_util.in_animation(main_window)
        main_window.refresh_window_show()
        main_window.is_mouse_trigger = True

def trigger_hide_animation(main_window):
    """ 触发隐藏动画 """
    # 如果登录窗口展示则不处理动画
    if main_window.start_login_view:
        return
    if main_window.show_form:
        # print("鼠标触发,隐藏窗口")
        main_window.toolkit.resolution_util.out_animation(main_window)
        main_window.is_mouse_trigger = False
