#!/usr/bin/env python
# -*-coding:utf-8 -*-

from collections import OrderedDict

# 注意：这是两个全局变量，下次启动就没了
# 定义一个字典来存储已配置渠道的配置信息
CHANNEL_CONFIG = {}
# 定义一个字典来存储已配置渠道的图标信息信息
CHANNEL_ICON = {}


# 返回图标的默认项
def get_channel_icon(channel_name='default', channel_id='1', channel_version='1.0.0'):

    default_icon = CHANNEL_ICON.get(channel_id)
    if default_icon == None:
        default_icon = get_default_icon()

    return default_icon


# 获取默认的Icon配置
def get_default_icon():
    icons = OrderedDict([(u'游戏图标', {u'选择图标': ''}), (u'游戏角标', {u'选择角标': ''}), (u'游戏闪屏', {u'选择闪屏': ''})])
    return icons


# 获取默认的配置项
def get_channel_configs(channel_name='default', channel_id='1', channel_version='1.0.0'):

    default_config = CHANNEL_CONFIG.get(channel_id)

    if default_config == None:
        default_config = get_default_config()

    if channel_id == '17':
        default_config = get_oppo_config()

    elif channel_id == '20':  # 华为渠道SDK
        default_config = get_huawei_config()

    elif channel_id == '28':  # 应用宝渠道SDK
        default_config = get_ysdk_config()

    elif channel_id == '36':  # 联想渠道SDK
        default_config = get_lenovo_config()

    elif channel_id == '39':  # 头号游戏渠道SDK
        default_config = get_thyx_config()

    elif channel_id == '41':  # 鲁大师渠道SDK
        default_config = get_ludashi_config()

    elif channel_id == '45':  # 当乐渠道SDK
        default_config = get_dangle_config()

    elif channel_id == '46':  # 怪猫渠道SDK
        default_config = get_guaimao_config()

    elif channel_id == '47':  # 游戏Fan渠道SDK
        default_config = get_youxifan_config()

    elif channel_id == '49':  # 悟饭游戏渠道SDK
        default_config = get_wufanyouxi_config()

    elif channel_id == '50':  # 易接渠道SDK
        default_config = get_yijie_config()

    elif channel_id == '52':  # TT渠道SDK
        default_config = get_tt_config()

    elif channel_id == '55':  # 绝峰渠道SDK
        default_config = get_juefeng_config()

    elif channel_id == '56':  # 骑士助手渠道SDK
        default_config = get_qszs_config()

    elif channel_id == '57':  # 朋友玩渠道SDK
        default_config = get_pyw_config()

    elif channel_id == '58':  # 拇指玩渠道SDK
        default_config = get_mzw_config()

    elif channel_id == '67':  # 天宇游渠道SDK
        default_config = get_tyy_config()

    elif channel_id == '68':  # 乐游渠道SDK
        default_config = get_leyou_config()

    return default_config


# 获取默认的配置
def get_default_config():
    configs = OrderedDict([(u'app_id', ''), (u'app_key', ''), (u'app_secret', '')])
    return configs


# 获取oppo默认的配置
def get_oppo_config():
    configs = OrderedDict([(u'app_key', '')])
    return configs


# 获取华为默认的配置
def get_huawei_config():
    configs = OrderedDict([(u'app_id', ''), (u'cp_id', '')])
    return configs


# 获取YSDK默认的配置
def get_ysdk_config():
    configs = OrderedDict([(u'app_id', ''), (u'wx_app_id', '')])
    return configs


# 获取联想默认的配置
def get_lenovo_config():
    configs = OrderedDict([(u'app_id', '')])
    return configs


# 获取头号游戏默认的配置
def get_thyx_config():
    configs = OrderedDict([(u'app_id', ''), (u'app_key', '')])
    return configs


# 获取鲁大师默认的配置
def get_ludashi_config():
    configs = OrderedDict([(u'sdk_channel', ''), (u'ludashi_channel', '')])
    return configs


# 获取当乐默认的配置
def get_dangle_config():
    configs = OrderedDict([(u'gameMainActivity', ''), (u'MERCHANT_ID', ''), (u'app_id', ''), (u'app_key', ''), (u'seq_num', '')])
    return configs


# 获取怪猫默认的配置
def get_guaimao_config():
    configs = OrderedDict([(u'app_id', '')])
    return configs


# 获取游戏Fan默认的配置
def get_youxifan_config():
    configs = OrderedDict([(u'app_id', ''), (u'gameid', ''), (u'SDK_AGENT', ''), (u'YG_APPID', '')])
    return configs


# 获取悟饭游戏默认的配置
def get_wufanyouxi_config():
    configs = OrderedDict([(u'app_key', ''), (u'private_key', '')])
    return configs


# 获取易接默认的配置
def get_yijie_config():
    configs = OrderedDict([(u'app_id', '')])
    return configs


# 获取TT默认的配置
def get_tt_config():
    configs = OrderedDict([(u'game_ids', ''), (u'secret_key', '')])
    return configs


# 获取绝峰默认的配置
def get_juefeng_config():
    configs = OrderedDict([(u'game_ids', ''), (u'app_key', '')])
    return configs


# 获取骑士助手默认的配置
def get_qszs_config():
    configs = OrderedDict([(u'game_ids', '')])
    return configs


# 获取朋友玩默认的配置
def get_pyw_config():
    configs = OrderedDict([(u'app_key', '')])
    return configs


# 获取拇指玩默认的配置
def get_mzw_config():
    configs = OrderedDict([(u'Appkey', '')])
    return configs


# 获取天宇游默认的配置
def get_tyy_config():
    configs = OrderedDict([(u'tygrm_ak', ''), (u'tygrm_config_p', '')])
    return configs


# 获取乐游默认的配置
def get_leyou_config():
    configs = OrderedDict([(u'app_id', ''), (u'gameid', ''), (u'agent', '')])
    return configs