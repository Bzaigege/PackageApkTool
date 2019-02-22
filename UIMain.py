#!/usr/bin/env python
# -*-coding:utf-8 -*-

import wx
import os
from utils.ConfigUtils import *
from ui.JChannelSDKListPanelUI import JChannelSDKListPanel
from ui.JChannelPanelUI import JChannelPanel
from ui.PackageApkUI import PackageApkPanel
from ui.ToolBarEventListener import ToolBarEventListener


TOOL_TITLE = u'游戏打渠道包工具'


# 显示主页面
class GuiMainFrame(wx.Frame):

    def __init__(self, flag=True):
        wx.Frame.__init__(self, parent=None, id=-1, title=TOOL_TITLE, size=(1000, 800))
        self.Center()  # 窗口居中

        # 将窗体传递到子控件
        self.windowFrame = self

        self.first = 0
        self.flag = flag

        self.width = self.Size.width
        self.height = self.Size.height

        self.up = self.height/2  # 上面窗口高度
        self.left = (self.width/5)*2  # 嵌套窗口左窗口宽度

        self.spWindow = wx.SplitterWindow(self, size=(self.width, self.height))  # 创建一个主分割窗体, parent是frame, 区分上下两部分
        self.up_panel = wx.Panel(self.spWindow)  # 创建上半部分面板
        self.down_panel = PackageApkPanel(self.spWindow, self.windowFrame)  # 创建下半部分面板

        self.child_spWindow = wx.SplitterWindow(self.up_panel)  # 创建一个子分割窗, parent是up_panel, 区分上半区左右部分
        self.child_layout = wx.BoxSizer(wx.VERTICAL)  # 创建一个垂直布局
        self.child_layout.Add(self.child_spWindow, 1, wx.EXPAND)  # 将子分割窗布局延伸至整个p1空间
        self.up_panel.SetSizer(self.child_layout)

        self.resourcePanel = JChannelSDKListPanel(self.child_spWindow, self.windowFrame, self.up_data_ui)  # 在子分割窗上创建左面板
        self.channelPanel = JChannelPanel(self.child_spWindow, self.windowFrame, self.up_data_ui)  # 在子分割窗上创建右面板

        self.spWindow.SplitHorizontally(self.up_panel, self.down_panel, 0)
        self.child_spWindow.SplitVertically(self.resourcePanel, self.channelPanel, self.left)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.on_erase_back)

        # 工具栏
        self.ToolBar = wx.ToolBar(self, wx.ID_ANY)  # 创建工具栏对象
        toolbar_size = (30, 27)  # 设置工具栏图标大小

        # 创建图标
        open_game_apk_bmp = wx.ArtProvider.GetBitmap(wx.ART_PLUS, wx.ART_TOOLBAR, toolbar_size)
        set_output_dir_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, toolbar_size)
        down_sdk_bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_TOOLBAR, toolbar_size)
        set_sign_file_bmp = wx.ArtProvider.GetBitmap(wx.ART_FIND_AND_REPLACE, wx.ART_TOOLBAR, toolbar_size)
        tool_help_bmp = wx.ArtProvider.GetBitmap(wx.ART_HELP, wx.ART_TOOLBAR, toolbar_size)

        # 将这图标放入工具栏
        self.ToolBar.AddTool(200, u'导入游戏包体', open_game_apk_bmp, u'导入游戏包体')
        self.ToolBar.AddTool(201, u'设置游戏包体输出目录', set_output_dir_bmp, u'设置游戏包体输出目录')
        self.ToolBar.AddTool(202, u'设置游戏签名', set_sign_file_bmp, u'设置游戏签名')
        self.ToolBar.AddTool(203, u'下载渠道SDK', down_sdk_bmp, u'下载渠道SDK')
        self.ToolBar.AddTool(204, u'帮助说明', tool_help_bmp, u'帮助说明')

        self.ToolBar.AddSeparator()  # 分割
        self.Bind(wx.EVT_MENU, self.on_click_tool, id=200, id2=204)
        self.tool_bar_listener = ToolBarEventListener()
        self.ToolBar.Realize()  # 提交工具栏设置

        self.old_panel = self.channelPanel
        self.new_panel = None

        self.old_list_panel = self.resourcePanel
        self.new_list_panel = None

    # 选择渠道资源后，更新为对应的配置界面
    def up_data_ui(self, channel_name, channel_id, channel_version, channel_path):

        # 将每次选择的SDK信息,写到配置文件中
        dir_config = os.path.join(DIR_WorkSpace, DIR_UIConfig)
        config_str = {}
        if channel_path:
            config_str['channel_file_path'] = channel_path
            self.tool_bar_listener.write_config_data(dir_config, UI_CONFIG_PARAMS, config_str)

        if self.new_panel is not None:
            self.old_panel.Destroy()
            self.old_panel = self.new_panel

        self.new_panel = JChannelPanel(self.child_spWindow, self.windowFrame, self.up_data_ui,
                                       channel_name, channel_id, channel_version)  # 创建新的面板
        self.child_spWindow.ReplaceWindow(self.old_panel, self.new_panel)

        self.old_panel.Hide()

    # 下载完成后，更新列表
    def up_data_list(self):

        if self.new_list_panel is not None:
            self.old_list_panel.Destroy()
            self.old_list_panel = self.new_list_panel

        self.new_list_panel = JChannelSDKListPanel(self.child_spWindow, self.windowFrame, self.up_data_ui)  # 创建新的面板
        self.child_spWindow.ReplaceWindow(self.old_list_panel, self.new_list_panel)

        self.old_list_panel.Hide()

    def on_size_change(self, event):
        size = self.Size
        self.spWindow.Size = size  # 这一句很重要
        self.spWindow.SetSashPosition(size.height / 2)
        self.child_spWindow.SetSashPosition((size.width / 5)*2)

    def on_erase_back(self, event):
        if self.first < 2 or self.flag:
            self.spWindow.SetSashPosition(0)
            self.child_spWindow.SetSashPosition(self.left)
            self.first = self.first + 1
        self.Refresh()

    # 为工具栏的图标添加事件处理
    def on_click_tool(self, event):
        event_id = event.GetId()
        if event_id == 200:
            self.tool_bar_listener.open_game_apk(self)

        elif event_id == 201:
            self.tool_bar_listener.choose_apk_output_dir(self)

        elif event_id == 202:
            self.tool_bar_listener.set_sign_info(self)

        elif event_id == 203:
            self.tool_bar_listener.down_sdk_resource(self, self.up_data_list)


# 程序运行入口
if __name__ == "__main__":
    app = wx.App()
    frame = GuiMainFrame()
    frame.Show()
    app.MainLoop()




