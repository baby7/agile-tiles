# -*- coding: utf-8 -*-
import sys
import logging
import datetime
import src.util.time_util as time_util


def print_message(level, message):
    sys.stdout.write("[{}] [{}] {}".format(time_util.get_datetime_str(datetime.datetime.now()), level, message) + '\n')


class Logger:
    base_level = None
    def __init__(self, path, base_level=logging.DEBUG, cmd_level=logging.DEBUG, file_level=logging.DEBUG):
        self.logger = logging.getLogger(path or "default_logger")
        self.logger.setLevel(base_level)
        self.base_level = base_level
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')

        # 设置CMD日志
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(cmd_level)
        self.logger.addHandler(sh)

        # 如果提供了日志文件路径，则设置文件日志
        if path:
            fh = logging.FileHandler(path, encoding='utf-8')
            fh.setFormatter(fmt)
            fh.setLevel(file_level)
            self.logger.addHandler(fh)

    def debug(self, message):
        if self.base_level <= logging.DEBUG:
            print_message("DEBUG", message)
        self.logger.debug(message)
        print("[{}] [{}] {}".format(time_util.get_datetime_accurate_str(datetime.datetime.now()), "DEBUG", message) + '\n')

    def info(self, message):
        if self.base_level <= logging.INFO:
            print_message("INFO", message)
        self.logger.info(message)

    def warning(self, message):
        if self.base_level <= logging.WARNING:
            print_message("WARNING", message)
        self.logger.warning(message)

    def error(self, message):
        if self.base_level <= logging.ERROR:
            print_message("ERROR", message)
        self.logger.error(message)

    def card_debug(self, card_title, message):
        self.debug("卡片[{}]:{}".format(card_title, message))

    def card_info(self, card_title, message):
        self.info("卡片[{}]:{}".format(card_title, message))

    def card_warning(self, card_title, message):
        self.warning("卡片[{}]:{}".format(card_title, message))

    def card_error(self, card_title, message):
        self.error("卡片[{}]:{}".format(card_title, message))
