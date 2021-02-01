# encoding: utf-8
import datetime,os

from utils import getprojectpath
from utils.appiumserver import AppiumServer
from utils.baseapk import AndroidDebugBridge
from utils.log import LOG

project_path = getprojectpath.get_project_path()
result_path = os.path.join(project_path, 'result')
config_path = os.path.join(project_path, 'config')
l_devices = []


'''主运行文件'''
class AllTest:


    def __init__(self):
        global resultPath
        # result/report.xml
        if not os.path.exists(result_path):
            os.makedirs(result_path)
        resultPath = os.path.join(result_path, "result.xls")

    def run(self):
        LOG.info("测试开始执行...")
        start_time = datetime.datetime.now()
        devicess = AndroidDebugBridge().attached_devices()
        if len(devicess) > 0:
            for dev in devicess:
                app = {}
                app["devices"] = dev
                app["port"] = "4723"
                l_devices.append(app)
                appium_server = AppiumServer(l_devices)
                appium_server.start_server()  # 启动服务

        else:
            LOG.info("没有可用的安卓设备")



if __name__ == '__main__':
    AllTest().run()