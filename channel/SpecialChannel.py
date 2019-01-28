#!/usr/bin/env python
# -*- coding:utf-8 -*-


# 定义特殊渠道父类
class SpecialChannel(object):

    def __init__(self, channel_name):
        self.channel_name = channel_name

    # 修改assets_resource
    def modify_assets_resource(self, channel_path, channel_version, config):
        print "%s modify_assets_resource" % self.channel_name
        return 0, "%s modify_assets_resource" % self.channel_name

    # 修改res_resource
    def modify_res_resource(self, channel_path, channel_version, config):
        print "%s modify_res_resource" % self.channel_name
        return 0, "%s modify_res_resource" % self.channel_name

    # 修改manifest_resource
    def modify_manifest_resource(self, channel_path, channel_version, config):
        print "%s modify_manifest_resource" % self.channel_name
        return 0, "%s modify_manifest_resource" % self.channel_name

    # 修改微信回调包名.wxapi.xxx.java问题
    def modify_wx_callback_resource(self, tools_path, temp_path, channel_path, channel_version, config):
        print "%s modify_wx_callback_resource" % self.channel_name
        return 0, "%s modify_wx_callback_resource" % self.channel_name
