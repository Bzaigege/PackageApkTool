#!/usr/bin/env python
# -*- coding:utf-8 -*-


from utils.LogUtils import *
from merge.MergeUtils import *
from utils.IconUtils import *
from channel.ModifyChannel import *


# 合并assets目录资源
def merge_assets_resource(task_id, temp_path, channel_path, channel_id, channel_version, build_config):
    logger = get_logger(task_id)
    logger.info(u'合并assets资源...')

    # 合并之前修改渠道的assets资源配置文件
    status, result = modify_channel_assets_resource(channel_path, channel_id, channel_version, build_config)
    if not status == 0:
        return status, result

    status, result = copy_command(os.path.join(channel_path, 'assets'), os.path.join(temp_path, 'assets'))
    if not status == 0:
        return status, result

    return 0, u'合并 assets 资源成功'


# 合并libs目录资源
def merge_libs_resource(task_id, tools_path, temp_path, channel_path, channel_id, channel_version, build_config):

    logger = get_logger(task_id)
    logger.info(u'合并libs资源...')

    # 在这里需要先处理下jar包问题,jar里其他不是.class的文件需要转化下,要么放到assets目录下，要么放到unknown目录下
    status, result = modify_jars(temp_path, channel_path)
    if not status == 0:
        return status, result

    status, result = copy_command(os.path.join(channel_path, 'libs'), os.path.join(temp_path, 'lib'))
    if not status == 0:
        return status, result

    # 在这里处理下微信回调问题
    status, result = modify_channel_wx_callback(tools_path, temp_path, channel_path,
                                                channel_id, channel_version, build_config)
    if not status == 0:
        return status, result

    return 0, u'合并 libs 资源成功'


# 合并res目录资源
def merge_res_resource(task_id, tools_path, temp_path, channel_path, channel_id, channel_version, build_config):

    logger = get_logger(task_id)
    logger.info(u'合并res资源...')

    # 合并之前修改渠道的res资源配置文件
    status, result = modify_channel_res_resource(channel_path, channel_id, channel_version, build_config)
    if not status == 0:
        return status, result

    # 需要处理下后缀是-v4的文件夹，因为游戏反编译后的资源文件大多为-v4后缀，
    # 而渠道资源文件是没有后缀的，如果xxx 和 xxx-v4资源相同的话,会报错,需将两者合并
    dirs = ['drawable', 'drawable-hdpi', 'drawable-ldpi', 'drawable-mdpi', 'drawable-xhdpi', 'drawable-xxhdpi',
            'values', 'values-hdpi', 'values-ldpi', 'values-mdpi', 'values-xhdpi', 'values-xxhdpi']

    v4_dirs = ['drawable-hdpi-v4', 'drawable-ldpi-v4', 'drawable-mdpi-v4', 'drawable-xhdpi-v4','drawable-xxhdpi-v4',
               'values-hdpi-v4', 'values-ldpi-v4', 'values-mdpi-v4', 'values-xhdpi-v4', 'values-xxhdpi-v4']

    temp_res_dirs = os.listdir(os.path.join(temp_path, 'res'))
    channel_res_dirs = os.listdir(os.path.join(channel_path, 'res'))
    difference_list = list(set(channel_res_dirs).difference(set(temp_res_dirs)))  # 获取渠道特有的目录

    # 保证后面渠道复制时，有对应的目录路径
    for difference_dir in difference_list:

        # 如果文件名为没有v4后缀的，需判断游戏目录是否存在对应的-v4目录
        # 存在就不新建目录，后面直接复制到存在的对应-v4目录
        # 不存在就新建该名称目录，后面直接复制到该名称目录
        if difference_dir in dirs:
            difference_dir_v4 = difference_dir + '-v4'
            if difference_dir_v4 not in temp_res_dirs:
                os.makedirs(os.path.join(temp_path, 'res', difference_dir))  # 在temp中创建该目录

        # 如果文件名为有v4后缀的，需判断游戏目录是否存在对应去掉-v4后缀的目录
        # 存在就不新建目录，后面直接复制到存在的对应去掉-v4后缀目录
        # 不存在就新建该有v4后缀的目录，后面直接复制到该有v4名称目录
        elif difference_dir in v4_dirs:
            difference_dir_temp = difference_dir.replace('-v4', '')
            if difference_dir_temp not in temp_res_dirs:
                os.makedirs(os.path.join(temp_path, 'res', difference_dir))  # 在temp中创建该目录

        # 其他名称目录直接新建
        else:
            os.makedirs(os.path.join(temp_path, 'res', difference_dir))  # 在temp中创建该目录

    # 重新赋值
    temp_res_dirs = os.listdir(os.path.join(temp_path, 'res'))

    # 遍历渠道res目录
    for channel_dir in channel_res_dirs:
        if os.path.isdir(os.path.join(channel_path, 'res', channel_dir)):

            # 如果文件名为没有v4后缀的，需判断游戏目录是否存在目录
            # 如果游戏中有对应的没有v4后缀的目录，则直接合并到对应目录
            # 如果游戏中不存在没有v4后缀的目录，找到对应存在的v4后缀目录
            if channel_dir in dirs:
                if channel_dir in temp_res_dirs:
                    status, result = merge_special_dirs(temp_path, channel_path, channel_dir, channel_dir)

                else:
                    game_dir_v4 = channel_dir + '-v4'
                    status, result = merge_special_dirs(temp_path, channel_path, game_dir_v4, channel_dir)

                if status == 0:
                    logger.info(u'合并目录' + channel_dir + u' 资源成功')
                else:
                    break  # 跳出循环

            # 如果文件名为v4后缀的，需判断游戏目录是否存在目录
            # 如果游戏中有对应的v4后缀的目录，则直接合并到对应目录
            # 如果游戏中不存在v4后缀的目录，找到对应存在的去掉v4后缀目录
            elif channel_dir in v4_dirs:
                if channel_dir in temp_res_dirs:
                    status, result = merge_special_dirs(temp_path, channel_path, channel_dir, channel_dir)

                else:
                    game_dir_temp = channel_dir.replace('-v4', '')
                    status, result = merge_special_dirs(temp_path, channel_path, game_dir_temp, channel_dir)

                if status == 0:
                    logger.info(u'合并目录' + channel_dir + u' 资源成功')
                else:
                    break  # 跳出循环

            # 其他的文件夹直接复制就可以了
            else:
                status, result = copy_command(os.path.join(channel_path, 'res', channel_dir),
                                              os.path.join(temp_path, 'res', channel_dir))

                if status == 0:
                    logger.info(u'合并目录' + channel_dir + u' 资源成功')
                else:
                    break  # 跳出循环

    # 注意跳出循环后，判读状态
    if not status == 0:
        return status, result

    # 需要处理下一种特殊情况:游戏反编译后,没有v4后缀的目录和有v4后缀的目录同时存在，且文件夹合并后会有重复的文件存在,
    # 需删掉其中一个,保留v4目录的(这个bug是在windows上发现的，但是在MAC上就打包成功，很奇怪)
    temp_res_dirs = os.listdir(os.path.join(temp_path, 'res'))
    for dir in temp_res_dirs:
        if dir in dirs:
            dir_v4 = dir + '-v4'
            if dir_v4 in temp_res_dirs:
                dir_file_list = os.listdir(os.path.join(temp_path, 'res', dir))
                dir_v4_file_list = os.listdir(os.path.join(temp_path, 'res', dir_v4))
                for file in dir_file_list:
                    if file in dir_v4_file_list:
                        os.remove(os.path.join(temp_path, 'res', dir_v4, file))

    return 0, u'合并 res 资源成功'


# 合并androidManifest.xml文件资源
def merger_manifest_resource(task_id, temp_path, channel_path, channel_id, channel_version, build_config):

    logger = logging.getLogger(task_id)

    # 读取配置文件的信息
    package_name = ''
    minSdk = ''
    targetSdk = ''
    if build_config.has_key('package'):
        package_name = build_config['package']

    if build_config.has_key('minSdk'):
        minSdk = build_config['minSdk']

    if build_config.has_key('targetSdk'):
        targetSdk = build_config['targetSdk']

    # 合并之前修改渠道的配置文件
    status, result = modify_channel_manifest(channel_path, channel_id, channel_version, build_config)
    if not status == 0:
        return status, result, package_name

    try:

        game_AndroidManifest = os.path.join(temp_path, 'AndroidManifest.xml')
        channel_AndroidManifest = os.path.join(channel_path, 'AndroidManifest.xml')

        # 读取游戏母包的AndroidManifest
        gameDom = xml.dom.minidom.parse(game_AndroidManifest)
        gameRoot = gameDom.documentElement
        game_old_package_name = gameRoot.getAttribute('package')
        game_application = gameRoot.getElementsByTagName('application')
        game_permissions = gameRoot.getElementsByTagName('uses-permission')
        game_supports_screens = gameRoot.getElementsByTagName('supports-screens')

        game_sdk = gameRoot.getElementsByTagName('uses-sdk')
        if game_sdk:
            game_min_sdk = game_sdk[0].getAttribute('android:minSdkVersion')
            game_target_sdk = game_sdk[0].getAttribute('android:targetSdkVersion')
            logger.info(u'game_min_sdk : %s' % game_min_sdk)
            logger.info(u'game_target_sdk : %s' % game_target_sdk)

        # 读取渠道AndroidManifest
        channelDom = xml.dom.minidom.parseString(del_xml_note(channel_AndroidManifest))
        channelRoot = channelDom.documentElement
        channel_application = channelRoot.getElementsByTagName('application')
        channel_permissions = channelRoot.getElementsByTagName('uses-permission')
        channel_supports_screens = channelRoot.getElementsByTagName('supports-screens')

        logger.info(u'开始修改游戏包名....')
        if package_name:
            new_package_name = package_name
        else:
            new_package_name = game_old_package_name

        gameRoot.setAttribute('package', new_package_name)
        logger.info(u'设置游戏包名: ' + new_package_name)

        logger.info(u'开始修改 uses-Sdk....')
        if not game_sdk:
            if minSdk or targetSdk:
                sdk_node = gameDom.createElement('uses-sdk')
                gameRoot.appendChild(sdk_node)
                game_sdk = gameRoot.getElementsByTagName('uses-sdk')
        if minSdk:
            game_sdk[0].setAttribute('android:minSdkVersion', minSdk)
            logger.info(u'设置游戏minSdk: %s' % minSdk)
        if targetSdk:
            game_sdk[0].setAttribute('android:targetSdkVersion', targetSdk)
            logger.info(u'设置游戏targetSdk: %s' % targetSdk)

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
        return 1, u'合并AndroidManifest异常:' + str(e), game_old_package_name


# 合并图标资源
def merge_icon_resource(temp_path, channel_path, layout=RIGHT_BOTTOM):

    channel_icon_path = os.path.join(channel_path, 'icon')
    if not os.path.isdir(channel_icon_path):
        return 0, u'渠道icon目录不存在，无法进行合并'

    channel_icon_name = '%s.png' % layout

    # 读取androidManifest图标配置信息
    game_android_manifest = os.path.join(temp_path, 'AndroidManifest.xml')
    game_dom = xml.dom.minidom.parse(game_android_manifest)
    game_root = game_dom.documentElement
    game_application = game_root.getElementsByTagName('application')
    game_icon_name = game_application[0].getAttribute('android:icon')
    if game_icon_name:
        game_icon_name = game_icon_name.replace('@drawable/', '') + '.png'

    game_res_path = os.path.join(temp_path, 'res')
    for parent, dir_names, file_names in os.walk(game_res_path):

        for filename in file_names:
            if filename == game_icon_name:
                icon_path = os.path.join(parent, game_icon_name)  # 获取游戏图标路径

                # 根据游戏图标路径匹配渠道对应目录是否存在对应的角标图片,如果没有就到下已层循环找
                if 'drawable' in parent:
                    icon_merge_path = find_merge_icon_path('drawable', channel_icon_path,channel_icon_name)

                elif 'drawable-hdpi' in parent:
                    icon_merge_path = find_merge_icon_path('drawable-hdpi', channel_icon_path,channel_icon_name)

                elif 'drawable-ldpi' in parent:
                    icon_merge_path = find_merge_icon_path('drawable-ldpi', channel_icon_path,channel_icon_name)

                elif 'drawable-mdpi' in parent:
                    icon_merge_path = find_merge_icon_path('drawable-mdpi', channel_icon_path,channel_icon_name)

                elif 'drawable-xhdpi' in parent:
                    icon_merge_path = find_merge_icon_path('drawable-xhdpi', channel_icon_path,channel_icon_name)

                elif 'drawable-xxhdpi' in parent:
                    icon_merge_path = find_merge_icon_path('drawable-xxhdpi', channel_icon_path,channel_icon_name)

                elif 'drawable-xxxhdpi' in parent:
                    icon_merge_path = find_merge_icon_path('drawable-xxxhdpi', channel_icon_path,channel_icon_name)

                else:
                    icon_merge_path = ''
                    
                if not icon_merge_path:
                    return 0, u"无下标,不合并"

                status, result = mark_icon(icon_path, icon_merge_path, icon_path)
                if not status == 0:
                    return status, result

    return 0, u'合并角标成功'


# 匹配渠道对应目录是否存在对应的角标图片
def find_merge_icon_path(icon_path, channel_icon_path, channel_icon_name):

    icon_merge_path = os.path.join(channel_icon_path, icon_path, channel_icon_name)

    # 渠道默认图标列表
    icon_dirs = ['drawable', 'drawable-hdpi', 'drawable-ldpi', 'drawable-mdpi',
                 'drawable-xhdpi', 'drawable-xxhdpi', 'drawable-xxxhdpi']

    if not os.path.isfile(icon_merge_path):
        icon_dirs.remove(icon_path)

    # 遍历剩下的list集合
    for icon_dir in icon_dirs:
        icon_merge_path = os.path.join(channel_icon_path, icon_dir, channel_icon_name)
        if os.path.isfile(icon_merge_path):
            return icon_merge_path
        else:
            continue

    # 如果渠道不存在角标资源，返回为空。
    return ''


# 删除xml中的注释
def del_xml_note(xmlfile):
    fp = open(xmlfile, 'r')
    data = fp.read()
    fp.close()
    a = re.subn(r'<!--.*?-->', '', data, flags=re.DOTALL)
    return a[0]
