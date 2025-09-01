import os
import time
import datetime

from winotify import Notification


def send_message(app_title, title, descript, url=None):
    """
    发送Win10右下角弹框提醒
    :param app_title: 程序名称
    :param title: 消息标题
    :param descript: 消息内容
    :param url: 点击跳转的地址
    """
    if url is not None:
        Notification(app_id=app_title + " " + str(datetime.datetime.now().strftime("%H:%M:%S")),
                     title=title,
                     msg=descript,
                     icon=":static/img/icon/icon.png",
                     launch=url).show()
    else:
        Notification(app_id=app_title + " " + str(datetime.datetime.now().strftime("%H:%M:%S")),
                     title=title,
                     msg=descript,
                     icon=":static/img/icon/icon.png").show()
    time.sleep(1)
