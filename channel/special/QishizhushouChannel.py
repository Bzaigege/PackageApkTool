#!/usr/bin/env python
# -*- coding:utf-8 -*-

from channel import SpecialChannel
from channel.ModifyResourceUtils import *


# 修改骑士助手渠道资源
class QishizhushouChannel(SpecialChannel.SpecialChannel):

    def modify_manifest_resource(self, channel_path, channel_version, config):

        try:
            app_id = ''
            if config.has_key('game_ids'):
                app_id = config['game_ids']

            tree = read_manifest(channel_path)
            meta_data_nodes = find_metadata_nodes(tree)

            appid_meta = find_node_by_name(meta_data_nodes, 'VQS_GAMEID')
            if app_id and appid_meta != None:
                appid_meta.set(Node_value, app_id)

            write_manifest(tree, channel_path)
            return 0, u'modify manifest success'

        except Exception as e:
            return 1, u'modify manifest fail' + str(e)