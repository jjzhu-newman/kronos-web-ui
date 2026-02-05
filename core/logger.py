"""
日志记录系统模块
提供统一的日志记录功能
"""

import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from typing import Optional


class Logger:
    """日志记录器类"""

    def __init__(
        self,
        name: str = "KronosUI",
        log_dir: str = None,
        level: str = "INFO",
        console: bool = True,
        file: bool = True,
        max_bytes: int = 10485760,  # 10MB
        backup_count: int = 5
    ):
        """
        初始化日志记录器

        Args:
            name: 日志记录器名称
            log_dir: 日志目录
            level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            console: 是否输出到控制台
            file: 是否输出到文件
            max_bytes: 单个日志文件最大字节数
            backup_count: 保留的备份文件数量
        """
        self.name = name
        self.log_dir = log_dir
        self.level = getattr(logging, level.upper(), logging.INFO)
        self.console = console
        self.file = file
        self.max_bytes = max_bytes
        self.backup_count = backup_count

        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """设置日志记录器"""
        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)

        # 清除现有的处理器
        logger.handlers.clear()

        # 创建日志格式
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 控制台处理器
        if self.console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self.level)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        # 文件处理器
        if self.file and self.log_dir:
            # 确保日志目录存在
            os.makedirs(self.log_dir, exist_ok=True)

            # 应用日志文件
            app_log_file = os.path.join(self.log_dir, 'app.log')
            app_handler = RotatingFileHandler(
                app_log_file,
                maxBytes=self.max_bytes,
                backupCount=self.backup_count,
                encoding='utf-8'
            )
            app_handler.setLevel(self.level)
            app_handler.setFormatter(formatter)
            logger.addHandler(app_handler)

            # 错误日志文件（只记录ERROR及以上级别）
            error_log_file = os.path.join(self.log_dir, 'error.log')
            error_handler = RotatingFileHandler(
                error_log_file,
                maxBytes=self.max_bytes,
                backupCount=self.backup_count,
                encoding='utf-8'
            )
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(formatter)
            logger.addHandler(error_handler)

        return logger

    def debug(self, message: str):
        """记录DEBUG级别日志"""
        self.logger.debug(message)

    def info(self, message: str):
        """记录INFO级别日志"""
        self.logger.info(message)

    def warning(self, message: str):
        """记录WARNING级别日志"""
        self.logger.warning(message)

    def error(self, message: str, exc_info: bool = False):
        """记录ERROR级别日志"""
        self.logger.error(message, exc_info=exc_info)

    def critical(self, message: str, exc_info: bool = False):
        """记录CRITICAL级别日志"""
        self.logger.critical(message, exc_info=exc_info)

    def exception(self, message: str):
        """记录异常信息（包含堆栈跟踪）"""
        self.logger.exception(message)


# 全局日志实例
_logger_instance: Optional[Logger] = None


def setup_logger(
    name: str = "KronosUI",
    log_dir: str = None,
    level: str = "INFO",
    console: bool = True,
    file: bool = True
) -> Logger:
    """
    设置全局日志记录器

    Args:
        name: 日志记录器名称
        log_dir: 日志目录
        level: 日志级别
        console: 是否输出到控制台
        file: 是否输出到文件

    Returns:
        Logger实例
    """
    global _logger_instance
    _logger_instance = Logger(
        name=name,
        log_dir=log_dir,
        level=level,
        console=console,
        file=file
    )
    return _logger_instance


def get_logger() -> Optional[Logger]:
    """
    获取全局日志记录器实例

    Returns:
        Logger实例，如果未设置则返回None
    """
    return _logger_instance


def log_info(message: str):
    """快捷方式：记录INFO级别日志"""
    if _logger_instance:
        _logger_instance.info(message)


def log_warning(message: str):
    """快捷方式：记录WARNING级别日志"""
    if _logger_instance:
        _logger_instance.warning(message)


def log_error(message: str, exc_info: bool = False):
    """快捷方式：记录ERROR级别日志"""
    if _logger_instance:
        _logger_instance.error(message, exc_info=exc_info)


def log_debug(message: str):
    """快捷方式：记录DEBUG级别日志"""
    if _logger_instance:
        _logger_instance.debug(message)


def log_exception(message: str):
    """快捷方式：记录异常信息"""
    if _logger_instance:
        _logger_instance.exception(message)
