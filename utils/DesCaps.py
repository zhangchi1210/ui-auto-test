# encoding: utf-8


def make_des(Testplatform, Testdevicesname, TestappPackage, TestappActivity):
    des_caps = {
        'platformName': Testplatform,
        'deviceName': Testdevicesname,
        'udid': Testdevicesname,
        'appPackage': TestappPackage,
        'appActivity': TestappActivity,
        'automationName': 'UiAutomator2'
    }
    return des_caps