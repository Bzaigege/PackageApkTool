#!/usr/bin/env python
# -*-coding:utf-8 -*-

import wx
import os
from ui.JChannelConfig import *
from ui.JChannelConfigUI import JChannelConfigDialog


# 渠道参数配置面板
class JChannelPanel(wx.ScrolledWindow):

    def __init__(self, parent, frame, func, channel_name=u'默认', channel_id=u'1', channel_version=u'1.0.0'):
        wx.ScrolledWindow.__init__(self, parent=parent, style=wx.SUNKEN_BORDER)
        self.SetScrollbars(1, 1, 500, 400)

        # print 'channel_name=%s  channel_id=%s  channel_version=%s' % (channel_name, channel_id, channel_version)

        self.window = frame
        self.function = func

        self.channel_name = channel_name
        self.channel_id = channel_id
        self.channel_version = channel_version

        self.channel_configs = get_channel_configs(channel_name, channel_id, channel_version)
        # 默认都添加包名
        if not self.channel_configs.get(u'package'):
            self.channel_configs.update({u'package': ''})

        self.channel_icon = get_channel_icon(channel_name, channel_id, channel_version)

        # 存储渠道配置输入框对象
        self.channel_config_text_objects = OrderedDict([])

        # 存储配置信息
        self.channel_configs_dict = OrderedDict({})
        self.channel_icon_dict = OrderedDict({})
        self.channel_current_icon_paths = {}  # 存储icon当前选择图标路径

        # 整体布局界面
        self.channelLayout = None
        self.channelParamsLayout = None
        self.channelIconLayout = None
        self.channelLabel = None
        self.channelBox = None

        # 配置项控件
        self.channelConfig = None
        self.channelConfigText = None
        self.channelConfigValue = None
        self.channelConfigAddButton = None

        # 图标项控件
        self.channelIcon = None
        self.channelIconText = None
        self.channelIconButton = None

        # 保存按钮
        self.channelSaveButton = None

        self.build_ui()

    def build_ui(self):

        # 渠道参数配置布局
        self.channelLayout = wx.BoxSizer(wx.VERTICAL)

        self.channelLabel = wx.StaticBox(self, -1, self.channel_name + u'配置')
        self.channelBox = wx.StaticBoxSizer(self.channelLabel, wx.HORIZONTAL)

        self.channelParamsLayout = wx.BoxSizer(wx.VERTICAL)
        self.channelIconLayout = wx.BoxSizer(wx.VERTICAL)
        self.channelBox.Add(self.channelParamsLayout, 5, wx.ALL | wx.EXPAND, 0)
        self.channelBox.Add(self.channelIconLayout, 2, wx.ALL | wx.EXPAND, 0)

        # 参数配置界面
        for config_key, config_value in self.channel_configs.items():
            self.add_channel_config(config_key, config_value)

        self.channelConfigAddButton = wx.Button(self, label=u'添加配置项', style=wx.BORDER_MASK)
        self.channelConfigAddButton.Bind(wx.EVT_BUTTON, self.on_add_config)
        self.channelParamsLayout.Add(self.channelConfigAddButton, 0, wx.EXPAND | wx.ALL | wx.CENTER, 0)

        # Icon配置界面
        for icon_key, icon_object in self.channel_icon.items():
            for icon_value, icon_path in icon_object.items():
                self.add_channel_icon(icon_key, icon_value, icon_path)

        self.channelSaveButton = wx.Button(self, label=u'保存配置', style=wx.BORDER_MASK)
        self.channelSaveButton.Bind(wx.EVT_BUTTON, self.save_channel_config)

        self.channelLayout.Add(self.channelBox, 0, wx.EXPAND | wx.ALL, 6)
        self.channelLayout.Add(self.channelSaveButton, 0, wx.EXPAND | wx.ALL, 6)
        self.SetSizer(self.channelLayout)

    # 添加配置项
    def add_channel_config(self, config_key, config_value):

        self.channelConfig = wx.BoxSizer(wx.HORIZONTAL)
        self.channelConfigText = wx.StaticText(self, -1, config_key)
        self.channelConfigValue = wx.TextCtrl(self, -1, style=wx.ALIGN_LEFT | wx.EXPAND)
        self.channelConfigValue.SetValue(config_value)

        # 存储key值和TextCtrl对象,点击打包时会对应来取对应的对象并获取值
        self.channel_config_text_objects.update({config_key: self.channelConfigValue})

        self.channelConfig.Add(self.channelConfigText, 0, wx.ALL | wx.CENTER, 5)
        self.channelConfig.Add(self.channelConfigValue, 1, wx.ALL | wx.CENTER, 5)

        self.channelParamsLayout.Add(self.channelConfig, 0, wx.ALL | wx.EXPAND, 0)

    # 添加图标项
    def add_channel_icon(self, icon_key, icon_value, icon_path):

        self.channelIcon = wx.BoxSizer(wx.HORIZONTAL)
        self.channelIconText = wx.StaticText(self, -1, icon_key)
        self.channelIconButton = wx.Button(self, -1, label=icon_value, style=wx.BORDER_MASK, size=(50, 24))

        self.channel_current_icon_paths[icon_value] = icon_path

        button_marks = {}
        button_marks[u'icon_key'] = icon_key
        button_marks[u'icon_value'] = icon_value
        self.channelIconButton.Bind(wx.EVT_BUTTON, lambda evt, mark=button_marks: self.button_checked(evt, mark))

        self.channelIcon.Add(self.channelIconText, 0, wx.ALL | wx.CENTER, 5)
        self.channelIcon.Add(self.channelIconButton, 1, wx.ALL | wx.CENTER, 5)

        self.channelIconLayout.Add(self.channelIcon, 0, wx.ALL | wx.EXPAND, 0)

    # 动态添加配置项
    def on_add_config(self, event):
        dlg = JChannelConfigDialog(self.window, self.get_add_config)
        if dlg.IsEnabled():
            self.window.Enable(enable=False)
            if not dlg.ShowModal() == wx.ID_OK:
                self.window.Enable(enable=True)

    # 接收收到的配置项
    def get_add_config(self, new_config_key, new_config_value):

        # 先保存配置信息
        for config_key, config_value in self.channel_config_text_objects.items():
            self.channel_configs_dict.update({config_key: config_value.GetValue()})

        self.channel_configs_dict.update({new_config_key: new_config_value})

        CHANNEL_CONFIG[self.channel_id] = self.channel_configs_dict

        # 刷新界面
        self.function(self.channel_name, self.channel_id, self.channel_version, '')

    # 保存配置信息
    def save_channel_config(self, event):

        for config_key, config_value in self.channel_config_text_objects.items():
            self.channel_configs_dict.update({config_key: config_value.GetValue()})

        CHANNEL_CONFIG[self.channel_id] = self.channel_configs_dict

    # 点击按钮
    def button_checked(self, event, mark):
        icon_key = mark[u'icon_key']
        icon_value = mark[u'icon_value']

        wildcard_text = '*.png'
        file_path = self.on_choose_file(self.window, wildcard_text, icon_value, os.getcwd().decode('GB2312').encode('utf-8'))

        if file_path:
            self.channel_current_icon_paths[icon_value] = file_path
            self.channel_icon_dict.update({icon_key: {icon_value: file_path}})

        CHANNEL_ICON[self.channel_id] = self.channel_icon_dict

    # 创建标准文件对话框
    def on_choose_file(self, pand, wildcard_text, title_name, default_dir):

        filename = ''
        dialog = wx.FileDialog(pand, title_name, default_dir, wildcard=wildcard_text)
        if dialog.ShowModal() == wx.ID_OK:
            filename = dialog.GetPath()
        dialog.Destroy()
        return filename


