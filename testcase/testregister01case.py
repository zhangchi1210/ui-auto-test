# encoding: utf-8
import time

from utils.BaseRunner import ParametrizedTestCase
from utils.log import LOG


class RegisterTest(ParametrizedTestCase):

    @classmethod
    def setUpClass(cls):
        super(RegisterTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(RegisterTest, cls).tearDownClass()

    def testrpen(self):
        time.sleep(10)
        LOG.info("RegisterTest")
