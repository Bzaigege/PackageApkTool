#!/usr/bin/env python
# -*- coding:utf-8 -*-

from channel import SpecialChannel
from channel.ModifyResourceUtils import *


# 修改奇虎360渠道资源
class QihooChannel(SpecialChannel.SpecialChannel):

    def modify_res_resource(self, channel_path, channel_version, config):

        # 需要修改文件的名称
        modify_xml_dir = 'xml'
        modify_xml_name = 'qihoo_game_sdk_sync_adapter.xml'
        channel_res_path = os.path.join(channel_path, 'res')

        modify_xml_path = find_specific_resource_path(channel_res_path, modify_xml_dir, modify_xml_name)
        if modify_xml_path:
            if config.has_key(CONF_package):  # 游戏包名
                game_package_name = config[CONF_package]

        if game_package_name:
            try:
                # 在parse前一定要设置namespace, 不然就会出现 ns0:name错误，而不是预期的 android:name
                ET.register_namespace('android', "http://schemas.android.com/apk/res/android")
                modify_xml_dom = ET.parse(modify_xml_path)
                modify_xml_root = modify_xml_dom.getroot()

                suffix_str = '.cx.accounts.syncprovider'
                modify_value = game_package_name + suffix_str
                modify_xml_root.set(namespace + 'contentAuthority', modify_value)

                modify_xml_dom.write(modify_xml_path, encoding='UTF-8', xml_declaration=True)

                return 0, u'modify res resource success'

            except Exception as e:
                return 1, u'modify res resource fail' + str(e)

    def modify_manifest_resource(self, channel_path, channel_version, config):

        try:

            app_id = ''
            if config.has_key('appid'):
                app_id = config['appid']

            app_key = ''
            if config.has_key('appkey'):
                app_key = config['appkey']

            private_pay_key = ''
            if config.has_key('private_pay_key'):
                private_pay_key = config['private_pay_key']

            tree = read_manifest(channel_path)
            activity_nodes = find_activity_nodes(tree)

            QhDeepLinkActivity_node = find_node_by_name(activity_nodes,
                                                        'com.qihoo.gamecenter.sdk.activity.QhDeepLinkActivity')
            link_node_child_data = QhDeepLinkActivity_node.find('intent-filter/data')
            if app_key and link_node_child_data != None:
                link_node_child_data.set(namespace + 'host', app_key)

            mete_nodes = find_metadata_nodes(tree)
            appid_meta = find_node_by_name(mete_nodes, 'QHOPENSDK_APPID')
            appkey_meta = find_node_by_name(mete_nodes, 'QHOPENSDK_APPKEY')
            app_private_key_meta = find_node_by_name(mete_nodes, 'QHOPENSDK_PRIVATEKEY')

            if app_id and appid_meta != None:
                appid_meta.set(Node_value, app_id)

            if app_key and appkey_meta != None:
                appkey_meta.set(Node_value, app_key)

            if private_pay_key and app_private_key_meta != None:
                app_private_key_meta.set(Node_value, private_pay_key)

            write_manifest(tree, channel_path)

            return 0, u'modify manifest success'

        except Exception as e:
            return 1, u'modify manifest fail' + str(e)