#!/usr/bin/env python
# -*-coding:utf-8 -*-

import wx
import os
import json
from UIBuildApkThread import PackageApkThread


TOOL_TITLE = u'游戏打渠道包工具'
TOTAL_MESSAGE = u"温馨提示：请确认游戏包已接入聚合SDK母包,否则无法打包"


# 显示主页面
class GuiMainFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=-1, title=TOOL_TITLE, size=(1000, 800))

        self.panel = wx.Panel(self)

        # 控件排列布局
        self.packageLayout = wx.BoxSizer(wx.VERTICAL)

        # 第一栏
        self.gameApkLabel = wx.StaticBox(self.panel, -1, u'游戏信息')
        self.gameApkBox = wx.StaticBoxSizer(self.gameApkLabel, wx.HORIZONTAL)

        self.apkFileLabel = wx.StaticText(self.panel, -1, u"游戏APK")
        self.apkFileName = wx.TextCtrl(self.panel, style=wx.EXPAND)
        self.apkFileButton = wx.Button(self.panel, label=u'选择文件')
        self.apkFileButton.Bind(wx.EVT_BUTTON, self.on_choose_apk_file)

        self.gameApkBox.Add(self.apkFileLabel, 0, wx.ALL | wx.CENTER, 8)
        self.gameApkBox.Add(self.apkFileName, 1, wx.ALL | wx.CENTER, 6)
        self.gameApkBox.Add(self.apkFileButton, 0, wx.ALL | wx.CENTER, 8)

        # 第二栏
        self.gameSignLabel = wx.StaticBox(self.panel, -1, u'签名信息')
        self.gameSignBox = wx.StaticBoxSizer(self.gameSignLabel, wx.VERTICAL)

        # 获取签名文件行
        self.sigFileRow = wx.BoxSizer(wx.HORIZONTAL)
        self.signFileLabel = wx.StaticText(self.panel, -1, u"游戏签名")
        self.signFileName = wx.TextCtrl(self.panel, style=wx.EXPAND)
        self.signFileButton = wx.Button(self.panel, label=u'选择文件')
        self.signFileButton.Bind(wx.EVT_BUTTON, self.on_choose_sign_file)

        self.sigFileRow.Add(self.signFileLabel, 0, wx.ALL | wx.CENTER, 8)
        self.sigFileRow.Add(self.signFileName, 1, wx.ALL | wx.CENTER, 6)
        self.sigFileRow.Add(self.signFileButton, 0, wx.ALL | wx.CENTER, 8)

        # 签名信息行
        self.sigInfoRow = wx.BoxSizer(wx.HORIZONTAL)
        self.keystore = wx.StaticText(self.panel, -1, u'keystore：')  # 签名文件
        self.Keystore_text = wx.TextCtrl(self.panel, -1, style=wx.ALIGN_LEFT | wx.EXPAND)
        self.sigInfoRow.Add(self.keystore, 0, wx.ALL | wx.CENTER, 2)
        self.sigInfoRow.Add(self.Keystore_text, 1, wx.ALL | wx.CENTER, 3)

        self.store_pass = wx.StaticText(self.panel, -1, u'StorePass：')  # 签名文件密码
        self.store_pass_text = wx.TextCtrl(self.panel, -1, style=wx.ALIGN_LEFT | wx.EXPAND)
        self.sigInfoRow.Add(self.store_pass, 0, wx.ALL | wx.CENTER, 2)
        self.sigInfoRow.Add(self.store_pass_text, 1, wx.ALL | wx.CENTER, 3)

        self.alias = wx.StaticText(self.panel, -1, u'Alias：')  # 签名文件别名
        self.alias_text = wx.TextCtrl(self.panel, -1, style=wx.ALIGN_LEFT | wx.EXPAND)
        self.sigInfoRow.Add(self.alias, 0, wx.ALL | wx.CENTER, 2)
        self.sigInfoRow.Add(self.alias_text, 1, wx.ALL | wx.CENTER, 3)

        self.key_pass = wx.StaticText(self.panel, -1, u'KeyPass：')  # 签名文件别名密码
        self.key_pass_text = wx.TextCtrl(self.panel, -1, style=wx.ALIGN_LEFT | wx.EXPAND)
        self.sigInfoRow.Add(self.key_pass, 0, wx.ALL | wx.CENTER, 2)
        self.sigInfoRow.Add(self.key_pass_text, 1, wx.ALL | wx.CENTER, 3)

        self.gameSignBox.Add(self.sigFileRow, 1, wx.ALL | wx.EXPAND, 0)
        self.gameSignBox.Add(self.sigInfoRow, 1, wx.ALL | wx.EXPAND, 1)

        # 第三栏
        self.configLabel = wx.StaticBox(self.panel, -1, u'参数信息')
        self.configBox = wx.StaticBoxSizer(self.configLabel, wx.HORIZONTAL)

        self.compileRow = wx.BoxSizer(wx.HORIZONTAL)
        self.compileFileLabel = wx.StaticText(self.panel, -1, u"编译参数")
        self.compileName = wx.TextCtrl(self.panel, style=wx.EXPAND)
        self.compileButton = wx.Button(self.panel, label=u'选择文件')
        self.compileButton.Bind(wx.EVT_BUTTON, self.on_choose_compile_file)

        self.compileRow.Add(self.compileFileLabel, 0, wx.ALL | wx.CENTER, 8)
        self.compileRow.Add(self.compileName, 1, wx.ALL | wx.CENTER, 6)
        self.compileRow.Add(self.compileButton, 0, wx.ALL | wx.CENTER, 8)

        self.configBox.Add(self.compileRow, 1, wx.ALL | wx.EXPAND, 0)

        # 第四栏
        self.channelResourceLabel = wx.StaticBox(self.panel, -1, u'渠道信息')
        self.channelBox = wx.StaticBoxSizer(self.channelResourceLabel, wx.VERTICAL)

        # 选择本地的资源文件
        self.channelFileRow = wx.BoxSizer(wx.HORIZONTAL)
        self.channelFileLabel = wx.StaticText(self.panel, -1, u"渠道资源")
        self.channelFileName = wx.TextCtrl(self.panel, style=wx.EXPAND)
        self.channelFileButton = wx.Button(self.panel, label=u'选择文件')
        self.channelFileButton.Bind(wx.EVT_BUTTON, self.on_choose_channel_file)

        self.channelFileRow.Add(self.channelFileLabel, 0, wx.ALL | wx.CENTER, 8)
        self.channelFileRow.Add(self.channelFileName, 1, wx.ALL | wx.CENTER, 6)
        self.channelFileRow.Add(self.channelFileButton, 0, wx.ALL | wx.CENTER, 8)

        self.channelBox.Add(self.channelFileRow, 1, wx.ALL | wx.EXPAND, 0)

        # 第五栏：开始打包
        self.PromptMessageLabel = wx.StaticBox(self.panel, -1, u'')
        self.PromptMessageBox = wx.StaticBoxSizer(self.PromptMessageLabel, wx.VERTICAL)

        self.MessageRow = wx.BoxSizer(wx.HORIZONTAL)
        self.packageRMessage = wx.StaticText(self.panel, -1, TOTAL_MESSAGE)
        self.packageButton = wx.Button(self.panel, label=u'开始打包')
        self.packageButton.Bind(wx.EVT_BUTTON, self.on_package_apk)
        self.MessageRow.Add(self.packageRMessage, 1, wx.ALL | wx.CENTER, 3)
        self.MessageRow.Add(self.packageButton, 0, wx.ALL | wx.CENTER, 12)
        self.PromptMessageBox.Add(self.MessageRow, 1, wx.ALL | wx.EXPAND, 0)

        # 第六栏：日志信息
        self.logLabel = wx.StaticBox(self.panel, -1, u'日志信息')
        self.logBox = wx.StaticBoxSizer(self.logLabel, wx.VERTICAL)

        self.logRow = wx.BoxSizer()
        self.logText = wx.TextCtrl(self.panel, size=(1000, 800), style=wx.HSCROLL | wx.TE_MULTILINE)
        self.logRow.Add(self.logText, proportion=1, flag=wx.EXPAND | wx.ALL)
        self.logBox.Add(self.logRow, 1, wx.ALL | wx.EXPAND, 5)

        # 将所有的栏添加到布局中
        self.packageLayout.Add(self.gameApkBox, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        self.packageLayout.Add(self.gameSignBox, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        self.packageLayout.Add(self.configBox, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        self.packageLayout.Add(self.channelBox, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        self.packageLayout.Add(self.PromptMessageBox, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        self.packageLayout.Add(self.logBox, proportion=0, flag=wx.EXPAND | wx.ALL, border=3)
        self.panel.SetSizer(self.packageLayout)

        # 读取上一次的配置信息
        self.setConfig = os.path.join('WorkSpace', 'UIConfig')
        try:
            if os.path.exists(os.path.join(self.setConfig, "uiConfig.json")):
                with open(os.path.join(self.setConfig, "uiConfig.json"), 'r') as uiConfig:
                    setting_config = json.load(uiConfig)

                    if setting_config.has_key('game_apk_path'):
                        game_apk_path = setting_config['game_apk_path']
                        self.apkFileName.SetValue(game_apk_path)

                    if setting_config.has_key('game_sign_path'):
                        game_sign_path = setting_config['game_sign_path']
                        self.signFileName.SetValue(game_sign_path)

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

                    if setting_config.has_key('game_compile_path'):
                        game_compile_path = setting_config['game_compile_path']
                        self.compileName.SetValue(game_compile_path)

                    if setting_config.has_key('channel_file_path'):
                        channel_file_path = setting_config['channel_file_path']
                        self.channelFileName.SetValue(channel_file_path)

        except Exception as e:
            print str(e)

    # 选择APK文件
    def on_choose_apk_file(self, event):

        wildcard_text = '*.apk'
        filename = self.on_choose_file(self, wildcard_text, u"选择游戏APK文件")
        self.apkFileName.SetValue(filename)

    # 选择签名文件
    def on_choose_sign_file(self, event):

        wildcard_text = '*.keystore'
        filename = self.on_choose_file(self, wildcard_text, u"选择游戏签名文件")
        self.signFileName.SetValue(filename)

    # 选择渠道资源
    def on_choose_channel_file(self, event):

        wildcard_text = "ZIP files (*.zip)|*.zip|RAR files (*.rar)|*.rar"
        filename = self.on_choose_file(self, wildcard_text, u"选择渠道资源文件")
        self.channelFileName.SetValue(filename)

    # 选择打包编译文件
    def on_choose_compile_file(self, event):

        # 创建标准文件对话框
        wildcard_text = '*.json'
        filename = self.on_choose_file(self, wildcard_text, u"选择打包编译文件")
        self.compileName.SetValue(filename)

    # 创建标准文件对话框
    def on_choose_file(self, pand, wildcard_text, title_name):

        filename = ''
        dialog = wx.FileDialog(pand, title_name, os.getcwd().decode('GB2312').encode('utf-8'), wildcard=wildcard_text)
        if dialog.ShowModal() == wx.ID_OK:
            filename = dialog.GetPath()
        dialog.Destroy()
        return filename

    # 开始打包
    def on_package_apk(self, event):

        # 清空日志
        self.logText.Clear()

        game_apk_file_path = self.apkFileName.GetValue()
        if not game_apk_file_path:
            self.show_message(u'请先选择游戏apk文件')
            return

        # 选择了签名文件必须填写签名信息
        game_sign_file_path = self.signFileName.GetValue()
        keystore = ''
        store_pass = ''
        alias = ''
        key_pass = ''
        if game_sign_file_path:

            keystore = self.Keystore_text.GetValue()
            if not keystore:
                self.show_message(u'keystore 值不能为空')
                return

            store_pass = self.store_pass_text.GetValue()
            if not store_pass:
                self.show_message(u'StorePass 值不能为空')
                return

            alias = self.alias_text.GetValue()
            if not alias:
                self.show_message(u'Alias 值不能为空')
                return

            key_pass = self.key_pass_text.GetValue()
            if not key_pass:
                self.show_message(u'KeyPass 值不能为空')
                return

        game_compile_file_path = self.compileName.GetValue()
        if not game_compile_file_path:
            self.show_message(u'请先选择打包编译文件')
            return

        channel_file_path = self.channelFileName.GetValue()
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

        if game_compile_file_path:
            config_str['game_compile_path'] = self.compileName.GetValue()

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
        if game_sign_file_path:
            thread = PackageApkThread(self, game_apk_file_path, channel_file_path, game_compile_file_path,
                                      game_sign_file_path, keystore, store_pass, alias, key_pass)
        else:
            thread = PackageApkThread(self, game_apk_file_path,  channel_file_path, game_compile_file_path)

        thread.start()

    # 显示提示信息
    def show_message(self, msg):

        dlg = wx.MessageDialog(None, msg, u"提示信息", wx.OK | wx.ICON_QUESTION)
        dlg.ShowModal()
        dlg.Destroy()

    # 写入日志信息
    def write_log(self, msg):
        self.logText.write(msg)


# 程序运行入口
if __name__ == "__main__":
    app = wx.App()
    frame = GuiMainFrame()
    frame.Show()
    app.MainLoop()




