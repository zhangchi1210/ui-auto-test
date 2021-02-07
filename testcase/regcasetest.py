# encoding: utf-8
import time
from appium import webdriver

from utils.Parmeris import Parmer
from utils.log import LOG
from utils.DesCaps import make_des


class Regtest(Parmer):

    def __init__(self, parm, methodName='runTest'):
        super(Regtest, self).__init__(methodName)
        self.port = parm['port']
        LOG.info(parm)
        self.parm = parm

    """这是reg测试用例"""
    def setUp(self):
        """ setup """
        self.dis_app = make_des(
            Testplatform='Android',
            Testdevicesname=self.parm['deviceName'],
            TestappPackage=self.parm['appPackage'],
            TestappActivity=self.parm['appActivity']
        )
        self.driver = webdriver.Remote('http://127.0.0.1:'+self.port+'/wd/hub', self.dis_app)
        LOG.info('测试用例开始执行...')

    def tearDown(self):
        """ tearDown  """
        LOG.info('测试用例执行完毕，测试环境正在还原！')
        time.sleep(15)
        self.driver.quit()

    def testopen(self):
        print("1")
