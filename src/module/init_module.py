# 基础包
import os
import logging
import winreg

from PySide6.QtCore import Qt
from qframelesswindow.utils import win32_utils as win_utils

from src.constant import current_version_info
# 模块
from src.module.Icon import icon_tool
# 初始化日志
import src.util.logger as logger
from src.ui import style_util


def init_module(main_object):
    # 设置标题栏文字和版本信息
    main_object.app_name = "AgileTiles"
    main_object.app_title = "灵卡面板"
    main_object.app_version = current_version_info.current_version
    main_object.setWindowTitle(main_object.app_title)
    # 初始化日志
    # config_path = str(os.getcwd()) + r"\log.log"
    config_path = None
    main_object.info_logger = logger.Logger(config_path, logging.INFO, logging.DEBUG, logging.DEBUG)
    main_object.info_logger.info(main_object.app_title + "启动中...")
    # 隐藏标题栏
    main_object.titleBar.raise_()
    main_object.titleBar.minBtn.close()
    main_object.titleBar.maxBtn.close()
    main_object.titleBar.closeBtn.hide()
    # 初始化图标和托盘菜单
    icon_tool.set_icon(main_object)
    icon_tool.set_tray_menu(main_object)
    # 默认禁止右键菜单
    main_object.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
    # 其他
    main_object.info_logger.info(main_object.app_title + "启动完成")


def init_style(main_object):
    """
    全局样式
    """
    if main_object.is_first:
        main_object.setStyleSheet("*{outline: none;}")
        # 禁用窗口的手动调整大小功能
        main_object.setResizeEnabled(False)
    # 设置字体
    style_util.set_font_and_right_click_style(main_object, main_object)


def is_light_theme():
    """
    判断Windows当前是否为浅色主题
    返回True表示浅色，False表示深色
    """
    try:
        # 打开注册表键
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        )
        # 读取AppsUseLightTheme的值
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        return value == 1
    except FileNotFoundError:
        # 键不存在时默认返回浅色
        return True
    except Exception as e:
        print(f"读取注册表出错: {e}")
        return True  # 默认返回浅色

def set_theme(main_object, is_main=False):
    # 1. 全局主题设置
    if is_main:
        style_util.set_all_theme(main_object)

    # 2. 背景中的label_background设置
    if main_object.is_dark:
        # 深色
        print(f"{'主窗口' if is_main else '子窗口'}:set_theme:深色")
        # 背景
        if hasattr(main_object, 'label_background'):
            if is_main:
                main_object.label_background.setStyleSheet("background-color: rgb(24, 24, 24); border: none;")
            else:
                main_object.label_background.setStyleSheet("background-color: rgb(24, 24, 24); border-radius: 10px; border: none;")
            main_object.label_background.lower()
            main_object.label_background.resize(main_object.width(), main_object.height())
            main_object.label_background.move(0, 0)
            main_object.label_background.show()
    else:
        # 浅色
        print(f"{'主窗口' if is_main else '子窗口'}:set_theme:浅色")
        if hasattr(main_object, 'label_background'):
            if hasattr(main_object, 'form_theme_transparency'):
                print(f"{'主窗口' if is_main else '子窗口'}:set_theme:浅色:背景")
                transparency = int(main_object.form_theme_transparency * 2.55)
                if is_main:
                    main_object.label_background.setStyleSheet(f"background-color: rgba(200, 200, 200, {transparency}); border: none;")
                else:
                    main_object.label_background.setStyleSheet(f"background-color: rgba(200, 200, 200, {transparency}); border-radius: 10px; border: none;")
                main_object.label_background.lower()
                main_object.label_background.resize(main_object.width(), main_object.height())
                main_object.label_background.move(0, 0)
                main_object.label_background.show()
        if hasattr(main_object, 'form_theme_mode') and main_object.form_theme_mode == "Acrylic":
            # 亚克力
            print(f"{'主窗口' if is_main else '子窗口'}:set_theme:浅色:亚克力")
            # 背景
            if hasattr(main_object, 'label_background'):
                main_object.label_background.hide()
            main_object.setStyleSheet("*{ outline: none; background:transparent; color:rgb(0, 0, 0) };")
        else:
            # 半透明
            print(f"{'主窗口' if is_main else '子窗口'}:set_theme:浅色:半透明")
            main_object.setStyleSheet("*{ outline: none; background:transparent; color:rgb(0, 0, 0) };")

    # 3. 背景中的windowEffect设置(需要幂等控制，主要为了注销再登录时出现的重复设置windowEffect问题，引入theme_idempotence[开始是false，注销前是true])
    if is_main:
        if main_object.theme_idempotence:
            main_object.theme_idempotence = False
            return

    # 设置窗口特效窗体
    form_theme_mode = None
    if hasattr(main_object, 'form_theme_mode'):
        form_theme_mode = main_object.form_theme_mode
    main_object.setFrameless(is_main=is_main, is_dark=main_object.is_dark, form_theme_mode=form_theme_mode)

    print(f"styleSheet:{main_object.styleSheet()}")
