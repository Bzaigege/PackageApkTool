#!/usr/bin/env python
# -*-coding:utf-8 -*-

import wx
from ui.ResourceUI import ResourcePanel
from ui.JChannelPanelUI import JChannelPanel
from ui.PackageApkUI import PackageApkPanel


TOOL_TITLE = u'游戏打渠道包工具'


# 显示主页面
class GuiMainFrame(wx.Frame):

    def __init__(self, flag=True):
        wx.Frame.__init__(self, parent=None, id=-1, title=TOOL_TITLE, size=(1000, 800))

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

        self.old_panel = self.channelPanel
        self.new_panel = None

    # 动态更新渠道的配置布局
    def up_data_ui(self, channel_name, channel_id, channel_version):
        print ('更新UI')

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


# 程序运行入口
if __name__ == "__main__":
    app = wx.App()
    frame = GuiMainFrame()
    frame.Show()
    app.MainLoop()




