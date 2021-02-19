# encoding: utf-8
from utils.BaseError import *


class BaseOperate(object):

    def __init__(self, driver):
        self.driver = driver

    def swipeLeft(self, t):  # 向左滑行swipLeft
        l = self.getSize()
        x1 = int(l[0] * 0.75)
        y1 = int(l[1] * 0.5)
        x2 = int(l[0] * 0.25)
        self.driver.swipe(x1, y1, x2, y1, t)

    def swipeRight(self, t):  # 向右滑行swipLeft
        l = self.getSize()
        x1 = int(l[0] * 0.25)
        y1 = int(l[1] * 0.5)
        x2 = int(l[0] * 0.75)
        self.driver.swipe(x1, y1, x2, y1, t)

    def swipeUp(self, t):  # 向上滑动
        l = self.getSize()
        x1 = int(l[0] * 0.5)
        y1 = int(l[1] * 0.75)
        y2 = int(l[1] * 0.25)
        self.driver.swipe(x1, y1, x1, y2, t)

    def swipeDown(self, t):  # 向下滑动
        l = self.getSize()
        x1 = int(l[0] * 0.5)
        y1 = int(l[1] * 0.25)
        y2 = int(l[1] * 0.75)
        self.driver.swipe(x1, y1, x1, y2, t)

    def find_element(self, _type, location):
        if _type == 'desc':
            el = self.driver.find_element_by_accessibility_id(location)
        return el

    def getSize(self):
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return (x, y)

