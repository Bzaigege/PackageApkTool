#!/usr/bin/python
# -*- coding: utf-8 -*-


import re
import os
import tempfile


class Properties:

    def __init__(self, file_name):
        self.file_name = file_name
        self.properties = {}
        try:
            fopen = open(self.file_name, 'r')
            for line in fopen:
                line = line.strip()
                if line.find('=') > 0 and not line.startswith('#'):
                    strs = line.split('=')
                    self.properties[strs[0].strip()] = strs[1].strip()
        except Exception, e:
            raise e
        else:
            fopen.close()

    def has_key(self, key):
        return self.properties.has_key(key)

    def get(self, key, default_value=''):
        if self.properties.has_key(key):
            return self.properties[key]
        return default_value

    def put(self, key, value):
        self.properties[key] = value
        replace_property(self.file_name, key, value, True)

    def get_properties(self):
        return self.properties


def parse(file_name):
    return Properties(file_name)


# 保留原格式修改
# 新增字段, 默认用key=value形式添加。(中间没有空格)
def replace_property(file_name, key, value, append_on_not_exists=True):
    tmpfile = tempfile.TemporaryFile()

    if os.path.exists(file_name):
        r_open = open(file_name, 'r')
        found = False

        for line in r_open:
            if line.find('=') > 0 and not line.startswith('#'):
                strs = line.split('=')
                from_regex = strs[0]
                pattern = re.compile(r'' + key)
                if pattern.search(from_regex) and not line.strip().startswith('#'):
                    found = True
                    line = re.sub(strs[1].strip(), value, line)
                    tmpfile.write(line)

                else:
                    tmpfile.write(line)

            else:
                tmpfile.write(line)

        if not found and append_on_not_exists:
            tmpfile.write('\n' + key + '=' + value)

        r_open.close()
        tmpfile.seek(0)

        content = tmpfile.read()

        if os.path.exists(file_name):
            os.remove(file_name)

        w_open = open(file_name, 'w')
        w_open.write(content)
        w_open.close()

        tmpfile.close()
    else:
        print "file %s not found" % file_name


# # 原始代码无法原格式修改。有bug, 无法处理文件的key值前后空格问题,导致已有key还会添加。
# def replace_property(file_name, from_regex, to_str, append_on_not_exists=True):
#     tmpfile = tempfile.TemporaryFile()
#
#     if os.path.exists(file_name):
#         r_open = open(file_name, 'r')
#         pattern = re.compile(r'' + from_regex)
#         found = False
#
#         for line in r_open:
#             if pattern.search(line) and not line.strip().startswith('#'):
#                 found = True
#                 line = re.sub(from_regex, to_str, line)
#             tmpfile.write(line)
#
#         if not found and append_on_not_exists:
#             tmpfile.write('\n' + to_str)
#
#         r_open.close()
#         tmpfile.seek(0)
#
#         content = tmpfile.read()
#
#         if os.path.exists(file_name):
#             os.remove(file_name)
#
#         w_open = open(file_name, 'w')
#         w_open.write(content)
#         w_open.close()
#
#         tmpfile.close()
#     else:
#         print "file %s not found" % file_name
