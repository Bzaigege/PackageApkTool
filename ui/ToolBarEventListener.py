#!/usr/bin/env python
# -*-coding:utf-8 -*-

import wx
import os
import json
from utils.ConfigUtils import *
from ui.JChannelSDKDownUI import JChannelSDKDownDialog
from ui.JChannelSignUI import JChannelSignDialog


# 工具栏按钮监听事件
class ToolBarEventListener(object):

    def __init__(self):

        self.dir_config = os.path.join(DIR_WorkSpace, DIR_UIConfig)

    def open_game_apk(self, window):
        frame = window

        wildcard_text = '*.apk'
        game_apk_file_path = self.on_choose_file(frame, wildcard_text, u"选择游戏APK文件", os.getcwd().decode('GB2312').encode('utf-8'))

        config_str = {}
        if game_apk_file_path:
            config_str['game_apk_path'] = game_apk_file_path
            self.write_config_data(self.dir_config, UI_CONFIG_PARAMS, config_str)

    def set_sign_info(self, window):

        frame = window

        dlg = JChannelSignDialog(frame, self.write_sign_info)
        if dlg.IsEnabled():
            frame.Enable(enable=False)
            if not dlg.ShowModal() == wx.ID_OK:
                frame.Enable(enable=True)

    def write_sign_info(self, game_sign_file_path, keystore, store_pass, alias, key_pass):
        print (game_sign_file_path, keystore, store_pass, alias, key_pass)
        config_str = {}
        if game_sign_file_path:
            config_str['game_sign_path'] = game_sign_file_path
            config_str['game_keystore'] = keystore
            config_str['game_store_pass'] = store_pass
            config_str['game_alias'] = alias
            config_str['game_key_pass'] = key_pass
            self.write_config_data(self.dir_config, UI_CONFIG_PARAMS, config_str)

    def choose_apk_output_dir(self, window):

        frame = window

        # 设置包体输出目录
        apk_out_dir = ''
        dlg = wx.DirDialog(frame, u"选择文件夹", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            print dlg.GetPath()  # 文件夹路径
            apk_out_dir = dlg.GetPath()

        dlg.Destroy()

        # 保存信息
        dir_config_str = {}
        if apk_out_dir:
            dir_config_str['game_channel_apk_output_path'] = apk_out_dir
            self.write_config_data(self.dir_config, NAME_APK_OUTPUT, dir_config_str)

    def down_sdk_resource(self, window, updata_func):

        frame = window
        func = updata_func

        down_dlg = JChannelSDKDownDialog(frame, func)
        if down_dlg.IsEnabled():
            frame.Enable(enable=False)
            if not down_dlg.ShowModal():
                frame.Enable(enable=True)

    # 创建标准文件对话框
    def on_choose_file(self, pand, wildcard_text, title_name, default_dir):

        filename = ''
        dialog = wx.FileDialog(pand, title_name, default_dir, wildcard=wildcard_text)
        if dialog.ShowModal() == wx.ID_OK:
            filename = dialog.GetPath()
        dialog.Destroy()
        return filename

    # 写入配置文件
    def write_config_data(self, json_file_dir, json_file_name, config_str):

        try:
            if not os.path.exists(json_file_dir):
                os.makedirs(json_file_dir)

            json_path = os.path.join(json_file_dir, json_file_name)

            if not os.path.exists(json_path):
                with open(json_path, 'wb') as uiConfig:
                    uiConfig.write(json.dumps(config_str, ensure_ascii=False))

            else:
                # 如果已存在,先读取之前的信息,
                with open(json_path, 'r') as hasConfig:
                    compile_config = json.load(hasConfig)
                    for key in config_str:
                        compile_config[key] = config_str[key]

                with open(json_path, 'w') as uiConfig:
                    uiConfig.write(json.dumps(compile_config, ensure_ascii=False))

        except Exception as e:
            print e
