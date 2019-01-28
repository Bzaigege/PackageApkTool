#!/usr/bin/env python
# -*- coding:utf-8 -*-

from channel import SpecialChannel
from channel.ModifyResourceUtils import *


# 修改OPPO渠道资源
class OppoChannel(SpecialChannel.SpecialChannel):

    # 修改manifest_resource
    def modify_manifest_resource(self, channel_path, channel_version, config):

        try:

            app_key = ''
            if config.has_key('app_key'):
                app_key = config['app_key']

            tree = read_manifest(channel_path)
            meta_data_nodes = find_metadata_nodes(tree)

            oppo_appkey_meta = find_node_by_name(meta_data_nodes, 'app_key')
            if app_key and oppo_appkey_meta != None:
                oppo_appkey_meta.set(Node_value, app_key)

            write_manifest(tree, channel_path)

            return 0, u'modify manifest success'

        except Exception as e:
            return 1, u'modify manifest fail' + str(e)