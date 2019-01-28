#!/usr/bin/env python
# -*- coding:utf-8 -*-

from channel import SpecialChannel
from channel.ModifyResourceUtils import *


# 修改悟饭游戏渠道资源
class WufanYouxiChannel(SpecialChannel.SpecialChannel):

    def modify_manifest_resource(self, channel_path, channel_version, config):

        try:
            app_key = ''
            if config.has_key('app_key'):
                app_key = config['app_key']

            private_key = ''
            if config.has_key('private_key'):
                private_key = config['private_key']

            tree = read_manifest(channel_path)
            meta_data_nodes = find_metadata_nodes(tree)

            APP_KEY_meta = find_node_by_name(meta_data_nodes, 'PA_APP_KEY')
            if app_key and APP_KEY_meta != None:
                APP_KEY_meta.set(Node_value, app_key)

            PRIVATE_KEY_meta = find_node_by_name(meta_data_nodes, 'PA_APP_PRIVATE_KEY')
            if private_key and PRIVATE_KEY_meta != None:
                PRIVATE_KEY_meta.set(Node_value, private_key)

            write_manifest(tree, channel_path)
            return 0, u'modify manifest success'

        except Exception as e:
            return 1, u'modify manifest fail' + str(e)