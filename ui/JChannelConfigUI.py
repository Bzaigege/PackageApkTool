#!/usr/bin/env python
# -*-coding:utf-8 -*-

import wx


# 弹出配置项框
class JChannelConfigDialog(wx.Dialog):

    def __init__(self, parent, func):
        super(JChannelConfigDialog, self).__init__(parent, title='添加配置项', size=(300, 180))
        self.Center()  # 窗口居中

        self.func = func
        self.config_key_text = None
        self.config_value_text = None
        self.init_ui()  # 绘制Dialog的界面

    def init_ui(self):

        panel = wx.Panel(self)

        config_key_name = wx.StaticText(panel, -1, '配置项', pos=(10, 25))
        self.config_key_text = wx.TextCtrl(panel, -1, u'', pos=(55, 25), size=(230, -1))
        self.config_key_text.SetForegroundColour('gray')

        config_value_name = wx.StaticText(panel, -1, '配置值', pos=(10, 65))
        self.config_value_text = wx.TextCtrl(panel, -1, u'', pos=(55, 65), size=(230, -1))
        self.config_value_text.SetForegroundColour('gray')

        sure_button = wx.Button(panel, -1, u'确定', pos=(10, 105))
        sure_button.Bind(wx.EVT_BUTTON, self.sure_event)

        cancel_button = wx.Button(panel, -1, u'取消', pos=(195, 105))
        cancel_button.Bind(wx.EVT_BUTTON, self.cancel_event)

    def sure_event(self, event):
        config_key = self.config_key_text.GetValue()
        config_value = self.config_value_text.GetValue()
        self.func(config_key, config_value)
        self.EndModal(wx.ID_CANCEL)
        self.Destroy()  # 销毁隐藏Dialog

    def cancel_event(self, event):
        self.EndModal(wx.ID_CANCEL)
        self.Destroy()  # 销毁隐藏Dialog