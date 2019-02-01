#!/usr/bin/env python
# -*-coding:utf-8 -*-

from collections import OrderedDict

DEFAULT_CONFIG = OrderedDict([(u'app_id', ''), (u'app_key', ''), (u'app_secret', '')])

CONFIG_Oppo = OrderedDict([(u'app_key', '')])

CONFIG_Huawei = OrderedDict([(u'app_id', ''), (u'cp_id', '')])

CONFIG_Ysdk = OrderedDict([(u'app_id', ''), (u'wx_app_id', '')])

CONFIG_Lenovo = OrderedDict([(u'app_id', '')])

CONFIG_Thyx = OrderedDict([(u'app_id', ''), (u'app_key', '')])

CONFIG_Ludashi = OrderedDict([(u'sdk_channel', ''), (u'ludashi_channel', '')])

CONFIG_Dangle = OrderedDict([(u'gameMainActivity', ''), (u'MERCHANT_ID', ''), (u'app_id', ''), (u'app_key', ''), (u'seq_num', '')])

CONFIG_Guaimao = OrderedDict([(u'app_id', '')])

CONFIG_YouxiFan = OrderedDict([(u'app_id', ''), (u'gameid', ''), (u'SDK_AGENT', ''), (u'YG_APPID', '')])

CONFIG_WufanYouxi = OrderedDict([(u'app_key', ''), (u'private_key', '')])

CONFIG_Yijie = OrderedDict([(u'app_id', '')])

CONFIG_TT = OrderedDict([(u'game_ids', ''), (u'secret_key', '')])

CONFIG_JueFeng = OrderedDict([(u'game_ids', ''), (u'app_key', '')])

CONFIG_Qishizhushou = OrderedDict([(u'game_ids', '')])

CONFIG_Pengyouwan = OrderedDict([(u'app_key', '')])

CONFIG_Muzhiwan = OrderedDict([(u'Appkey', '')])

CONFIG_Tianyuyou = OrderedDict([(u'tygrm_ak', ''), (u'tygrm_config_p', '')])

CONFIG_Leyou = OrderedDict([(u'app_id', ''), (u'gameid', ''), (u'agent', '')])


# 获取默认的配置
def get_channel_configs(channel_name='default', channel_id='1', channel_version='1.0.0'):

    default_config = DEFAULT_CONFIG
    if channel_id == '17':
        default_config = CONFIG_Oppo

    elif channel_id == '20':  # 华为渠道SDK
        default_config = CONFIG_Huawei

    elif channel_id == '28':  # 应用宝渠道SDK
        default_config = CONFIG_Ysdk

    elif channel_id == '36':  # 联想渠道SDK
        default_config = CONFIG_Lenovo

    elif channel_id == '39':  # 头号游戏渠道SDK
        default_config = CONFIG_Thyx

    elif channel_id == '41':  # 鲁大师渠道SDK
        default_config = CONFIG_Ludashi

    elif channel_id == '45':  # 当乐渠道SDK
        default_config = CONFIG_Dangle

    elif channel_id == '46':  # 怪猫渠道SDK
        default_config = CONFIG_Guaimao

    elif channel_id == '47':  # 游戏Fan渠道SDK
        default_config = CONFIG_YouxiFan

    elif channel_id == '49':  # 悟饭游戏渠道SDK
        default_config = CONFIG_WufanYouxi

    elif channel_id == '50':  # 易接渠道SDK
        default_config = CONFIG_Yijie

    elif channel_id == '52':  # TT渠道SDK
        default_config = CONFIG_TT

    elif channel_id == '55':  # 绝峰渠道SDK
        default_config = CONFIG_JueFeng

    elif channel_id == '56':  # 骑士助手渠道SDK
        default_config = CONFIG_Qishizhushou

    elif channel_id == '57':  # 朋友玩渠道SDK
        default_config = CONFIG_Pengyouwan

    elif channel_id == '58':  # 拇指玩渠道SDK
        default_config = CONFIG_Muzhiwan

    elif channel_id == '67':  # 天宇游渠道SDK
        default_config = CONFIG_Tianyuyou

    elif channel_id == '68':  # 乐游渠道SDK
        default_config = CONFIG_Leyou

    # 默认都添加包名
    default_config.update({u'game_package': ''})
    return default_config