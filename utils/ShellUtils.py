#!/usr/bin/env python
# -*- coding:utf-8 -*-

#
# 命令库: 用于执行打包命令
#

import subprocess
import os
import platform
from ConfigUtils import *


# 执行cmd命令
def execute_command(cmd):
    # status, result = subprocess.getstatusoutput(cmd)  #  python3.4
    print u'%s\n' % cmd
    res = subprocess.Popen(cmd, shell=isinstance(cmd, basestring), stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    sout, serr = res.communicate()

    print sout.decode('cp936').encode('utf-8')
    return res.returncode, sout.decode('cp936').encode('utf-8')


def copy_command(files_path, copy_path):

    system = platform.system()

    if system == 'Windows':
        status, result = copy_command_windows(files_path,copy_path)
    elif system == 'Darwin':
        status, result = copy_command_mac(files_path,copy_path)
    elif system == 'Linux':
        status, result = copy_command_mac(files_path, copy_path)
    else:
        status, result = copy_command_mac(files_path, copy_path)

    return status, result


# 执行复制命令(命令行执行windows)
def copy_command_windows(files_path, copy_path):

    if os.path.isfile(files_path):
        cmd = 'COPY %s /Y %s' % (files_path, copy_path)
    else:
        cmd = 'XCOPY %s /E /H /Y %s' % (files_path, copy_path)

    status, result = execute_command(cmd)
    return status, result


# 解决资源层级太深，Windows无法删除目录
def delete_command_windows(files_path):
    cmd = 'rmdir %s /S /Q' % files_path
    status, result = execute_command(cmd)
    return status, result


# 执行复制命令(命令行执行Mac)
def copy_command_mac(files_path, copy_path):

    if os.path.isfile(files_path):
        cmd = 'cp -rf %s %s' % (files_path,copy_path)
    else:
        cmd = 'cp -rf %s/. %s' % (files_path,copy_path)

    status, result = execute_command(cmd)
    return status, result


# 执行反编译命令
def decompile_command(apktool_path, apk_source_path, apk_file_output_path):

    cmd = 'java -jar %s/apktool.jar d -o %s %s -f' % (apktool_path, apk_source_path, apk_file_output_path)
    status, result = execute_command(cmd)
    return status, result


# 执行将.java编译为.class文件
# class_library_path 和 class_output_path 为绝对路径
def java_compile_class(java_file_path, class_library_path, class_output_path):

    cmd = 'cd %s && javac -classpath %s -d %s -sourcepath src *.java' % (java_file_path, class_library_path, class_output_path)
    status, result = execute_command(cmd)
    return status, result


# 执行.java 编译为.jar
def class_compile_jar(class_path, jar_file_name):

    cmd = 'cd %s && jar cvf %s *' % (class_path, jar_file_name)
    status, result = execute_command(cmd)
    return status, result


# 执行将资源文件编译生成R.java文件
def resource_compile_r_java(aapt_path, r_output_path, res_path, android_version_path, manifest_path):

    cmd = '%s p -f -m -J %s -S %s -I %s -M %s' % (aapt_path, r_output_path, res_path, android_version_path, manifest_path)
    status, result = execute_command(cmd)
    return status, result


# 执行将R.java文件编译为R.class文件
def r_java_compile_r_class(java_resource_path):

    cmd = 'javac -source 1.7 -target 1.7 -encoding UTF-8 %s' % java_resource_path
    status, result = execute_command(cmd)
    return status, result


# 执行将R.class 编译为R.jar文件
def r_class_compile_r_jar(class_path, r_file_name):

    cmd = 'cd %s && jar cvf %s *' % (class_path, r_file_name)
    status, result = execute_command(cmd)
    return status, result


# 执行将.jar文件编译为.dex
def jar_compile_dex(tools_path, jar_file_path, dex_file_path):

    cmd = "java -jar %s/dx.jar --dex --output=%s %s" % (tools_path, dex_file_path, jar_file_path)
    status, result = execute_command(cmd)
    return status, result


# 执行将dex编译为smali
def dex_compile_smali(tools_path, dex_file_path, smali_path):

    cmd = "java -jar %s/baksmali.jar -o %s %s" % (tools_path, smali_path, dex_file_path)
    status, result = execute_command(cmd)
    return status, result


# 执行将资源编译成apk
def resource_build_apk(tools_path, temp_path, apk_output_path):

    cmd = "java -jar %s/apktool.jar b %s -o %s" % (tools_path, temp_path, apk_output_path)
    status, result = execute_command(cmd)
    return status, result


# 给apk文件签名
def apk_sign(apk_file_path, sign_file_path,  keystore, alias, storepass, keypass):

    cmd = "jarsigner -verbose -keystore %s -storepass %s  -keypass %s -signedjar %s %s %s" % (
           keystore, storepass, keypass, sign_file_path, apk_file_path, alias)
    status, result = execute_command(cmd)
    return status, result


# 给apk文件优化
def apk_zipa(zipa_tool_path, sign_file_path, final_apk_path):

    cmd = "%s -v 4 %s %s" % (zipa_tool_path, sign_file_path, final_apk_path)
    status, result = execute_command(cmd)
    return status, result

