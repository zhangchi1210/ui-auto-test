import os
import logging
import time
from logging.handlers import TimedRotatingFileHandler
from utils import ProjectPath

path = ProjectPath.get_project_path()
log_path = os.path.join(path, 'log')  # 存放log文件的路径


class Logger(object):

    def __init__(self, logger_name='logs'):
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        self.logger = logging.getLogger(logger_name)
        logging.root.setLevel(logging.NOTSET)
        rq = time.strftime('%Y-%m-%d-%H-%M', time.localtime(time.time()))
        self.log_file_name = rq + '.log'  # 日志文件的名称
        self.backup_count = 5  # 最多存放日志的数量
        # 日志输出级别
        self.console_output_level = 'DEBUG'
        self.file_output_level = 'DEBUG'
        # 日志输出格式
        DATE_FORMAT = "%Y-%d-%m %H:%M:%S"
        self.formatter = logging.Formatter(
            '%(asctime)s %(levelname)s %(filename)s %(lineno)s -- %(message)s', DATE_FORMAT
        )

    def get_logger(self):
        """在logger中添加日志句柄并返回，如果logger已有句柄，则直接返回"""
        if not self.logger.handlers:  # 避免重复日志
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)
            console_handler.setLevel(self.console_output_level)
            self.logger.addHandler(console_handler)

            # 每天重新创建一个日志文件，最多保留backup_count份
            file_handler = TimedRotatingFileHandler(
                filename=os.path.join(log_path, self.log_file_name),
                when='H',
                interval=1,
                backupCount=self.backup_count,
                delay=True,
                encoding='utf-8'
            )
            file_handler.setFormatter(self.formatter)
            file_handler.setLevel(self.file_output_level)
            self.logger.addHandler(file_handler)
        return self.logger


LOG = Logger().get_logger()

