#!/usr/bin/env python
# -*- coding:utf-8 -*-

from channel import SpecialChannel
from channel.ModifyResourceUtils import *


# 修改当乐渠道资源
class DangleChannel(SpecialChannel.SpecialChannel):

    def modify_manifest_resource(self, channel_path, channel_version, config):

        try:

            gameMainActivity = ''
            if config.has_key('gameMainActivity'):
                gameMainActivity = config['gameMainActivity']

            MERCHANT_ID = ''
            if config.has_key('MERCHANT_ID'):
                MERCHANT_ID = config['MERCHANT_ID']

            app_id = ''
            if config.has_key('app_id'):
                app_id = config['app_id']

            app_key = ''
            if config.has_key('app_key'):
                app_key = config['app_key']

            seq_num = ''
            if config.has_key('seq_num'):
                seq_num = config['seq_num']

            tree = read_manifest(channel_path)
            activities_nodes = find_activity_nodes(tree)
            tag_activity = find_node_by_name(activities_nodes, 'com.downjoy.activity.SdkLoadActivity')
            tag_activity_meta_nodes = find_nodes(tag_activity, 'meta-data')

            cp_main_node = find_node_by_name(tag_activity_meta_nodes, 'CP_ACTIVITY')
            if gameMainActivity and cp_main_node != None:
                cp_main_node.set(Node_value, gameMainActivity)

            merchat_id_node = find_node_by_name(tag_activity_meta_nodes, 'MERCHANT_ID')
            if MERCHANT_ID and merchat_id_node != None:
                merchat_id_node.set(Node_value, MERCHANT_ID)

            app_id_node = find_node_by_name(tag_activity_meta_nodes, 'APP_ID')
            if app_id and app_id_node != None:
                app_id_node.set(Node_value, app_id)

            app_key_node = find_node_by_name(tag_activity_meta_nodes, 'APP_KEY')
            if app_key and app_key_node != None:
                app_key_node.set(Node_value, app_key)

            seq_num_node = find_node_by_name(tag_activity_meta_nodes, 'SERVER_SEQ_NUM')
            if seq_num and seq_num_node != None:
                seq_num_node.set(Node_value, seq_num)

            SdkActivity_node = find_node_by_name(activities_nodes, 'com.downjoy.activity.SdkActivity')
            SdkActivity_data = SdkActivity_node.find('intent-filter/data')
            if app_id and SdkActivity_data != None:
                SdkActivity_data.set(Node_scheme, app_id)

            write_manifest(tree, channel_path)
            return 0, u'modify manifest success'

        except Exception as e:
            return 1, u'modify manifest fail' + str(e)