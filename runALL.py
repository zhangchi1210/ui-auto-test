# encoding: utf-8
import datetime, os, sys

import configparser as cfgparser

from utils import getprojectpath
from utils.appiumserver import AppiumServer
from utils.baseapk import AndroidDebugBridge
from utils.log import Log

logger = Log('runAll.py').get_log()

project_path = getprojectpath.get_project_path()  # 项目路径
app_path = os.path.join(project_path, 'app')  # app文件夹路径
config_path = os.path.join(project_path, 'config')  # config文件夹路径
result_path = os.path.join(project_path, 'result')  # result文件夹路径

configPath = os.path.join(config_path, 'config.ini')
cfg = cfgparser.ConfigParser()
cfg.read(configPath, encoding='utf-8')
target_app = cfg.get('TEST_APP', 'target_app')

l_devices = []


class AllTest:

    def __init__(self):
        if not target_app:
            logger.error("未指定待测试的APK文件!")
            sys.exit()
        elif not os.path.exists(os.path.join(app_path, target_app)):
            logger.error("未找到指定测试的APK文件!")
            sys.exit()
        else:
            logger.info("开始测试APP：%s..."%target_app)

        # result/report.xml
        if not os.path.exists(result_path):
            os.makedirs(result_path)
        self.resultPath = os.path.join(result_path, "result.xls")

    def run(self):
        logger.info("测试开始执行...")
        # start_time = datetime.datetime.now()
        # devicess = AndroidDebugBridge().attached_devices()
        # if len(devicess) > 0:
        #     for dev in devicess:
        #         app = {}
        #         app["devices"] = dev
        #         app["port"] = "4723"
        #         l_devices.append(app)
        #         appium_server = AppiumServer(l_devices)
        #         appium_server.start_server()  # 启动服务
        # else:
        #     LOG.info("没有可用的安卓设备")


if __name__ == '__main__':
    AllTest().run()
