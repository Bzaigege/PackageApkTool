#!/usr/bin/env python
# -*- coding:utf-8 -*-

from channel import SpecialChannel
from channel.ModifyResourceUtils import *


# 修改联想渠道资源
class LenovoChannel(SpecialChannel.SpecialChannel):

    def modify_manifest_resource(self, channel_path, channel_version, config):

        try:

            app_id = ''
            if config.has_key('app_id'):
                app_id = config['app_id']

            tree = read_manifest(channel_path)
            meta_data_nodes = find_metadata_nodes(tree)

            lenovo_appid_meta = find_node_by_name(meta_data_nodes, 'lenovo.open.appid')
            if app_id and lenovo_appid_meta != None:
                lenovo_appid_meta.set(Node_value, app_id)

            lenovo_app_channel_meta = find_node_by_name(meta_data_nodes, 'lenovo:channel')
            if app_id and lenovo_app_channel_meta != None:
                lenovo_app_channel_meta.set(Node_value, app_id)

            lenovo_alipay_meta = find_node_by_name(meta_data_nodes, 'alipayquick')
            if app_id and lenovo_alipay_meta != None:
                lenovo_alipay_meta.set(Node_value, app_id)

            receiver_nodes = find_receiver_nodes(tree)
            GameSdkReceiver_node = find_node_by_name(receiver_nodes, 'com.lenovo.lsf.gamesdk.receiver.GameSdkReceiver')
            # 注意：intent-filter/action 的标签可能有多个action
            node_action_data = GameSdkReceiver_node.findall('intent-filter/action')

            for node in node_action_data:
                action_name = node.get(Node_name)
                # 根据标识来读取，因为lenovo的app_id规则包含有app.ln
                if action_name.find('app.ln') >= 0:
                    node.set(Node_name, app_id)

            activity_nodes = find_activity_nodes(tree)
            TempVBTypeChooseActivity_node = find_node_by_name(activity_nodes,
                                                              'com.lenovo.lsf.pay.ui.TempVBTypeChooseActivity')
            wx_node_child_data = TempVBTypeChooseActivity_node.find('intent-filter/data')
            if app_id and wx_node_child_data != None:
                wx_node_child_data.set(Node_scheme, app_id)

            write_manifest(tree, channel_path)

            return 0, u'modify manifest success'

        except Exception as e:
            return 1, u'modify manifest fail' + str(e)