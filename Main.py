#!/usr/bin/env python
# -*-coding:utf-8 -*-

from BuildApkTask import *


""" 本地打包任务入口 """
def startBuildApkTask():

    """
    # taskId                       任务ID
    # gameName                     游戏名称
    # gameId                       游戏ID
    # gameVersion                  游戏版本
    # gameApkName                  游戏母包名称
    # channelName                  渠道名称
    # channelId                    渠道ID
    # channelVersion               渠道版本
    # isLocal                      是否是本地打包(区分服务器打包,主要处理差异化配置)
    # signId                       签名文件ID，默认为0, 本地桌面打包默认设置为1
    # keystore                     签名文件名称,为默认
    # alias                        签名文件别名，为默认
    # storepass                    签名文件密码，为默认
    # keypass                      签名文件别名密码，为默认

    """

    # 基准包任务
    task = BuildApkTask('180', 'TESTGame', '1', '1.0.0', 'GameSDKFrame.apk', 'lexiang' '1', '1.0.0')
    # 开始打包任务
    task.buildApk()


""" 主函数入口 """
if __name__ == '__main__':
    startBuildApkTask()