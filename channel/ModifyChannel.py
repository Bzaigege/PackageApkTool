#!/usr/bin/env python
# -*- coding:utf-8 -*-

from ModifyChannelAssets import *
from ModifyChannelRes import *
from ModifyChannelManifest import *
from ModifyChannelWxCallBack import *


#
#  修改渠道assets目录资源统一入口, 根据渠道的id来分发, version来做版本版本控制
#
def modify_channel_assets_resource(channel_path, channel_id, channel_version, config):

    # 默认成功
    status = 0
    result = ''

    if channel_id == '28':  # 应用宝渠道YSDK
        status, result = modify_ysdk_assets_resource(channel_path, channel_version, config)

    return status, result


#
#  修改渠道res目录资源统一入口, 根据渠道的id来分发, version来做版本版本控制
#
def modify_channel_res_resource(channel_path, channel_id, channel_version, config):

    # 默认成功
    status = 0
    result = ''
    if channel_id == '30':  # 360渠道SDK
        status, result = modify_360_res_resource(channel_path, channel_version, config)

    return status, result


#
#  修改渠道AndroidManifest.xml资源统一入口, 根据渠道的id来分发, version来做版本版本控制
#
def modify_channel_manifest(channel_path, channel_id, channel_version, config):

    # 默认成功
    status = 0
    result = ''

    if channel_id == '28':  # 应用宝渠道SDK
        status, result = modify_ysdk_manifest(channel_path, channel_version, config)

    return status, result


#
#  处理下,渠道微信登录、支付等相关功能需在包名下配置： 包名.wxapi.xxx.java问题
#
def modify_channel_wx_callback(tools_path, temp_path, channel_path, channel_id, channel_version, config):

    # 默认成功
    status = 0
    result = ''

    if channel_id == '28':  # 应用宝渠道SDK
        status, result = modify_ysdk_wx_resource(tools_path, temp_path, channel_path, channel_version, config)

    return status, result