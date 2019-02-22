#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import shutil
from utils.LogUtils import *
from xml.dom.minidom import *
from PIL import Image,ImageEnhance

# 合并Icon 和 角标 库


# # 图标下标位置
LEFT_TOP = 'lt'
LEFT_BOTTOM = 'lb'
RIGHT_TOP = 'rt'
RIGHT_BOTTOM = 'rb'


# 合并图标资源和角标(默认在右下角)
def merge_icon_subscript(task_id, temp_path, channel_path, build_config, layout=RIGHT_BOTTOM):

    logger = LogUtils.sharedInstance(task_id)

    # 读取配置信息
    game_icon_path = ''
    game_icon_file_name = ''
    if build_config.has_key('game_icon'):
        game_icon_path = build_config['game_icon']
        game_icon_file_name = os.path.basename(game_icon_path)

    game_subs_path = ''
    game_subs_name = ''
    if build_config.has_key('game_subs'):
        game_subs_path = build_config['game_subs']
        game_subs_name = os.path.basename(game_subs_path)

    # 处理角标目录
    channel_icon_path = os.path.join(channel_path, 'icon')
    channel_icon_name = '%s.png' % layout
    if game_subs_path:
        if not os.path.isdir(channel_icon_path):
            os.makedirs(channel_icon_path)

        icon_drawable = os.path.join(channel_icon_path, 'drawable')
        if not os.path.isdir(icon_drawable):
            os.makedirs(icon_drawable)
        else:
            shutil.rmtree(icon_drawable)

        # 将角标拷贝到该目录内
        shutil.copy(game_subs_path, icon_drawable)
        channel_subs_file_path = os.path.join(icon_drawable, game_subs_name)
        rename_file(channel_subs_file_path, channel_icon_name)

    else:
        if not os.path.isdir(channel_icon_path):
            logger.info(u'渠道icon目录不存在，无法进行合并')
            return 0, u'渠道icon目录不存在，无法进行合并'

    # 读取androidManifest图标配置信息
    game_android_manifest = os.path.join(temp_path, 'AndroidManifest.xml')
    game_dom = xml.dom.minidom.parse(game_android_manifest)
    game_root = game_dom.documentElement
    game_application = game_root.getElementsByTagName('application')
    game_icon_name = game_application[0].getAttribute('android:icon')
    if game_icon_name:
        game_icon_name = game_icon_name.replace('@drawable/', '') + '.png'

    game_res_path = os.path.join(temp_path, 'res')
    for parent, dir_names, file_names in os.walk(game_res_path):

        for filename in file_names:
            if filename == game_icon_name:
                icon_path = os.path.join(parent, game_icon_name)  # 获取游戏图标路径

                # 替换游戏原生的图标
                if game_icon_path:
                    os.remove(icon_path)
                    shutil.copy(game_icon_path, parent)
                    game_icon_file_path = os.path.join(parent, game_icon_file_name)
                    rename_file(game_icon_file_path, game_icon_name)

                # 根据游戏图标路径匹配渠道对应目录是否存在对应的角标图片,如果没有就到下已层循环找
                if 'drawable' in parent:
                    icon_merge_path = find_merge_icon_path('drawable', channel_icon_path, channel_icon_name)

                elif 'drawable-hdpi' in parent:
                    icon_merge_path = find_merge_icon_path('drawable-hdpi', channel_icon_path, channel_icon_name)

                elif 'drawable-ldpi' in parent:
                    icon_merge_path = find_merge_icon_path('drawable-ldpi', channel_icon_path, channel_icon_name)

                elif 'drawable-mdpi' in parent:
                    icon_merge_path = find_merge_icon_path('drawable-mdpi', channel_icon_path, channel_icon_name)

                elif 'drawable-xhdpi' in parent:
                    icon_merge_path = find_merge_icon_path('drawable-xhdpi', channel_icon_path, channel_icon_name)

                elif 'drawable-xxhdpi' in parent:
                    icon_merge_path = find_merge_icon_path('drawable-xxhdpi', channel_icon_path, channel_icon_name)

                elif 'drawable-xxxhdpi' in parent:
                    icon_merge_path = find_merge_icon_path('drawable-xxxhdpi', channel_icon_path, channel_icon_name)

                else:
                    icon_merge_path = ''

                if not icon_merge_path:
                    logger.info(u'无下标,不合并')
                    return 0, u"无下标,不合并"

                status, result = mark_icon(icon_path, icon_merge_path, icon_path)
                if not status == 0:
                    return status, result

    return 0, u'合并角标成功'


# 匹配渠道对应目录是否存在对应的角标图片
def find_merge_icon_path(icon_path, channel_icon_path, channel_icon_name):

    icon_merge_path = os.path.join(channel_icon_path, icon_path, channel_icon_name)

    # 渠道默认图标列表
    icon_dirs = ['drawable', 'drawable-hdpi', 'drawable-ldpi', 'drawable-mdpi',
                 'drawable-xhdpi', 'drawable-xxhdpi', 'drawable-xxxhdpi']

    if not os.path.isfile(icon_merge_path):
        icon_dirs.remove(icon_path)

    # 遍历剩下的list集合
    for icon_dir in icon_dirs:
        icon_merge_path = os.path.join(channel_icon_path, icon_dir, channel_icon_name)
        if os.path.isfile(icon_merge_path):
            return icon_merge_path
        else:
            continue

    # 如果渠道不存在角标资源，返回为空。
    return ''


def mark_layout(im, mark, layout=RIGHT_BOTTOM):
    im_width, im_hight = im.size
    mark_width, mark_hight = mark.size

    coordinates = {LEFT_TOP: (int(im_width), int(im_hight)),
                   LEFT_BOTTOM: (int(im_width), int(im_hight - mark_hight)),
                   RIGHT_TOP: (int(im_width - mark_width), int(im_hight)),
                   RIGHT_BOTTOM: (int(im_width - mark_width), int(im_hight - mark_hight)),
                   }
    return coordinates[layout]


def reduce_opacity(mark, opacity):
    assert opacity >= 0 and opacity <= 1
    mark = mark.convert('RGBA') if mark.mode != 'RGBA' else mark.copy()
    alpha = mark.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    mark.putalpha(alpha)
    return mark


def mark_icon(base_path, mark_path, new_img, layout=RIGHT_BOTTOM, opacity=1):
    """
    :param base_path: icon文件
    :param mark_path: 角标文件
    :param new_img: 输出新的文件
    :param layout: 默认
    :param opacity: 默认
    :return:
    """
    if not os.path.isfile(base_path) or not os.path.isfile(mark_path):
        result = u'[%s,%s]img file is not exits.' % (base_path, mark_path)
        return -101, result

    if os.path.getsize(base_path) == 0 or os.path.getsize(mark_path) == 0:
        result = u'[%s,%s]img file is empty.' % (base_path, mark_path)
        return -102, result

    try:
        img = Image.open(base_path)
        mark = Image.open(mark_path)
        # 判断图片分辨率，把两张图片分辨率调整为一样再合并
        img_x, img_y = img.size
        mark_x, mark_y = mark.size
        if img_x > mark_x:
            mark
            mark = mark.resize((img_x, img_y), Image.ANTIALIAS)
        elif img_x < mark_x:
            img = img.resize((mark_x, mark_y), Image.ANTIALIAS)

        if not mark:
            result = u'Not mark image file.'
            return 0, result

        if opacity < 1:
            mark = reduce_opacity(mark, opacity)

        if img.mode != 'RGBA':
            # print 'NO_PGBA',base_path,mark_path
            img = img.convert('RGBA')
            img_format = 'PNG'
        else:
            img_format = 'PNG'

        layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
        layer.paste(mark, mark_layout(img, mark, layout))

        img = Image.composite(layer, img, layer)
        img.save(new_img, img_format, quality=100)
        return 0, u'合并图片成功'

    except Exception as e:
        return -100, str(e)


def rename_file(file_path, new_name):
    icon_name = os.path.basename(file_path)
    icon_dir = os.path.dirname(file_path) + get_system_tag()
    icon_new_name = icon_name.replace(icon_name, new_name)
    os.rename(icon_dir + icon_name, icon_dir + icon_new_name)


# 获取系统目录的标志
def get_system_tag():
    system = platform.system()
    if system == 'Windows':
        return '\\'
    else:
        return '/'