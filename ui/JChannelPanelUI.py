#!/usr/bin/env python
# -*-coding:utf-8 -*-

import wx

from ui.ChannelConfig import *
from ui.JChannelConfigUI import JChannelConfigDialog


# 渠道参数配置面板
class JChannelPanel(wx.Panel):

    def __init__(self, parent, frame, func, channel_name='default', channel_id='6', channel_version='1.0.0'):
        wx.Panel.__init__(self, parent=parent, style=wx.SUNKEN_BORDER)

        print 'channel_name=%s  channel_id=%s channel_version=%s' % (channel_name, channel_id, channel_version)

        self.window = frame
        self.function = func

        self.channel_name = channel_name
        self.channel_id = channel_id
        self.channel_version = channel_version

        self.channel_configs = get_channel_configs(channel_name, channel_id, channel_version)

        self.channelLayout = None
        self.channelLabel = None
        self.channelBox = None
        self.channelConfig = None
        self.channelConfigText = None
        self.channelConfigValue = None
        self.channelConfigAddButton = None

        self.build_ui()

    def build_ui(self):

        # 渠道参数配置布局
        self.channelLayout = wx.BoxSizer(wx.VERTICAL)

        self.channelLabel = wx.StaticBox(self, -1, u'渠道配置')
        self.channelBox = wx.StaticBoxSizer(self.channelLabel, wx.VERTICAL)

        for config_key, config_value in self.channel_configs.items():
            self.add_channel_config(config_key, config_value)

        self.channelConfigAddButton = wx.Button(self, label=u'添加配置项', style=wx.BORDER_MASK)
        self.channelConfigAddButton.Bind(wx.EVT_BUTTON, self.on_add_config)

        self.channelLayout.Add(self.channelBox, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)
        self.channelLayout.Add(self.channelConfigAddButton, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)
        self.SetSizer(self.channelLayout)

    # 添加配置项
    def add_channel_config(self, config_key, config_value):

        self.channelConfig = wx.BoxSizer(wx.HORIZONTAL)
        self.channelConfigText = wx.StaticText(self, -1, config_key)
        self.channelConfigValue = wx.TextCtrl(self, -1, style=wx.ALIGN_LEFT | wx.EXPAND)
        self.channelConfigValue.SetValue(config_value)
        self.channelConfig.Add(self.channelConfigText, 0, wx.ALL | wx.CENTER, 5)
        self.channelConfig.Add(self.channelConfigValue, 1, wx.ALL | wx.CENTER, 5)

        self.channelBox.Add(self.channelConfig, 1, wx.ALL | wx.EXPAND, 0)

    # 动态添加配置项
    def on_add_config(self, event):
        dlg = JChannelConfigDialog(self, self.get_add_config)
        dlg.Show()

    # 接收收到的配置项
    def get_add_config(self, config_key, config_value):
        self.channel_configs.update({config_key: config_value})  # 添加到字典里
        self.function(self.channel_name, self.channel_id, self.channel_version)
