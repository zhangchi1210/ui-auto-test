# encoding: utf-8

from utils.BaseOperate import BaseOperate
from utils.log import LOG


class LoginPage(object):

    def __init__(self, driver):
        self.operate = BaseOperate(driver)

    def enterAccount(self, account):
        el = self.operate.find_element("text", u"请输入手机号码")
        el.sendKeys(account)

    def enterPwd(self, pwd):
        el = self.operate.find_element("text", u"请输入密码")
        el.sendKeys(pwd)

    def clickButton(self):
        el = self.operate.find_element("desc", u"登录")
        el.click()
        LOG.info(u">>> click '登录' button <<<")

