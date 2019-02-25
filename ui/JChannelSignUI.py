#!/usr/bin/env python
# -*-coding:utf-8 -*-

import wx
import os


# 弹出配置签名信息框
class JChannelSignDialog(wx.Dialog):

    def __init__(self, parent, func):
        super(JChannelSignDialog, self).__init__(parent, title='配置签名信息', size=(400, 230))
        self.Center()  # 窗口居中

        self.func = func
        self.signFilePath = None
        self.Keystore_text = None
        self.store_pass_text = None
        self.alias_text = None
        self.key_pass_text = None

        self.init_ui()  # 绘制Dialog的界面

    def init_ui(self):

        panel = wx.Panel(self)

        signFileText = wx.StaticText(panel, -1, '签名文件', pos=(10, 25))
        self.signFilePath = wx.TextCtrl(panel, -1, u'', pos=(65, 25), size=(240, 25))
        self.signFilePath.SetForegroundColour('gray')
        signFileButton = wx.Button(panel, label=u'选择文件', pos=(310, 25), size=(70, 25))
        signFileButton.Bind(wx.EVT_BUTTON, self.on_choose_sign_file)

        keystore = wx.StaticText(panel, -1, '签名名称', pos=(10, 65))
        self.Keystore_text = wx.TextCtrl(panel, -1, u'', pos=(65, 65), size=(120, 25))
        self.Keystore_text.SetForegroundColour('gray')

        store_pass = wx.StaticText(panel, -1, '签名密码', pos=(200, 65))
        self.store_pass_text = wx.TextCtrl(panel, -1, u'', pos=(260, 65), size=(120, 25))
        self.store_pass_text.SetForegroundColour('gray')

        alias = wx.StaticText(panel, -1, '签名别名', pos=(10, 105))
        self.alias_text = wx.TextCtrl(panel, -1, u'', pos=(65, 105), size=(120, 25))
        self.alias_text.SetForegroundColour('gray')

        key_pass = wx.StaticText(panel, -1, '别名密码', pos=(200, 105))
        self.key_pass_text = wx.TextCtrl(panel, -1, u'', pos=(260, 105), size=(120, 25))
        self.key_pass_text.SetForegroundColour('gray')

        sure_button = wx.Button(panel, -1, u'确定', pos=(30, 145))
        sure_button.Bind(wx.EVT_BUTTON, self.sure_event)

        cancel_button = wx.Button(panel, -1, u'取消', pos=(265, 145))
        cancel_button.Bind(wx.EVT_BUTTON, self.cancel_event)

    def sure_event(self, event):

        # 选择了签名文件必须填写签名信息
        game_sign_file_path = self.signFilePath.GetValue()
        keystore = u''
        store_pass = u''
        alias = u''
        key_pass = u''
        if game_sign_file_path:
            keystore = self.Keystore_text.GetValue()
            if not keystore:
                self.show_message(u'签名名称 不能为空')
                return

            store_pass = self.store_pass_text.GetValue()
            if not store_pass:
                self.show_message(u'签名密码 不能为空')
                return

            alias = self.alias_text.GetValue()
            if not alias:
                self.show_message(u'签名别名 不能为空')
                return

            key_pass = self.key_pass_text.GetValue()
            if not key_pass:
                self.show_message(u'别名密码 不能为空')
                return

        self.func(game_sign_file_path, keystore, store_pass, alias, key_pass)
        self.EndModal(wx.ID_CANCEL)
        self.Destroy()  # 销毁隐藏Dialog

    def cancel_event(self, event):
        self.EndModal(wx.ID_CANCEL)
        self.Destroy()  # 销毁隐藏Dialog

    # 选择签名文件
    def on_choose_sign_file(self, event):

        wildcard_text = '*.keystore'
        filename = self.on_choose_file(self, wildcard_text, u"选择游戏签名文件", os.getcwd().decode('GB2312').encode('utf-8'))
        self.signFilePath.SetValue(filename)
        self.Keystore_text.SetValue(self.get_file_path_name(filename))

    # 创建标准文件对话框
    def on_choose_file(self, pand, wildcard_text, title_name, default_dir):

        filename = ''
        dialog = wx.FileDialog(pand, title_name, default_dir, wildcard=wildcard_text)
        dialog.Center()  # 窗口居中
        if dialog.ShowModal() == wx.ID_OK:
            filename = dialog.GetPath()
        dialog.Destroy()
        return filename

    # 返回文件的路径截取后的文件名
    def get_file_path_name(self, file_path):
        return os.path.basename(file_path)

    # 显示提示信息
    def show_message(self, msg):

        dlg = wx.MessageDialog(None, msg, u"提示信息", wx.OK | wx.ICON_QUESTION)
        dlg.ShowModal()
        dlg.Destroy()