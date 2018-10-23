#!/usr/bin/env python
# -*- coding:utf-8 -*-

#
# 命令库: 用于执行打包命令
#

import subprocess
import os
import platform


# 执行cmd命令
def execute_command(cmd):
    # status, result = subprocess.getstatusoutput(cmd)  #  python3.4
    res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    sout, serr = res.communicate()
    return res.returncode, sout


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

    cmd = 'cd %s && java -jar -Xms512m apktool.jar d -o %s %s -f' % (apktool_path, apk_source_path, apk_file_output_path)
    status, result = execute_command(cmd)
    return status, result


# 执行将.java编译为.class文件
def java_compile_class(java_file_path, calss_library_path, class_output_path):

    cmd = 'cd %s && javac -classpath %s -d %s -sourcepath src *.java' % (java_file_path, calss_library_path, class_output_path)
    status, result = execute_command(cmd)
    return status, result


# 执行.java 编译为.jar
def class_compile_jar(class_path, jar_output_path):

    cmd = 'cd %s && jar cvf %s *' % (class_path, jar_output_path)
    status, result = execute_command(cmd)
    return status, result


# 执行将资源文件编译生成R.java文件
def resource_compile_r(tools_path, aapt_path, r_output_path, res_path, android_version_path, manifest_path):

    cmd = 'cd %s && %s p -f -m -J %s -S %s -I %s -M %s' % (tools_path, aapt_path, r_output_path, res_path,
                                                           android_version_path, manifest_path)
    status, result = execute_command(cmd)
    return status, result


# 执行将R.java文件编译为R.class文件
def r_compile_class(tools_path, java_resource_path):

    cmd = 'cd %s && javac -source 1.7 -target 1.7 -encoding UTF-8 %s' % (tools_path, java_resource_path)
    status, result = execute_command(cmd)
    return status, result


# 执行将.jar文件编译为.dex
def jar_compile_dex(tools_path, jar_file_path, dex_file_path):

    cmd = "cd %s && java -jar dx.jar --dex --output=%s %s" % (tools_path, dex_file_path, jar_file_path)
    status, result = execute_command(cmd)
    return status, result


# 执行将dex编译为smali
def dex_compile_smali(tools_path, dex_file_path, smali_path):

    cmd = "cd %s && java -jar baksmali.jar -o %s %s" % (tools_path, smali_path, dex_file_path)
    status, result = execute_command(cmd)
    return status, result


# 执行将资源编译成apk
def resource_build_apk(tools_path, temp_path, apk_output_path):

    cmd = "cd %s && java -jar apktool.jar b -o %s %s" % (tools_path, apk_output_path, temp_path)
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