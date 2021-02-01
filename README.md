# ui-auto-test
## 一、框架结构
### 1、框架原理
框架结构设计分为4层，自下而上分别为：对象库`base`层、页面操作`page`层、测试用例集`testcase`层和主程序`runAll.py`。
### 2.各模块说明
* app - 存放待测apk
* base - 存放与对网页的一些基础操作并进行封装Base页适用于整个项目
* config - 存放配置文件
* log - 存放日志
* page - 通过base页，添加定位元素，将Base页封装的方法拿来调用
* result - 存放测试结果
* testcase - 通过page页调用方法来实现用例
* testdata - 存放测试驱动数据（excel格式）
* untils - 存放基础工具类
* runAll.py - 主脚本
