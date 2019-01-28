#!/usr/bin/env python
# -*- coding:utf-8 -*-

from channel import SpecialChannel
from channel.ModifyResourceUtils import *


# 修改鲁大师渠道资源
class LudashiChannel(SpecialChannel.SpecialChannel):

    def modify_manifest_resource(self, channel_path, channel_version, config):

        try:
            sdk_channel = ''
            if config.has_key('sdk_channel'):
                sdk_channel = config['sdk_channel']

            ludashi_channel = ''
            if config.has_key('ludashi_channel'):
                ludashi_channel = config['ludashi_channel']

            tree = read_manifest(channel_path)
            meta_data_nodes = find_metadata_nodes(tree)

            sdk_meta = find_node_by_name(meta_data_nodes, 'SDK_CHANNEL')
            if sdk_channel and sdk_meta != None:
                sdk_meta.set(Node_value, sdk_channel)

            ludashi_meta = find_node_by_name(meta_data_nodes, 'LUDASHI_CHANNEL')
            if ludashi_channel and ludashi_meta != None:
                ludashi_meta.set(Node_value, ludashi_channel)

            write_manifest(tree, channel_path)

            return 0, u'modify manifest success'

        except Exception as e:
            return 1, u'modify manifest fail' + str(e)