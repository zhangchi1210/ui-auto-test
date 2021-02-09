# encoding: utf-8
import time

from utils.log import LOG
from utils.BaseRunner import ParametrizedTestCase


class LoginTest(ParametrizedTestCase):

    def testlogin(self):
        time.sleep(10)
        LOG.info("10")

    @classmethod
    def setUpClass(cls):
        super(LoginTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(LoginTest, cls).tearDownClass()
