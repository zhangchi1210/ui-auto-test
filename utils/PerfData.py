# encoding: utf-8
from utils.log import LOG
import platform, os

'''
获取配置相关手机性能的数据
'''


def getsystemsta():
	"""根据所运行的系统获取adb不一样的筛选条件"""
	system = platform.system()
	if system == 'Windows':
		find_manage = 'findstr'
	else:
		find_manage = 'grep'
	return find_manage


find = getsystemsta()


def getcpu(packagename, devices):
	"""这里采集的cpu时候可以是执行操作采集 就是-n  -d  刷新间隔"""
	LOG.info('采集cpu信息')
	try:
		cpu = 'adb -s %s shell top -n 1| %s %s'%(devices,find,packagename)
		re_cpu = os.popen(cpu).read().split()[2]
		return re_cpu
	except:
		pass


def getnencun(devices, packagename):
	"""Total 的实际使用过物理内存"""
	LOG.info('获取使用的物理内存信息')
	try:
		cpu = 'adb -s %s shell top -n 1| %s %s' % (devices,find, packagename)
		re_cpu = os.popen(cpu).read().split()[6]
		re_cpu_m = str(round(int(re_cpu[:-1])/1024)) + 'M'
		return re_cpu_m
	except:
		pass