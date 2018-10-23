#!/usr/bin/env python
# -*-coding:utf-8 -*-

import shutil
import json
from BuildApkTools import *
from utils import LogUtils


class BuildApkTask(object):

    """
    # taskId                       任务ID
    # gameName                     游戏名称
    # gameId                       游戏ID
    # gameVersion                  游戏版本
    # gameApkName                  游戏母包名称
    # channelId                    渠道ID
    # channelVersion               渠道版本
    # keystore                     签名文件名称,为默认
    # alias                        签名文件别名，为默认
    # storepass                    签名文件密码，为默认
    # keypass                      签名文件别名密码，为默认

    """

    def __init__(self, taskId, gameName, gameId, gameVersion, gameApkName, channelId, channelVersion,
                 keystore='android.keystore', alias='sg', storepass='s123456', keypass='s123456'):

        self.WorkPath = os.path.dirname(os.path.realpath(__file__))  # 当前运行绝对路径
        self.WorkSpace = os.path.join(self.WorkPath, 'WorkSpace')  # 工作目录

        self.Build = os.path.join(self.WorkSpace, 'BuildApk')  # 打包工作目录
        self.Resources = os.path.join(self.WorkSpace, 'Resources')  # 本地模拟服务器资源目录
        self.Tools = os.path.join(self.WorkSpace, 'Tools')  # 打包工具路径

        # 本地模拟服务器同步信息
        self.originGamesPath = os.path.join(self.Resources, 'Games', gameId, gameVersion)  # 服务器母包
        self.originChannelsPath = os.path.join(self.Resources, 'ChannelSDKs', channelId, channelVersion)  # 服务器SDK资源
        self.originSignsPath = os.path.join(self.Resources, 'Signs', gameId)  # 签名文件
        self.originConfigsPath = os.path.join(self.Resources, 'Configs')  # 打包编译参数

        # 服务器同步资源到本地的资源目录
        self.ResourceData = os.path.join(self.Build, 'ResourceData', taskId)  # 同步数据目录
        self.BaseGameApkPath = os.path.join(self.ResourceData, 'Game', gameId, gameVersion)  # 游戏母包
        self.BaseChannelsDataPath = os.path.join(self.ResourceData, 'Channel', channelId, channelVersion)  # 渠道资源
        self.BaseSignDataPath = os.path.join(self.ResourceData, 'Signs', gameId)  # 签名资源
        self.BaseConfigPath = os.path.join(self.ResourceData, 'Configs', gameId, channelId, channelVersion)  # 打包编译参数

        # 打包过程工作目录
        self.Work = os.path.join(self.Build, 'Work')  # 打包目录
        self.BakPath = os.path.join(self.Work, 'Bak', taskId, gameId, gameVersion)  # 游戏母包反编译解包后路径
        self.TempPath = os.path.join(self.Work, 'Temp', taskId)  # 打包过程缓存路径

        # 打包完成包体输出目录
        self.OutputApkPath = os.path.join(self.Build, 'OutputApk', taskId)  # 输出包体路径

        # 打包过程日志输出目录
        self.logger = LogUtils.init_log(taskId, self.Build, gameName, channelId)

        # 配置其他信息:游戏、渠道、签名、日志
        self.taskId = taskId
        self.gameName = gameName
        self.gameId = gameId
        self.gameVersion = gameVersion
        self.gameApkName = gameApkName
        self.ChannelId = channelId
        self.ChannelVersion = channelVersion

        self.compile_config = {}

        self.keystore = keystore
        self.alias = alias
        self.storepass = storepass
        self.keypass = keypass

    #  开始打包
    def buildApk(self):

        self.logger.info(u'开始打包...')
        self.logger.info(u'任务ID：%s' % self.taskId)
        self.logger.info(u'游戏ID：%s' % self.gameId)
        self.logger.info(u'渠道ID：%s\n' % self.ChannelId)

        #  第一步：复制服务器资源文件
        self.logger.info(u'开始复制游戏母包....')
        if os.path.isdir(self.BaseGameApkPath):
            shutil.rmtree(self.BaseGameApkPath)
        os.makedirs(self.BaseGameApkPath)

        status, result = copy_resource(self.originGamesPath, self.BaseGameApkPath)
        if status == 0:
            self.logger.info(u'复制游戏母包成功')
        else:
            self.logger.info(result)
            self.logger.info(u'复制游戏母包失败')
            return status, result

        self.logger.info(u'开始复制渠道资源....')
        if os.path.isdir(self.BaseChannelsDataPath):
            shutil.rmtree(self.BaseChannelsDataPath)
        os.makedirs(self.BaseChannelsDataPath)

        status, result = copy_resource(self.originChannelsPath, self.BaseChannelsDataPath)
        if status == 0:
            self.logger.info(u'复制渠道资源成功')
        else:
            self.logger.info(result)
            self.logger.info(u'复制渠道资源失败')
            return status, result

        self.logger.info(u'开始复制游戏签名文件....')
        if os.path.isdir(self.BaseSignDataPath):
            shutil.rmtree(self.BaseSignDataPath)
        os.makedirs(self.BaseSignDataPath)

        status, result = copy_resource(self.originSignsPath, self.BaseSignDataPath)
        if status == 0:
            self.logger.info(u'复制游戏签名文件成功\n')
        else:
            self.logger.info(result)
            self.logger.info(u'复制游戏签名文件失败\n')
            return status, result

        #  第二步： 获取打包编译参数
        self.logger.info(u'获取打包编译参数....')
        if os.path.isdir(self.BaseConfigPath):
            shutil.rmtree(self.BaseConfigPath)
        os.makedirs(self.BaseConfigPath)

        status, result = copy_resource(self.originConfigsPath, self.BaseConfigPath)
        if not status == 0:
            self.logger.info(u'复制打包编译参数文件失败\n')
            return 1, u'复制打包编译参数文件失败'

        if not os.path.exists(os.path.join(self.BaseConfigPath, "build_config.json")):
            self.logger.info(u"打包编译参数文件： build_config.json不存在 请检查")
            return 1, u'打包编译参数文件： build_config.json不存在 请检查'

        try:
            with open(os.path.join(self.BaseConfigPath, "build_config.json"), 'r') as build_config:
                compile_config = json.load(build_config)
                self.compile_config = compile_config
                self.logger.info(u"获取打包编译参数成功")
                self.logger.info(u"%s\n" % self.compile_config)

        except Exception as e:
            self.logger.info(e)
            return 1, u'读取配置文件出错'

        # 这里需要处理下，当后台参数build_config没有配置包名时，需读取反编译后的包名
        if not self.compile_config.has_key('package'):
            game_package_name = get_game_apk_package_name(self.TempPath)
            self.compile_config[u'package'] = game_package_name

        #  第三步： 反编译解压游戏母包
        if os.path.isdir(self.BakPath):
            shutil.rmtree(self.BakPath)
        os.makedirs(self.BakPath)

        self.logger.info(u'开始反编译解压游戏母包....')
        status, result = decompile_apk(self.Tools, self.BakPath, os.path.join(self.BaseGameApkPath, self.gameApkName))
        if status == 0:
            self.logger.info(u'反编译解压游戏母包成功')
        else:
            self.logger.info(result)
            self.logger.info(u'反编译解压游戏母包失败')
            return status, result

        self.logger.info(u'开始将反编译文件拷贝到临时目录Temp....')
        if os.path.isdir(self.TempPath):
            shutil.rmtree(self.TempPath)
        os.makedirs(self.TempPath)

        status, result = copy_resource(self.BakPath, self.TempPath)
        if status == 0:
            self.logger.info(u'将反编译文件拷贝到临时目录Temp成功\n')
        else:
            self.logger.info(result)
            self.logger.info(u'将反编译文件拷贝到临时目录Temp失败\n')
            return status, result

        # 第四步：合并资源文件
        self.logger.info(u'开始合并资源....')
        status, result = merge_resources(self.taskId, self.Tools, self.TempPath, self.BaseChannelsDataPath,
                                         self.ChannelId, self.ChannelVersion, self.compile_config)
        if status == 0:
            self.logger.info(u'合并资源成功\n')
        else:
            self.logger.info(result)
            self.logger.info(u'合并资源失败\n')
            return status, result

        # 第五步: 合并Manifest.xml
        self.logger.info(u'开始合并Manifest.xml文件....')
        status, result, package_name = merge_manifest(self.taskId, self.TempPath, self.BaseChannelsDataPath,
                                                      self.ChannelId, self.ChannelVersion, self.compile_config)
        if status == 0:
            self.logger.info(u'合并Manifest.xml文件成功\n')
        else:
            self.logger.info(result)
            self.logger.info(u'合并Manifest.xml文件失败\n')
            return status, result

        # # 第六步： 合并角标
        self.logger.info(u'开始合并角标....')
        status, result = merge_icon(self.TempPath, self.BaseChannelsDataPath)
        if status == 0:
            self.logger.info(u'合并角标成功\n')
        else:
            self.logger.info(result)
            self.logger.info(u'合并角标失败\n')
            return status, result

        # 第七步： 根据资源生成R文件
        self.logger.info(u'开始生成R文件....')
        status, result = create_r_file(self.taskId, self.Tools, self.TempPath, package_name)
        if status == 0:
            self.logger.info(u'生成R文件成功\n')
        else:
            self.logger.info(result)
            self.logger.info(u'生成R文件失败\n')
            return status, result

        # 第八步: 将jar文件转为smali代码
        self.logger.info(u'开始将jar文件转化为smali代码....')
        status, result = jar_compile_smali(self.taskId, self.Tools, self.TempPath)
        if status == 0:
            self.logger.info(u'将jar文件转化为smali代码成功\n')
        else:
            self.logger.info(result)
            self.logger.info(u'将jar文件转化为smali代码失败\n')
            return status, result

        # 第九步：将smail代码打包成apk文件
        self.logger.info(u'开始将smail代码打成apk包....')
        status, result = compile_build_apk(self.taskId, self.Tools, self.TempPath, self.OutputApkPath)
        if status == 0:
            self.logger.info(u'将smail代码打成apk包成功\n')
        else:
            self.logger.info(result)
            self.logger.info(u'将smail代码打成apk包失败\n')
            return status, result

        # 第十步：将apk包签名
        self.logger.info(u'开始将apk包签名....')
        status, result = sign_temp_apk(self.OutputApkPath, self.BaseSignDataPath, self.keystore, self.alias,
                                       self.storepass, self.keypass)
        if status == 0:
            self.logger.info(u'将apk包签名成功\n')
        else:
            self.logger.info(result)
            self.logger.info(u'将apk包签名失败\n')
            return status, result

        # 第十一步：优化签名apk包
        self.logger.info(u'开始优化签名apk包....')
        status, result, final_apk = zipa_sign_apk(self.Tools, self.OutputApkPath, self.gameName,
                                                  self.gameVersion, self.ChannelId, self.ChannelVersion)
        if status == 0:
            self.logger.info(u'优化签名apk包成功')
            self.logger.info(u"最终输出包：%s " % final_apk)

            refree(os.path.join(self.Build, 'ResourceData', self.taskId), os.path.join(self.Work, 'Bak', self.taskId))

            return status, result, final_apk

        else:
            self.logger.info(u'优化签名apk包失败')
            self.logger.info(result)
            refree(os.path.join(self.Build, 'ResourceData', self.taskId), os.path.join(self.Work, 'Bak', self.taskId))
            return status, result, final_apk


# 释放工作目录资源
def refree(datapath, bakpatth):
    if os.path.isdir(datapath):
        shutil.rmtree(datapath)

    if os.path.isdir(bakpatth):
        shutil.rmtree(bakpatth)


