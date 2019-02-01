#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import threading
from BuildApkTask import *
from utils.ConfigUtils import *
from ui.JChannelPanelUI import *


# 打包任务线程
class PackageApkThread(threading.Thread):

    def __init__(self, window, game_apk_path, channel_file_path,
                 sign_file_path, keystore, store_pass, alias, key_pass):

        threading.Thread.__init__(self)
        self.window = window
        self.timeToQuit = threading.Event()

        # 资源路径
        self.game_apk_path = game_apk_path
        self.channel_file_path = channel_file_path

        # 签名信息
        self.sign_file_path = sign_file_path
        self.keystore = keystore
        self.store_pass = store_pass
        self.alias = alias
        self.key_pass = key_pass

        # 编译参数写入目录
        self.setConfig = os.path.join('WorkSpace', 'UIConfig')
        self.compile_file_path = ''

    def stop(self):
        self.timeToQuit.set()

    def run(self):

        try:

            build_config_str = {}
            for config_key, config_value in DEFAULT_CONFIG.items():
                build_config_str[config_key] = config_value

            if not os.path.exists(os.path.join(self.setConfig)):
                os.makedirs(self.setConfig)

            self.compile_file_path = os.path.join(self.setConfig, 'build_config.json')

            # 如果存在就删除，保证配置文件是最新的配置文件
            if os.path.exists(self.compile_file_path):
                os.remove(self.compile_file_path)

            with open(self.compile_file_path, 'wb') as uiConfig:
                uiConfig.write(json.dumps(build_config_str, ensure_ascii=False))

            # 打包任务配置
            taskId = '180'
            gameApkName = os.path.basename(self.game_apk_path)
            gameName = os.path.splitext(gameApkName)[0]
            gameId = '1'
            gameVersion = '1.0.0'

            # 截取渠道ID 和 渠道版本
            channelFileName = os.path.splitext(os.path.basename(self.channel_file_path))[0]
            file_dist = channelFileName.split('_')
            channelName = file_dist[0]
            channelId = file_dist[1]
            channelVersion = file_dist[2]

            LogUtils.sharedInstance(taskId).setLoggingToHanlder(self.write_text_log)

            # 将本地资源拷贝到对应的目录中
            Resources = os.path.join(DIR_WorkSpace, DIR_Resources)  # 本地模拟服务器资源目录
            BaseGameApkPath = os.path.join(Resources, DIR_Game, gameId, gameVersion)  # 游戏母包
            BaseChannelPath = os.path.join(Resources, DIR_ChannelSDK, channelId, channelVersion)  # 渠道资源
            BaseSignPath = os.path.join(Resources, DIR_Sign, DIR_local_signId)  # 签名资源
            BaseConfigPath = os.path.join(Resources, DIR_Config, gameId, channelId, channelVersion)  # 打包编译配置文件

            # 拷贝游戏资源
            if os.path.isdir(BaseGameApkPath):
                shutil.rmtree(BaseGameApkPath)
            os.makedirs(BaseGameApkPath)
            shutil.copy(self.game_apk_path, BaseGameApkPath)

            # 解压渠道资源
            if os.path.isdir(BaseChannelPath):
                shutil.rmtree(BaseChannelPath)
            os.makedirs(BaseChannelPath)

            unzip_file = zipfile.ZipFile(self.channel_file_path, 'r')
            unzip_file.extractall(BaseChannelPath)
            unzip_file.close()

            # 拷贝签名资源
            if os.path.isdir(BaseSignPath):
                shutil.rmtree(BaseSignPath)
            os.makedirs(BaseSignPath)
            shutil.copy(self.sign_file_path, BaseSignPath)

            # 拷贝配置文件
            if os.path.isdir(BaseConfigPath):
                shutil.rmtree(BaseConfigPath)
            os.makedirs(BaseConfigPath)
            shutil.copy(self.compile_file_path, BaseConfigPath)

            # 启动打包任务
            task = BuildApkTask(taskId, gameName, gameId, gameVersion, gameApkName, channelName, channelId, channelVersion,
                                True, '1', self.keystore, self.alias, self.store_pass, self.key_pass)

            status, result = task.buildApk()
            if status == 0:
                free_local_resource(os.path.join(Resources, DIR_Game, gameId), os.path.join(Resources, DIR_ChannelSDK, channelId),
                                    os.path.join(Resources, DIR_Sign, DIR_local_signId), os.path.join(Resources, DIR_Config, gameId))

            else:
                self.window.show_message(u'打包失败：%s' % result)

            # 按钮点击恢复
            self.window.packageButton.Enable()

        except Exception, e:
            self.window.show_message(u'打包失败：%s' % e)
            self.window.packageButton.Enable()

    def write_text_log(self, text_str):
        self.window.write_log(text_str)


# 清除本地工作目录
def free_local_resource(gameRes_path, sdkRes_path, configRes_Path, signRes_Path):

    if os.path.isdir(gameRes_path):
        shutil.rmtree(gameRes_path)

    if os.path.isdir(sdkRes_path):
        shutil.rmtree(sdkRes_path)

    if os.path.isdir(configRes_Path):
        shutil.rmtree(configRes_Path)

    if os.path.isdir(signRes_Path):
        shutil.rmtree(signRes_Path)



