#!/usr/bin/env python
# -*- coding:utf-8 -*-

from channel import SpecialChannel
from channel.ModifyResourceUtils import *


# 修改乐游渠道资源
class LeyouChannel(SpecialChannel.SpecialChannel):

    def modify_manifest_resource(self, channel_path, channel_version, config):

        try:
            app_id = ''
            if config.has_key('app_id'):
                app_id = config['app_id']

            gameid = ''
            if config.has_key('gameid'):
                gameid = config['gameid']

            agent = ''
            if config.has_key('agent'):
                agent = config['agent']

            tree = read_manifest(channel_path)
            meta_data_nodes = find_metadata_nodes(tree)

            appID_meta = find_node_by_name(meta_data_nodes, 'MG_APPID')
            if app_id and appID_meta != None:
                appID_meta.set(Node_value, app_id)

            gameID_meta = find_node_by_name(meta_data_nodes, 'MG_GAMEID')
            if gameid and gameID_meta != None:
                gameID_meta.set(Node_value, gameid)

            agent_meta = find_node_by_name(meta_data_nodes, 'MG_AGENT')
            if agent and agent_meta != None:
                agent_meta.set(Node_value, agent)

            write_manifest(tree, channel_path)
            return 0, u'modify manifest success'

        except Exception as e:
            return 1, u'modify manifest fail' + str(e)