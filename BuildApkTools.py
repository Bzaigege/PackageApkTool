#!/usr/bin/env python
# -*- coding:utf-8 -*-

from merge.MergeResource import *
from utils.LogUtils import *


# 拷贝资源
def copy_resource(files_path, copy_path):
    status, result = copy_command(files_path, copy_path)
    return status, result


# 反编译包体
def decompile_apk(apktool_path, apk_source_path, apk_file_output_path):
    status, result = decompile_command(apktool_path, apk_source_path, apk_file_output_path)
    return status, result


# 合并包体和渠道资源
def merge_resources(task_id, tools_path, temp_path, channel_path, channel_id, channel_version, build_config):
    logger = LogUtils.sharedInstance(task_id)

    logger.info(u'合并资源...')

    # 合并assets目录文件
    if os.path.isdir(os.path.join(channel_path, 'assets')):
        status, result = merge_assets_resource(task_id, temp_path, channel_path,
                                               channel_id, channel_version, build_config)
        if status == 0:
            logger.info(u'合并assets目录资源成功')
        else:
            logger.info(u'合并assets目录资源失败: %s' % result)
            return status, result

    # 合并libs目录文件
    # 注意: 游戏apk反编译的目录为lib，里面会存放.so文件, 因此libs复制到lib
    if os.path.isdir(os.path.join(channel_path, 'libs')):
        if not os.path.exists(os.path.join(temp_path, 'lib')):
            os.makedirs(os.path.join(temp_path, 'lib'))

        status, result = merge_libs_resource(task_id, tools_path, temp_path, channel_path,
                                             channel_id, channel_version, build_config)
        if status == 0:
            logger.info(u'合并libs目录资源成功')
        else:
            logger.info(u'合并libs目录资源失败: %s' % result)
            return status, result

    # 合并res目录文件
    if os.path.isdir(os.path.join(channel_path, 'res')):
        status, result = merge_res_resource(task_id, tools_path, temp_path, channel_path,
                                            channel_id, channel_version, build_config)
        if status == 0:
            logger.info(u'合并res目录资源成功')
        else:
            logger.info(u'合并res目录资源失败: %s' % result)
            return status, result

    return 0, u'合并 assets/libs/res 资源成功'


# 合并配置文件
# todo 合并游戏的闪屏配置及SDK的特殊配置文件配置
def merge_config(temp_path, channel_path, build_config):

    splash_files = os.path.join(channel_path, 'splash')
    # 读取配置信息
    if build_config.has_key('game_splash'):
        game_splash_path = build_config['game_splash']
        status, result = copy_command(game_splash_path, splash_files)
        if not status == 0:
            return status, result

    status, result = copy_command(splash_files, os.path.join(temp_path, 'assets', 'splash'))
    if not status == 0:
        return status, result

    return 0, u"合并闪屏及配置文件成功"


# 合并游戏和渠道的AndroidManifest.xml文件
def merge_manifest(task_id, temp_path, channel_path, channel_id, channel_version, build_config):

    logger = LogUtils.sharedInstance(task_id)
    logger.info(u'合并AndroidManifest资源...')
    status, result, package_name = merger_manifest_resource(task_id, temp_path, channel_path, channel_id,
                                                            channel_version, build_config)
    return status, result, package_name


# 合并图片资源
def merge_icon(task_id, temp_path, channel_path, build_config):

    status, result = merge_icon_resource(task_id, temp_path, channel_path, build_config)
    return status, result


# 根据资源生成R文件(可能生成多个R文件)
def create_r_files(task_id, tools_path, temp_path, channel_path, channel_id, channel_version, build_config, package_name):

    logger = LogUtils.sharedInstance(task_id)
    logger.info(u'合并R文件资源...')

    status, result = merge_r_resource(task_id, tools_path, temp_path, channel_path, channel_id,
                                      channel_version, build_config, package_name)
    return status, result


# jar文件编译为smali代码
def jar_compile_smali(task_id, tools_path, temp_path):

    logger = LogUtils.sharedInstance(task_id)

    temp_lib_path = os.path.join(temp_path, 'lib')
    for parent, dirs, files in os.walk(temp_lib_path):
        for filename in files:
            if filename.endswith(".jar"):
                jar_file_path = os.path.join(parent, filename)
                dex_file_path = os.path.join(parent, filename.replace('.jar', '.dex'))

                logger.info(u'%s 编译为 %s' % (filename, filename.replace('.jar', '.dex')))
                status, result = jar_compile_dex(tools_path, jar_file_path, dex_file_path)
                if status == 0:
                    os.remove(jar_file_path)
                else:
                    return status, result

                logger.info(u'%s 编译为为smali代码' % (filename.replace('.jar', '.dex')))
                smali_path = os.path.join(temp_path, "smali")
                status, result = dex_compile_smali(tools_path, dex_file_path, smali_path)
                if status == 0:
                    os.remove(dex_file_path)
                else:
                    return status, result

    return 0, u'转化为smali成功'


# 编译打包成apk
def compile_build_apk(task_id, tools_path, temp_path, apk_output_apk):

    temp_apk_path = os.path.join(apk_output_apk, 'temp.apk')
    status, result = resource_build_apk(tools_path, temp_path, temp_apk_path)
    if status == 0 and os.path.isdir(temp_path):
        system = platform.system()
        if system == 'Windows':
            delete_command_windows(temp_path)
        else:
            shutil.rmtree(temp_path)

    return status, result


# 给apk文件签名
def sign_temp_apk(apk_output_apk, sign_file_path, keystore, alias, storepass, keypass):
    temp_apk_path = os.path.join(apk_output_apk, 'temp.apk')
    sign_apk_path = os.path.join(apk_output_apk, 'sign.apk')

    keystore = os.path.join(sign_file_path, keystore)
    status, result = apk_sign(temp_apk_path, sign_apk_path, keystore, alias, storepass, keypass)
    if status == 0:
        os.remove(temp_apk_path)

    return status, result


# 优化已签名apk文件
def zipa_sign_apk(tools_path, apk_output_apk, game_name, game_version, channel_id, channel_version):

    zipa_tool_path = os.path.join(tools_path, "zipalign")
    sign_apk_path = os.path.join(apk_output_apk, 'sign.apk')

    last_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    final_output_apk = "%s_%s_%s_%s_%s.apk" % (game_name, game_version, channel_id, channel_version, last_time)
    final_output_apk_path = os.path.join(apk_output_apk, final_output_apk)

    status, result = apk_zipa(zipa_tool_path, sign_apk_path, final_output_apk_path)
    if status == 0:
        os.remove(sign_apk_path)
        return status, result, final_output_apk, final_output_apk_path

    else:
        return status, result, '', ''


# 获取游戏包体原始包名
def get_game_package_name(game_path):

    try:
        game_android_manifest = os.path.join(game_path, 'AndroidManifest.xml')
        game_dom = xml.dom.minidom.parse(game_android_manifest)
        gamer_oot = game_dom.documentElement
        game_package_name = gamer_oot.getAttribute(CONF_package)
        return game_package_name
    except Exception as e:
        return ''


