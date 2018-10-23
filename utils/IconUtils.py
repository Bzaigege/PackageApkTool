
# -*- coding:utf-8 -*-
import os
from PIL import Image,ImageEnhance


# # 图标下标位置
LEFT_TOP = 'lt'
LEFT_BOTTOM = 'lb'
RIGHT_TOP = 'rt'
RIGHT_BOTTOM = 'rb'


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


