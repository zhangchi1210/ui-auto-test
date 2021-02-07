# encoding: utf-8
import re, subprocess, os
from utils.log import LOG

'''
apk文件的读取信息
'''


def getApkBaseInfo(path):
    """获取Apk的一些基本信息"""
    cmd = "aapt dump badging %s" % path
    LOG.info("执行命令：%s" % cmd)
    p = subprocess.Popen(cmd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         stdin=subprocess.PIPE,
                         shell=True
                         )
    (output, err) = p.communicate()

    match = re.compile("package: name='(\S+)' versionCode='(\d+)' versionName='(\S+)'").match(output.decode())
    if not match:
        raise Exception("can't get packageinfo")
    packagename = match.group(1)
    appKey = match.group(2)
    appVersion = match.group(3)

    # 启动类
    match = re.compile("launchable-activity: name='(\S+)'").search(output.decode())
    if match is not None:
        appActivity = match.group(1)

    # 应用名字
    match = re.compile("application-label:'(\S+)'").search(output.decode())
    if match is not None:
        appName = match.group(1)

    base_info = {
        "packageName": packagename,
        "appKey": appKey,
        "appVersion": appVersion,
        "appActivity": appActivity,
        "appName": appName
    }
    LOG.info("Apk基本信息：%s" % base_info)
    return base_info


def getPhoneInfo(devices):
    """获取设备的一些基本信息"""
    cmd = "adb -s " + devices + " shell cat /system/build.prop"
    LOG.info("执行命令：%s" % cmd)
    phone_info = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).stdout.readlines()
    release = "ro.build.version.release="  # 版本
    model = "ro.product.model="  # 型号
    brand = "ro.product.brand="  # 品牌
    device = "ro.product.device="  # 设备名
    result = {"release": release}
    for line in phone_info:
        for i in line.split():
            temp = i.decode()
            if temp.find(release) >= 0:
                result["release"] = temp[len(release):]
                break
            if temp.find(model) >= 0:
                result["model"] = temp[len(model):]
                break
            if temp.find(brand) >= 0:
                result["brand"] = temp[len(brand):]
                break
            if temp.find(device) >= 0:
                result["device"] = temp[len(device):]
                break
    LOG.info("移动设备信息：%s" % result)
    return result


class AndroidDebugBridge(object):

    def call_adb(self, command):
        command_result = ''
        command_text = 'adb %s' % command
        results = os.popen(command_text, "r")
        while 1:
            line = results.readline()
            if not line: break
            command_result += line
        results.close()
        return command_result

    # 拉数据到本地
    def pull(self, remote, local):
        result = self.call_adb("pull %s %s" % (remote, local))
        return result

    # 获取连接的设备
    def attached_devices(self):
        LOG.info("执行命令 'adb devices' ...")
        devices = []
        result = subprocess.Popen("adb devices",
                                  shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE
                                  ).stdout.readlines()
        for item in result:
            t = item.decode().split("\tdevice")
            if len(t) >= 2:
                devices.append(t[0])
        LOG.info("设备信息: %s" % ",".join(devices))
        return devices
