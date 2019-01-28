#!/usr/bin/env python
# -*- coding:utf-8 -*-

from channel import SpecialChannel
from channel.ModifyResourceUtils import *


# 修改朋友玩渠道资源
class PengyouwanChannel(SpecialChannel.SpecialChannel):

    def modify_assets_resource(self, channel_path, channel_version, config):

        modify_file_name = 'pywsdk.data'
        modify_file_path = find_specific_resource_path(channel_path, 'assets', modify_file_name)
        if not modify_file_path:
            return 1, 'not find assets/pywsdk.data'

        try:

            app_id = ''
            if config.has_key('app_key'):
                app_id = config['app_key']

            fr = open(modify_file_path, 'r')
            data = fr.read()
            fr.close()

            json_str = json.loads(data)

            info_str = ''
            if json_str.has_key('info'):
                info_str = json_str['info']

            if info_str:
                if info_str.has_key('game_key') and app_id:
                    info_str['game_key'] = app_id

            print json_str

            fw = open(modify_file_path, 'w')
            fw.write(json.dumps(json_str, ensure_ascii=False))

            return 0, u'modify assets resource success'

        except Exception as e:
            return 1, u'modify assets resource fail' + str(e)