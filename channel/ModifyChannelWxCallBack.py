#!/usr/bin/env python
# -*- coding:utf-8 -*-

import shutil,json
from ModifyResourceUtils import *
from utils.ShellUtils import *


def modify_ysdk_wx_resource(tools_path, temp_path, channel_path, channel_version, config):

    try:

        wx_callback_dir = os.path.join(channel_path, 'wxcallback')

        # 处理下.java文件，不然会报编码错误
        java_list = get_file_list(wx_callback_dir, '.java')
        for java_file in java_list:
            delete_java_note(java_file)

        package_name = ''
        if config.has_key('package'):
            package_name = config['package']

        # 处理包名问题：
        if package_name:
            wx_callback_file = os.path.join(wx_callback_dir, 'WXEntryActivity.java')
            new_package_str = 'package ' + package_name + '.wxapi;'
            # 删除包名所在行
            delete_file_specific_row(wx_callback_file, 'package')
            # 添加新的包名在第一行
            write_file_insert_specific_row(wx_callback_file, 0, new_package_str)

        # 将.java文件转化为.class文件
        wx_callback_class_dir = os.path.join(channel_path, 'wxcallback', 'class')
        if not os.path.exists(wx_callback_class_dir):
            os.makedirs(wx_callback_class_dir)

        class_resource = get_compile_class_path(temp_path, tools_path)
        status, result = java_compile_class(wx_callback_dir, class_resource, wx_callback_class_dir)
        if not status == 0:
            return status, result

        # 将.class文件打包成.jar文件
        wx_callback_jar_path = os.path.join(temp_path, 'lib', 'wx_callback.jar')
        status, result = class_compile_jar(wx_callback_class_dir, wx_callback_jar_path)
        if not status == 0:
            return status, result

        if os.path.exists(wx_callback_jar_path):
            shutil.rmtree(wx_callback_class_dir)
            return 0, u'modify wx_callback success'
        else:
            return 1, u'modify wx_callback fail'

    except Exception as e:
        return 1, u'modify wx_callback fail' + str(e)



