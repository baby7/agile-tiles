# -*- coding: utf-8 -*-
import os
from PySide6.QtGui import QIcon, QAction, QPixmap, Qt
from PySide6.QtWidgets import QMenu, QSystemTrayIcon

from src.client import common
from src.ui import style_util
from src.util import browser_util


# 设置图标
def set_icon(main_object):
    main_object.sys_icon = QIcon(":static/img/icon/icon.ico")
    main_object.sys_icon_pixmap = QPixmap(":static/img/icon/icon.png")
    main_object.setWindowIcon(main_object.sys_icon)


# 设置托盘图标和菜单
def set_tray_menu(main_object):
    menu = QMenu(main_object)
    menu.addAction(QAction(u'打开官网', main_object, icon=style_util.get_icon_by_path("Base/home"), triggered=open_index_url))
    menu.addAction(QAction(u'开源地址', main_object, icon=style_util.get_icon_by_path("Brand/github-one"), triggered=open_open_source_url))
    menu.addSeparator()
    menu.addAction(QAction(u'用户协议', main_object, icon=style_util.get_icon_by_path("Office/agreement"), triggered=open_user_agreement_url))
    menu.addAction(QAction(u'隐私政策', main_object, icon=style_util.get_icon_by_path("Peoples/personal-privacy"), triggered=open_privacy_policy_url))
    menu.addSeparator()
    menu.addAction(QAction(u'版本信息', main_object, icon=style_util.get_icon_by_path("Communicate/message"), triggered=main_object.open_update_view))
    menu.addAction(QAction(u'关于我们', main_object, icon=style_util.get_icon_by_path("Character/info"), triggered=lambda : open_about_us_url(main_object)))
    menu.addSeparator()
    menu.addAction(QAction(u'显示/隐藏', main_object, icon=style_util.get_icon_by_path("Base/lightning"), triggered=main_object.show_hide_form))
    menu.addAction(QAction(u'取消操作', main_object, icon=style_util.get_icon_by_path("Edit/back"), triggered=lambda : hide_tray_icon_menu(main_object)))
    menu.addSeparator()
    menu.addAction(QAction(u'退出软件', main_object, icon=style_util.get_icon_by_path("Base/power"), triggered=lambda : main_object.quit_before(False)))
    menu.setStyleSheet("""
    QMenu {
        background-color: #f0f0f0;
        color: black;
        border: 1px solid #cccccc;
        border-radius: 10px;
        padding: 3px;
    }
    QMenu::item {
        margin: 0px 5px 0px 5px;
        padding: 5px;
        background-color: transparent;
    }
    QMenu::item:selected {
        background-color: #c0c0c0;
        border-radius: 5px;
    }""")
    # 不设置Popup则列表不能弹出；不设置FramelessWindowHint则不能无边框；不设置NoDropShadowWindowHint则有阴影
    menu.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint | Qt.WindowType.NoDropShadowWindowHint)
    # 设置背景透明，否则qss透明度不生效
    menu.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    # 设置菜单
    main_object.tray_icon = QSystemTrayIcon(main_object)
    main_object.tray_icon.setIcon(main_object.sys_icon)
    main_object.tray_icon.setToolTip("灵卡面板")
    main_object.tray_icon.setContextMenu(menu)
    main_object.tray_icon.activated.connect(main_object.show_hide_form)
    main_object.tray_icon.show()


# 设置托盘图标
def set_tray_icon(main_object):
    main_object.tray_icon.setIcon(main_object.sys_icon)
    main_object.tray_icon.show()

def hide_tray_icon_menu(main_object):
    main_object.tray_icon.contextMenu().hide()

def open_index_url():
    browser_util.open_url(common.index_url)

def open_open_source_url():
    browser_util.open_url(common.open_source_url)

def open_user_agreement_url():
    browser_util.open_url(common.user_agreement_url)

def open_privacy_policy_url():
    browser_util.open_url(common.privacy_policy_url)

def open_about_us_url(main_object):
    # 不能放到上面引用，否则会报错
    from src.module.About.about_us import AboutUsWindow
    main_object.setting_about_us_win = AboutUsWindow(None, main_object)
    main_object.setting_about_us_win.refresh_geometry(main_object.toolkit.resolution_util.get_screen(main_object))
    main_object.setting_about_us_win.show()
