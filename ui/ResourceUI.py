#!/usr/bin/env python
# -*-coding:utf-8 -*-

import wx
import os
import json


# 选择打包资源布局面板
class ResourcePanel(wx.Panel):

    def __init__(self, parent, frame, func):
        wx.Panel.__init__(self, parent=parent, style=wx.SUNKEN_BORDER)

        self.window = frame
        self.function = func

        self.resourceLayout = wx.BoxSizer(wx.VERTICAL)

        # 第一栏
        self.gameApkLabel = wx.StaticBox(self, -1, u'游戏信息')
        self.gameApkBox = wx.StaticBoxSizer(self.gameApkLabel, wx.HORIZONTAL)

        self.apkFileText = wx.StaticText(self, -1, u"游戏APK")
        self.apkFilePath = wx.TextCtrl(self, style=wx.EXPAND)
        self.apkFileButton = wx.Button(self, label=u'选择文件')
        self.apkFileButton.Bind(wx.EVT_BUTTON, self.on_choose_apk_file)

        self.gameApkBox.Add(self.apkFileText, 0, wx.ALL | wx.CENTER, 3)
        self.gameApkBox.Add(self.apkFilePath, 1, wx.ALL | wx.CENTER, 3)
        self.gameApkBox.Add(self.apkFileButton, 0, wx.ALL | wx.CENTER, 3)

        # 第二栏
        self.gameSignLabel = wx.StaticBox(self, -1, u'签名信息')
        self.gameSignBox = wx.StaticBoxSizer(self.gameSignLabel, wx.VERTICAL)

        # 签名文件栏
        self.sigFileBar = wx.BoxSizer(wx.HORIZONTAL)
        self.signFileText = wx.StaticText(self, -1, u"签名文件")
        self.signFilePath = wx.TextCtrl(self, style=wx.EXPAND)
        self.signFileButton = wx.Button(self, label=u'选择文件')
        self.signFileButton.Bind(wx.EVT_BUTTON, self.on_choose_sign_file)

        self.sigFileBar.Add(self.signFileText, 0, wx.ALL | wx.CENTER, 3)
        self.sigFileBar.Add(self.signFilePath, 1, wx.ALL | wx.CENTER, 3)
        self.sigFileBar.Add(self.signFileButton, 0, wx.ALL | wx.CENTER, 3)

        # 签名信息栏
        self.signInfoBar = wx.BoxSizer(wx.VERTICAL)

        self.signInfoFirst = wx.BoxSizer(wx.HORIZONTAL)
        self.keystore = wx.StaticText(self, -1, u'签名名称', style=wx.TE_LEFT)  # 签名文件
        self.Keystore_text = wx.TextCtrl(self, -1, style=wx.ALIGN_LEFT | wx.EXPAND)
        self.signInfoFirst.Add(self.keystore, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT, 0)
        self.signInfoFirst.Add(self.Keystore_text, 1, wx.EXPAND | wx.ALL, 6)

        self.store_pass = wx.StaticText(self, -1, u'签名密码', style=wx.TE_LEFT)  # 签名文件密码
        self.store_pass_text = wx.TextCtrl(self, -1, style=wx.ALIGN_LEFT | wx.EXPAND)
        self.signInfoFirst.Add(self.store_pass, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT, 0)
        self.signInfoFirst.Add(self.store_pass_text, 1, wx.EXPAND | wx.ALL, 6)

        self.signInfoSecond = wx.BoxSizer(wx.HORIZONTAL)
        self.alias = wx.StaticText(self, -1, u'签名别名', style=wx.TE_LEFT)  # 签名文件别名
        self.alias_text = wx.TextCtrl(self, -1, style=wx.ALIGN_LEFT | wx.EXPAND)
        self.signInfoSecond.Add(self.alias, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT, 0)
        self.signInfoSecond.Add(self.alias_text, 1, wx.EXPAND | wx.ALL, 6)

        self.key_pass = wx.StaticText(self, -1, u'别名密码', style=wx.TE_LEFT)  # 签名文件别名密码
        self.key_pass_text = wx.TextCtrl(self, -1, style=wx.ALIGN_LEFT | wx.EXPAND)
        self.signInfoSecond.Add(self.key_pass, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT, 0)
        self.signInfoSecond.Add(self.key_pass_text, 1, wx.EXPAND | wx.ALL, 6)

        self.signInfoBar.Add(self.signInfoFirst, 0, wx.ALL | wx.EXPAND, 3)
        self.signInfoBar.Add(self.signInfoSecond, 0, wx.ALL | wx.EXPAND, 3)
        self.gameSignBox.Add(self.sigFileBar, 0, wx.ALL | wx.EXPAND, 3)
        self.gameSignBox.Add(self.signInfoBar, 0, wx.ALL | wx.EXPAND, 3)

        # 第三栏
        self.channelResourceLabel = wx.StaticBox(self, -1, u'渠道信息')
        self.channelBox = wx.StaticBoxSizer(self.channelResourceLabel, wx.HORIZONTAL)

        self.channelFileText = wx.StaticText(self, -1, u"渠道资源")
        self.channelFilePath = wx.TextCtrl(self, style=wx.EXPAND)
        self.channelFileButton = wx.Button(self, label=u'选择文件')
        self.channelFileButton.Bind(wx.EVT_BUTTON, self.on_choose_channel_file)

        self.channelBox.Add(self.channelFileText, 0, wx.ALL | wx.CENTER, 3)
        self.channelBox.Add(self.channelFilePath, 1, wx.ALL | wx.CENTER, 3)
        self.channelBox.Add(self.channelFileButton, 0, wx.ALL | wx.CENTER, 3)

        # 添加所有栏目到布局中
        self.resourceLayout.Add(self.gameApkBox, proportion=1, flag=wx.EXPAND | wx.ALL, border=12)
        self.resourceLayout.Add(self.gameSignBox, proportion=1.5, flag=wx.EXPAND | wx.ALL, border=12)
        self.resourceLayout.Add(self.channelBox, proportion=1, flag=wx.EXPAND | wx.ALL, border=12)
        self.SetSizer(self.resourceLayout)

        # 读取上一次的配置信息
        self.setConfig = os.path.join('WorkSpace', 'UIConfig')
        try:
            if os.path.exists(os.path.join(self.setConfig, "uiConfig.json")):
                with open(os.path.join(self.setConfig, "uiConfig.json"), 'r') as uiConfig:
                    setting_config = json.load(uiConfig)

                    if setting_config.has_key('game_apk_path'):
                        game_apk_path = setting_config['game_apk_path']
                        self.apkFilePath.SetValue(game_apk_path)

                    if setting_config.has_key('game_sign_path'):
                        game_sign_path = setting_config['game_sign_path']
                        self.signFilePath.SetValue(game_sign_path)

                    if setting_config.has_key('game_keystore'):
                        game_keystore = setting_config['game_keystore']
                        self.Keystore_text.SetValue(game_keystore)

                    if setting_config.has_key('game_store_pass'):
                        game_store_pass = setting_config['game_store_pass']
                        self.store_pass_text.SetValue(game_store_pass)

                    if setting_config.has_key('game_alias'):
                        game_alias = setting_config['game_alias']
                        self.alias_text.SetValue(game_alias)

                    if setting_config.has_key('game_key_pass'):
                        game_key_pass = setting_config['game_key_pass']
                        self.key_pass_text.SetValue(game_key_pass)

                    # 这里有个小bug,界面初始化时，无法刷新直接对应渠道的配置，需加载完后才能刷新
                    if setting_config.has_key('channel_file_path'):
                        channel_file_path = setting_config['channel_file_path']
                        self.channelFilePath.SetValue(channel_file_path)

        except Exception as e:
            print str(e)

    # 选择APK文件
    def on_choose_apk_file(self, event):

        wildcard_text = '*.apk'
        filename = self.on_choose_file(self, wildcard_text, u"选择游戏APK文件")
        self.apkFilePath.SetValue(filename)

    # 选择签名文件
    def on_choose_sign_file(self, event):

        wildcard_text = '*.keystore'
        filename = self.on_choose_file(self, wildcard_text, u"选择游戏签名文件")
        self.signFilePath.SetValue(filename)

    # 选择渠道资源
    def on_choose_channel_file(self, event):

        wildcard_text = "ZIP files (*.zip)|*.zip|RAR files (*.rar)|*.rar"
        filename = self.on_choose_file(self, wildcard_text, u"选择渠道资源文件")
        self.channelFilePath.SetValue(filename)
        self.on_up_data_channel_ui()

    # 创建标准文件对话框
    def on_choose_file(self, pand, wildcard_text, title_name):

        filename = ''
        dialog = wx.FileDialog(pand, title_name, os.getcwd().decode('GB2312').encode('utf-8'), wildcard=wildcard_text)
        if dialog.ShowModal() == wx.ID_OK:
            filename = dialog.GetPath()
        dialog.Destroy()
        return filename

    # 选择渠道资源后，更新渠道配置UI,对应默认的值
    def on_up_data_channel_ui(self):

        self.channel_file_path = self.channelFilePath.GetValue()
        if self.channel_file_path:
            channelFileName = os.path.splitext(os.path.basename(self.channel_file_path))[0]
            file_dist = channelFileName.split('_')
            channelName = file_dist[0]
            channelId = file_dist[1]
            channelVersion = file_dist[2]

            self.function(channelName, channelId, channelVersion)

