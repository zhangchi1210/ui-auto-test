# encoding: utf-8
import unittest

'''
uittest的再次封装
'''


class Parmer(unittest.TestCase):

    def __init__(self, methodName='runTest', parme=None):
        super(Parmer, self).__init__(methodName)
        self.parme = parme

    def parametrize(testcase_class, param=None):
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_class)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_class(methodName=name, parm=param))
        return suite

