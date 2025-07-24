# -*- coding: utf-8 -*-
from PySide6.QtGui import QColor

COLOR_TYPE_HEX = "HEX"
COLOR_TYPE_RGB = "RGB"
COLOR_TYPE_RGBA = "RGBA"


def get_hex_color(index):
    return get_rgb_color(index, COLOR_TYPE_HEX)

def get_rgba_color(index, alpha):
    return get_rgb_color(index, COLOR_TYPE_RGBA, alpha)

def get_rgb_color(index, color_type=COLOR_TYPE_RGB, alpha=1, is_dark=False):
    light_color_list = [
        "#33a3dc",
        "#f36c21",
        "#f173ac",
        "#ef4136",
        "#7fb80e",
        "#4e72b8",
        "#7d5886",
        "#fdb933",
        "#2585a6",
        "#6f599c",
        "#f58220",
    ]
    dark_color_list = [
        "#33a3dc",
        "#f36c21",
        "#f173ac",
        "#ef4136",
        "#7fb80e",
        "#4e72b8",
        "#7d5886",
        "#fdb933",
        "#2585a6",
        "#6f599c",
        "#f58220",
    ]
    if is_dark:
        color_list = dark_color_list
    else:
        color_list = light_color_list
    if color_type == COLOR_TYPE_HEX:
        return color_list[index % len(color_list)]
    elif color_type == COLOR_TYPE_RGB:
        return hex_to_rgb_string(color_list[index % len(color_list)])
    else:
        return hex_to_rgba_string(color_list[index % len(color_list)], alpha)

def hex_to_rgb(hex_color):
    """
    hex格式转rgb格式
    """
    # 去掉可能存在的#符号
    hex_color = hex_color.lstrip('#')
    # 将十六进制字符串转换为RGB元组
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

def hex_to_rgb_string(hex_color):
    """
    hex格式转rgb格式字符串
    """
    # 去掉可能存在的#符号
    hex_color = hex_color.lstrip('#')
    # 将十六进制字符串转换为RGB元组
    rgb_tuple = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    # 将RGB元组格式化为rgb(x, x, x)字符串
    return f"rgb({rgb_tuple[0]}, {rgb_tuple[1]}, {rgb_tuple[2]})"

def hex_to_rgba_string(hex_color, alpha):
    """
    hex格式转rgba格式字符串
    """
    # 去掉可能存在的#符号
    hex_color = hex_color.lstrip('#')
    # 将十六进制字符串转换为RGB元组
    rgb_tuple = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    # 将RGB元组格式化为rgb(x, x, x)字符串
    return f"rgba({rgb_tuple[0]}, {rgb_tuple[1]}, {rgb_tuple[2]}, {alpha})"

def get_prospect_color(is_dark=False, rgb=False, rgba=False, hex=False, hexa=False, qt_type=False):
    if is_dark:
        if rgb:
            return "rgb(239, 240, 241)"
        elif rgba:
            return "rgba(239, 240, 241, 255)"
        elif hex:
            return "#EFF0F1"
        elif hexa:
            return "#EFF0F1FF"
        elif qt_type:
            return QColor(239, 240, 241, 255)
    else:
        if rgb:
            return "rgb(24, 24, 24)"
        elif rgba:
            return "rgba(24, 24, 24, 255)"
        elif hex:
            return "#181818"
        elif hexa:
            return "#181818FF"
        elif qt_type:
            return QColor(24, 24, 24, 255)

def get_background_color(is_dark=False, rgb=False, rgba=False, hex=False, hexa=False, qt_type=False):
    if is_dark:
        if rgb:
            return "rgb(24, 24, 24)"
        elif rgba:
            return "rgba(24, 24, 24, 255)"
        elif hex:
            return "#181818"
        elif hexa:
            return "#181818FF"
        elif qt_type:
            return QColor(24, 24, 24, 255)
    else:
        if rgb:
            return "rgb(239, 240, 241)"
        elif rgba:
            return "rgba(239, 240, 241, 255)"
        elif hex:
            return "#EFF0F1"
        elif hexa:
            return "#EFF0F1FF"
        elif qt_type:
            return QColor(239, 240, 241, 255)
