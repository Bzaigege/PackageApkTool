#!/usr/bin/env python
# -*-coding:utf-8 -*-

import wx
import os
import json
from UIBuildApkThread import PackageApkThread
from utils.ConfigUtils import *

TOTAL_MESSAGE = u"温馨提示：请确认游戏包已接入聚合SDK母包,否则无法打包"


# 打包任务面板
class PackageApkPanel(wx.Panel):

    def __init__(self, parent, frame):
        wx.Panel.__init__(self, parent=parent, style=wx.SUNKEN_BORDER)

        self.window = frame

        # 提示信息栏
        self.packageLayout = wx.BoxSizer(wx.VERTICAL)

        self.WarnMessageLabel = wx.StaticBox(self, -1, u'')
        self.WarnMessageBox = wx.StaticBoxSizer(self.WarnMessageLabel, wx.VERTICAL)
        self.packageFrame = wx.BoxSizer()
        self.packageMessageText = wx.StaticText(self, -1, TOTAL_MESSAGE)
        self.packageButton = wx.Button(self, label=u'开始打包')
        self.packageButton.Bind(wx.EVT_BUTTON, self.on_package_apk)
        self.packageFrame.Add(self.packageMessageText, 1, wx.ALL | wx.CENTER, 3)
        self.packageFrame.Add(self.packageButton, 0, wx.ALL | wx.CENTER, 3)
        self.WarnMessageBox.Add(self.packageFrame, 1, wx.ALL | wx.EXPAND, 0)

        self.logLabel = wx.StaticBox(self, -1, u'日志信息')
        self.logBox = wx.StaticBoxSizer(self.logLabel, wx.VERTICAL)
        self.logFrame = wx.BoxSizer()
        self.logText = wx.TextCtrl(self, size=(1000, 800), style=wx.HSCROLL | wx.TE_MULTILINE)
        self.logFrame.Add(self.logText, proportion=1, flag=wx.EXPAND | wx.ALL)
        self.logBox.Add(self.logFrame, 1, wx.ALL | wx.EXPAND, 3)

        self.packageLayout.Add(self.WarnMessageBox, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        self.packageLayout.Add(self.logBox, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        self.SetSizer(self.packageLayout)

        self.setConfig = os.path.join(DIR_WorkSpace, DIR_UIConfig)

    # 开始打包
    def on_package_apk(self, event):

        # 清空日志
        self.logText.Clear()

        # 检测Java环境
        check_java_cmd = u"java -version"
        stdin, stdout = os.popen4(check_java_cmd.encode("GB2312"))
        data = stdout.read()
        if 'java version' not in data:
            self.show_message(u'未检测java环境，如未安装请先安装java环境，如已经安装，请重启程序')
            return

        # 读取配置信息
        package_config_file = os.path.join(self.setConfig, UI_CONFIG_PARAMS)
        if not os.path.exists(package_config_file):
            self.show_message(u'请先选择游戏apk文件')
            return
        else:

            try:

                # 如果已存在,先读取之前的信息,
                with open(package_config_file, 'r') as hasConfig:
                    configs = json.load(hasConfig)
                    game_apk_file_path = ''
                    if configs.has_key('game_apk_path'):
                        game_apk_file_path = configs['game_apk_path']
                        if not game_apk_file_path:
                            self.show_message(u'请先选择游戏apk文件')
                            return

                    # 选择了签名文件必须填写签名信息
                    game_sign_file_path = ''
                    if configs.has_key('game_sign_path'):
                        game_sign_file_path = configs['game_sign_path']
                        if not game_sign_file_path:
                            self.show_message(u'请先选择游戏签名文件')
                            return

                    keystore = ''
                    store_pass = ''
                    alias = ''
                    key_pass = ''
                    if game_sign_file_path:

                        if configs.has_key('game_keystore'):
                            keystore = configs['game_keystore']
                            if not keystore:
                                self.show_message(u'签名名称 不能为空')
                                return

                        if configs.has_key('game_store_pass'):
                            store_pass = configs['game_store_pass']
                            if not store_pass:
                                self.show_message(u'签名密码 不能为空')
                                return

                        if configs.has_key('game_alias'):
                            alias = configs['game_alias']
                            if not alias:
                                self.show_message(u'签名别名 不能为空')
                                return

                        if configs.has_key('game_key_pass'):
                            key_pass = configs['game_key_pass']
                            if not key_pass:
                                self.show_message(u'别名密码 不能为空')
                                return

                    channel_file_path = ''
                    if configs.has_key('channel_file_path'):
                        channel_file_path = configs['channel_file_path']
                        if not channel_file_path:
                            self.show_message(u'请先选择渠道压缩文件')
                            return

                    # 启动打包任务
                    event.GetEventObject().Disable()
                    thread = PackageApkThread(self.window, game_apk_file_path, channel_file_path,
                                              game_sign_file_path, keystore, store_pass, alias, key_pass)
                    thread.start()

            except Exception as e:
                print e

    # 显示提示信息
    def show_message(self, msg):

        dlg = wx.MessageDialog(None, msg, u"提示信息", wx.OK | wx.ICON_QUESTION)
        dlg.ShowModal()
        dlg.Destroy()

    # 写入日志信息
    def write_log(self, msg):
        self.logText.write(msg)