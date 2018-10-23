#!/usr/bin/env python
# -*- coding:utf-8 -*-

from ModifyResourceUtils import *


# 修改360渠道res/xml目录下的 qihoo_game_sdk_sync_adapter.xml
def modify_360_res_resource(channel_path, channel_version, config):

    # 需要修改文件的名称
    modify_xml_dir = 'xml'
    modify_xml_name = 'qihoo_game_sdk_sync_adapter.xml'
    channel_res_path = os.path.join(channel_path, 'res')

    modify_xml_path = find_specific_resource_path(channel_res_path, modify_xml_dir, modify_xml_name)
    if modify_xml_path:
        if config.has_key('package'):  # 游戏包名
            game_package_name = config['package']

    if game_package_name:
        try:
            # 在parse前一定要设置namespace, 不然就会出现 ns0:name错误，而不是预期的 android:name
            ET.register_namespace('android', "http://schemas.android.com/apk/res/android")
            modify_xml_dom = ET.parse(modify_xml_path)
            modify_xml_root = modify_xml_dom.getroot()

            suffix_str = '.cx.accounts.syncprovider'
            modify_value = game_package_name + suffix_str
            modify_xml_root.set('{http://schemas.android.com/apk/res/android}contentAuthority', modify_value)

            modify_xml_dom.write(modify_xml_path, encoding='UTF-8', xml_declaration=True)

            return 0, u'modify res resource success'

        except Exception as e:
            return 1, u'modify res resource fail' + str(e)