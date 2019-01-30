# PackageApkTool

## 项目介绍
PackageApkTool 为手游SDK联运系统打包系统部分核心模块，用于快速便捷的帮助游戏包打入渠道SDK资源生成游戏-渠道包，快速上架渠道上线。


## 项目前提
使用该项目的前提条件是，游戏包体已经接入手游SDK框架Demo的SDK接口及申请好了对应的渠道参数信息。

* 关于手游SDK的相关资源说明:
* 手游SDK — 第一篇（序言）
* 手游SDK — 第二篇（SDK架构设计篇）
* 手游SDK — 第三篇（SDK架构设计代码实现篇（上）- 基础库）
* 手游SDK — 第四篇（SDK架构设计代码实现篇（下）- 项目需求开发）

及开源项目地址：
[手游SDK框架Demo](https://github.com/Bzaigege/GameSDKFrameDemo)



## 项目实现功能

* 实现游戏和渠道assets/libs/res/AndroidManifest.xml资源的动态合并
* 渠道资源及参数的自动化修改及支持多种类型解析及修改，如xml/text/ini/pro/json等类型文件
* 游戏Icon和渠道角标的合并
* 游戏闪屏和渠道闪屏逻辑兼容处理
* 支持动态修改游戏的minSdk、TargetSdk、包名等配置
* 支持第三方库多包名R文件资源引用
* 打包过程的日志信息显示


## 项目功能使用

首先下载PackageApkTool项目中的DeskDemo.zip和PackageResource.zip两个压缩包，解压后，目录结构如下：

DeskDemo： 

![image text](https://github.com/Bzaigege/PackageApkTool/blob/master/git/DeskDemoDir.png)

uiconfig和WorkSpace为目录，UIMain.exe为可执行文件

PackageResource：

![image text](https://github.com/Bzaigege/PackageApkTool/blob/master/git/PackageResourceDir.png)

build_config.json 为打包编译参数配置，可根据不同的渠道需求定制不同的key_value值

GameSDKFrame.apk 为模拟已接入测试渠道SDK的游戏母包

lexiang_1_1.0.0.zip 为渠道资源包，格式为：渠道名_渠道ID_渠道版本。 内置为渠道资源目录

启动UIMain.exe后依次选择资源。然后打包运行。

![image text](https://github.com/Bzaigege/PackageApkTool/blob/master/git/%E6%89%93%E5%8C%85.gif)

### build_config.json 配置文件说明：
编译过程用到的参数都可以在这里配置对饮的Key_Value值，但是涉及到渠道参数的配置的时候，需要修改渠道适配代码读取Key值
[代码地址](https://github.com/Bzaigege/PackageApkTool/tree/master/channel/special)

### 渠道资源包 说明：
格式为：渠道名_渠道ID_渠道版本。 内置为渠道资源目录 
![image text](https://github.com/Bzaigege/PackageApkTool/blob/master/git/channelresource.png)

* assets 为渠道assets资源目录，与游戏assets目录合并
* config 为配置文件资源目录，可根据需求拓展
* icon 为渠道角标资源目录，与游戏自有Icon合并
* libs 为渠道.jar和.so文件资源目录，与游戏lib目录合并
* res 为渠道res资源目录,与游戏res资源目录合并
* splash 为渠道闪屏资源目录，打包时，拷贝到assets对应目录下
* wxcallback 为渠道处理微信登录、支付特殊处理的类文件，打包时会编译成jar文件，最终打包到游戏包内
* AndroidManifest.xml 为渠道配置文件，与游戏AndroidManifest.xml合并


## 资源参考

* [手游SDK — 第五篇（游戏打包篇（上）- 打包系统设计）](https://www.jianshu.com/p/e86e106304d3)
* [手游SDK — 第六篇（游戏打包篇（中）- 自动化打包）](https://www.jianshu.com/p/e75dceb6c7f2)
* [手游SDK — 第七篇（游戏打包篇（下）- 自动化打包踩坑记录）](https://www.jianshu.com/p/16f852b3aabb)



