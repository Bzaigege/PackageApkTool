#!/usr/bin/env python
# -*- coding:utf-8 -*-

from channel import SpecialChannel
from channel.ModifyResourceUtils import *


# 修改绝峰渠道资源
class JueFengChannel(SpecialChannel.SpecialChannel):

    def modify_manifest_resource(self, channel_path, channel_version, config):

        try:
            app_id = ''
            if config.has_key('game_ids'):
                app_id = config['game_ids']

            app_key = ''
            if config.has_key('app_key'):
                app_key = config['app_key']

            tree = read_manifest(channel_path)
            meta_data_nodes = find_metadata_nodes(tree)

            appid_meta = find_node_by_name(meta_data_nodes, 'JF_APPID')
            if app_id and appid_meta != None:
                appid_meta.set(Node_value, app_id)

            appkey_meta = find_node_by_name(meta_data_nodes, 'JF_APPKEY')
            if app_key and appkey_meta != None:
                appkey_meta.set(Node_value, app_key)

            write_manifest(tree, channel_path)
            return 0, u'modify manifest success'

        except Exception as e:
            return 1, u'modify manifest fail' + str(e)