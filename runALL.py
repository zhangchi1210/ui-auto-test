# encoding: utf-8
import os, random, sys, unittest, subprocess
from multiprocessing import Pool

import configparser as cfgparser
from utils.HTMLTestRunner import HTMLTestRunner

from utils import ProjectPath
from utils.AppiumServer import AppiumServer
from utils.BaseApk import getPhoneInfo, AndroidDebugBridge, getApkBaseInfo
from utils.BaseRunner import ParametrizedTestCase
from utils.log import LOG
from utils.BaseError import *


project_path = ProjectPath.get_project_path()  # 项目路径
app_path = os.path.join(project_path, 'app')  # app文件夹路径
config_path = os.path.join(project_path, 'config')  # config文件夹路径
case_path = os.path.join(project_path, 'testcase')  # testcase文件夹路径
result_path = os.path.join(project_path, 'result')  # result文件夹路径

configPath = os.path.join(config_path, 'config.ini')
caseListPath = os.path.join(config_path, "case.ini")
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

    def runnerPool(self):
        """
            根据连接的设备生成不同的dict
            然后放到设备的list里面
            设备list的长度产生进程池大小
        """
        devices_pool = []
        for i in range(0, len(self.l_devices)):
            _initApp = {
                "deviceName": self.l_devices[i]["devices"],
                "udid": self.l_devices[i]["devices"],
                "platformVersion": getPhoneInfo(devices=self.l_devices[i]["devices"])["release"],
                "platformName": "android",
                "port": self.l_devices[i]["port"],
                "appPackage": self.app_info["packageName"],
                "appActivity": self.app_info["appActivity"]
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
    execute_case_list = set_case_list()
    suite_module = []
    print("运行测试用例：")
    for case in execute_case_list:
        num = execute_case_list.index(case) + 1
        case_name = case.split("/")[-1]  # 通过split函数来将aaa/bbb分割字符串，-1取后面，0取前面
        print("\t%s.%s" % (num, case_name))  # 打印出取出来的名称
        discover = unittest.defaultTestLoader.discover(case_path, pattern=case_name + '.py', top_level_dir=None)
        suite_module.append(discover)

    ParametrizedTestCase(params=devices)

    test_suite = unittest.TestSuite()
    if len(suite_module) > 0:  # 判断suite_module元素组是否存在元素
        for suite in suite_module:  # 如果存在，循环取出元素组内容，命名为suite
            for test_name in suite:  # 从discover中取出test_name，使用addTest添加到测试集
                test_suite.addTest(test_name)
    else:
        print('else:')
        return None

    if not os.path.exists(result_path):
        os.makedirs(result_path)
    report_path = os.path.join(result_path, 'result_%s.html' % devices["deviceName"].split(":")[1])
    with(open(report_path, 'wb')) as fp:
        runner = HTMLTestRunner(
            stream=fp,
            verbosity=2,
            title='Ui Auto Test Report'
        )
        runner.run(test_suite)
    LOG.info("测试报告:%s" % report_path)


def set_case_list():
    """
        读取caselist.txt文件中的用例名称，并添加到caselist元素组
    :return:
    """
    execute_case_list = []
    with open(caseListPath) as f:
        for value in f.readlines():
            data = str(value)
            if data != '' and not data.startswith("#"):  # 如果data非空且不以#开头
                execute_case_list.append(data.replace("\n", ""))  #读取每行数据会将换行转换为\n，去掉每行数据中的\n
    return execute_case_list


def run():
    try:
        all_test = AllTest()
        all_test.runnerPool()
    except Exception as e:
        LOG.error("运行程序失败，原因：%s" % e)
    finally:
        """关闭Appium服务"""
        appium_server = AppiumServer(all_test.l_devices)
        appium_server.stop_server()
        sys.exit()


if __name__ == '__main__':
    run()

