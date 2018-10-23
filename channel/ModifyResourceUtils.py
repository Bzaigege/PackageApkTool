#!/usr/bin/env python
# -*-coding:utf-8 -*-

#
# 修改渠道资源库: 用于处理修改渠道资源的库代码
#

import os,re,platform
from xml.etree import ElementTree as ET


# 找某个名称的文件，可能存在多个文件夹里面，如strings.xml就可能存在在values/values-xxx里，需要批量修改
def find_resource_paths(parent_path, file_name):

    file_res_paths = []
    # parent : 当前文件夹的根目录路径
    # dir_names： 当前文件夹下的目录集合
    # file_names：当前文件夹下的文件集合
    for parent, dir_names, file_names in os.walk(parent_path):
        if file_name in file_names:
            file_path = os.path.join(parent, file_name)  # 获取文件路径
            file_res_paths.append(file_path)

    return file_res_paths


# 找指定目录下的指定文件
def find_specific_resource_path(parent_path, dir_name, file_name):

    file_path = ''
    channel_res_dirs = os.listdir(parent_path)
    for channel_dir in channel_res_dirs:  # 遍历渠道res目录,找指定目录下的指定文件
        if channel_dir == dir_name:
            dir_list = os.listdir(os.path.join(parent_path, channel_dir))
            for value_xml in dir_list:
                if value_xml == file_name:
                    file_path = os.path.join(parent_path, channel_dir, value_xml)
                else:
                    continue
        else:
            continue

    return file_path


# 修改包名
def modify_manifest_package_name(channel_path, compile):

    modify_manifest_path = os.path.join(channel_path, 'AndroidManifest.xml')

    game_package_name = ''
    if compile.has_key('package'):  # 游戏包名
        game_package_name = compile['package']

    if game_package_name:
        # 注意特殊字符问题，需先转义
        modify_xml_text(modify_manifest_path, '\$\{applicationId\}', game_package_name)


# 返回xml的节点树
def read_manifest(channel_path):

    modify_manifest_path = os.path.join(channel_path, 'AndroidManifest.xml')

    # 在parse前一定要设置namespace, 不然就会出现 ns0:name错误，而不是预期的 android:name
    ET.register_namespace('android', "http://schemas.android.com/apk/res/android")
    modify_xml_tree = ET.parse(modify_manifest_path)
    return modify_xml_tree


# 将修改的manifest输出
def write_manifest(tree, channel_path):

    out_manifest_path = os.path.join(channel_path, 'AndroidManifest.xml')
    tree.write(out_manifest_path, encoding="utf-8", xml_declaration=True)


# 返回 manifest.xml 的 activity 的节点列表
def find_activity_nodes(tree):
    return find_nodes(tree, 'application/activity')


# 返回 manifest.xml 的 service 的节点列表
def find_service_nodes(tree):
    return find_nodes(tree, 'application/service')


# 返回 manifest.xml 的 receiver 的节点列表
def find_receiver_nodes(tree):
    return find_nodes(tree, 'application/receiver')


# 返回 manifest.xml 的 provider 的节点列表
def find_provider_nodes(tree):
    return find_nodes(tree, 'application/provider')


# 返回 manifest.xml 的 meta-data 的节点列表
def find_metadata_nodes(tree):
    return find_nodes(tree, 'application/meta-data')


# 获取 manifest.xml 的 activity 名称列表
def get_activity_list(tree):

    activity_node_list = find_activity_nodes(tree)
    activity_list = []
    for node in activity_node_list:
        activity_list.append(node.get('{http://schemas.android.com/apk/res/android}name'))

    return activity_list


# 获取 manifest.xml 的 service 名称列表
def get_manifest_service_list(tree):

    service_node_list = find_service_nodes(tree)
    service_list = []
    for node in service_node_list:
        service_list.append(node.get('{http://schemas.android.com/apk/res/android}name'))

    return service_list


# 获取 manifest.xml 的 receiver 名称列表
def get_manifest_receiver_list(tree):

    receiver_node_list = find_receiver_nodes(tree)
    receiver_list = []
    for node in receiver_node_list:
        receiver_list.append(node.get('{http://schemas.android.com/apk/res/android}name'))

    return receiver_list


# 获取 manifest.xml 的 provider 名称列表
def get_manifest_provider_list(tree):

    provider_node_list = find_provider_nodes(tree)
    provider_list = []
    for node in provider_node_list:
        provider_list.append(node.get('{http://schemas.android.com/apk/res/android}name'))

    return provider_list


# 获取 manifest.xml 的 meta-data 名称列表
def get_manifest_metadata_list(tree):

    metadata_node_list = find_metadata_nodes(tree)
    metadata_list = []
    for node in metadata_node_list:
        metadata_list.append(node.get('{http://schemas.android.com/apk/res/android}name'))

    return metadata_list


# 返回某个路径匹配的所有节点
# tree: xml树
# path: 节点路径
def find_nodes(tree, path):
    return tree.findall(path)


# 根据属性 name 返回该节点
def find_node_by_name(nodes_list, name):

    key_value = {'{http://schemas.android.com/apk/res/android}name':name}
    for node in nodes_list:
        if node_match(node, key_value):
            return node


# 根据属性及属性值定位符合的节点，返回节点集合
# nodelist: 节点列表
# kv_map: 匹配属性及属性值map
def find_nodes_by_key_value(nodelist, kv_map):

    result_nodes = []
    for node in nodelist:
        if node_match(node, kv_map):
            result_nodes.append(node)
    return result_nodes


# 判断某个节点是否包含所有传入参数属性
# node: 节点
# kv_map: 属性及属性值组成的map
def node_match(node, kv_map):
    for key in kv_map:
        if node.get(key) != kv_map.get(key):
            return False
    return True


# 批量修改xml中的某个字段
def modify_xml_text(xml_path, old_text, new_text):

    # 注意open 在2.7没法处理中文字符问题, 使用个笨方法，先将中文的注释去掉
    delete_xml_note(xml_path)

    fr = open(xml_path, 'r')
    buff = ''
    for line in fr.readlines():
        a = re.sub(old_text, new_text, line)
        buff += a

    fw = open(xml_path, 'w')
    fw.write(buff)

    fr.close()
    fw.close()


# 删除.java中的注释
def delete_java_note(xml_path):
    fr = open(xml_path, 'r')
    data = fr.read()
    fr.close()
    a = re.subn(r'/\*.*?\*/', '', data, flags=re.DOTALL)
    fw = open(xml_path, 'w')
    fw.write(a[0])
    fw.close()


# 删除.xml中的注释
def delete_xml_note(xml_path):

    fr = open(xml_path, 'r')
    data = fr.read()
    fr.close()
    a = re.subn(r'<!--.*?-->', '', data, flags=re.DOTALL)
    fw = open(xml_path, 'w')
    fw.write(a[0])
    fw.close()


# 指定行写入指定内容, 第一行为0
def write_file_insert_specific_row(file_path, row, text):

    lines = []
    fr = open(file_path, 'r')
    for line in fr:
        lines.append(line)
    fr.close()
    lines.insert(row, '%s\n' % text)
    s = ''.join(lines)
    f = open(file_path, 'w+')
    f.write(s)
    f.close()
    del lines[:]


# 删除指定内容所在行
def delete_file_specific_row(file_path, text):

    fr = open(file_path, "r")
    lines = fr.readlines()
    fr.close()

    fw = open(file_path, "w")
    for line in lines:
        if text in line:
            continue
        fw.write(line)
    fw.close()


# 获取文件列表
def get_file_list(libs_path, suffix_test):

    jar_path_list = []
    for parent, dir_names, file_names in os.walk(libs_path):
        for file_name in file_names:
            if file_name.endswith(suffix_test):
                jar_path_list.append(os.path.join(parent, file_name))
    return jar_path_list


# 获取相关联的jar包路径
def get_compile_class_path(temp_path, tools_path):

    class_path = ''
    jar_list = get_file_list(os.path.join(temp_path, 'lib'), '.jar')
    for jar_path in jar_list:
        if class_path.strip():
            class_path = class_path + get_system_delimiter();
        class_path = class_path + jar_path

    android_jar_path = os.path.join(tools_path, 'android.jar')
    class_path = class_path + get_system_delimiter() + android_jar_path
    return class_path


# 获取系统的标志
def get_system_delimiter():
    system = platform.system()
    if system == 'Windows':
        return ';'
    else:
        return ':'

