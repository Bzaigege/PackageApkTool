#!/usr/bin/env python
# -*- coding:utf-8 -*-

#
# 合并资源库: 合并游戏和渠道资源
#

import os
import zipfile
import shutil
import re
from xml.dom.minidom import *
from ruamel import yaml
from utils.ShellUtils import *
from channel.ModifyResourceUtils import *


# 获取.xxx类型文件列表
def get_file_list(libs_path, match_file_text):

    file_path_list = []
    for parent, dir_names, file_names in os.walk(libs_path):
        for file_name in file_names:
            if file_name.endswith(match_file_text):
                file_path_list.append(os.path.join(parent, file_name))

    return file_path_list


# 将.jars文件里面的非.class资源提取出来
def modify_jars(temp_path, channel_path):

    temp_assets_path = os.path.join(temp_path, 'assets')
    channel_libs_path = os.path.join(channel_path, 'libs')

    # 获取jar列表
    libs_jar_list = get_file_list(channel_libs_path, '.jar')
    if libs_jar_list:
        for jar_file in libs_jar_list:
            status, result = handle_jar(temp_path, temp_assets_path, jar_file)
            if not status == 0:
                break

    # 注意跳出循环后，判读状态
    if not status == 0:
        return status, result
    else:
        return 0, u"处理jar成功"


# 处理单个.jar文件
def handle_jar(temp_path, temp_assets_path, jar_path):

    try:

        status = 0
        result = ''

        # 将jar文件解压到对应的目录下
        unzip_jar_path = jar_path.replace('.jar', '')
        unzip_file = zipfile.ZipFile(jar_path, 'r')
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

    except Exception as e:
        return 1, str(e)


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


# 合并res的特殊目录
def merge_special_dirs(temp_path, channel_path, game_dir, channel_dir):

    # 处理values目录下xml资源冲突问题,如：strings.xml等
    values_dirs = ['values', 'values-hdpi', 'values-ldpi', 'values-mdpi', 'values-xhdpi',
                   'values-xxhdpi']

    # 处理values目录下xml资源冲突问题,如：strings.xml等
    if channel_dir in values_dirs:
        status, result = merge_values_dirs(temp_path, channel_path, game_dir, channel_dir)
        if not status == 0:
            return status, result

    # 不是values目录直接复制
    else:
        status, result = copy_command(os.path.join(channel_path, 'res', channel_dir),
                                      os.path.join(temp_path, 'res', game_dir))
        if not status == 0:
            return status, result

    return 0, u"合并res/values/%s成功 " % channel_dir


# 合并values目录
def merge_values_dirs(temp_path, channel_path, game_dir, channel_dir):

    channel_values_list = os.listdir(os.path.join(channel_path, 'res', channel_dir))
    game_values_list = os.listdir(os.path.join(temp_path, 'res', game_dir))

    values_xml_names = ['values.xml', 'values-hdpi.xml', 'values-ldpi.xml', 'values-mdpi.xml',
                        'values-xhdpi.xml', 'values-xxhdpi.xml']

    # 处理下values.xml/values-hdpi.xml等文件
    status = 0
    result = ''
    for values_xml in channel_values_list:
        if values_xml in values_xml_names:
            status, result = compile_values_xml(os.path.join(channel_path, 'res', channel_dir),
                                                os.path.join(channel_path, 'res', channel_dir, values_xml))
            if not status == 0:
                break  # 跳出循环

    # 注意跳出循环后，判读状态
    if not status == 0:
        return status, result

    # 重新赋值文件列表
    channel_values_list = os.listdir(os.path.join(channel_path, 'res', channel_dir))

    # 判断资源文件是否在游戏的文件列表里，在就合并，不在就复制进去
    value_xml = ''
    for value_xml in channel_values_list:
        if value_xml in game_values_list:
            game_value_xml = os.path.join(temp_path, 'res', game_dir, value_xml)
            channel_value_xml = os.path.join(channel_path, 'res', channel_dir, value_xml)
            status, result = merge_res_xml(game_value_xml, channel_value_xml)
            if not status == 0:
                break  # 跳出循环

        else:
            status, result = copy_command(os.path.join(channel_path, 'res', channel_dir, value_xml),
                                          os.path.join(temp_path, 'res', game_dir))
            if not status == 0:
                break  # 跳出循环

    # 注意跳出循环后，判读状态
    if not status == 0:
        return status, result
    else:
        return 0, u"合并values/%s成功 " % value_xml


# 需要处理下values.xml/values-hdpi.xml等文件
# 如果游戏之前接过渠道对应的资源，但是没有删除干净，生成的游戏母包apk，反编译后的资源strings.xml等格式
# 因此将渠道存在的values的文件先转化为资源strings.xml等格式后再和游戏的资源合并
def compile_values_xml(xml_dir_path, xml_file_path):

    try:

        values_xml_dom = ET.parse(xml_file_path)

        # 解析xxx-array节点，并合并到arrays.xml
        arrays = find_nodes(values_xml_dom, 'array')
        for temp_node in find_nodes(values_xml_dom, 'string-array'):
            arrays.append(temp_node)

        for temp_node in find_nodes(values_xml_dom, 'integer-array'):
            arrays.append(temp_node)

        if arrays:
            arrays_xml_path = create_resources_xml(xml_dir_path, 'arrays.xml')
            arrays_xml_dom = ET.parse(arrays_xml_path)
            arrays_xml_root = arrays_xml_dom.getroot()

            # 返回arrays.xml已存在的节点
            arrays_has_nodes = []
            for node in arrays_xml_root:
                arrays_has_nodes.append(node.get('name'))

            for arrays_node in arrays:
                arrays_node_name = arrays_node.get('name')
                if arrays_node_name not in arrays_has_nodes:
                    arrays_xml_root.append(arrays_node)

            arrays_xml_dom.write(arrays_xml_path, encoding='UTF-8', xml_declaration=True)

        # 解析string节点，并合并到strings.xml
        strings = find_nodes(values_xml_dom, 'string')
        if strings:
            string_xml_path = create_resources_xml(xml_dir_path, 'strings.xml')
            strings_xml_dom = ET.parse(string_xml_path)
            strings_xml_root = strings_xml_dom.getroot()

            # 返回strings.xml已存在的节点
            strings_has_nodes = []
            for node in strings_xml_root:
                strings_has_nodes.append(node.get('name'))

            for strings_node in strings:
                strings_node_name = strings_node.get('name')
                if strings_node_name not in strings_has_nodes:
                    strings_xml_root.append(strings_node)

            strings_xml_dom.write(string_xml_path, encoding='UTF-8', xml_declaration=True)

        # 解析color节点，并合并到colors.xml
        colors = find_nodes(values_xml_dom, 'color')
        if colors:
            colors_xml_path = create_resources_xml(xml_dir_path, 'colors.xml')
            colors_xml_dom = ET.parse(colors_xml_path)
            colors_xml_root = colors_xml_dom.getroot()

            # 返回colors.xml已存在的节点
            colors_has_nodes = []
            for node in colors_xml_root:
                colors_has_nodes.append(node.get('name'))

            for colors_node in colors:
                colors_node_name = colors_node.get('name')
                if colors_node_name not in colors_has_nodes:
                    colors_xml_root.append(colors_node)

            colors_xml_dom.write(colors_xml_path, encoding='UTF-8', xml_declaration=True)

        # 解析style节点，并合并到styles.xml
        styles = find_nodes(values_xml_dom, 'style')
        if styles:
            styles_xml_path = create_resources_xml(xml_dir_path, 'styles.xml')
            styles_xml_dom = ET.parse(styles_xml_path)
            styles_xml_root = styles_xml_dom.getroot()

            # 返回styles.xml已存在的节点
            styles_has_nodes = []
            for node in styles_xml_root:
                styles_has_nodes.append(node.get('name'))

            for styles_node in styles:
                styles_node_name = styles_node.get('name')
                if styles_node_name not in styles_has_nodes:
                    styles_xml_root.append(styles_node)

            styles_xml_dom.write(styles_xml_path, encoding='UTF-8', xml_declaration=True)

        # 解析dimen节点，并合并到dimens.xml
        dimens = find_nodes(values_xml_dom, 'dimen')
        if dimens:
            dimens_xml_path = create_resources_xml(xml_dir_path, 'dimens.xml')
            dimens_xml_dom = ET.parse(dimens_xml_path)
            dimens_xml_root = dimens_xml_dom.getroot()

            # 返回dimens.xml已存在的节点
            dimens_has_nodes = []
            for node in dimens_xml_root:
                dimens_has_nodes.append(node.get('name'))

            for dimens_node in dimens:
                dimens_node_name = dimens_node.get('name')
                if dimens_node_name not in dimens_has_nodes:
                    dimens_xml_root.append(dimens_node)

            dimens_xml_dom.write(dimens_xml_path, encoding='UTF-8', xml_declaration=True)

        # 将values.xml/values-hdpi.xml转化完之后就删除当前的文件
        os.remove(xml_file_path)

        return 0, 'compile %s 成功' % xml_file_path

    except Exception as e:
        return 1, str(e)


# 返回文件的路径
def create_resources_xml(xml_dir, xml_file_name):
    resources_root = ET.Element('resources')
    resources_tree = ET.ElementTree(resources_root)
    xml_file_out_path = os.path.join(xml_dir, xml_file_name)

    # 文件不存在才创建，存在就直接返回
    if not os.path.isfile(xml_file_out_path):
        resources_tree.write(xml_file_out_path, encoding="utf-8", xml_declaration=True)

    return xml_file_out_path


# 使用xml.etree.ElementTree 模块合并文件, 解决 minidom 在python2.7 没法解决中文字符问题
def merge_res_xml(game_xml, channel_xml):

    try:

        xml_dir = os.path.basename(game_xml)

        game_xml_dom = ET.parse(game_xml)
        game_xml_root = game_xml_dom.getroot()  #根节点为resources

        channel_xml_dom = ET.parse(channel_xml)
        channel_xml_root = channel_xml_dom.getroot()

        game_has_resources = []
        for game_node in game_xml_root:
            game_has_resources.append(game_node.get('name'))

        game_add_resources = []
        for channel_node in channel_xml_root:
            channel_node_name = channel_node.get('name')
            if channel_node_name not in game_has_resources:
                game_xml_root.append(channel_node)
                game_add_resources.append(channel_node_name)

        game_xml_dom.write(game_xml, encoding='UTF-8')

        return 0, u'合并%s文件成功' % xml_dir

    except Exception as e:

        return 1, u'合并%s异常:' % xml_dir + str(e)

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