#!/usr/bin/env python
# -*- coding:utf-8 -*-

from channel import SpecialChannel
from channel.ModifyResourceUtils import *


# 修改拇指玩渠道资源
class MuzhiwanChannel(SpecialChannel.SpecialChannel):

    def modify_manifest_resource(self, channel_path, channel_version, config):

        try:
            app_key = ''
            if config.has_key('Appkey'):
                app_key = config['Appkey']

            tree = read_manifest(channel_path)
            meta_data_nodes = find_metadata_nodes(tree)

            appkey_meta = find_node_by_name(meta_data_nodes, 'MZWAPPKEY')
            if app_key and appkey_meta != None:
                appkey_meta.set(Node_value, app_key)

            write_manifest(tree, channel_path)
            return 0, u'modify manifest success'

        except Exception as e:
            return 1, u'modify manifest fail' + str(e)