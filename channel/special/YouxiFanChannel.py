#!/usr/bin/env python
# -*- coding:utf-8 -*-

from channel import SpecialChannel
from channel.ModifyResourceUtils import *


# 修改游戏Fan渠道资源
class YouxiFanChannel(SpecialChannel.SpecialChannel):

    def modify_manifest_resource(self, channel_path, channel_version, config):

        try:
            app_id = ''
            if config.has_key('app_id'):
                app_id = config['app_id']

            gameid = ''
            if config.has_key('gameid'):
                gameid = config['gameid']

            SDK_AGENT = ''
            if config.has_key('SDK_AGENT'):
                SDK_AGENT = config['SDK_AGENT']

            YG_APPID = ''
            if config.has_key('YG_APPID'):
                YG_APPID = config['YG_APPID']

            tree = read_manifest(channel_path)
            meta_data_nodes = find_metadata_nodes(tree)

            YG_APPID_meta = find_node_by_name(meta_data_nodes, 'YG_APPID')
            if YG_APPID and YG_APPID_meta != None:
                YG_APPID_meta.set(Node_value, 'YG_APPID:' + YG_APPID)

            SDK_APPID_meta = find_node_by_name(meta_data_nodes, 'SDK_APPID')
            if app_id and SDK_APPID_meta != None:
                SDK_APPID_meta.set(Node_value, app_id)

            SDK_GAMEID_meta = find_node_by_name(meta_data_nodes, 'SDK_GAMEID')
            if gameid and SDK_GAMEID_meta != None:
                SDK_GAMEID_meta.set(Node_value, gameid)

            SDK_AGENT_meta = find_node_by_name(meta_data_nodes, 'SDK_AGENT')
            if SDK_AGENT and SDK_AGENT_meta != None:
                SDK_AGENT_meta.set(Node_value, SDK_AGENT)

            write_manifest(tree, channel_path)
            return 0, u'modify manifest success'

        except Exception as e:
            return 1, u'modify manifest fail' + str(e)