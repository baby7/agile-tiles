#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
    name:       日期时间工具
    by:         baby7
    blog:       https://www.baby7blog.com
    annotation: 日期时间工具
"""
import time
import cnlunar
import datetime
from zhdate import ZhDate


def get_datetime_str(in_datetime=datetime.datetime.now()):
    """
    获取当前日期时间的字符串
    :param in_datetime: 时间
    """
    return str(in_datetime.strftime("%Y-%m-%d %H:%M:%S"))

def get_datetime_str_by_timestamp(timestamp):
    """
    获取时间戳对应的日期时间字符串
    :param timestamp: 时间戳,例如:1716426823229
    """
    return str(datetime.datetime.fromtimestamp(timestamp / 1000).strftime("%Y-%m-%d %H:%M:%S"))

def get_datetime_accurate_str(in_datetime=datetime.datetime.now()):
    """
    获取当前日期时间的精确字符串
    :param in_datetime: 时间
    """
    return str(in_datetime.strftime("%Y-%m-%d %H:%M:%S.%f"))


def get_datetime_hour_str(in_datetime=datetime.datetime.now()):
    """
    获取当前日期时间的格式化小时的字符串
    :param in_datetime: 时间
    """
    in_datetime = in_datetime + datetime.timedelta(hours=1)
    return str(in_datetime.strftime("%Y-%m-%d %H:00:00"))


def get_date_str(in_datetime=datetime.datetime.today()):
    """
    获取当前日期的字符串
    :param in_datetime: 日期
    """
    return str(in_datetime.strftime("%Y-%m-%d"))


def get_time_str(in_datetime=datetime.datetime.now()):
    """
    获取当前时间的字符串
    :param in_datetime: 时间
    """
    return str(in_datetime.strftime("%H:%M:%S"))


def get_week_str(in_datetime=datetime.datetime.today()):
    """
    获取当前周几的字符串
    :param in_datetime: 日期
    """
    return f"周{list('一二三四五六日')[in_datetime.weekday()]}"


def get_chinese_date_str(in_datetime=datetime.datetime.today()):
    """
    获取当前日期时间的字符串
    :param in_datetime: 日期
    """
    return str(in_datetime.strftime("%Y年%m月%d日"))


def get_lunar_calendar_str(in_datetime=datetime.datetime.today()):
    """
    返回农历字符串
    :param in_datetime: 日期
    :return: 例如: 癸卯兔年 农历正月十四
    """
    date4 = ZhDate.from_datetime(in_datetime)
    str_long = str(date4.chinese())[5:].replace("年 (", "").replace(")", "").replace("二十", "廿").replace("三十", "卅")
    return str_long.split(" ")[1] + " 农历" + str_long.split(" ")[0]


def get_constellation(in_datetime=datetime.datetime.today()):
    """
    获取星座
    :param in_datetime: 日期
    :return: 例如：巨蟹座
    """
    constellation = ['魔羯', '水瓶', '双鱼', '牡羊', '金牛', '双子', '巨蟹', '狮子', '处女', '天秤', '天蝎', '射手']
    cutoff_days = (20, 19, 21, 21, 21, 22, 23, 23, 23, 23, 22, 22)
    _month = in_datetime.month - (1 if in_datetime.day < cutoff_days[in_datetime.month - 1] else 0)
    _month = _month if _month < 12 else 0
    return constellation[_month] + "座"


def get_week_by_year():
    """
    获取这周是今年的第几周
    """
    return "第 " + str(int(time.strftime("%W")) + 1) + " 周"


def get_holiday(in_datetime=datetime.datetime.today()):
    """
    获取节气
    """
    return str(cnlunar.Lunar(in_datetime).todaySolarTerms).replace("无", "")
