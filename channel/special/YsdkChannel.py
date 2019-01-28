#!/usr/bin/env python
# -*- coding:utf-8 -*-

from channel import SpecialChannel
from channel.MyConfigParser import *
from channel.ModifyResourceUtils import *
import codecs


# 修改YSDK渠道资源
class YsdkChannel(SpecialChannel.SpecialChannel):

    def modify_assets_resource(self, channel_path, channel_version, config):

        modify_file_name = 'ysdkconf.ini'
        modify_file_path = find_specific_resource_path(channel_path, 'assets', modify_file_name)
        if not modify_file_path:
            return 1, 'not find assets/ysdkconf.ini'

        try:

            qq_app_id = ''
            if config.has_key('app_id'):
                qq_app_id = config['app_id']

            wx_app_id = ''
            if config.has_key('wx_app_id'):
                wx_app_id = config['wx_app_id']

            #
            # 这里需要处理下：因为ysdkconf.ini的原始文件不是.ini的标准格式：
            # [default]
            # key1 = value1
            # key2 = value2
            # 需要添加头[YSDK]
            # 而且ysdkconf.ini的字符集为utf-8-sig,需要处理下为utf-8(蛋疼)
            #

            fr = codecs.open(modify_file_path, "r", "utf-8-sig")
            ini_text = fr.read()
            fr.close()
            fw = codecs.open(modify_file_path, 'w+', 'utf-8')
            fw.write(ini_text)
            fw.close()

            head = 'YSDK'
            write_file_insert_specific_row(modify_file_path, 0, '[' + head + ']')

            # 解析.ini格式内容 (解决ConfigParser库没法保留注释和强制转化为小写问题)
            config = RawConfigParser()
            config.readfp(open(modify_file_path, 'r'))

            if qq_app_id:
                config.set(head, 'QQ_APP_ID', qq_app_id)
                config.set(head, 'OFFER_ID', qq_app_id)

            if wx_app_id:
                config.set(head, 'WX_APP_ID', wx_app_id)

            config.write(open(modify_file_path, 'w'))

            delete_file_specific_row(modify_file_path, '[' + head + ']')

            return 0, u'modify assets resource success'

        except Exception as e:
            return 1, u'modify assets resource fail' + str(e)

    def modify_manifest_resource(self, channel_path, channel_version, config):

        try:

            qq_app_id = ''
            if config.has_key('app_id'):
                qq_app_id = config['app_id']

            wx_app_id = ''
            if config.has_key('wx_app_id'):
                wx_app_id = config['wx_app_id']

            access_id = ''
            if config.has_key('xg_access_id'):
                access_id = config['xg_access_id']

            access_key = ''
            if config.has_key('xg_access_key'):
                access_key = config['xg_access_key']

            game_package_name = ''
            if config.has_key(CONF_package):  # 游戏包名
                game_package_name = config[CONF_package]

            tree = read_manifest(channel_path)
            activity_nodes = find_activity_nodes(tree)

            # 修改授权的QQ_app_id
            qq_activity_node = find_node_by_name(activity_nodes, 'com.tencent.tauth.AuthActivity')
            qq_node_child_data = qq_activity_node.find('intent-filter/data')
            if qq_app_id and qq_node_child_data != None:
                modify_value = 'tencent' + qq_app_id
                qq_node_child_data.set(Node_scheme, modify_value)

            # 修改授权的wx_app_id
            wx_activity_name = game_package_name + '.wxapi.WXEntryActivity'
            wx_activity_node = find_node_by_name(activity_nodes, wx_activity_name)
            if wx_activity_node != None:
                wx_node_child_data = wx_activity_node.find('intent-filter/data')
                if wx_app_id and wx_node_child_data != None:
                    wx_node_child_data.set(Node_scheme, wx_app_id)

            meta_data_nodes = find_metadata_nodes(tree)

            # 修改授权的信鸽 access_id
            access_id_meta = find_node_by_name(meta_data_nodes, 'XG_V2_ACCESS_ID')
            if access_id and access_id_meta != None:
                access_id_meta.set(Node_value, access_id)

            # 修改授权的信鸽 access_key
            access_key_meta = find_node_by_name(meta_data_nodes, 'XG_V2_ACCESS_KEY')
            if access_key and access_key_meta != None:
                access_key_meta.set(Node_value, access_key)

            write_manifest(tree, channel_path)

            return 0, u'modify manifest success'

        except Exception as e:
            return 1, u'modify manifest fail' + str(e)

    def modify_wx_callback_resource(self, tools_path, temp_path, channel_path, channel_version, config):

        status, result = modify_wx_resource(tools_path, temp_path, channel_path, config, 'WXEntryActivity.java')
        return status, result