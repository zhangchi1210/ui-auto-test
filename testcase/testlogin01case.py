# encoding: utf-8
import time

from utils.BaseRunner import ParametrizedTestCase
from utils.log import LOG


class LoginTest(ParametrizedTestCase):

    @classmethod
    def setUpClass(cls):
        super(LoginTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(LoginTest, cls).tearDownClass()

    def testopen(self):
        time.sleep(10)
        LOG.info("LoginTest")

    def testclose(self):
        time.sleep(10)
        LOG.info("testclose")
