#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from xml.dom.minidom import *
from xml.etree import ElementTree as ET
from utils.LogUtils import *
from utils.ShellUtils import *

# 合并Res目录资源的库

# 处理渠道和游戏目录不统一问题
dirs = ['drawable', 'drawable-hdpi', 'drawable-ldpi', 'drawable-mdpi', 'drawable-xhdpi', 'drawable-xxhdpi',
        'values', 'values-hdpi', 'values-ldpi', 'values-mdpi', 'values-xhdpi', 'values-xxhdpi']

v4_dirs = ['drawable-hdpi-v4', 'drawable-ldpi-v4', 'drawable-mdpi-v4', 'drawable-xhdpi-v4', 'drawable-xxhdpi-v4',
           'values-hdpi-v4', 'values-ldpi-v4', 'values-mdpi-v4', 'values-xhdpi-v4', 'values-xxhdpi-v4']

# 处理values目录下xml资源冲突问题,如：strings.xml等
values_dirs = ['values', 'values-hdpi', 'values-ldpi', 'values-mdpi', 'values-xhdpi', 'values-xxhdpi']

# 处理values目录下的特殊xml文件
values_xml_names = ['values.xml', 'values-hdpi.xml', 'values-ldpi.xml', 'values-mdpi.xml',
                    'values-xhdpi.xml', 'values-xxhdpi.xml']

# 处理特殊资源xml文件
values_dir_special_xml_names = ['colors.xml', 'dimens.xml', 'drawables.xml', 'strings.xml', 'styles.xml', 'arrays.xml',
                                'attrs.xml', 'booleans.xml', 'integers.xml']

# 这两个特殊文件不做处理
values_dir_default_xml_names = ['ids.xml', 'public.xml']


# 处理渠道和游戏目录不统一问题
# 通常渠道目录时没有v4后缀的
# 游戏反编译后的目录通常是没有v4后缀和有v4后缀的混合
def handle_res_dirs(task_id, temp_path, channel_path):

    logger = LogUtils.sharedInstance(task_id)

    temp_res_dirs = os.listdir(os.path.join(temp_path, 'res'))
    channel_res_dirs = os.listdir(os.path.join(channel_path, 'res'))
    difference_list = list(set(channel_res_dirs).difference(set(temp_res_dirs)))  # 获取渠道特有的目录

    # 保证后面复制渠道资源时时，游戏有对应的目录路径, 先创建对应目录
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

    status = 0
    result = ''

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

        else:

            # 不是文件夹，直接复制就可以了
            status, result = copy_command(os.path.join(channel_path, 'res'), os.path.join(temp_path, 'res'))

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

    return 0, 'handle res dirs success'


# 合并res的特殊目录
def merge_special_dirs(temp_path, channel_path, game_dir, channel_dir):

    # 处理游戏原有的图标被渠道同名资源覆盖问题
    status, result = handle_icon_covered(temp_path, channel_path, channel_dir)
    if not status == 0:
        return status, result

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


# 处理游戏原有的图标被渠道同名资源覆盖问题
def handle_icon_covered(temp_path, channel_path, channel_dir):

    try:

        # 读取androidManifest图标配置信息,避免游戏图标被渠道icon替换掉,将渠道的icon资源删掉
        game_android_manifest = os.path.join(temp_path, 'AndroidManifest.xml')
        game_dom = xml.dom.minidom.parse(game_android_manifest)
        game_root = game_dom.documentElement
        game_application = game_root.getElementsByTagName('application')
        game_icon_name = game_application[0].getAttribute('android:icon')
        if game_icon_name:
            game_icon_name = game_icon_name.replace('@drawable/', '') + '.png'

        channel_dir_files = os.listdir(os.path.join(channel_path, 'res', channel_dir))
        if game_icon_name in channel_dir_files:
            channel_icon_file_path = os.path.join(channel_path, 'res', channel_dir, game_icon_name)  # 获取文件路径
            os.remove(channel_icon_file_path)

        return 0, u'handle channel icon resource success'

    except Exception as e:
        return 1, u'handle channel icon resource exception' + str(e)


# 合并values目录资源
def merge_values_dirs(temp_path, channel_path, game_dir, channel_dir):

    channel_values_list = os.listdir(os.path.join(channel_path, 'res', channel_dir))
    game_values_list = os.listdir(os.path.join(temp_path, 'res', game_dir))

    # 先处理下渠道目录下values.xml/values-hdpi.xml等文件
    status = 0
    result = ''
    for values_xml in channel_values_list:
        if values_xml in values_xml_names:
            status, result = compile_change_values_xml(os.path.join(channel_path, 'res', channel_dir),
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
            status, result = merge_value_dir_xml_resource(game_value_xml, channel_value_xml)
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

    # 合并完整个目录资源后，合并重复定义的属性
    status, result = handle_values_xml_duplicate_attribute(temp_path, game_dir)
    if not status == 0:
        return status, result

    else:
        return 0, u"合并values/%s成功 " % value_xml


# 使用xml.etree.ElementTree 模块合并文件, 解决 minidom 在python2.7 没法解决中文字符问题
# 合并渠道和游戏类似String.xml/Style.xml同名资源
def merge_value_dir_xml_resource(game_xml, channel_xml):

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


# 需要先处理下渠道values.xml/values-hdpi.xml等文件
# 如果游戏之前接过渠道对应的资源，但是没有删除干净，生成的游戏母包apk，反编译后的资源strings.xml等格式
# 因此将渠道存在的values-xxx.xml的文件先转化为资源strings.xml等格式后再和游戏的资源合并
def compile_change_values_xml(xml_dir_path, xml_file_path):

    try:

        values_xml_dom = ET.parse(xml_file_path)

        # todo 关于属性类型后续遇到后补充扩展
        status, result = attributes_change_xml(values_xml_dom, xml_dir_path, 'array', 'arrays.xml')
        if not status == 0:
            return status, result

        status, result = attributes_change_xml(values_xml_dom, xml_dir_path, 'string-array', 'arrays.xml')
        if not status == 0:
            return status, result

        status, result = attributes_change_xml(values_xml_dom, xml_dir_path, 'integer-array', 'arrays.xml')
        if not status == 0:
            return status, result

        status, result = attributes_change_xml(values_xml_dom, xml_dir_path, 'string', 'strings.xml')
        if not status == 0:
            return status, result

        status, result = attributes_change_xml(values_xml_dom, xml_dir_path, 'color', 'colors.xml')
        if not status == 0:
            return status, result

        status, result = attributes_change_xml(values_xml_dom, xml_dir_path, 'drawable', 'drawables.xml')
        if not status == 0:
            return status, result

        status, result = attributes_change_xml(values_xml_dom, xml_dir_path, 'style', 'styles.xml')
        if not status == 0:
            return status, result

        status, result = attributes_change_xml(values_xml_dom, xml_dir_path, 'dimen', 'dimens.xml')
        if not status == 0:
            return status, result

        status, result = attributes_change_xml(values_xml_dom, xml_dir_path, 'declare-styleable', 'attrs.xml')
        if not status == 0:
            return status, result

        status, result = attributes_change_xml(values_xml_dom, xml_dir_path, 'bool', 'booleans.xml')
        if not status == 0:
            return status, result

        status, result = attributes_change_xml(values_xml_dom, xml_dir_path, 'integer ', 'integers.xml')
        if not status == 0:
            return status, result

        # 将values.xml/values-hdpi.xml转化完之后就删除当前的文件
        os.remove(xml_file_path)

        return 0, 'compile conversion %s 成功' % xml_file_path

    except Exception as e:
        return 1, str(e)


# 属性变对应的属性文件
def attributes_change_xml(values_xml_dom, attributes_xml_dir_path, attributes_name, attributes_xml_name):

    try:

        # 解析string节点，并合并到strings.xml
        attributes = find_nodes(values_xml_dom, attributes_name)
        attributes_xml_path = ''
        if attributes:
            attributes_xml_path = create_resources_xml(attributes_xml_dir_path, attributes_xml_name)
            attributes_xml_dom = ET.parse(attributes_xml_path)
            attributes_xml_root = attributes_xml_dom.getroot()

            # 返回xxx.xml已存在的节点
            attributes_has_nodes = []
            for node in attributes_xml_root:
                attributes_has_nodes.append(node.get('name'))

            for attributes_node in attributes:
                attributes_node_name = attributes_node.get('name')
                if attributes_node_name not in attributes_has_nodes:
                    attributes_xml_root.append(attributes_node)

            attributes_xml_dom.write(attributes_xml_path, encoding='UTF-8', xml_declaration=True)

        return 0, 'attributes change xml %s 成功' % attributes_xml_path

    except Exception as e:
        return 1, str(e)


# 处理重复定义的属性名称
def handle_values_xml_duplicate_attribute(temp_path, game_dir):

    try:

        game_values_list = os.listdir(os.path.join(temp_path, 'res', game_dir))

        # 获取属性集合
        # todo 关于属性类型后续遇到后补充扩展
        colors_attributes_list = []
        dimens_attributes_list = []
        drawables_attributes_list = []
        strings_attributes_list = []
        styles_attributes_list = []
        arrays_attributes_list = []
        attrs_attributes_list = []
        booleans_attributes_list = []
        integers_attributes_list = []

        for values_dir_xml in game_values_list:
            if values_dir_xml in values_dir_special_xml_names:

                values_dir_xml_path = os.path.join(temp_path, 'res', game_dir, values_dir_xml)
                if values_dir_xml == 'colors.xml':
                    colors_attributes_list = get_values_attributes(values_dir_xml_path)

                elif values_dir_xml == 'dimens.xml':
                    dimens_attributes_list = get_values_attributes(values_dir_xml_path)

                elif values_dir_xml == 'drawables.xml':
                    drawables_attributes_list = get_values_attributes(values_dir_xml_path)

                elif values_dir_xml == 'strings.xml':
                    strings_attributes_list = get_values_attributes(values_dir_xml_path)

                elif values_dir_xml == 'styles.xml':
                    styles_attributes_list = get_values_attributes(values_dir_xml_path)

                elif values_dir_xml == 'arrays.xml':
                    arrays_attributes_list = get_values_attributes(values_dir_xml_path)

                elif values_dir_xml == 'attrs.xml':
                    attrs_attributes_list = get_values_attributes(values_dir_xml_path)

                elif values_dir_xml == 'booleans.xml':
                    booleans_attributes_list = get_values_attributes(values_dir_xml_path)

                elif values_dir_xml == 'integers.xml':
                    integers_attributes_list = get_values_attributes(values_dir_xml_path)

        # 再遍历获取其他文件属性
        for values_dir_other_xml in game_values_list:

            if (values_dir_other_xml not in values_dir_special_xml_names) and (
                    values_dir_other_xml not in values_dir_default_xml_names):

                values_other_xml_path = os.path.join(temp_path, 'res', game_dir, values_dir_other_xml)

                # 在parse前一定要设置namespace, 不然就会出现 ns0:name错误，而不是预期的 android:name
                ET.register_namespace('android', "http://schemas.android.com/apk/res/android")
                # 安智渠道
                ET.register_namespace('xliff', "urn:oasis:names:tc:xliff:document:1.2")

                values_other_xml_dom = ET.parse(values_other_xml_path)
                values_other_xml_root = values_other_xml_dom.getroot()
                for child in values_other_xml_root:
                    child_type = child.tag
                    child_name = child.get('name')

                    # 去掉重复的属性
                    if child_type == 'color':
                        if child_name in colors_attributes_list:
                            values_other_xml_root.remove(child)

                    elif child_type == 'dimen':
                        if child_name in dimens_attributes_list:
                            values_other_xml_root.remove(child)

                    elif child_type == 'drawable':
                        if child_name in drawables_attributes_list:
                            values_other_xml_root.remove(child)

                    elif child_type == 'string':
                        if child_name in strings_attributes_list:
                            values_other_xml_root.remove(child)

                    elif child_type == 'style':
                        if child_name in styles_attributes_list:
                            values_other_xml_root.remove(child)

                    elif (child_type == 'array') or (child_type == 'string-array') or (child_type == 'integer-array'):
                        if child_name in arrays_attributes_list:
                            values_other_xml_root.remove(child)

                    elif (child_type == 'declare-styleable'):
                        if child_name in attrs_attributes_list:
                            values_other_xml_root.remove(child)

                    elif (child_type == 'bool'):
                        if child_name in booleans_attributes_list:
                            values_other_xml_root.remove(child)

                    elif (child_type == 'integer'):
                        if child_name in integers_attributes_list:
                            values_other_xml_root.remove(child)

                values_other_xml_dom.write(values_other_xml_path, encoding='UTF-8', xml_declaration=True)

        return 0, 'handle duplicate attribute 成功'

    except Exception as e:
        return 1, str(e)


# 获取属性集合
def get_values_attributes(values_dir_special_xml):

    values_special_xml_dom = ET.parse(values_dir_special_xml)
    values_special_xml_root = values_special_xml_dom.getroot()
    attribute_list = []
    for child in values_special_xml_root:
        attribute_list.append(child.get('name'))
    return attribute_list


# 返回某个路径匹配的所有节点
# tree: xml树
# path: 节点路径
def find_nodes(tree, path):
    return tree.findall(path)


# 返回文件的路径
def create_resources_xml(xml_dir, xml_file_name):
    resources_root = ET.Element('resources')
    resources_tree = ET.ElementTree(resources_root)
    xml_file_out_path = os.path.join(xml_dir, xml_file_name)

    # 文件不存在才创建，存在就直接返回
    if not os.path.isfile(xml_file_out_path):
        resources_tree.write(xml_file_out_path, encoding="utf-8", xml_declaration=True)

    return xml_file_out_path