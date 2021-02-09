# encoding: utf-8
import os, urllib.request
from multiprocessing import Process
import threading, time, platform

from utils.log import LOG
from utils.BaseError import *


class RunServer(threading.Thread):  # 启动服务的线程

    def __init__(self, cmd):
        threading.Thread.__init__(self)
        self.cmd = cmd

    def run(self):
        os.system(self.cmd)


class AppiumServer(object):  # 启动appium服务

    def __init__(self, kwargs):
        self.kwargs = kwargs

    def start_server(self):
        for i in range(0, len(self.kwargs)):
            cmd = "appium --session-override -p %s -U %s" % (
                self.kwargs[i]["port"], self.kwargs[i]["devices"])
            if platform.system() == "Windows":  # windows下启动server
                LOG.info("执行命令 '%s' ..." % cmd)
                t1 = RunServer(cmd)
                p = Process(target=t1.start())
                p.start()
                while True:
                    time.sleep(4)
                    url = "http://127.0.0.1:" + self.kwargs[i]["port"] + "/wd/hub/status"
                    if test_web(url):
                        LOG.info("-------在 win 上启动 appium server 成功--------------")
                        break

    def stop_server(self):
        systemstr = platform.system()
        if systemstr == "Windows":
            for i in range(0, len(self.kwargs)):
                port = self.kwargs[i]["port"]
                pid = get_pid(port)
                if pid:
                    # 执行被占用端口的pid
                    cmd_kill = 'taskkill -f -pid "%s"' % pid
                    LOG.info("端口：%s，执行命令 '%s' ..." % (port, cmd_kill))
                    try:
                        os.popen(cmd_kill)
                    except Exception as err:
                        raise BaseErorr("关闭Appium服务失败，原因：%s" % err)
                    LOG.info("端口：%s，apppium-server is killed!" % port)
                    break
                else:
                    raise BaseErorr("关闭Appium服务失败，端口'%s'未启用！" % port)


def test_web(url):
    time.sleep(10)
    flag = False
    LOG.info("测试访问：%s..." % url)
    response = urllib.request.urlopen(url, timeout=5)
    if str(response.getcode()).startswith("2"):
        flag = True
    return flag


def get_pid(port):
    pid = None
    cmd_find = 'netstat -aon | findstr "%s"' % port
    LOG.info("执行命令 '%s' ..." % cmd_find)
    result = os.popen(cmd_find)
    pid_list = result.readlines()
    if pid_list != "":
        for pid_info in pid_list:
            pid_info = pid_info.strip()
            if "LISTENING" in pid_info:
                pid = pid_info.split(" ")[-1]
    return pid