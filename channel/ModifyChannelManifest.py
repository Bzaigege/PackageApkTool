#!/usr/bin/env python
# -*- coding:utf-8 -*-

from ModifyResourceUtils import *


# 修改应用宝YSDK渠道的AndroidManifest
def modify_ysdk_manifest(channel_path, channel_version, config):

    try:

        modify_manifest_package_name(channel_path, config)

        qq_app_id = ''
        if config.has_key('app_id'):
            qq_app_id = config['app_id']

        wx_app_id = ''
        if config.has_key('wx_app_id'):
            wx_app_id = config['wx_app_id']

        access_id = ''
        if config.has_key('xg_access_id'):
            wx_app_id = config['xg_access_id']

        access_key = ''
        if config.has_key('xg_access_key'):
            access_key = config['xg_access_key']

        game_package_name = ''
        if config.has_key('package'):  # 游戏包名
            game_package_name = config['package']

        tree = read_manifest(channel_path)
        activity_nodes = find_activity_nodes(tree)

        # 修改授权的QQ_app_id
        qq_activity_node = find_node_by_name(activity_nodes, 'com.tencent.tauth.AuthActivity')
        qq_node_child_data = qq_activity_node.find('intent-filter/data')
        if qq_app_id and qq_node_child_data!=None:
            modify_value = 'tencent'+ qq_app_id
            qq_node_child_data.set('{http://schemas.android.com/apk/res/android}scheme', modify_value)

        # 修改授权的wx_app_id
        wx_activity_name = game_package_name + '.wxapi.WXEntryActivity'
        wx_activity_node = find_node_by_name(activity_nodes, wx_activity_name)
        wx_node_child_data = wx_activity_node.find('intent-filter/data')
        if wx_app_id and wx_node_child_data!=None:
            wx_node_child_data.set('{http://schemas.android.com/apk/res/android}scheme', wx_app_id)

        meta_data_nodes = find_metadata_nodes(tree)

        # 修改授权的信鸽 access_id
        access_id_meta = find_node_by_name(meta_data_nodes, 'XG_V2_ACCESS_ID')
        if access_id and access_id_meta!=None:
            access_id_meta.set('{http://schemas.android.com/apk/res/android}value', access_id)

        # 修改授权的信鸽 access_key
        access_key_meta = find_node_by_name(meta_data_nodes, 'XG_V2_ACCESS_KEY')
        if access_key and access_key_meta!=None:
            access_key_meta.set('{http://schemas.android.com/apk/res/android}value', access_key)

        write_manifest(tree, channel_path)

        return 0, u'modify manifest success'

    except Exception as e:
        return 1, u'modify manifest fail' + str(e)
