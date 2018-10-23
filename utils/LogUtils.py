# -*- coding:utf-8 -*-

import logging
import os
import time
import platform


def init_log(taskid, workpath, gameName, channelId, logName=''):

    logger = logging.getLogger(taskid)  # logging对象
    fm = logging.Formatter('%(asctime)s - %(filename)s - [line:%(lineno)-d] - %(levelname)s - %(message)s')# 格式化对象

    logs = os.path.join(workpath, 'Logs')   # 工作目录
    if not os.path.exists(logs):
        os.makedirs(logs)

    if logName == '':
        logName = '%s_%s_%s_%s' % (taskid, gameName, channelId, int(time.time()))

    system = platform.system()  # 区分操作系统平台
    if system == 'Windows':
        logs_path = logs + '\\' + logName + ".log"
    elif system == 'Darwin':  # Mac
        logs_path = logs + '/' + logName + ".log"
    elif system == 'Linux':
        logs_path = logs + '/' + logName + ".log"
    else:
        logs_path = logs + '/' + logName + ".log"

    fh = logging.FileHandler(logs_path)  # 文件对象
    # fh = logging.FileHandler(logs_path, encoding='utf-8')  # 文件对象(python3.6.5)
    fh.setFormatter(fm)  # 设置格式
    logger.addHandler(fh)  # logger添加文件输出流

    # 输出到控制台
    sh = logging.StreamHandler()  # 输出流对象
    sh.setFormatter(fm)  # 设置格式
    logger.addHandler(sh)  # logger添加标准输出流（std out）

    logger.setLevel(logging.DEBUG)  # 设置从那个等级开始提示

    logger.debug(u'开始写入日志...\n')

    return logger


def get_logger(taskid):
    logger = logging.getLogger(taskid)  # logging对象
    return logger