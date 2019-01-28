#!/usr/bin/env python
# -*- coding:utf-8 -*-

from channel import SpecialChannel
from channel.ModifyResourceUtils import *


# 修改华为渠道资源
class HuaweiChannel(SpecialChannel.SpecialChannel):

    def modify_manifest_resource(self, channel_path, channel_version, config):

        try:

            app_id = ''
            if config.has_key('app_id'):
                app_id = config['app_id']

            cp_id = ''
            if config.has_key('cp_id'):
                cp_id = config['cp_id']

            tree = read_manifest(channel_path)
            meta_data_nodes = find_metadata_nodes(tree)
            appid_meta = find_node_by_name(meta_data_nodes, 'com.huawei.hms.client.appid')
            if app_id and appid_meta != None:
                appid_meta.set(Node_value, app_id)

            cpid_meta = find_node_by_name(meta_data_nodes, 'com.huawei.hms.client.cpid')
            if cp_id and cpid_meta != None:
                cpid_meta.set(Node_value, cp_id)

            write_manifest(tree, channel_path)

            return 0, u'modify manifest success'

        except Exception as e:
            return 1, u'modify manifest fail' + str(e)