# encoding: utf-8
import os, random, sys, unittest, subprocess
from multiprocessing import Pool

import configparser as cfgparser

from testcase.regcasetest import Regtest
from utils import ProjectPath
from utils.AppiumServer import AppiumServer
from utils.BaseApk import getPhoneInfo, AndroidDebugBridge, getApkBaseInfo
from utils.Parmeris import Parmer
from utils.log import LOG, logger
from utils.BaseError import *


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
        """检测待测试APK文件是否存在"""
        if not target_app:
            raise BaseErorr("未指定待测试的APK文件!")
        target_app_path = os.path.join(app_path, target_app)
        if not os.path.exists(target_app_path):
            raise BaseErorr("未找到指定测试的APK文件!")
        else:
            LOG.info("开始测试APP：%s..." % target_app)

        """检测是否连接移动设备"""
        self.l_devices = []
        devices = AndroidDebugBridge().attached_devices()
        if len(devices) > 0:
            for dev in devices:
                app = {
                    "devices": dev,
                    "port": "4723"
                }
                self.l_devices.append(app)
        else:
            raise BaseErorr("没有可用的安卓设备!")

        """获取Apk基本信息"""
        self.app_info = getApkBaseInfo(target_app_path)

        """向移动设备中安装Apk文件"""
        pool_app_list = []
        for i in range(0, len(self.l_devices)):
            pool_app_list.append(
                {"device": self.l_devices[i]["devices"], "info": self.app_info, "path": target_app_path}
            )
        pool = Pool(len(pool_app_list))
        pool.map(installApp, pool_app_list)
        pool.close()
        pool.join()

        """启动appium"""
        appium_server = AppiumServer(self.l_devices)
        appium_server.start_server()

        """判断结果文件result/report.xml是否存在"""
        if not os.path.exists(result_path):
            os.makedirs(result_path)
        self.resultPath = os.path.join(result_path, "result.xls")

    def run(self):
        runnerPool(self.l_devices, self.app_info)

        """关闭Appium服务"""
        appium_server = AppiumServer(self.l_devices)
        appium_server.stop_server()


def runnerPool(devices, app_info):
    """
        根据连接的设备生成不同的dict
        然后放到设备的list里面
        设备list的长度产生进程池大小
    """
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

    LOG.info("进程数量：%s" % len(devices_pool))
    pool = Pool(len(devices_pool))
    # """运行测试用例"""
    pool.map(runnerCaseApp, devices_pool)
    pool.close()
    pool.join()


def installApp(app_dict):
    """
        判断移动设备中是否安装App
    """
    app = app_dict["path"]
    app_info = app_dict["info"]
    device = app_dict["device"]
    cmd = 'adb -s %s shell pm list packages | find "%s"' % (device, app_info["packageName"])
    LOG.info("设备：%s，执行命令：%s" % (device, cmd))
    phone_info = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).stdout.readlines()
    if phone_info:
        LOG.info("设备：%s，已安装App: %s" % (device, app_info["packageName"]))

        """卸载App"""
        cmd_uninstall = "adb -s %s uninstall %s" % (device, app_info["packageName"])
        LOG.info("设备：%s，执行命令：%s" % (device, cmd_uninstall))
        result = subprocess.Popen(
            cmd_uninstall, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        ).stdout.readlines()
        if result[0].decode().strip() == "Success":
            LOG.info("设备：%s，成功卸载App！" % device)
        else:
            raise BaseErorr("设备：%s，卸载App失败!" % device)
    else:
        LOG.info("设备：%s，未安装App: %s" % (device, app_info["packageName"]))

    """安装Apk文件"""
    cmd_install = "adb -s %s install %s" % (device, app)
    LOG.info("设备：%s，执行命令：%s" % (device, cmd_install))
    result = subprocess.Popen(
        cmd_install, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).stdout.readlines()
    if result[-1].decode().strip() == "Success":
        LOG.info("设备：%s，成功安装Apk文件！" % device)
    else:
        raise BaseErorr("设备：%s，安装App失败!" % device)


def runnerCaseApp(devices):
    """
        利用unittest的testsuite来组织测试用例
    """
    test_suit = unittest.TestSuite()
    test_suit.addTest(Parmer.parametrize(Regtest, param=devices))  # 扩展的其他的测试用例均这样添加
    unittest.TextTestRunner(verbosity=2).run(test_suit)


if __name__ == '__main__':
    try:
        AllTest().run()
        sys.exit(0)
    except Exception as e:
        LOG.error("运行程序失败，原因：%s" % e)
        sys.exit(1)

