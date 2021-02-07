# -*- coding: utf-8 -*-
import os, logbook
import logbook.more
from functools import wraps

from utils import ProjectPath

# create the log_path
project_path = ProjectPath.get_project_path()  # 项目路径
LOG_DIR = os.path.join(project_path, 'log')  # log文件夹路径


def logFormate(record, handler):
    formate = "{date} {level} {filename} {lineno} {msg}".format(
        date=record.time,               # 日志时间
        level=record.level_name,            # 日志等级
        filename=os.path.split(record.filename)[-1],  # 文件名
        lineno=record.lineno,             # 行号
        msg=record.message               # 日志内容
        )
    return formate


def initLogger(filename, fileLogFlag=True, stdOutFlag=True):
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    logbook.set_datetime_format('local')
    logger = logbook.Logger(filename)
    logger.handlers = []

    if fileLogFlag:#日志输出到文件
        logFile = logbook.TimedRotatingFileHandler(
            os.path.join(LOG_DIR, '%s.log' % 'log'),
            date_format='%Y-%m-%d',
            bubble=True,
            encoding='utf-8'
        )
        logFile.formatter = logFormate
        logger.handlers.append(logFile)
    if stdOutFlag:#日志打印到屏幕
        logStd = logbook.more.ColorizedStderrHandler(bubble=True)
        logStd.formatter = logFormate
        logger.handlers.append(logStd)
    return logger


LOG = initLogger('log.txt')


def logger(param):
    def wrap(function):
        @wraps(function)
        def _wrap(*args, **kwargs):
            LOG.info("当前模块 {}".format(param))
            LOG.info("全部kwargs参数信息 , {}".format(str(kwargs)))
            return function(*args, **kwargs)
        return _wrap
    return wrap