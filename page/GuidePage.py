# encoding: utf-8

from utils.BaseOperate import BaseOperate
from utils.log import LOG


class GuidePage(object):

    def __init__(self, driver):
        self.operate = BaseOperate(driver)

    def scrollLeft(self):
        self.operate.swipeLeft(200)
        LOG.info('>>> slide left <<<')

    def scrollRight(self):
        self.operate.swipeRight(200)
        LOG.info('>>> slide right <<<')

    def clickButton(self):
        el = self.operate.find_element("desc", u"立即体验")
        el.click()
        LOG.info(u">>> click '立即体验' button <<<")

    def check(self):
        try:
            el = self.operate.find_element("desc", u"添加云手机")
            # print(el)
            return True
        except Exception as e:
            return False

