#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, zipfile, shutil, re
from ruamel import yaml
from utils.LogUtils import *
from utils.ShellUtils import *


# 合并Lib目录资源的库


# 将.jars文件里面的非.class资源提取出来
def modify_jars(task_id, temp_path, channel_path):

    logger = LogUtils.sharedInstance(task_id)

    temp_assets_path = os.path.join(temp_path, 'assets')
    channel_libs_path = os.path.join(channel_path, 'libs')

    status = 0
    result = ''

    # 获取jar列表
    libs_jar_list = get_file_list(channel_libs_path, '.jar')
    if libs_jar_list:
        for jar_file in libs_jar_list:
            status, result = handle_jar(temp_path, temp_assets_path, jar_file)
            if not status == 0:
                break

            else:
                logger.info(result)

    # 注意跳出循环后，判读状态
    if not status == 0:
        return status, result

    # 处理下apktool.yml文件
    apktool_yal_path = os.path.join(temp_path, 'apktool.yml')
    status, result = modify_apktool_yml_notCompress(apktool_yal_path)

    return status, result


# 处理单个.jar文件
def handle_jar(temp_path, temp_assets_path, jar_path):

    try:

        status = 0
        result = ''

        unzip_file = zipfile.ZipFile(jar_path, 'r')
        namelist = unzip_file.namelist()
        jar_root_dirs = get_jar_root_dirs(namelist)
        jar_root_dir_list = jar_root_dirs[0]
        jar_root_file_list = jar_root_dirs[1]

        # 只有包含文件或者assets目录时才解压文件
        if jar_root_file_list or 'assets' in jar_root_dir_list:

            # 将jar文件解压到对应的目录下
            unzip_jar_path = jar_path.replace('.jar', '')
            unzip_file.extractall(unzip_jar_path)
            unzip_file.close()

            # 提取文件后,处理非.class文件
            unzip_dir_list = os.listdir(unzip_jar_path)
            for temp in unzip_dir_list:
                # 如果是文件夹
                if os.path.isdir(os.path.join(unzip_jar_path, temp)):
                    if temp == 'assets':
                        status, result = copy_command(os.path.join(unzip_jar_path, temp), temp_assets_path)
                        if not status == 0:
                            break

                    else:
                        continue

                # 如果是文件,拷贝到unknown目录下
                else:
                    unknown_path = os.path.join(temp_path, 'unknown')
                    if not os.path.exists(unknown_path):
                        os.makedirs(unknown_path)
                    status, result = copy_command(os.path.join(unzip_jar_path, temp), unknown_path)
                    if not status == 0:
                        break

                    apktool_yal_path = os.path.join(temp_path, 'apktool.yml')
                    status, result = handle_apktool_yml(apktool_yal_path, temp)
                    if not status == 0:
                        break

            # 注意跳出循环后，判读状态
            if not status == 0:
                return status, result
            else:
                shutil.rmtree(unzip_jar_path)
                return 0, u"处理jar: %s 成功 " % jar_path

        else:
            return status, u"%s 无特殊资源, 不需要处理 " % jar_path

    except Exception as e:
        return 1, str(e)


# 获取jar包根目录结构及文件名集合
def get_jar_root_dirs(jar_file_list):

    jar_root_dir_list = []
    jar_root_file_names = []

    for file_path in jar_file_list:
        dir_names = file_path.split('/')
        if dir_names[0] not in jar_root_dir_list:
            jar_root_dir_list.append(dir_names[0])

            # 获取文件的拓展名
            file_type = os.path.splitext(dir_names[0])[1]
            if file_type and file_type not in jar_root_file_names:
                jar_root_file_names.append(dir_names[0])

    return jar_root_dir_list, jar_root_file_names


# 每复制一个文件到unknown目录下，都需要修改下
def handle_apktool_yml(yml_file_path, file_name):
    try:

        modify_apktool_yml(yml_file_path)

        fr = open(yml_file_path, 'r')
        yml_str = yaml.load(fr.read(), Loader=yaml.Loader)
        fr.close()

        # 不存在就添加
        if not yml_str.has_key('unknownFiles'):
            yml_str['unknownFiles'] = {}

        unknown_files = yml_str['unknownFiles']
        unknown_files[file_name] = '8'  # 0 不压缩  8 压缩

        fw = open(yml_file_path, 'w')
        yaml.dump(yml_str, fw, Dumper=yaml.RoundTripDumper)
        fw.close()

        return 0, 'handle apktool.yml success'

    except Exception as e:
        return 1, str(e)


# 处理下doNotCompress 字段
# 在不同的apktool对这个字段处理不一致
# apktool 2.0.2版本下，没有做这个处理
# 到apktool 2.3.2版本还有不压缩过滤规则：
# "\\.(jpg|jpeg|png|gif|wav|mp2|mp3|ogg|aac|mpg|mpeg|mid|midi|smf|jet|rtttl|imy|xmf|mp4|m4a|m4v|3gp|3gpp|3g2|3gpp2|amr|awb|wma|wmv|webm|mkv)$"
# 到apktool 2.3.3以上版本只针对apk文件不压缩。
# "classes.dex", "AndroidManifest.xml", "resources.arsc", "res", "r", "R", "lib", "libs", "assets", "META-INF", "kotlin"
#
# 而且游戏的大资源都放在assets目录比较多，
# 但是魔龙游戏TM的，回编译时，老是挂掉.manifest类型无法处理：brut.androlib.AndrolibException: brut.common.BrutException: could not exec
#
def modify_apktool_yml_notCompress(yml_file_path):

    try:

        modify_apktool_yml(yml_file_path)

        fr = open(yml_file_path, 'r')
        yml_str = yaml.load(fr.read(), Loader=yaml.Loader)
        fr.close()

        doNotCompress_str = []
        if yml_str.has_key('doNotCompress'):
            doNotCompress_str = yml_str['doNotCompress']

        pattern_rule = 'manifest|assets|unity3d'
        pattern = re.compile(r'' + pattern_rule)

        delete_list = []
        for notCompress in doNotCompress_str:
            if pattern.search(notCompress):
                delete_list.append(notCompress)

        for i in delete_list:
            doNotCompress_str.remove(i)

        yml_str['doNotCompress'] = doNotCompress_str
        fw = open(yml_file_path, 'w')
        yaml.dump(yml_str, fw, Dumper=yaml.RoundTripDumper)
        fw.close()

        return 0, 'handle apktool.yml success'

    except Exception as e:
        return 1, str(e)


# 处理下'!!brut.androlib.meta.MetaInfo'
# 新版本的apktool.jar反编译后，apktool.yml中会有这个字段,
def modify_apktool_yml(yml_file_path):
    fr = open(yml_file_path, 'r')
    buff = ''
    for line in fr.readlines():
        a = re.sub('!!brut.androlib.meta.MetaInfo', '', line)
        buff += a

    fw = open(yml_file_path, 'w')
    fw.write(buff)

    fr.close()
    fw.close()


# 适配so库问题,armeabi/armeabi-v7a/x86都必须保证so文件保持一致，不然会在部分机型crash
# todo 后续还需要根据游戏的目录对应的复制资源就可以了
def handle_so_dirs(temp_path, channel_path):

    # 第一步：读取channel包含的so的文件集合及路径集合 和 对应的目录集合
    channel_so_file_list = []
    channel_so_file_path_list = []  # 获取渠道so文件的路径,重复的以第一个为主
    for parent, dir_names, file_names in os.walk(os.path.join(channel_path, 'libs')):
        for file_name in file_names:
            if file_name.endswith('.so'):
                if file_name not in channel_so_file_list:
                    channel_so_file_list.append(file_name)
                    channel_so_file_path_list.append(os.path.join(parent, file_name))

    channel_so_dir_list = []  # 渠道so目录列表
    channel_libs_lists = os.listdir(os.path.join(channel_path, 'libs'))
    for channel_name in channel_libs_lists:
        if os.path.isdir(os.path.join(channel_path, 'libs', channel_name)):
            channel_so_dir_list.append(channel_name)

    # 第二步：读取游戏反编译后包含的so的文件集合及路径集合 和 对应的目录集合
    game_so_file_list = []
    game_so_file_path_list = []  # 获取游戏so文件的路径,重复的以第一个为主
    for parent, dir_names, file_names in os.walk(os.path.join(temp_path, 'lib')):
        for file_name in file_names:
            if file_name.endswith('.so'):
                if file_name not in game_so_file_list:
                    game_so_file_list.append(file_name)
                    game_so_file_path_list.append(os.path.join(parent, file_name))

    game_so_dir_list = []  # 游戏so目录列表
    game_libs_lists = os.listdir(os.path.join(temp_path, 'lib'))
    for game_name in game_libs_lists:
        if os.path.isdir(os.path.join(temp_path, 'lib', game_name)):
            game_so_dir_list.append(game_name)

    status = 0
    result = ''
    difference_so_dir_list = list(set(channel_so_dir_list).difference(set(game_so_dir_list)))  # 获取渠道特有的目录
    for difference_so_dir in difference_so_dir_list:
        game_so_dir_list.append(difference_so_dir)
        os.makedirs(os.path.join(temp_path, 'lib', difference_so_dir))  # 在temp中创建该目录

        # 把游戏的so资源拷贝到新建的目录
        if game_so_file_path_list:
            for game_so_file in game_so_file_path_list:
                status, result = copy_command(game_so_file, os.path.join(temp_path, 'lib', difference_so_dir))
                if not status == 0:
                    break

    # 注意跳出循环后，判读状态
    if not status == 0:
        return status, result

    # 遍历游戏so目录,将渠道so文件拷贝进去
    for game_so_dir in game_so_dir_list:
        for channel_so_file in channel_so_file_path_list:
            status, result = copy_command(channel_so_file, os.path.join(temp_path, 'lib', game_so_dir))
            if not status == 0:
                break

    # 注意跳出循环后，判读状态
    if not status == 0:
        return status, result

    return 0, u'处理lib目录下的so文件资源成功'


# 获取.xxx类型文件列表
def get_file_list(libs_path, match_file_text):

    file_path_list = []
    for parent, dir_names, file_names in os.walk(libs_path):
        for file_name in file_names:
            if file_name.endswith(match_file_text):
                file_path_list.append(os.path.join(parent, file_name))

    return file_path_list
