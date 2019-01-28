#!/usr/bin/env python
# -*- coding:utf-8 -*-

from channel import SpecialChannel
from channel.ModifyResourceUtils import *


# 修改怪猫渠道资源
class GuaimaoChannel(SpecialChannel.SpecialChannel):

    def modify_assets_resource(self, channel_path, channel_version, config):

        modify_file_name = 'GMConfig.xml'
        modify_file_path = find_specific_resource_path(channel_path, 'assets', modify_file_name)
        if not modify_file_path:
            return 1, 'not find assets/GMConfig.xml'

        try:

            app_id = ''
            if config.has_key('app_id'):
                app_id = config['app_id']

            modify_xml_dom = ET.parse(modify_file_path)
            modify_xml_root = modify_xml_dom.getroot()
            gameInfo_node = find_nodes(modify_xml_root, 'gameinfo')
            # print gameInfo_node[0].attrib

            gssAppId = gameInfo_node[0].get('gssAppId')
            appMode = gameInfo_node[0].get('appMode')

            if app_id and gssAppId:
                gameInfo_node[0].set('gssAppId', app_id)

            # 打包时, 默认设置为正式环境
            if appMode:
                gameInfo_node[0].set('appMode', 'release')

            modify_xml_dom.write(modify_file_path, encoding='UTF-8', xml_declaration=True)

            return 0, u'modify assets resource success'

        except Exception as e:
            return 1, u'modify assets resource fail' + str(e)