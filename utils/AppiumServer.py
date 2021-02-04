# encoding: utf-8
import os, urllib.request
from multiprocessing import Process
import threading, time, platform, subprocess

from utils.log import Log

logger = Log('AppiumServer.py').get_log()


class RunServer(threading.Thread):  # 启动服务的线程

    def __init__(self, cmd):
        threading.Thread.__init__(self)
        self.cmd = cmd

    def run(self):
        os.system(self.cmd)


class AppiumServer(object):  # 启动appium服务

    def __init__(self, kwargs):
        self.kwargs = kwargs

    def run(self, url):
        time.sleep(10)
        logger.info("测试访问：%s..." % url)
        response = urllib.request.urlopen(url, timeout=5)
        if str(response.getcode()).startswith("2"):
            return True

    def start_server(self):
        for i in range(0, len(self.kwargs)):
            cmd = "appium --session-override -p %s -U %s" % (
                self.kwargs[i]["port"], self.kwargs[i]["devices"])
            logger.info("执行命令 '%s' ..." % cmd)
            if platform.system() == "Windows":  # windows下启动server
                t1 = RunServer(cmd)
                p = Process(target=t1.start())
                p.start()
                while True:
                    time.sleep(4)
                    url = "http://127.0.0.1:" + self.kwargs[i]["port"] + "/wd/hub/status"
                    if self.run(url):
                        logger.info("-------在 win 上启动 appium server 成功--------------")
                        break

    def stop_server(devices: list):
        sysstr = platform.system()
        if sysstr == 'Windows':
            os.popen("taskkill /f /im node.exe")
        else:
            for device in devices:
                cmd = "lsof -i :{0}".format(device["port"])
                plist = os.popen(cmd).readlines()
                plisttmp = plist[1].split("    ")
                plists = plisttmp[1].split(" ")
                os.popen("kill -9 {0}".format(plists[0]))
