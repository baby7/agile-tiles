#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
    name:       动画和分辨率工具
    by:         baby7
    blog:       https://www.baby7blog.com
    annotation: 分辨率参数初始化和动画执行
"""
import time
from win32api import GetMonitorInfo, MonitorFromPoint
from PySide6.QtCore import QSequentialAnimationGroup, QPropertyAnimation, QRect, QEasingCurve
from PySide6.QtWidgets import QApplication

ANIMATION_RUN_TIME = 100    # 动画执行时间


def start_line_y_animation(control, start_y, end_y, run_time=ANIMATION_RUN_TIME):
    """
    动画执行
    :param control: 控件
    :param start_y: 初始点y
    :param end_y: 结束点y
    :param run_time: 动画持续时间
    :return:
    """
    start_animation(control, control.x(), start_y, control.width(), control.height(), control.x(), end_y, control.width(), control.height(), run_time)


def start_line_x_animation(control, start_x, end_x, run_time=ANIMATION_RUN_TIME):
    """
    动画执行
    :param control: 控件
    :param start_x: 初始点x
    :param end_x: 结束点x
    :param run_time: 动画持续时间
    :return:
    """
    start_animation(control, start_x, control.y(), control.width(), control.height(), end_x, control.y(), control.width(), control.height(), run_time)


def start_animation(control, start_x, start_y, start_width, start_height, end_x, end_y, end_width, end_height, run_time):
    """
    动画执行
    :param control: 控件
    :param start_x: 初始点x
    :param start_y: 初始点y
    :param start_width: 初始宽度
    :param start_height: 初始高度
    :param end_x: 结束点x
    :param end_y: 结束点y
    :param end_width: 结束宽度
    :param end_height: 结束高度
    :param run_time: 动画持续时间
    :return:
    """
    control.group = QSequentialAnimationGroup()
    animation = QPropertyAnimation(control, b'geometry')
    animation.setDuration(run_time)  # 持续时间
    animation.setStartValue(QRect(start_x, start_y, start_width, start_height))
    animation.setEndValue(QRect(end_x, end_y, end_width, end_height))
    # animation.setEasingCurve(QEasingCurve.OutBounce)     # 动画特效: 特别弹
    # animation.setEasingCurve(QEasingCurve.OutElastic)     # 动画特效: 特别弹
    # animation.setEasingCurve(QEasingCurve.InBack)     # 动画特效: 弹
    animation.setEasingCurve(QEasingCurve.OutBack)     # 动画特效: 弹
    # animation.setEasingCurve(QEasingCurve.Linear)     # 动画特效: 线性
    control.group.addAnimation(animation)
    control.group.start()