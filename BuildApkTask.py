#!/usr/bin/env python
# -*-coding:utf-8 -*-

import shutil
import json
from BuildApkTools import *
from utils.ConfigUtils import *
from utils.LogUtils import *


class BuildApkTask(object):

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

    def __init__(self, taskId, gameName, gameId, gameVersion, gameApkName, channelName, channelId, channelVersion,
                 isLocal = True, signId= DIR_signId, keystore='android.keystore', alias='sg', storepass='s123456', keypass='s123456'):

        self.WorkSpace = os.path.join(DIR_WorkSpace)  # 工作目录

        self.Build = os.path.join(self.WorkSpace, DIR_BuildApk)  # 打包工作目录
        self.Resources = os.path.join(self.WorkSpace, DIR_Resources)  # 本地打包资源目录
        self.Tools = os.path.join(self.WorkSpace, DIR_Tools)  # 打包工具路径

        # 资源目录
        self.BaseGameApkPath = os.path.join(self.Resources, DIR_Game, gameId, gameVersion)  # 游戏母包
        self.BaseChannelPath = os.path.join(self.Resources, DIR_ChannelSDK, channelId, channelVersion)  # 渠道资源
        self.BaseSignPath = os.path.join(self.Resources, DIR_Sign, signId)  # 签名资源
        self.BaseConfigPath = os.path.join(self.Resources, DIR_Config, gameId, channelId, channelVersion)  # 打包编译配置文件

        # 打包过程工作目录
        self.Work = os.path.join(self.Build, DIR_Work)  # 打包目录
        self.TempPath = os.path.join(self.Work, 'Temp', taskId)  # 打包过程缓存路径(处理多任务资源冲突问题)

        # 打包完成包体输出目录
        self.OutputApkPath = os.path.join(self.Build, DIR_OutputApk, taskId)  # 输出包体路径

        # 打包过程日志输出目录
        self.logger = LogUtils.sharedInstance(taskId)
        self.logger.set_logger(taskId, self.Build, gameName, channelId)

        # 配置其他信息赋值:游戏、渠道、签名
        self.taskId = taskId
        self.gameName = gameName
        self.gameId = gameId
        self.gameVersion = gameVersion
        self.gameApkName = gameApkName
        self.channelName = channelName
        self.ChannelId = channelId
        self.ChannelVersion = channelVersion

        self.compile_config = {}

        self.sign_id = signId  # 内置默认签名
        self.keystore = keystore
        self.alias = alias
        self.storepass = storepass
        self.keypass = keypass

        self.Local = isLocal

    #  开始打包
    def buildApk(self):

        self.logger.info(u'开始打包...')
        self.logger.info(u'任务ID：%s' % self.taskId)
        self.logger.info(u'游戏ID：%s' % self.gameId)
        self.logger.info(u'渠道ID：%s\n' % self.ChannelId)

        # todo 如果是服务器打包，可以在这里处理拉取资源步骤
        if not self.Local:
            self.logger.info(u'服务器打包,开始从后台同步资源文件....')

        # 读取打包编译参数
        self.logger.info(u'获取打包编译参数....')
        if not os.path.exists(os.path.join(self.BaseConfigPath, "build_config.json")):
            self.logger.info(u"打包编译参数文件： build_config.json不存在 请检查")
            return 1, u'打包编译参数文件： build_config.json不存在 请检查'

        try:
            with open(os.path.join(self.BaseConfigPath, "build_config.json"), 'r') as build_config:
                compile_config = json.load(build_config)
                self.compile_config = compile_config
                self.logger.info(u"获取打包编译参数成功")
                self.logger.info(u"%s\n" % self.compile_config)

                # todo 服务器打包时，需要获取签名信息

                # 这里需要处理下，当build_config没有配置包名时，需读取反编译后的包名
                if not self.compile_config.has_key(CONF_package):
                    game_package_name = get_game_package_name(self.TempPath)
                    self.compile_config[CONF_package] = game_package_name

        except Exception as e:
            self.logger.info(e)
            return 1, u'读取配置文件build_config.json出错'

        self.logger.info(u'处理签名资源....')
        if self.sign_id != DIR_signId:
            self.BaseSignPath = os.path.join(self.Resources, DIR_Sign, self.sign_id)  # 签名资源
        self.logger.info(u'签名文件为：%s 签名别名：%s\n' % (self.keystore, self.alias))

        # 开始反编译包体
        self.logger.info(u'反编译解包到Temp目录....')
        if os.path.isdir(self.TempPath):
            system = platform.system()
            if system == 'Windows':
                delete_command_windows(self.TempPath)
            else:
                shutil.rmtree(self.TempPath)
        os.makedirs(self.TempPath)

        status, result = decompile_apk(self.Tools, self.TempPath, os.path.join(self.BaseGameApkPath, self.gameApkName))
        if status == 0:
            self.logger.info(u'反编译解包到Temp目录成功\n')
            # todo 可以在这里读取原始包体的信息，用于判断是否支持打包

        else:
            self.logger.info(result)
            self.logger.info(u'反编译解包到Temp目录失败\n')
            return status, result

        # 开始打包的核心逻辑，第一步：合并资源文件,包括assets/libs/res等目录资源
        self.logger.info(u'开始合并资源....')
        status, result = merge_resources(self.taskId, self.Tools, self.TempPath, self.BaseChannelPath, self.ChannelId,
                                         self.ChannelVersion, self.compile_config)
        if status == 0:
            self.logger.info(u'合并资源成功\n')
        else:
            self.logger.info(result)
            self.logger.info(u'合并资源失败\n')
            return status, result

        # 第二步： 配置渠道的闪屏图片及特殊配置文件等
        self.logger.info(u'合并配置文件....')
        status, result = merge_config(self.TempPath, self.BaseChannelPath)
        if status == 0:
            self.logger.info(u'合并配置文件成功\n')
        else:
            self.logger.info(result)
            self.logger.info(u'合并配置文件失败\n')
            return status, result

        # 第三步：合并游戏的Icon和角标资源
        self.logger.info(u'开始合并角标....')
        status, result = merge_icon(self.taskId, self.TempPath, self.BaseChannelPath)
        if status == 0:
            self.logger.info(u'合并角标成功\n')
        else:
            self.logger.info(result)
            self.logger.info(u'合并角标失败\n')
            return status, result

        # 第四步：合并Manifest.xml
        self.logger.info(u'开始合并Manifest.xml文件....')
        status, result, package_name = merge_manifest(self.taskId, self.TempPath, self.BaseChannelPath, self.ChannelId,
                                                      self.ChannelVersion, self.compile_config)
        if status == 0:
            self.logger.info(u'合并Manifest.xml文件成功\n')
        else:
            self.logger.info(result)
            self.logger.info(u'合并Manifest.xml文件失败\n')
            return status, result

        # 第五步：根据资源生成对应的R文件
        self.logger.info(u'开始生成R文件....')
        status, result = create_r_files(self.taskId, self.Tools, self.TempPath, self.BaseChannelPath,
                                        self.ChannelId, self.ChannelVersion, self.compile_config, package_name)
        if status == 0:
            self.logger.info(u'生成R文件成功\n')
        else:
            self.logger.info(result)
            self.logger.info(u'生成R文件失败\n')
            return status, result

        # 第六步：将代码编译为smali代码
        self.logger.info(u'开始将jar文件转化为smali代码....')
        status, result = jar_compile_smali(self.taskId, self.Tools, self.TempPath)
        if status == 0:
            self.logger.info(u'将jar文件转化为smali代码成功\n')
        else:
            self.logger.info(result)
            self.logger.info(u'将jar文件转化为smali代码失败\n')
            return status, result

        # 第七步：将Temp目录资源打包成Apk文件
        self.logger.info(u'开始将Temp目录打成apk包....')
        status, result = compile_build_apk(self.taskId, self.Tools, self.TempPath, self.OutputApkPath)
        if status == 0:
            self.logger.info(u'将Temp目录打成apk包成功\n')
        else:
            self.logger.info(result)
            self.logger.info(u'将Temp目录打成apk包失败\n')
            return status, result

        # 第八步：将生成的apk签名
        self.logger.info(u'开始将apk包签名....')
        status, result = sign_temp_apk(self.OutputApkPath, self.BaseSignPath, self.keystore, self.alias,
                                       self.storepass, self.keypass)
        if status == 0:
            self.logger.info(u'将apk包签名成功\n')
        else:
            self.logger.info(result)
            self.logger.info(u'将apk包签名失败\n')
            return status, result

        # 第九步：将签名的Apk优化
        self.logger.info(u'开始优化签名apk包....')
        status, result, final_apk = zipa_sign_apk(self.Tools, self.OutputApkPath, self.gameName,
                                                  self.gameVersion, self.ChannelId, self.ChannelVersion)
        if status == 0:
            self.logger.info(u'优化签名apk包成功, 最终输出包：%s '% final_apk)
        else:
            self.logger.info(result)
            self.logger.info(u'优化签名apk包失败')

        return status, result



