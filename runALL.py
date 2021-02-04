# encoding: utf-8
import os, random, sys, unittest
from multiprocessing import Pool

import configparser as cfgparser

from testcase.regcasetest import regtest
from utils import ProjectPath
from utils.AppiumServer import AppiumServer
from utils.BaseApk import getPhoneInfo, AndroidDebugBridge, getApkBaseInfo
from utils.Parmeris import Parmer
from utils.log import Log

logger = Log('runAll.py').get_log()

project_path = ProjectPath.get_project_path()  # 项目路径
app_path = os.path.join(project_path, 'app')  # app文件夹路径
config_path = os.path.join(project_path, 'config')  # config文件夹路径
result_path = os.path.join(project_path, 'result')  # result文件夹路径

configPath = os.path.join(config_path, 'config.ini')
cfg = cfgparser.ConfigParser()
cfg.read(configPath, encoding='utf-8')
target_app = cfg.get('TEST_APP', 'target_app')


class AllTest:

    def __init__(self):
        """
            检测待测试APK文件是否存在
        """
        if not target_app:
            logger.error("未指定待测试的APK文件!")
            sys.exit()
        target_app_path = os.path.join(app_path, target_app)
        if not os.path.exists(target_app_path):
            logger.error("未找到指定测试的APK文件!")
            sys.exit()
        else:
            logger.info("开始测试APP：%s..." % target_app)

        """
            检测是否连接移动设备
        """
        l_devices = []
        devices = AndroidDebugBridge().attached_devices()
        if len(devices) > 0:
            for dev in devices:
                app = {
                    "devices": dev,
                    "port": str(random.randint(4593, 4598))
                }
                l_devices.append(app)
        else:
            logger.error("没有可用的安卓设备!")
            sys.exit()

        """
            启动appium
        """
        appium_server = AppiumServer(l_devices)
        appium_server.start_server()

        runnerPool(l_devices, target_app_path)

        """
            判断结果文件result/report.xml是否存在
        """
        if not os.path.exists(result_path):
            os.makedirs(result_path)
        self.resultPath = os.path.join(result_path, "result.xls")

    def run(self):
        pass


def runnerPool(devices, app):
    """
        根据连接的设备生成不同的dict
        然后放到设备的list里面
        设备list的长度产生进程池大小
    """
    app_info = getApkBaseInfo(app)

    devices_pool = []
    for i in range(0, len(devices)):
        _initApp = {
            "deviceName": devices[i]["devices"],
            "udid": devices[i]["devices"],
            "platformVersion": getPhoneInfo(devices=devices[i]["devices"])["release"],
            "platformName": "android",
            "port": devices[i]["port"],
            "appPackage": app_info["packageName"],
            "appActivity": app_info["appActivity"]
        }
        devices_pool.append(_initApp)

    pool = Pool(len(devices_pool))
    pool.map(runnerCaseApp, devices_pool)
    pool.close()
    pool.join()


def runnerCaseApp(devices):
    """
        利用unittest的testsuite来组织测试用例
    """
    test_suit = unittest.TestSuite()
    test_suit.addTest(Parmer.parametrize(regtest,param=devices))#扩展的其他的测试用例均这样添加
    unittest.TextTestRunner(verbosity=2).run(test_suit)

if __name__ == '__main__':
    AllTest().run()
