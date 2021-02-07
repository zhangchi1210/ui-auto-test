# coding:utf-8
import os


def get_project_path():
    parent_path = os.path.split(os.path.realpath(__file__))[0]    # ../utils
    project_path = os.path.dirname(parent_path)    # .../ui-auto-test
    return project_path


if __name__ == '__main__':
    # 执行该文件，测试下是否OK
    print('测试路径是否OK,路径为：', get_project_path())

