#!/usr/bin/env python
# -*- coding:utf-8 -*-

from channel.ModifyResourceUtils import *
from channel.ModifyChannelSplash import *
import channel.SpecialChannel as special
import special.DangleChannel as dangle
import special.YsdkChannel as ysdk
import special.QihooChannel as qihoo
import special.OppoChannel as oppo
import special.HuaweiChannel as huawei
import special.LenovoChannel as lenovo
import special.LudashiChannel as ludashi
import special.ThyxChannel as thyx
import special.GuaimaoChannel as guaimao
import special.TTChannel as tt
import special.PengyouwanChannel as pyw
import special.TianyuyouChannel as tyy
import special.YouxiFanChannel as yxf
import special.WufanYouxiChannel as wfyx
import special.YijieChannel as yijie
import special.JueFengChannel as jf
import special.QishizhushouChannel as vqs
import special.MuzhiwanChannel as mzw
import special.LeyouChannel as leyou
import special.BilibiliChannel as bili


#
#  修改渠道assets目录资源统一入口, 根据渠道的id来分发, version来做版本版本控制
#
def modify_channel_assets_resource(channel_path, channel_id, channel_version, config):

    # 默认特殊渠道
    special_channel = special.SpecialChannel('special_channel')

    if channel_id == '28':  # 应用宝渠道YSDK
        special_channel = ysdk.YsdkChannel('ysdk')

    elif channel_id == '46':  # 怪猫渠道SDK
        special_channel = guaimao.GuaimaoChannel('guaimao')

    elif channel_id == '52':  # TT渠道SDK
        special_channel = tt.TTChannel('tt')

    elif channel_id == '57':  # 朋友玩渠道SDK
        special_channel = pyw.PengyouwanChannel('pyw')

    elif channel_id == '67':  # 天宇游渠道SDK
        special_channel = tyy.TianyuyouChannel('tyy')

    status, result = special_channel.modify_assets_resource(channel_path, channel_version, config)
    return status, result


#
#  修改渠道res目录资源统一入口, 根据渠道的id来分发, version来做版本版本控制
#
def modify_channel_res_resource(channel_path, channel_id, channel_version, config):

    # 默认特殊渠道
    special_channel = special.SpecialChannel('special_channel')

    if channel_id == '26':  # 360渠道SDK
        special_channel = qihoo.QihooChannel('360')

    status, result = special_channel.modify_res_resource(channel_path, channel_version, config)
    return status, result


#
#  修改渠道AndroidManifest.xml资源统一入口, 根据渠道的id来分发, version来做版本版本控制
#
def modify_channel_manifest(channel_path, channel_id, channel_version, config):

    # 默认修改包名
    try:
        modify_manifest_package_name(channel_path, config)
    except Exception as e:
        return 1, u'modify manifest package_name fail' + str(e)

    # 默认特殊渠道
    special_channel = special.SpecialChannel('special_channel')

    if channel_id == '17':  # OPPO渠道SDK
        special_channel = oppo.OppoChannel('oppo')

    elif channel_id == '20':  # 华为渠道SDK
        special_channel = huawei.HuaweiChannel('huawei')

    elif channel_id == '26':  # 360渠道SDK
        special_channel = qihoo.QihooChannel('360')

    elif channel_id == '28':  # 应用宝渠道SDK
        special_channel = ysdk.YsdkChannel('ysdk')

    elif channel_id == '36':  # 联想渠道SDK
        special_channel = lenovo.LenovoChannel('lenovo')

    elif channel_id == '39':  # 头号游戏渠道SDK
        special_channel = thyx.ThyxChannel('thyx')

    elif channel_id == '41':  # 鲁大师渠道SDK
        special_channel = ludashi.LudashiChannel('ludashi')

    elif channel_id == '45':  # 当乐渠道SDK
        special_channel = dangle.DangleChannel('dangle')

    elif channel_id == '47':  # 游戏Fan渠道SDK
        special_channel = yxf.YouxiFanChannel('yxf')

    elif channel_id == '49':  # 悟饭游戏渠道SDK
        special_channel = wfyx.WufanYouxiChannel('wfyx')

    elif channel_id == '50':  # 易接渠道SDK
        special_channel = yijie.YijieChannel('yijie')

    elif channel_id == '55':  # 绝峰渠道SDK
        special_channel = jf.JueFengChannel('juefeng')

    elif channel_id == '56':  # 骑士助手渠道SDK
        special_channel = vqs.QishizhushouChannel('vqs')

    elif channel_id == '58':  # 拇指玩渠道SDK
        special_channel = mzw.MuzhiwanChannel('mzw')

    elif channel_id == '68':  # 乐游渠道SDK
        special_channel = leyou.LeyouChannel('leyou')

    status, result = special_channel.modify_manifest_resource(channel_path, channel_version, config)
    return status, result


#
#  处理下,渠道微信登录、支付等相关功能需在包名下配置： 包名.wxapi.xxx.java问题
#
def modify_channel_wx_callback(tools_path, temp_path, channel_path, channel_id, channel_version, config):

    # 默认特殊渠道
    special_channel = special.SpecialChannel('special_channel')

    if channel_id == '28':  # 应用宝渠道SDK
        special_channel = ysdk.YsdkChannel('ysdk')

    elif channel_id == '60':  # Bili渠道SDK
        special_channel = bili.BilibiliChannel('bili')

    status, result = special_channel.modify_wx_callback_resource(tools_path, temp_path, channel_path, channel_version, config)
    return status, result


#
#  处理下,渠道闪屏问题 和 修改游戏主入口问题
#
def modify_channel_splash_and_main(game_path, channel_id, channel_version, config):

    status, result = modify_splash_and_gameMain(game_path, channel_id, channel_version, config)
    return status, result



