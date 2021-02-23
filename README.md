# ui-auto-test
## 一、运行环境
### 1、appium安装(`appium-server`)
* 安装nodejs，官网`http://nodejs.cn/download/`
* 使用命令("`npm install -g appium`")安装appium
* 安装appium-doctor("`npm install -g appium-doctor`")
* 运行appium-doctor命令("`appium-doctor`")，快速检查appium的环境问题
### 2、jdk安装
* 下载地址：`https://www.oracle.com/java/technologies/javase/javase-jdk8-downloads.html`
* 设置JDK的环境变量，高级系统设置->环境变量->添加jdk/jre的安装路径(jdk\bin和jre\bin)
<br>CLASSPATH： `.;%JAVA_HOME%\lib;%JAVA_HOME%\lib\tools.jar;`
<br>PATH： `;%JAVA_HOME%\bin;%JAVA_HOME%\jre\bin;`
### 3、Android-sdk下载安装
* 下载地址：`https://www.androiddevtools.cn/` ，建议选择zip文件直接解压
* 双击 `SDK manager.exe` 进行选择安装
* 设置sdk的环境变量，把”\platform-tools“和”\tools”路径追加到系统环境变量Path中
<br>ANDROID_HOME： `D:\android\android-sdk`
<br>PATH： `;%ANDROID_SDK_HOME%\platform-tools;%ANDROID_SDK_HOME%\tools;`
### 3、python-client安装(`appium-client`)
### 4、移动设备(`逍遥模拟器`)
* 下载地址：`https://www.xyaz.cn/`
* 将模拟器文件`..\Microvirt\MEmu\adb.exe`替换sdk中文件`..\android-sdk-windows\platform-tools\adb.exe`
## 二、框架结构
### 1、框架原理
框架结构设计分为4层，自下而上分别为：对象库`base`层、页面操作`page`层、测试用例集`testcase`层和主程序`runAll.py`。
### 2.各模块说明
* app - 存放待测apk
* config - 存放配置文件
* log - 存放日志
* page - 通过base页，添加定位元素，将Base页封装的方法拿来调用
* result - 存放测试结果
* testcase - 通过page页调用方法来实现用例
* untils - 存放基础工具类
* runAll.py - 主脚本
