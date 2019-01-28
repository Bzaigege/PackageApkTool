#!/usr/bin/env python
# -*-coding:utf-8 -*-

import os,json
from utils.ConfigUtils import *
from xml.dom.minidom import *


# 修改游戏的闪屏逻辑及修改游戏入口名字
# TODO 游戏已接入聚合SDK的闪屏, 分三种情况讨论：
# TODO 1、游戏先闪屏，后SDK闪屏
# TODO 2、SDK先闪屏，后游戏闪屏
# TODO 3、游戏没有接入SDK闪屏,那部分渠道需要处理闪屏逻辑没法处理
#
# TODO 但是这里只讨论游戏已接入聚合SDK的闪屏且SDK先闪屏，游戏的闪屏教给SDK处理
def modify_splash_and_gameMain(game_path, channel_id, channel_version, config):

    try:

        gameMainActivity = ''
        if config.has_key('gameMainActivity'):
            gameMainActivity = config['gameMainActivity']

        package_name = ''
        if config.has_key(CONF_package):
            package_name = config[CONF_package]

        game_AndroidManifest = os.path.join(game_path, 'AndroidManifest.xml')
        gameDom = xml.dom.minidom.parse(game_AndroidManifest)
        gameRoot = gameDom.documentElement

        activity_nodes = gameRoot.getElementsByTagName('activity')
        activity_names_list = []     # activity名称列表

        # 聚合SDK闪屏的名字
        sdk_splash_activity_name = 'com.bzai.gamesdk.common.utils_ui.activity.SplashActivity'
        sdk_splash_activity = None

        # 游戏启动入口名字
        launcher_activity_name = ''
        launcher_activity = None

        # SDK闪屏后跳转标志SYSDK.MAIN列表
        sdk_tag_activities = []

        #  遍历获取合并后的gameActivity信息
        for activity in activity_nodes:

            activity_names_list.append(activity.getAttribute('android:name'))

            # 找到游戏启动项的activity, 只有一个
            if activity.toxml().find("android.intent.action.MAIN") > 0 \
                    and activity.toxml().find("android.intent.category.LAUNCHER") > 0:
                launcher_activity_name = activity.getAttribute('android:name')
                launcher_activity = activity

            # 找到SDK闪屏
            if activity.getAttribute('android:name') == sdk_splash_activity_name:
                sdk_splash_activity = activity

            # 找到可能存在的跳转标志activity, 可能有两个(但是一般只有一个，最多有两个)
            # 如联想渠道的闪屏入口就是Bzai.MAIN,需将游戏的配置改为lenovoid.MAIN
            if activity.toxml().find("Bzai.MAIN") > 0 \
                    and activity.toxml().find("android.intent.category.DEFAULT") > 0:
                sdk_tag_activities.append(activity)

        if sdk_splash_activity_name in activity_names_list:
            if launcher_activity_name == sdk_splash_activity_name:

                sdk_first_splash(channel_id, channel_version, activity_nodes, launcher_activity, sdk_tag_activities,
                                 package_name, gameMainActivity)

        else:
            print u'游戏没有接入SDK闪屏'
            # todo 游戏没有接入SDK闪屏,提示打包失败

        # 保存修改后的文件
        fp = open(game_AndroidManifest, 'w')
        # fp = open(game_AndroidManifest, 'w', encoding='utf-8')  # python3.6.5
        # 第一个参数是目标文件对象，第二个参数是根节点的缩进格式，第三个参数是其他子节点的缩进格式，
        # 第四个参数制定了换行格式，第五个参数制定了xml内容的编码。
        gameDom.writexml(fp, indent='', addindent='\t', newl='\n', encoding='UTF-8')
        fp.close()

        return 0, u'modify splashActivity success'

    except Exception as e:
        return 1, u'modify splashActivity fail' + str(e)


# 游戏接入了SDK闪屏，SDK先闪屏，后游戏闪屏, 注意这种情况下，默认是将SDK闪屏的配置Bzai.MAIN，认为为游戏主入口。
# 即若有游戏闪屏，则游戏闪屏为游戏主入口; 若无游戏闪屏,则配置的activity为游戏主入口
def sdk_first_splash(channel_id, channel_version, activity_nodes, launcher_activity, sdk_tag_activities,
                     package_name, gameMainActivity=None):

    print u'SDK先闪屏，channel_id: %s' % channel_id

    if channel_id == '36':  # 联想渠道
        modify_lenovo_splash(channel_version, sdk_tag_activities, gameMainActivity)

    elif channel_id == '45':  # 当乐渠道
        modify_dangle_splash(channel_version, sdk_tag_activities, gameMainActivity)

    elif channel_id == '47':  # 游戏Fan渠道
        modify_youxifan_splash(channel_version, sdk_tag_activities, gameMainActivity)

    elif channel_id == '50':  # 易接渠道
        modify_yijie_splash(channel_version, sdk_tag_activities, gameMainActivity)

    elif channel_id == '57':  # 朋友玩渠道
        modify_pengyouwan_splash(channel_version, sdk_tag_activities, package_name, gameMainActivity)

    elif channel_id == '68':  # 乐游渠道
        modify_leyou_splash(channel_version, sdk_tag_activities, gameMainActivity)

    elif channel_id == '69':  # 果盘渠道
        modify_guopan_splash(channel_version, sdk_tag_activities, gameMainActivity)

    else:

        if channel_id == '28':  # YSDK需将初始闪屏设置为singleTop启动模式
            launcher_activity.setAttribute('android:launchMode', 'singleTop')

        # 需改游戏入口的名称
        if gameMainActivity:
            for activity in activity_nodes:
                if activity.toxml().find("Bzai.MAIN") > 0 \
                        and activity.toxml().find("android.intent.category.DEFAULT") > 0:
                    activity.setAttribute('android:name', gameMainActivity)


# 联想渠道，需将游戏入口SYSDK.MAIN改为lenovoid.MAIN
def modify_lenovo_splash(channel_version, sdk_tag_activities, gameMainActivity=None):

    lenovo_splash_activity_name = 'com.lenovo.lsf.gamesdk.ui.WelcomeActivity'
    lenovo_splash_activity_tag = 'lenovoid.MAIN'
    modify_channel_splash(lenovo_splash_activity_name, lenovo_splash_activity_tag, sdk_tag_activities, gameMainActivity)


# 当乐渠道，需将原游戏配置入口SYSDK.MAIN去掉,保留SdkLoadActivity下的配置就可以了
# 且在修改SdkLoadActivity属性时，已修改游戏主入口
def modify_dangle_splash(channel_version, sdk_tag_activities, gameMainActivity=None):

    dangle_splash_activity_name = 'com.downjoy.activity.SdkLoadActivity'

    game_main_activity = ''
    for tag_activity in sdk_tag_activities:
        if dangle_splash_activity_name != tag_activity.getAttribute('android:name'):
            game_main_activity = tag_activity

    game_main_activity_filter = game_main_activity.getElementsByTagName('intent-filter')[0]
    if game_main_activity_filter:
        game_main_activity.removeChild(game_main_activity_filter)


# 游戏Fan渠道，需将游戏入口SYSDK.MAIN改为YouXiFan.MAIN
def modify_youxifan_splash(channel_version, sdk_tag_activities, gameMainActivity=None):

    youxifan_splash_activity_name = 'com.suyutech.sysdk.channel.youxiFan.YouxiFanSplashActivity'
    youxifan_splash_activity_tag = 'YouXiFan.MAIN'
    modify_channel_splash(youxifan_splash_activity_name, youxifan_splash_activity_tag, sdk_tag_activities, gameMainActivity)


# 易接渠道，需将游戏入口SYSDK.MAIN改为YiJie.MAIN
def modify_yijie_splash(channel_version, sdk_tag_activities, gameMainActivity=None):

    yijie_splash_activity_name = 'com.suyutech.sysdk.channel.yijie.YijieSplashActivity'
    yijie_splash_activity_tag = 'YiJie.MAIN'
    modify_channel_splash(yijie_splash_activity_name, yijie_splash_activity_tag, sdk_tag_activities, gameMainActivity)


# 乐游渠道，需将游戏入口SYSDK.MAIN改为LeYou.MAIN
def modify_leyou_splash(channel_version, sdk_tag_activities, gameMainActivity=None):

    leyou_splash_activity_name = 'com.suyutech.sysdk.channel.leyou.LeyouSplashActivity'
    leyou_splash_activity_tag = 'LeYou.MAIN'
    modify_channel_splash(leyou_splash_activity_name, leyou_splash_activity_tag, sdk_tag_activities, gameMainActivity)


# 果盘渠道，需将游戏入口SYSDK.MAIN改为com.flamingo.sdk.MAIN
def modify_guopan_splash(channel_version, sdk_tag_activities, gameMainActivity=None):

    guopan_splash_activity_name = 'com.flamingo.sdk.view.GPSplashActivity'
    guopan_splash_activity_tag = 'com.flamingo.sdk.MAIN'
    modify_channel_splash(guopan_splash_activity_name, guopan_splash_activity_tag, sdk_tag_activities, gameMainActivity)


# 朋友玩渠道，需将游戏入口SYSDK.MAIN改为${applicationId}.pyw.MAIN
def modify_pengyouwan_splash(channel_version, sdk_tag_activities, package_name, gameMainActivity=None):

    pyw_splash_activity_name = 'com.pengyouwan.sdk.activity.LauncherActivity'
    pyw_splash_activity_tag = package_name + '.pyw.MAIN'
    modify_channel_splash(pyw_splash_activity_name, pyw_splash_activity_tag, sdk_tag_activities, gameMainActivity)


#
# 统一修改渠道的闪屏标记位
#
def modify_channel_splash(channel_splash_activity_name, channel_splash_activity_tag, sdk_tag_activities,
                          gameMainActivity=None):

    game_main_activity = ''
    for tag_activity in sdk_tag_activities:
        if channel_splash_activity_name != tag_activity.getAttribute('android:name'):
            game_main_activity = tag_activity

    game_main_activity_filter = game_main_activity.getElementsByTagName('intent-filter')[0]
    game_main_activity_actions = game_main_activity_filter.getElementsByTagName('action')
    for tag_action in game_main_activity_actions:
        if tag_action.getAttribute('android:name') == 'SYSDK.MAIN':
            tag_action.setAttribute('android:name', channel_splash_activity_tag)

    # 需改游戏入口的名称
    if gameMainActivity:
        game_main_activity.setAttribute('android:name', gameMainActivity)


#
# xml.dom.minidom 原生库写入格式太丑，下面是重写方法：fixed_writexml
# 覆盖 xml.dom.minidom.Element.writexml = fixed_writexml
#
def fixed_writexml(self, writer, indent="", addindent="", newl=""):
    # indent = current indentation
    # addindent = indentation to add to higher levels
    # newl = newline string
    writer.write(indent + "<" + self.tagName)

    attrs = self._get_attributes()
    a_names = attrs.keys()
    a_names.sort()

    for a_name in a_names:
        writer.write(" %s=\"" % a_name)
        xml.dom.minidom._write_data(writer, attrs[a_name].value)
        writer.write("\"")
    if self.childNodes:
        if len(self.childNodes) == 1 \
                and self.childNodes[0].nodeType == xml.dom.minidom.Node.TEXT_NODE:
            writer.write(">")
            self.childNodes[0].writexml(writer, "", "", "")
            writer.write("</%s>%s" % (self.tagName, newl))
            return
        writer.write(">%s" % (newl))
        for node in self.childNodes:
            if node.nodeType is not xml.dom.minidom.Node.TEXT_NODE:
                node.writexml(writer, indent + addindent, addindent, newl)
        writer.write("%s</%s>%s" % (indent, self.tagName, newl))
    else:
        writer.write("/>%s" % (newl))

xml.dom.minidom.Element.writexml = fixed_writexml