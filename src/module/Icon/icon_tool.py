# -*- coding: utf-8 -*-
import os
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QMenu, QSystemTrayIcon

from src.client import common
from src.util import browser_util


# 设置图标
def set_icon(main_object):
    main_object.sys_icon = QIcon(":static/img/icon/icon.ico")
    main_object.setWindowIcon(main_object.sys_icon)


# 设置托盘图标和菜单
def set_tray_menu(main_object):
    menu = QMenu(main_object)
    menu.addAction(QAction(u'灵卡面板官网', main_object, triggered=open_index_url))
    menu.addAction(QAction(u'关于我们', main_object, triggered=lambda : open_about_us_url(main_object)))
    menu.addSeparator()
    menu.addAction(QAction(u'用户协议', main_object, triggered=open_user_agreement_url))
    menu.addAction(QAction(u'隐私政策', main_object, triggered=open_privacy_policy_url))
    menu.addSeparator()
    menu.addAction(QAction(u'更新记录', main_object, triggered=main_object.open_update_view))
    menu.addSeparator()
    menu.addAction(QAction(u'显示/隐藏', main_object, triggered=main_object.show_hide_form))
    menu.addAction(QAction(u'退出', main_object, triggered=lambda : main_object.quit_before(False)))
    menu.setStyleSheet("""
    QMenu{background:white;color:black;}
    QMenu::item:selected:enabled{background: lightgray;}
    """)
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

def open_index_url():
    browser_util.open_url(common.index_url)

def open_user_agreement_url():
    browser_util.open_url(common.user_agreement_url)

def open_privacy_policy_url():
    browser_util.open_url(common.privacy_policy_url)

def open_about_us_url(main_object):
    from src.module.About.about_us import AboutUsWindow
    main_object.setting_about_us_win = AboutUsWindow(None, main_object)
    main_object.setting_about_us_win.refresh_geometry(main_object.toolkit.resolution_util.get_screen(main_object))
    main_object.setting_about_us_win.show()
