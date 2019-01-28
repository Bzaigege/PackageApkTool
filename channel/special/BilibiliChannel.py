#!/usr/bin/env python
# -*- coding:utf-8 -*-

from channel import SpecialChannel
from channel.ModifyResourceUtils import *


# 修改哔哩哔哩渠道资源
class BilibiliChannel(SpecialChannel.SpecialChannel):

    def modify_wx_callback_resource(self, tools_path, temp_path, channel_path, channel_version, config):

        status, result = modify_wx_resource(tools_path, temp_path, channel_path, config, 'WXPayEntryActivity.java')
        return status, result