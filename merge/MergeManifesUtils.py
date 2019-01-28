#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
from utils.LogUtils import *
from utils.ConfigUtils import *
from MergeXmlUitls import *

# 合并Manifest.xml目录资源的库


# 合并androidManifest.xml文件资源
def merger_manifest_config(task_id, temp_path, channel_path, build_config):

    logger = LogUtils.sharedInstance(task_id)

    # 读取配置文件的信息
    package_name = ''
    minSdk = ''
    targetSdk = ''

    if build_config.has_key(CONF_package):
        package_name = build_config[CONF_package]

    if build_config.has_key(CONF_minSdkVersion):
        minSdk = build_config[CONF_minSdkVersion]

    if build_config.has_key(CONF_targetSdkVersion):
        targetSdk = build_config[CONF_targetSdkVersion]

    try:

        # 读取游戏母包的AndroidManifest
        game_AndroidManifest = os.path.join(temp_path, 'AndroidManifest.xml')
        gameDom = xml.dom.minidom.parse(game_AndroidManifest)
        gameRoot = gameDom.documentElement
        game_old_package_name = gameRoot.getAttribute('package')

        # 处理下apktool无法识别compileSdkVersion 、compileSdkVersionCodename 等问题
        # 还要注意，这两个字段是compileSdkVersion = 28 后才出现的,需要将targetSdkVersion设置为23以上
        compileSdkVersion = gameRoot.getAttribute('android:compileSdkVersion')
        compileSdkVersion_name = gameRoot.getAttribute('android:compileSdkVersionCodename')

        game_application = gameRoot.getElementsByTagName('application')
        game_permissions = gameRoot.getElementsByTagName('uses-permission')
        game_supports_screens = gameRoot.getElementsByTagName('supports-screens')

        game_sdk = gameRoot.getElementsByTagName('uses-sdk')
        if game_sdk:
            game_min_sdk = game_sdk[0].getAttribute('android:minSdkVersion')
            game_target_sdk = game_sdk[0].getAttribute('android:targetSdkVersion')
            logger.info(u'game_min_sdk : %s' % game_min_sdk)
            logger.info(u'game_target_sdk : %s' % game_target_sdk)

        logger.info(u'开始修改游戏包名....')
        if package_name:
            new_package_name = package_name
        else:
            new_package_name = game_old_package_name

        gameRoot.setAttribute('package', new_package_name)
        logger.info(u'设置游戏包名: ' + new_package_name)

        logger.info(u'开始修改 uses-Sdk....')
        if not game_sdk:
            if minSdk or targetSdk or compileSdkVersion:
                sdk_node = gameDom.createElement('uses-sdk')
                gameRoot.appendChild(sdk_node)
                game_sdk = gameRoot.getElementsByTagName('uses-sdk')
        if minSdk:
            game_sdk[0].setAttribute('android:minSdkVersion', minSdk)
            logger.info(u'设置游戏minSdk: %s' % minSdk)

        if targetSdk:
            game_sdk[0].setAttribute('android:targetSdkVersion', targetSdk)
            logger.info(u'设置游戏targetSdk: %s' % targetSdk)

        if compileSdkVersion:
            game_sdk[0].setAttribute('android:targetSdkVersion', compileSdkVersion)
            logger.info(u'设置游戏targetSdk: %s' % compileSdkVersion)

        # 修改完targetSdkVersion后, 删除属性
        if compileSdkVersion:
            gameRoot.removeAttribute('android:compileSdkVersion')

        if compileSdkVersion_name:
            gameRoot.removeAttribute('android:compileSdkVersionCodename')

        # 读取渠道AndroidManifest
        channel_AndroidManifest = os.path.join(channel_path, 'AndroidManifest.xml')
        channelDom = xml.dom.minidom.parseString(del_xml_note(channel_AndroidManifest))
        channelRoot = channelDom.documentElement
        channel_application = channelRoot.getElementsByTagName('application')
        channel_permissions = channelRoot.getElementsByTagName('uses-permission')
        channel_supports_screens = channelRoot.getElementsByTagName('supports-screens')

        logger.info(u'开始合并uses-permission....')
        game_has_permission = []
        if game_permissions:
            for game_permission in game_permissions:
                game_has_permission.append(game_permission.getAttribute('android:name'))
        logger.info(u'游戏已存在 uses-permission : ' + str(game_has_permission))

        game_add_permission = []
        if channel_permissions:
            for channel_permission in channel_permissions:
                name = channel_permission.getAttribute('android:name')
                if name not in game_has_permission:
                    gameRoot.appendChild(channel_permission)
                    game_add_permission.append(name)
        logger.info(u'游戏添加 uses-permission : ' + str(game_add_permission))

        logger.info(u'开始合并supports-screens....')
        game_add_supports_screens = []
        if channel_supports_screens:
            # 判断游戏是否存在该节点
            if not game_supports_screens:
                screens_node = gameDom.createElement('supports-screens')
                gameRoot.appendChild(screens_node)
                game_supports_screens = gameRoot.getElementsByTagName('supports-screens')
            logger.info(u'游戏已存在 supports-screens : ' + str(game_supports_screens[0].attributes.keys()))

            for supports_screen in channel_supports_screens[0].attributes.keys():

                if supports_screen not in game_supports_screens[0].attributes.keys():
                    game_supports_screens[0].setAttribute(
                        supports_screen, channel_supports_screens[0].getAttribute(supports_screen))
                    game_add_supports_screens.append(supports_screen)

            logger.info(u'游戏添加 supports-screens : ' + str(game_add_supports_screens))

        logger.info(u'开始合并application....')
        game_has_application_child = []
        if game_application:
            for game_application_child in game_application[0].childNodes:
                if game_application_child.nodeType == 1:
                    game_child_name = game_application_child.getAttribute('android:name')
                    game_has_application_child.append(game_child_name)
        logger.info(u'游戏已存在 application-child : ' + str(game_has_application_child))

        game_add_application_child = []
        if channel_application:
            for channel_application_child in channel_application[0].childNodes:
                if channel_application_child.nodeType == 1:
                    channel_child_name = channel_application_child.getAttribute('android:name')
                    if channel_child_name not in game_has_application_child:
                        game_application[0].appendChild(channel_application_child)
                        game_add_application_child.append(channel_child_name)
        logger.info(u'游戏添加 application-child : ' + str(game_add_application_child))

        # 保存修改后的文件
        fp = open(game_AndroidManifest, 'w')
        # fp = open(game_AndroidManifest, 'w', encoding='utf-8')  # python3.6.5
        # 第一个参数是目标文件对象，第二个参数是根节点的缩进格式，第三个参数是其他子节点的缩进格式，
        # 第四个参数制定了换行格式，第五个参数制定了xml内容的编码。
        gameDom.writexml(fp, indent='', addindent='\t', newl='\n', encoding='UTF-8')
        fp.close()

        return 0, u'合并Manifest.xml文件成功', new_package_name

    except Exception as e:
        return 1, u'合并AndroidManifest异常:' + str(e), ''


# 删除xml中的注释
def del_xml_note(xmlfile):
    fp = open(xmlfile, 'r')
    data = fp.read()
    fp.close()
    a = re.subn(r'<!--.*?-->', '', data, flags=re.DOTALL)
    return a[0]