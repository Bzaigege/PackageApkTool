#!/usr/bin/env python
# -*- coding:utf-8 -*-

from channel import SpecialChannel
from channel.ModifyResourceUtils import *
from channel import MyProperty


# 修改当乐渠道资源
class TTChannel(SpecialChannel.SpecialChannel):

    # 修改manifest_resource
    def modify_assets_resource(self, channel_path, channel_version, config):

        modify_file_name = 'TTGameSDKConfig.cfg'
        modify_file_path = find_specific_resource_path(channel_path, 'assets', modify_file_name)
        if not modify_file_path:
            return 1, 'not find assets/TTGameSDKConfig.cfg'

        modify_file_name_2 = 'tt_game_sdk_opt.properties'
        modify_file_path_2 = find_specific_resource_path(channel_path, 'assets', modify_file_name_2)
        if not modify_file_path_2:
            return 1, 'not find assets/tt_game_sdk_opt.properties'

        try:

            app_id = ''
            if config.has_key('game_ids'):
                app_id = config['game_ids']

            secret_key = ''
            if config.has_key('secret_key'):
                secret_key = config['secret_key']

            # 注意这里的TTGameSDKConfig.cfg不是规范的cfg格式,直接删除添加新的字符就可以了
            if secret_key:
                modify_text(modify_file_path, secret_key)

            if app_id:
                props = MyProperty.parse(modify_file_path_2)
                props.put('gameId', app_id)

            return 0, u'modify assets resource success'

        except Exception as e:
            return 1, u'modify assets resource fail' + str(e)