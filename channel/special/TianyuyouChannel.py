#!/usr/bin/env python
# -*- coding:utf-8 -*-

from channel import SpecialChannel
from channel.ModifyResourceUtils import *


# 修改天宇游渠道资源
class TianyuyouChannel(SpecialChannel.SpecialChannel):

    def modify_assets_resource(self, channel_path, channel_version, config):

        modify_file_name = 'tygrm_ak.json'
        modify_file_path = find_specific_resource_path(channel_path, 'assets', modify_file_name)
        if not modify_file_path:
            return 1, 'not find assets/tygrm_ak.json'

        modify_file_name2 = 'tygrm_config_p.json'
        modify_file_path2 = find_specific_resource_path(channel_path, 'assets', modify_file_name2)
        if not modify_file_path2:
            return 1, 'not find assets/tygrm_config_p.json'

        try:

            tygrm_ak = ''
            if config.has_key('tygrm_ak'):
                tygrm_ak = config['tygrm_ak']

            tygrm_config_p = ''
            if config.has_key('tygrm_config_p'):
                tygrm_config_p = config['tygrm_config_p']

            if tygrm_ak:
                modify_text(modify_file_path, tygrm_ak)

            if tygrm_config_p:
                modify_text(modify_file_path2, tygrm_config_p)

            return 0, u'modify assets resource success'

        except Exception as e:
            return 1, u'modify assets resource fail' + str(e)