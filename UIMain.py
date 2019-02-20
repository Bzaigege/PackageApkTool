#!/usr/bin/env python
# -*-coding:utf-8 -*-

import wx
import os
import json
from utils.ConfigUtils import *
from ui.ResourceUI import ResourcePanel
from ui.JChannelPanelUI import JChannelPanel
from ui.PackageApkUI import PackageApkPanel
from ui.JChannelSDKDownUI import JChannelSDKDownDialog


TOOL_TITLE = u'游戏打渠道包工具'


# 显示主页面
class GuiMainFrame(wx.Frame):

    def __init__(self, flag=True):
        wx.Frame.__init__(self, parent=None, id=-1, title=TOOL_TITLE, size=(1000, 850))
        self.Center()  # 窗口居中

        # 将窗体传递到子控件
        self.windowFrame = self

        self.first = 0
        self.flag = flag
        self.spWindow = wx.SplitterWindow(self)  # 创建一个主分割窗体, parent是frame, 区分上下两部分
        self.up_panel = wx.Panel(self.spWindow)  # 创建上半部分面板
        self.down_panel = PackageApkPanel(self.spWindow, self.windowFrame)  # 创建下半部分面板

        self.child_spWindow = wx.SplitterWindow(self.up_panel)  # 创建一个子分割窗, parent是up_panel, 区分上半区左右部分
        self.child_layout = wx.BoxSizer(wx.VERTICAL)  # 创建一个垂直布局
        self.child_layout.Add(self.child_spWindow, 1, wx.EXPAND)  # 将子分割窗布局延伸至整个p1空间
        self.up_panel.SetSizer(self.child_layout)

        self.resourcePanel = ResourcePanel(self.child_spWindow, self.windowFrame, self.up_data_ui)  # 在子分割窗上创建左面板
        self.channelPanel = JChannelPanel(self.child_spWindow, self.windowFrame, self.up_data_ui)  # 在子分割窗上创建右面板

        self.spWindow.SplitHorizontally(self.up_panel, self.down_panel, 0)
        self.child_spWindow.SplitVertically(self.resourcePanel, self.channelPanel, 0)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.on_erase_back)

        # 工具栏
        self.ToolBar = wx.ToolBar(self, wx.ID_ANY)  # 创建工具栏对象
        toolbar_size = (30, 25)  # 设置工具栏图标大小

        # 创建图标
        open_file_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, toolbar_size)
        down_sdk_bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_TOOLBAR, toolbar_size)

        # 将这图标放入工具栏
        self.ToolBar.AddTool(200, u'设置游戏包体输出目录', open_file_bmp, u'设置游戏包体输出目录')
        self.ToolBar.AddTool(201, u'下载渠道SDK', down_sdk_bmp, u'下载渠道SDK')

        self.ToolBar.AddSeparator()  # 分割
        self.Bind(wx.EVT_MENU, self.on_click_tool, id=200, id2=201)
        self.ToolBar.Realize()  # 提交工具栏设置

        self.old_panel = self.channelPanel
        self.new_panel = None

        self.first_complete_refresh_ui()

    # 加载整个界面后，刷新布局
    def first_complete_refresh_ui(self):
        self.resourcePanel.on_up_data_channel_ui()

    # 动态更新渠道的配置布局
    def up_data_ui(self, channel_name, channel_id, channel_version):

        if self.new_panel is not None:
            self.old_panel.Destroy()
            self.old_panel = self.new_panel

        self.new_panel = JChannelPanel(self.child_spWindow, self.windowFrame, self.up_data_ui,
                                       channel_name, channel_id, channel_version)  # 创建新的面板
        self.child_spWindow.ReplaceWindow(self.old_panel, self.new_panel)

        self.old_panel.Hide()

    def on_erase_back(self, event):

        if self.first < 2 or self.flag:
            self.spWindow.SetSashPosition(0)
            self.child_spWindow.SetSashPosition(0)
            self.first = self.first + 1
        self.Refresh()

    # 为工具栏的图标添加事件处理
    def on_click_tool(self, event):
        event_id = event.GetId()
        if event_id == 200:

            # 设置包体输出目录
            apk_out_dir = ''
            dlg = wx.DirDialog(self, u"选择文件夹", style=wx.DD_DEFAULT_STYLE)
            if dlg.ShowModal() == wx.ID_OK:
                print dlg.GetPath()  # 文件夹路径
                apk_out_dir = dlg.GetPath()

            dlg.Destroy()

            # 保存路径
            dir_config = os.path.join(DIR_WorkSpace, DIR_UIConfig)
            dir_config_str = {}
            if apk_out_dir:
                dir_config_str['game_channel_apk_output_path'] = apk_out_dir
            try:
                if not os.path.exists(os.path.join(dir_config)):
                    os.makedirs(dir_config)

                if not os.path.exists(os.path.join(dir_config, "dirConfig.json")):
                    with open(os.path.join(dir_config, "dirConfig.json"), 'wb') as uiConfig:
                        uiConfig.write(json.dumps(dir_config_str, ensure_ascii=False))

                else:
                    with open(os.path.join(dir_config, "dirConfig.json"), 'w') as uiConfig:
                        uiConfig.write(json.dumps(dir_config_str, ensure_ascii=False))

            except Exception as e:
                print e

        elif event_id == 201:

            down_dlg = JChannelSDKDownDialog(self)
            if down_dlg.IsEnabled():
                self.Enable(enable=False)
                if not down_dlg.ShowModal() == wx.ID_OK:
                    self.Enable(enable=True)


# 程序运行入口
if __name__ == "__main__":
    app = wx.App()
    frame = GuiMainFrame()
    frame.Show()
    app.MainLoop()




