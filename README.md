# ui-auto-test
一、框架结构
1、框架结构设计分为四层，自下而上分别为：
    ① 基础工具类base层;
    ② 页面操作pageobject层;
    ③ 测试用例集testcase层;
    ④ 主程序runAll.py。
2.各模块说明
  app - 存放待测apk
  base - 存放基础工具类
  log - 存放日志
  pageobject - 封装页面的操作逻辑和校验逻辑
  tesult - 存放测试结果
  testcase - 存放测试用例
  testdata - 存放测试驱动数据（excel格式）
  config.ini - 配置文件
  runAll.py - 主脚本
