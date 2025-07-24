import datetime
import calendar
import src.util.time_util


def push_button_copy_now_today_click():
    now = datetime.datetime.now()
    zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                          microseconds=now.microsecond)
    return src.util.time_util.get_datetime_str(zero_today) + "," + src.util.time_util.get_datetime_str(now)


def push_button_copy_now_15m_today_click():
    now = datetime.datetime.now()
    zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                          microseconds=now.microsecond)
    end_today = zero_today + datetime.timedelta(hours=now.hour, minutes=(int(now.minute/15) * 15), seconds=0,
                                          microseconds=now.microsecond)
    return src.util.time_util.get_datetime_str(zero_today) + "," + src.util.time_util.get_datetime_str(end_today)


def push_button_copy_now_month_click(status):
    now = datetime.datetime.now()
    zero_month = datetime.datetime(now.year, now.month, 1)
    if status:
        zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second + 1,
                                              microseconds=now.microsecond)
    else:
        zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                              microseconds=now.microsecond)
    return src.util.time_util.get_datetime_str(zero_month) + "," + src.util.time_util.get_datetime_str(zero_today)


def push_button_copy_now_year_click(status):
    now = datetime.datetime.now()
    zero_year = datetime.datetime(now.year, 1, 1)
    if status:
        zero_month = datetime.datetime(now.year, now.month, 1) - datetime.timedelta(microseconds=1)
    else:
        zero_month = datetime.datetime(now.year, now.month, 1)
    return src.util.time_util.get_datetime_str(zero_year) + "," + src.util.time_util.get_datetime_str(zero_month)


def push_button_copy_today_click(status):
    now = datetime.datetime.now()
    zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
    if status:
        last_today = zero_today + datetime.timedelta(hours=23, minutes=59, seconds=59)
        return src.util.time_util.get_datetime_str(zero_today) + "," + src.util.time_util.get_datetime_str(last_today)
    else:
        last_today = now - datetime.timedelta(days=-1, hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
        return src.util.time_util.get_datetime_str(zero_today) + "," + src.util.time_util.get_datetime_str(last_today)


def push_button_copy_yesterday_click(status):
    now = datetime.datetime.now()
    zero_today = now - datetime.timedelta(days=1, hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
    if status:
        last_today = zero_today + datetime.timedelta(hours=23, minutes=59, seconds=59)
        return src.util.time_util.get_datetime_str(zero_today) + "," + src.util.time_util.get_datetime_str(last_today)
    else:
        last_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
        return src.util.time_util.get_datetime_str(zero_today) + "," + src.util.time_util.get_datetime_str(last_today)


def push_button_copy_current_month_click(status):
    now = datetime.datetime.now()
    zero_month = datetime.datetime(now.year, now.month, 1)
    if status:
        last_month = datetime.datetime(zero_month.year, zero_month.month,
                                       calendar.monthrange(zero_month.year, zero_month.month)[1], hour=23, minute=59, second=59)
        return src.util.time_util.get_datetime_str(zero_month) + "," + src.util.time_util.get_datetime_str(last_month)
    else:
        last_month = (datetime.datetime(zero_month.year, zero_month.month,
                                       calendar.monthrange(zero_month.year, zero_month.month)[1], hour=0, minute=0, second=0)
                      + datetime.timedelta(hours=24, minutes=0, seconds=0))
        return src.util.time_util.get_datetime_str(zero_month) + "," + src.util.time_util.get_datetime_str(last_month)


def push_button_copy_last_month_click(status):
    now = datetime.datetime.now()
    zero_month = datetime.datetime(now.year, now.month, 1) - datetime.timedelta(days=1)
    zero_month = datetime.datetime(zero_month.year, zero_month.month, 1)
    if status:
        last_month = datetime.datetime(zero_month.year, zero_month.month,
                                       calendar.monthrange(zero_month.year, zero_month.month)[1], hour=23, minute=59, second=59)
        return src.util.time_util.get_datetime_str(zero_month) + "," + src.util.time_util.get_datetime_str(last_month)
    else:
        last_month = (datetime.datetime(zero_month.year, zero_month.month,
                                       calendar.monthrange(zero_month.year, zero_month.month)[1], hour=0, minute=0, second=0)
                      + datetime.timedelta(hours=24, minutes=0, seconds=0))
        return src.util.time_util.get_datetime_str(zero_month) + "," + src.util.time_util.get_datetime_str(last_month)


def push_button_copy_current_year_click(status):
    now = datetime.datetime.now()
    zero_year = datetime.datetime(now.year, 1, 1)
    if status:
        last_year = datetime.datetime(zero_year.year, zero_year.month,
                                       calendar.monthrange(zero_year.year, zero_year.month)[1], hour=23, minute=59, second=59)
        return src.util.time_util.get_datetime_str(zero_year) + "," + src.util.time_util.get_datetime_str(last_year)
    else:
        last_year = (datetime.datetime(zero_year.year, zero_year.month,
                                       calendar.monthrange(zero_year.year, zero_year.month)[1], hour=0, minute=0, second=0)
                      + datetime.timedelta(hours=24, minutes=0, seconds=0))
        return src.util.time_util.get_datetime_str(zero_year) + "," + src.util.time_util.get_datetime_str(last_year)


def push_button_copy_last_year_click(status):
    now = datetime.datetime.now()
    zero_year = datetime.datetime(now.year - 1, 1, 1)
    if status:
        last_year = datetime.datetime(zero_year.year, zero_year.month,
                                       calendar.monthrange(zero_year.year, zero_year.month)[1], hour=23, minute=59, second=59)
        return src.util.time_util.get_datetime_str(zero_year) + "," + src.util.time_util.get_datetime_str(last_year)
    else:
        last_year = (datetime.datetime(zero_year.year, zero_year.month,
                                       calendar.monthrange(zero_year.year, zero_year.month)[1], hour=0, minute=0, second=0)
                      + datetime.timedelta(hours=24, minutes=0, seconds=0))
        return src.util.time_util.get_datetime_str(zero_year) + "," + src.util.time_util.get_datetime_str(last_year)