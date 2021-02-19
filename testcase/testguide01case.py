# encoding: utf-8
import time

from utils.log import LOG
from utils.BaseRunner import ParametrizedTestCase
from page.GuidePage import GuidePage


class GuideTest(ParametrizedTestCase):

    def testguide(self):
        time.sleep(10)
        guide = GuidePage(self.driver)

        for i in range(0, 2):
            time.sleep(3)
            guide.scrollLeft()
            guide.scrollRight()
            guide.scrollLeft()
        time.sleep(3)

        guide.clickButton()
        time.sleep(10)

        # 断言
        result = guide.check()
        self.assertEqual(result, True)

    @classmethod
    def setUpClass(cls):
        super(GuideTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(GuideTest, cls).tearDownClass()
