# encoding: utf-8
import time

from utils.log import LOG
from utils.BaseRunner import ParametrizedTestCase
from page.LoginPage import LoginPage


class LoginTest(ParametrizedTestCase):

    def testlogin(self):
        time.sleep(10)
        login = LoginPage(self.driver)

        login.enterAccount("181212011")
        login.enterPwd("123")
        login.clickButton()

    @classmethod
    def setUpClass(cls):
        super(LoginTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(LoginTest, cls).tearDownClass()
