#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, shutil, json
from utils.LogUtils import *
from utils.ShellUtils import *
from channel.ModifyResourceUtils import *


# 生成R资源文件
def create_r_files(task_id, tools_path, temp_path, channel_path, channel_id, channel_version, build_config, package_name):

    r_path = os.path.join(temp_path, 'r')
    if not os.path.exists(r_path):
        os.makedirs(r_path)

    status, result = create_normal_package_r_file(task_id, tools_path, temp_path, r_path, package_name)
    if not status == 0:
        return status, result

    r_packages = []
    if build_config.has_key('R_package'): # R_package为字符数组["a","b"]
        r_packages = build_config['R_package']

    if r_packages:
        for real_package in r_packages:
            status, result = create_special_package_r_file(task_id, tools_path, temp_path, r_path, package_name, real_package)
            if not status == 0:
                break

    shutil.rmtree(r_path)
    return status, result


# 创建正常的包名R文件
def create_normal_package_r_file(task_id, tools_path, temp_path, r_path, package_name):

    res_resource_path = os.path.join(temp_path, 'res')
    manifest_resource_path = os.path.join(temp_path, 'AndroidManifest.xml')

    status, result = create_new_r_file(task_id, tools_path, temp_path, res_resource_path, manifest_resource_path,
                                       r_path, package_name)
    return status, result


# 创建指定包名的R文件
def create_special_package_r_file(task_id, tools_path, temp_path, r_path, package_name, real_compile_pack_name):

    res_resource_path = os.path.join(temp_path, 'res')
    manifest_resource_path = os.path.join(temp_path, 'AndroidManifest.xml')

    # 编译前修改AndroidManifest包名为对应的编译包名
    status, result = modify_real_package_name(temp_path, real_compile_pack_name)
    if not status == 0:
        return status, result

    status, result = create_new_r_file(task_id, tools_path, temp_path, res_resource_path, manifest_resource_path,
                                       r_path, real_compile_pack_name)
    if not status == 0:
        return status, result

    # 编译后修改AndroidManifest包名为对应的正确的包名
    status, result = modify_real_package_name(temp_path, package_name)
    if not status == 0:
        return status, result

    return status, result


# 修改文件的包名
def modify_real_package_name(temp_path, real_compile_package_name):
    try:

        tree = read_manifest(temp_path)
        root = tree.getroot()
        root.set('package', real_compile_package_name)
        write_manifest(tree, temp_path)

        return 0, u'modify manifest compile package name success'

    except Exception as e:
        return 1, u'modify manifest compile package name fail' + str(e)


# 创建R文件核心逻辑
def create_new_r_file(task_id, tools_path, temp_path, res_resource_path, manifest_resource_path, r_path, real_package_name):

    logger = LogUtils.sharedInstance(task_id)

    aapt_path = os.path.join(tools_path, 'aapt')  # 注意aapt版本
    android_jar_path = os.path.join(tools_path, 'android.jar')

    logger.info(u'资源编译为 %s R.java' % real_package_name)
    status, result = resource_compile_r_java(aapt_path, r_path, res_resource_path,
                                             android_jar_path, manifest_resource_path)
    if not status == 0:
        return status, result

    logger.info(u'%s R.java 编译为 %s R.class' % (real_package_name , real_package_name))
    package_path = os.path.join(temp_path, 'r', real_package_name.replace('.', '/'))
    r_java_path = os.path.join(package_path, 'R.java')
    status, result = r_java_compile_r_class(r_java_path)
    if status == 0:
        os.remove(r_java_path)
    else:
        return status, result

    r_file_name = '%s_R.jar' % real_package_name
    logger.info(u'%s R.class编译为 %s_R.jar文件' % (real_package_name , real_package_name))
    temp_lib_path = os.path.join(temp_path, 'lib')
    if not os.path.isdir(temp_lib_path):
        os.makedirs(temp_lib_path)

    status, result = r_class_compile_r_jar(r_path, r_file_name)
    if not status == 0:
        return status, result
    else:
        shutil.move(os.path.join(r_path, r_file_name), temp_lib_path)
        return 0, u'生成%s成功' % r_file_name
