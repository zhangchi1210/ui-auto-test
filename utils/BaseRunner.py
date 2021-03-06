# encoding: utf-8
import unittest
from appium import webdriver

from utils.log import LOG

'''
uittest的再次封装
'''


class ParametrizedTestCase(unittest.TestCase):
    """ TestCase classes that want to be parametrized should
        inherit from this class.
    """
    def __init__(self, methodName='runTest', params=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        global devices
        devices = params

    @classmethod
    def setUpClass(cls):
        # cls.data_path = devices['data_path']
        cls.driver = appium_desired_caps(devices)
        LOG.info('>>> A test_suite is starting <<<')

    @classmethod
    def tearDownClass(cls):
        cls.driver.close_app()
        LOG.info('>>> A test_suite is finished <<<')


def appium_desired_caps(device):
    des_caps = {
        'platformName': 'Android',
        'deviceName': device['deviceName'],
        'udid': device['deviceName'],
        'appPackage': device['appPackage'],
        'appActivity': device['appActivity'],
        'automationName': 'UiAutomator2'
    }
    LOG.info('desired_caps: %s' % des_caps)
    remote = 'http://127.0.0.1:%s/wd/hub' % device['port']
    LOG.info(remote)
    driver = webdriver.Remote(remote, des_caps)
    LOG.info('driver start-up successful!')
    return driver

