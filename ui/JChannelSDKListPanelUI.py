#!/usr/bin/env python
# -*-coding:utf-8 -*-

import wx
import os
import platform
import wx.lib.agw.ultimatelistctrl as ULC
from utils.ConfigUtils import *

SDK_ID = 'sdk_id'   # 渠道id
SDK_NAME = 'sdk_name'  # 渠道名
SDK_VERSION = 'sdk_version'  # 渠道别名
SDK_PATH = 'sdk_path'  # 资源路径


# 渠道SDK已下载资源列表布局面板
class JChannelSDKListPanel(wx.Panel):

    def __init__(self, parent, frame, func):
        wx.Panel.__init__(self, parent=parent, style=wx.SUNKEN_BORDER)

        self.window = frame
        self.function = func

        self.channel_data = self.get_local_sdk_lsit()

        self.main_layout = wx.BoxSizer(wx.VERTICAL)

        self.sdkLabel = wx.StaticBox(self, -1, u'已下载SDK列表')
        self.sdkBox = wx.StaticBoxSizer(self.sdkLabel, wx.VERTICAL)

        # 创建排序列表列标题
        main_list_columns = [("渠道ID", 50), ("图标", 45), ("SDK名称", 110), ("SDK版本", 80), ("选择", 70)]
        self.main_sdk_list = MySDKList(self, (400, 500), main_list_columns, self.channel_data, self.function)

        self.sdkBox.Add(self.main_sdk_list, 1, wx.ALL | wx.EXPAND, 0)
        self.main_layout.Add(self.sdkBox, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(self.main_layout)
        self.Fit()

    def get_local_sdk_lsit(self):
        """获取本地SDK资源的信息"""

        down_path_dir = os.path.join(DIR_WorkSpace, DIR_DownSdk)
        sys_tag = self.get_system_tag()
        sdk_list_data = []
        for parent, dir_names, file_names in os.walk(down_path_dir):
            for file_name in file_names:
                if file_name.endswith('zip'):

                    sdk_file_path = os.path.join(parent, file_name)
                    sdk_file_new_path = sdk_file_path.replace(down_path_dir + sys_tag, '')
                    sdk_file_info = os.path.splitext(sdk_file_new_path)[0].split(sys_tag)

                    sdk_name = sdk_file_info[0].decode('cp936').encode('utf-8')
                    sdk_version = sdk_file_info[1]
                    sdk_id = sdk_file_info[2].split('_')[1]

                    sdk_info_item = {}
                    sdk_info_item[SDK_ID] = sdk_id
                    sdk_info_item[SDK_NAME] = sdk_name
                    sdk_info_item[SDK_VERSION] = sdk_version
                    sdk_info_item[SDK_PATH] = sdk_file_path

                    sdk_list_data.append(sdk_info_item)

        return sdk_list_data

    # 获取系统目录的标志
    def get_system_tag(self):
        system = platform.system()
        if system == 'Windows':
            return '\\'
        else:
            return '/'

    # 选择渠道资源后，更新渠道配置UI
    def on_up_data_channel_ui(self, sdk_id, sdk_name, sdk_version):
        self.function(sdk_id, sdk_name, sdk_version)


# 自定义排序列表(可以添加控件的列表)
class MySDKList(ULC.UltimateListCtrl):

    def __init__(self, parent, list_size, columns, channel_data, updata_func):
        """
        list_size 为 (750, 700), 定义列表大小
        columns 为数组形式[("AA", 100), ("BB", 100)], 定义表头名称及大小
        """
        ULC.UltimateListCtrl.__init__(self, parent, -1, size=list_size, style=wx.LC_REPORT,
                                      agwStyle=ULC.ULC_REPORT | ULC.ULC_HAS_VARIABLE_ROW_HEIGHT
                                      | wx.LC_VRULES | wx.LC_HRULES | ULC.ULC_NO_HIGHLIGHT)

        self.func = updata_func
        self.set_columns(columns)

        # 转化数据格式, 进行排序, 数据必须得有索引
        # 数据格式为：{0:("a","abc","ABC"),  1:("1","123","一二三"),
        new_channel_data = {}
        for item in range(len(channel_data)):
            # 获取数据
            item_data = channel_data[item]
            sdk_id = item_data.get(SDK_ID, '')
            sdk_name = item_data.get(SDK_NAME, '')
            sdk_version = item_data.get(SDK_VERSION, '')
            sdk_path = item_data.get(SDK_PATH, '')

            # 添加图标
            icon_bmp = wx.ArtProvider.GetBitmap(wx.ART_TIP, wx.ART_TOOLBAR)
            sdk_icon = wx.StaticBitmap(self, -1, icon_bmp, (35, 35))

            # 添加下载按钮
            sdk_choose_button = wx.Button(self, label='选择', style=wx.BORDER_MASK, size=(65, 28))

            button_marks = {}  # 存储渠道信息
            button_marks[SDK_ID] = str(sdk_id)
            button_marks[SDK_NAME] = str(sdk_name)
            button_marks[SDK_VERSION] = str(sdk_version)
            button_marks[SDK_PATH] = str(sdk_path)

            sdk_choose_button.Bind(wx.EVT_BUTTON, lambda evt, mark=button_marks: self.button_checked(evt, mark))

            values = (str(sdk_id), sdk_icon, str(sdk_name), str(sdk_version), sdk_choose_button)

            new_channel_data[item] = values

        # 显示列表数据
        self.show_channel_list(new_channel_data)

    def set_columns(self, columns):
        """添加表头信息"""
        i = 0
        for name, width in columns:
            self.InsertColumn(i, name, wx.LIST_FORMAT_CENTRE, width)
            i += 1

    def show_channel_list(self, data):
        """显示列表数据"""

        for key, values in data.items():
            index = self.InsertStringItem(99999999999, values[0])  # 插入一行
            for i in range(len(values[1:])):  # 为这一行的列设置值

                if i == 0:  # 设置渠道图标
                    self.SetItemWindow(index, i + 1, values[i + 1], expand=True)

                elif i == 3:  # 设置选择按钮
                    self.SetItemWindow(index, i + 1, values[i + 1], expand=False)

                else:  # 设置文字
                    self.SetStringItem(index, i + 1, values[i + 1])

    def button_checked(self, event, mark):
        """点击按钮事件"""
        sdk_id = mark[SDK_ID]
        sdk_name = mark[SDK_NAME]
        sdk_version = mark[SDK_VERSION]
        sdk_path = mark[SDK_PATH]
        self.func(sdk_name, sdk_id, sdk_version, sdk_path)