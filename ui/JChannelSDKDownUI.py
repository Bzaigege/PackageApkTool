#!/usr/bin/env python
# -*-coding:utf-8 -*-
from __future__ import print_function
import wx
import os
import shutil
import json
import threading
import requests
from contextlib import closing
import wx.lib.agw.ultimatelistctrl as ULC
from utils.ConfigUtils import *

SDK_SERVER_URL = "xxxxxxxxxxxxxxxxxx"

CHANNEL_ID = 'id'   # 渠道id
CHANNEL_NAME = 'name'  # 渠道名
CHANNEL_ALIAS = 'alias'  # 渠道别名
CHANNEL_INFO = 'down_info'  # 渠道sdk{“sdk版本”：”下载地址”}
CHANNEL_VERSION = 'version'  # 渠道版本
CHANNEL_NEW_VERSION = 'new_version'  # 渠道版本
CHANNEL_DOWN_URL = 'down_url'  # 下载地址


# 弹出SDK下载框
class JChannelSDKDownDialog(wx.Dialog):

    def __init__(self, parent, frame_size, func):
        super(JChannelSDKDownDialog, self).__init__(parent, title='下载渠道SDK资源', size=frame_size)
        self.Center()  # 窗口居中

        self.window = parent
        self.panel = wx.Panel(self)
        self.main_layout = None
        self.main_channel_list = None

        self.func = func

        self.channel_data = self.get_local_data()

        self.init_ui()  # 绘制Dialog的界面

        # 拦截弹窗的关闭事件, 当用户在下载的时候, 不让用户关闭当前弹窗
        self.Bind(wx.EVT_CLOSE, self.on_close_dialog)

    def init_ui(self):

        self.main_layout = wx.BoxSizer(wx.VERTICAL)

        green_size = self.window.Size
        a = green_size[0]*0.8
        b = green_size[1]*0.8

        space_length = a/15

        # 创建排序列表列标题
        main_list_columns = [("渠道ID", space_length), ("图标", space_length), ("SDK名称", space_length*3),
                             ("SDK别名", space_length*2), ("SDK当前版本", space_length*1.8), ("SDK最新版本", space_length*1.8),
                             ("操作项", space_length*2), ("状态栏", space_length*2)]
        self.main_channel_list = MyChannelList(self.panel, (a, b), space_length, main_list_columns, self.channel_data)

        self.main_layout.Add(self.main_channel_list, 1, wx.EXPAND | wx.ALL, 2)
        self.panel.SetSizer(self.main_layout)
        self.panel.Fit()

    # 获取服务端数据
    def get_channel_data(self):

        try:

            data = requests.get(SDK_SERVER_URL)
            if data.status_code == 200:
                content = json.loads(data.text)
                return content

            else:
                return ''

        except Exception as e:
            return ''

    # 获取模拟数据
    def get_local_data(self):

        json_file_path = os.path.join(DIR_WorkSpace, DIR_UIConfig, 'channel_data.json')

        try:
            with open(json_file_path, 'r') as data_json:
                channel_json = json.load(data_json)
                return channel_json

        except Exception as e:
            print (str(e))
            return ''

    def on_close_dialog(self, evt):

        is_downing = False
        checked_buttons = self.main_channel_list.get_checked_buttons()
        for button in checked_buttons:
            is_downing = not (button.IsEnabled())
            if is_downing:  # 只要有一个没下载完就跳出循环
                break

        if is_downing:
            warning_box = wx.MessageDialog(None, "正在下载SDK资源, 无法关闭当前界面！", "警告", wx.OK)
            if warning_box.ShowModal() == wx.OK:
                warning_box.Destroy()

        else:
            self.EndModal(wx.ID_CANCEL)
            self.func()
            self.Destroy()


# 自定义排序列表(可以添加控件的列表)
class MyChannelList(ULC.UltimateListCtrl):

    def __init__(self, parent, list_size, space_length, columns, channel_data):
        """
        list_size 为 (750, 700), 定义列表大小
        columns 为数组形式[("AA", 100), ("BB", 100)], 定义表头名称及大小
        """
        ULC.UltimateListCtrl.__init__(self, parent, -1, size=list_size, style=wx.LC_REPORT,
                                      agwStyle=ULC.ULC_REPORT | ULC.ULC_HAS_VARIABLE_ROW_HEIGHT
                                      | wx.LC_VRULES | wx.LC_HRULES | ULC.ULC_NO_HIGHLIGHT)

        self.dialog = parent
        self.button_checked_dict = []  # 存储下载按钮的点击状态

        # 转化数据格式, 进行排序, 数据必须得有索引
        # 数据格式为：{0:("a","abc","ABC"),  1:("1","123","一二三"),
        new_channel_data = {}
        for item in range(len(channel_data)):
            # 获取数据
            item_data = channel_data[item]
            channel_id = item_data.get(CHANNEL_ID, '')
            channel_name = item_data.get(CHANNEL_NAME, '')
            channel_alias = item_data.get(CHANNEL_ALIAS, '')
            channel_info = item_data.get(CHANNEL_INFO, '')
            # print '%s=%s' % (channel_alias, item_data)

            channel_new_version = ''
            channel_new_down_url = ''
            channel_server_version_list = []

            # 下载地址可能为空
            if len(channel_info):
                channel_info_items = {}
                for version_item, down_url_item in channel_info.items():
                    channel_server_version_list.append(version_item)
                    channel_info_items[version_item] = down_url_item

                    channel_new_version = max(channel_server_version_list)  # 获取最新版本
                    channel_new_down_url = channel_info_items.get(channel_new_version)

            channel_current_version = self.get_local_version(str(channel_name))

            # 添加图标
            icon_bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_TOOLBAR)
            channel_icon = wx.StaticBitmap(self, -1, icon_bmp, (35, 35))

            # 添加下载按钮
            channel_down_button = wx.Button(self, label='下载', size=((space_length*2)-5, 28))
            if not channel_new_down_url:
                channel_down_button.SetLabel('无法下载')
                channel_down_button.SetBackgroundColour('#A9A9A9')

            version_error = False
            if not channel_current_version == '未下载':
                if channel_current_version <= channel_new_version:
                    channel_down_button.SetLabel('更新')
                else:
                    version_error = True
                    channel_down_button.SetLabel('无法下载')
                    channel_down_button.SetBackgroundColour('#A9A9A9')

            # 添加进度条
            down_progress = wx.Gauge(self, -1, range=100, style=wx.GA_HORIZONTAL | wx.GA_SMOOTH, size=((space_length*2)-5, 28))

            button_marks = {}  # 存储下载信息
            button_marks[u'id'] = item
            button_marks[u'channel_id'] = str(channel_id)
            button_marks[u'name'] = str(channel_name)
            button_marks[u'alias'] = str(channel_alias)
            button_marks[u'version'] = str(channel_new_version)
            button_marks[u'version_error'] = version_error
            button_marks[u'button'] = channel_down_button
            button_marks[u'url'] = channel_new_down_url
            button_marks[u'progress'] = down_progress
            channel_down_button.Bind(wx.EVT_BUTTON, lambda evt, mark=button_marks: self.down_button_checked(evt, mark))

            values = (str(channel_id), channel_icon, str(channel_name), str(channel_alias),
                      str(channel_current_version), str(channel_new_version), channel_down_button, down_progress)

            new_channel_data[item] = values

        self.set_columns(columns)

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

                elif i == 5:  # 设置下载按钮
                    self.SetItemWindow(index, i + 1, values[i + 1], expand=False)

                elif i == 6:  # 设置下载进度条
                    self.SetItemWindow(index, i + 1, values[i + 1], expand=False)

                else:  # 设置文字
                    self.SetStringItem(index, i + 1, values[i + 1])

    def get_local_version(self, down_name):
        """获取本地资源的版本信息"""

        down_path_dir = os.path.join(DIR_WorkSpace, DIR_DownSdk, u'%s' % down_name)
        version_list = []
        for parent, dir_names, file_names in os.walk(down_path_dir):
            for file_name in file_names:
                if file_name.endswith('zip'):
                    version_item = os.path.splitext(file_name)[0].split('_')[-1]
                    version_list.append(version_item)

        if len(version_list):
            return max(version_list)
        else:
            return '未下载'

    def down_button_checked(self, event, mark):
        """下载资源按钮事件"""

        row_id = mark[u'id']
        down_id = mark[u'channel_id']
        down_name = mark[u'name']
        down_alias = mark[u'alias']
        down_version = mark[u'version']
        down_version_error = mark[u'version_error']
        down_url = mark[u'url']
        down_button = mark[u'button']
        down_progress = mark[u'progress']

        if down_version_error:
            self.show_warning("服务器版本过低,无法下载! 请检查服务器资源。")

        else:
            if not down_url:
                self.show_warning("url为空,无法下载! 请检查服务器资源。")

            else:

                # 当前按钮设置为不可点击状态
                down_button.Disable()
                down_button.SetLabel('正在下载')
                self.button_checked_dict.append(down_button)

                thread = DownSdkThread(row_id, self.dialog, down_button, down_progress,
                                       down_id, down_name, down_alias, down_version, down_url, self.down_suc_updata_list)
                thread.start()

        event.Skip()

    def get_checked_buttons(self):
        """下载资源按钮集合"""
        return self.button_checked_dict

    def down_suc_updata_list(self, item, version):
        """下载成功后，刷新本地当前版本信息"""
        self.SetStringItem(item, 4, version)

    # 提示错误信息
    def show_warning(self, message):
        warning_msg = wx.MessageDialog(None, message, "警告", wx.OK)
        if warning_msg.ShowModal() == wx.OK:
            warning_msg.Destroy()


# 下载资源线程
class DownSdkThread(threading.Thread):

    def __init__(self, item_id, dialog, button, gauge, down_id, down_name, down_alias, down_version, down_url, updata_func):
        threading.Thread.__init__(self)

        self.item = item_id
        self.dialog = dialog
        self.button = button
        self.gauge = gauge
        self.down_id = down_id
        self.name = down_name
        self.alias = down_alias
        self.version = down_version
        self.url = down_url
        self.func = updata_func

    def run(self):

        try:
            self.down_file(self.url)

        except Exception as e:
            print (str(e))

    # 文件下载器
    def down_file(self, url):

        print (url)
        self.gauge.SetValue(0)  # 保证每次下载都是从0开始
        with closing(requests.get(url, stream=True)) as response:

            if response.status_code == 200:
                headers = response.headers
                if headers.get('content-length'):

                    # 创建下载地址, 注意创建目录乱码问题
                    down_path_dir = os.path.join(DIR_WorkSpace, DIR_DownSdk, u'%s' % self.name, self.version)
                    if not os.path.exists(down_path_dir):
                        os.makedirs(down_path_dir)

                    channel_resource_name = self.alias + '_' + self.down_id + '_' + self.version + '.zip'
                    file_down_path = os.path.join(down_path_dir, channel_resource_name)

                    size = 0
                    chunk_size = 1024  # 每次下载的数据大小
                    content_size = int(response.headers['content-length'])  # 内容体总大小
                    print('[文件大小]：%s' % (self.format_size(content_size)))
                    download_progress = 0
                    with open(file_down_path, "wb") as load_file:
                        for data in response.iter_content(chunk_size=chunk_size):
                            load_file.write(data)
                            size += len(data)
                            download_progress = size * 100 / content_size
                            # print('\r' + '[下载进度]：%s %s' % ('>' * int(size * 100 / content_size), download_progress))
                            self.gauge.SetValue(download_progress)

                    if download_progress == 100:
                        self.button.SetLabel('下载成功')
                        self.button.Enable()
                        self.func(self.item, self.version)  # 下载成功后，刷新当前版本信息

                    else:
                        self.show_warning("服务器中断,下载失败 ！请检查。")
                        if os.path.isdir(down_path_dir):
                            shutil.rmtree(down_path_dir)

                else:
                    self.show_warning("服务器资源为空,下载失败 ！请检查。")

            else:
                self.show_warning("连接服务器失败 ！请检查。")

    # 提示错误信息
    def show_warning(self, message):
        warning_msg = wx.MessageDialog(None, message, "警告", wx.OK)
        if warning_msg.ShowModal() == wx.OK:
            warning_msg.Destroy()

        self.button.SetLabel('重新下载')
        self.button.Enable()

    # 字节bytes转化kb\m\g
    def format_size(self, file_bytes):
        try:

            bytes = float(file_bytes)
            kb = bytes / 1024

        except Exception as e:
            return "Error"

        if kb >= 1024:
            M = kb / 1024
            if M >= 1024:
                G = M / 1024
                return "%fG" % (G)
            else:
                return "%fM" % (M)
        else:
            return "%fkb" % (kb)


