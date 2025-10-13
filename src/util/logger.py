# -*- coding: utf-8 -*-
import sys
import logging
import logging.handlers
import datetime
import src.util.time_util as time_util


def print_message(level, message):
    sys.stdout.write("[{}] [{}] {}".format(time_util.get_datetime_str(datetime.datetime.now()), level, message) + '\n')


class Logger:
    base_level = None
    def __init__(self, path, base_level=logging.DEBUG, cmd_level=logging.DEBUG, file_level=logging.DEBUG,
                 max_bytes=5*1024*1024, backup_count=5):
        """
        初始化日志器
        :param path: 日志文件路径
        :param base_level: 基础日志级别
        :param cmd_level: 控制台日志级别
        :param file_level: 文件日志级别
        :param max_bytes: 单个日志文件最大大小（字节），默认5MB
        :param backup_count: 备份文件数量，默认5个
        """
        self.logger = logging.getLogger(path or "default_logger")
        self.logger.setLevel(base_level)
        self.base_level = base_level
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')

        # 清除已有的handler，避免重复
        if self.logger.handlers:
            self.logger.handlers.clear()

        # 设置CMD日志
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(cmd_level)
        self.logger.addHandler(sh)

        # 如果提供了日志文件路径，则设置文件日志（使用RotatingFileHandler）
        if path:
            # 使用RotatingFileHandler，按文件大小轮转
            fh = logging.handlers.RotatingFileHandler(
                path,
                encoding='utf-8',
                maxBytes=max_bytes,      # 文件最大大小
                backupCount=backup_count # 备份文件数量
            )
            fh.setFormatter(fmt)
            fh.setLevel(file_level)
            self.logger.addHandler(fh)

    def debug(self, message):
        if self.base_level <= logging.DEBUG:
            print_message("DEBUG", message)
        self.logger.debug(message)

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