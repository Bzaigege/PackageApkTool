#!/usr/bin/env python
# -*- coding:utf-8 -*-

from ModifyResourceUtils import *
from MyConfigParser import *
import codecs


# 修改YSDK渠道SDK assets目录下的ysdkconf.ini文件
def modify_ysdk_assets_resource(channel_path, channel_version, config):

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