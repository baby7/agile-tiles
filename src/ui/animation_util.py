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
from PySide6.QtCore import QSequentialAnimationGroup, QPropertyAnimation, QRect, QEasingCurve, QParallelAnimationGroup
from PySide6.QtWidgets import QApplication

ANIMATION_RUN_TIME = 150    # 动画执行时间


def start_line_y_animation(control, start_y, end_y, run_time=ANIMATION_RUN_TIME, curve=QEasingCurve.Type.OutBack):
    """
    动画执行(纵轴移动)
    :param control: 控件
    :param start_y: 初始点y
    :param end_y: 结束点y
    :param run_time: 动画持续时间
    :return:
    """
    start_animation(control, control.x(), start_y, control.width(), control.height(), control.x(), end_y, control.width(), control.height(), run_time, curve)


def start_line_x_animation(control, start_x, end_x, run_time=ANIMATION_RUN_TIME, curve=QEasingCurve.Type.OutBack):
    """
    动画执行(横轴移动)
    :param control: 控件
    :param start_x: 初始点x
    :param end_x: 结束点x
    :param run_time: 动画持续时间
    :return:
    """
    start_animation(control, start_x, control.y(), control.width(), control.height(), end_x, control.y(), control.width(), control.height(), run_time, curve)


def get_line_x_animation(control, start_x, end_x, run_time=ANIMATION_RUN_TIME, curve=QEasingCurve.Type.OutBack):
    """
    动画执行(横轴移动)
    :param control: 控件
    :param start_x: 初始点x
    :param end_x: 结束点x
    :param run_time: 动画持续时间
    :return:
    """
    return get_animation(control, start_x, control.y(), control.width(), control.height(), end_x, control.y(), control.width(), control.height(), run_time, curve)

def start_line_width_animation(control, start_width, end_width, run_time=ANIMATION_RUN_TIME, curve=QEasingCurve.Type.OutBack):
    """
    动画执行(宽度改变)
    :param control: 控件
    :param start_width: 宽度初始值
    :param end_width: 宽度结束值
    :param run_time: 持续时间
    :return:
    """
    start_animation(control, control.x(), control.y(), start_width, control.height(), control.x(), control.y(), end_width, control.height(), run_time, curve)


def start_animation(control, start_x, start_y, start_width, start_height, end_x, end_y, end_width, end_height, run_time, curve=QEasingCurve.Type.OutBack):
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
    control.group = QParallelAnimationGroup()
    animation = QPropertyAnimation(control, b'geometry')
    animation.setDuration(run_time)  # 持续时间
    animation.setStartValue(QRect(start_x, start_y, start_width, start_height))
    animation.setEndValue(QRect(end_x, end_y, end_width, end_height))
    animation.setEasingCurve(curve)     # 动画特效
    control.group.addAnimation(animation)
    control.group.start()


def get_animation(control, start_x, start_y, start_width, start_height, end_x, end_y, end_width, end_height, run_time, curve=QEasingCurve.Type.OutBack):
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
    animation = QPropertyAnimation(control, b'geometry')
    animation.setTargetObject(control)
    animation.setDuration(run_time)  # 持续时间
    animation.setStartValue(QRect(start_x, start_y, start_width, start_height))
    animation.setEndValue(QRect(end_x, end_y, end_width, end_height))
    animation.setEasingCurve(curve)     # 动画特效
    return animation

def start_line_x_and_width_animation(control, start_x, end_x, start_width, end_width, run_time=ANIMATION_RUN_TIME, curve=QEasingCurve.Type.Linear):
    """
    动画执行(宽度和横轴改变)
    :param control: 控件
    :param start_x: 初始点x
    :param end_x: 结束点x
    :param start_width: 宽度初始值
    :param end_width: 宽度结束值
    :param run_time: 持续时间
    :return:
    """
    control.group = QParallelAnimationGroup()
    animation = QPropertyAnimation(control, b'geometry')
    animation.setDuration(run_time)  # 持续时间
    animation.setStartValue(QRect(start_x, control.y(), start_width, control.height()))
    animation.setEndValue(QRect(end_x, control.y(), end_width, control.height()))
    animation.setEasingCurve(curve)     # 动画特效
    control.group.addAnimation(animation)
    control.group.start()

def get_line_x_and_width_animation(control, start_x, end_x, start_width, end_width, run_time=ANIMATION_RUN_TIME, curve=QEasingCurve.Type.Linear):
    """
    动画执行(宽度和横轴改变)
    :param control: 控件
    :param start_x: 初始点x
    :param end_x: 结束点x
    :param start_width: 宽度初始值
    :param end_width: 宽度结束值
    :param run_time: 持续时间
    :return:
    """
    animation = QPropertyAnimation(control, b'geometry')
    animation.setTargetObject(control)
    animation.setDuration(run_time)  # 持续时间
    animation.setStartValue(QRect(start_x, control.y(), start_width, control.height()))
    animation.setEndValue(QRect(end_x, control.y(), end_width, control.height()))
    animation.setEasingCurve(curve)     # 动画特效
    return animation