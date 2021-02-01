# coding:utf-8


class BaseErorr(Exception):
    pass


class FileNotFoundError(BaseErorr):

    def __init__(self, path):
        self.path = path

    def __str__(self):
        error_msg = "'%s' is not found." % self.path
        return error_msg

