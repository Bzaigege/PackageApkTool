#!/usr/bin/env python
# -*- coding:utf-8 -*-


from merge.MergeLibUtils import *
from merge.MergeResUtils import *
from merge.MergeManifesUtils import *
from merge.MergeIconUtils import *
from merge.MergeRFileUtils import *
from channel.ModifyChannel import *


# 合并assets目录资源
def merge_assets_resource(task_id, temp_path, channel_path, channel_id, channel_version, build_config):
    logger = LogUtils.sharedInstance(task_id)
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

    logger = LogUtils.sharedInstance(task_id)
    logger.info(u'合并libs资源...')

    # 在这里需要先处理下jar包问题,jar里其他不是.class的文件需要转化下,要么放到assets目录下，要么放到unknown目录下
    status, result = modify_jars(task_id, temp_path, channel_path)
    if not status == 0:
        return status, result

    # 这里需要适配so库问题,armeabi/armeabi-v7a/x86都必须保证so文件保持一致，不然会在部分机型crash
    status, result = handle_so_dirs(temp_path, channel_path)
    if not status == 0:
        return status, result

    # 还需要将jar包拷贝进去
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

    logger = LogUtils.sharedInstance(task_id)
    logger.info(u'合并res资源...')

    # 合并之前修改渠道的res资源配置文件
    status, result = modify_channel_res_resource(channel_path, channel_id, channel_version, build_config)
    if not status == 0:
        return status, result

    status, result = handle_res_dirs(task_id, temp_path, channel_path)
    if not status == 0:
        return status, result

    return 0, u'合并 res 资源成功'


# 合并androidManifest.xml文件资源
def merger_manifest_resource(task_id, temp_path, channel_path, channel_id, channel_version, build_config):

    logger = LogUtils.sharedInstance(task_id)

    # 合并之前修改渠道的配置文件
    status, result = modify_channel_manifest(channel_path, channel_id, channel_version, build_config)
    if not status == 0:

        package_name = ''
        if build_config.has_key(CONF_package):
            package_name = build_config[CONF_package]

        return status, result, package_name

    status, result, package_name = merger_manifest_config(task_id, temp_path, channel_path, build_config)
    if not status == 0:
        return status, result, package_name

    # 合并完后，修改游戏闪屏逻辑
    logger.info(u'开始修改闪屏逻辑....')
    status, result = modify_channel_splash_and_main(temp_path, channel_id, channel_version, build_config)
    if not status == 0:
        return status, result, package_name
    else:
        logger.info(u'修改闪屏逻辑成功....')

    return 0, u'合并Manifest.xml文件成功', package_name


# 合并图标资源
def merge_icon_resource(task_id, temp_path, channel_path, build_config):

    status, result = merge_icon_subscript(task_id, temp_path, channel_path, build_config)
    return status, result


# 合并R文件资源
def merge_r_resource(task_id, tools_path, temp_path, channel_path, channel_id, channel_version, build_config, package_name):

    status, result = create_r_files(task_id, tools_path, temp_path, channel_path, channel_id,
                                    channel_version, build_config, package_name)
    return status, result

