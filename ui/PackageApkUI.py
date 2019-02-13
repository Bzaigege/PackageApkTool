#!/usr/bin/env python
# -*-coding:utf-8 -*-

import wx
import os
import json
from UIBuildApkThread import PackageApkThread

TOTAL_MESSAGE = u"温馨提示：请确认游戏包已接入聚合SDK母包,否则无法打包"


# 打包任务面板
class PackageApkPanel(wx.Panel):

    def __init__(self, parent, frame):
        wx.Panel.__init__(self, parent=parent, style=wx.SUNKEN_BORDER)

        self.window = frame
        self.resourceUI = ''

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

        self.setConfig = os.path.join('WorkSpace', 'UIConfig')

    # 开始打包
    def on_package_apk(self, event):

        self.resourceUI = self.window.resourcePanel

        # 清空日志
        self.logText.Clear()

        game_apk_file_path = self.resourceUI.apkFilePath.GetValue()
        if not game_apk_file_path:
            self.show_message(u'请先选择游戏apk文件')
            return

        # 选择了签名文件必须填写签名信息
        game_sign_file_path = self.resourceUI.signFilePath.GetValue()
        if not game_sign_file_path:
            self.show_message(u'请先选择游戏签名文件')
            return

        keystore = ''
        store_pass = ''
        alias = ''
        key_pass = ''
        if game_sign_file_path:

            keystore = self.resourceUI.Keystore_text.GetValue()
            if not keystore:
                self.show_message(u'签名名称 不能为空')
                return

            store_pass = self.resourceUI.store_pass_text.GetValue()
            if not store_pass:
                self.show_message(u'签名密码 不能为空')
                return

            alias = self.resourceUI.alias_text.GetValue()
            if not alias:
                self.show_message(u'签名别名 不能为空')
                return

            key_pass = self.resourceUI.key_pass_text.GetValue()
            if not key_pass:
                self.show_message(u'别名密码 不能为空')
                return

        channel_file_path = self.resourceUI.channelFilePath.GetValue()
        if not channel_file_path:
            self.show_message(u'请先选择渠道压缩文件')
            return

        # 将配置的信息写入文件，方便下次选择同样的任务时，不需要修改
        config_str = {}
        if game_apk_file_path:
            config_str['game_apk_path'] = game_apk_file_path

        if game_sign_file_path:
            config_str['game_sign_path'] = game_sign_file_path
            config_str['game_keystore'] = keystore
            config_str['game_store_pass'] = store_pass
            config_str['game_alias'] = alias
            config_str['game_key_pass'] = key_pass

        if channel_file_path:
            config_str['channel_file_path'] = channel_file_path

        try:
            if not os.path.exists(os.path.join(self.setConfig)):
                os.makedirs(self.setConfig)

            if not os.path.exists(os.path.join(self.setConfig, "uiConfig.json")):
                with open(os.path.join(self.setConfig, "uiConfig.json"), 'wb') as uiConfig:
                    uiConfig.write(json.dumps(config_str, ensure_ascii=False))

            else:
                with open(os.path.join(self.setConfig, "uiConfig.json"), 'w') as uiConfig:
                    uiConfig.write(json.dumps(config_str, ensure_ascii=False))

        except Exception as e:
            self.show_message(u'程序异常, msg=%s' % e.message)
            return

        # 检测Java环境
        check_java_cmd = u"java -version"
        stdin, stdout = os.popen4(check_java_cmd.encode("GB2312"))
        data = stdout.read()
        if 'java version' not in data:
            self.show_message(u'未检测java环境，如未安装请先安装java环境，如已经安装，请重启程序')
            return

        # 启动打包任务
        event.GetEventObject().Disable()
        thread = PackageApkThread(self.window, game_apk_file_path, channel_file_path,
                                  game_sign_file_path, keystore, store_pass, alias, key_pass)
        thread.start()

    # 显示提示信息
    def show_message(self, msg):

        dlg = wx.MessageDialog(None, msg, u"提示信息", wx.OK | wx.ICON_QUESTION)
        dlg.ShowModal()
        dlg.Destroy()

    # 写入日志信息
    def write_log(self, msg):
        self.logText.write(msg)