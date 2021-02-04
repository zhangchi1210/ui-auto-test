# -*- coding: utf-8 -*-
import os, time, logging

from utils import ProjectPath

# create the log_path
now = time.strftime('%Y%m%d%H%M%S')
project_path = ProjectPath.get_project_path()  # 项目路径
log_path = os.path.join(project_path, 'log')  # log文件夹路径
if not os.path.exists(log_path):
    os.mkdir(log_path)


class Log(object):

    """定义日志类"""

    def __init__(self, _name):
        """
        初始化logger
        :param _name: 写每条log的名字
        """
        # structure a logger
        self.logger = logging.getLogger(_name)
        self.logger.setLevel(logging.INFO)

        # create a log file handler
        fh = logging.FileHandler(os.path.join(log_path, now + '.log'), encoding='utf-8')
        fh.setLevel(logging.INFO)

        # create a log terminal handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # define logger output format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # logger add handler function
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def get_log(self):
        """
        return logger
        :return:
        """
        return self.logger


if __name__ == '__main__':

    logger = Log('lidi').get_log()
    logger.info('lidi test logger')

