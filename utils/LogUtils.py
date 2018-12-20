# -*- coding:utf-8 -*-

import logging
import os
import time
import platform


class NullHandler(logging.Handler):
    def emit(self, record): pass


class LogUtils(object):

    log = None

    @staticmethod
    def sharedInstance(task_id):
        if LogUtils.log == None:
            LogUtils.log = LogUtils(task_id)
        return LogUtils.log

    def __init__(self, task_id):
        self.handler = None
        self.logger = logging.getLogger(task_id)
        self.level = logging.INFO
        self.fm = logging.Formatter('%(asctime)s - %(filename)s - [line:%(lineno)-d] - %(levelname)s - %(message)s')
        h = NullHandler()
        self.logger.addHandler(h)

    def set_logger(self, taskid, workpath, gameName, channelId, logName=''):

        logs = os.path.join(workpath, 'Logs')  # 工作目录
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
        fh.setFormatter(self.fm)  # 设置格式
        self.logger.addHandler(fh)  # logger添加文件输出流

        # 输出到控制台
        sh = logging.StreamHandler()  # 输出流对象
        sh.setFormatter(self.fm)  # 设置格式
        self.logger.addHandler(sh)  # logger添加标准输出流（std out）

        self.logger.setLevel(logging.INFO)  # 设置从那个等级开始提示
        self.logger.info(u'开始写入日志...\n')

    def info(self, s):
        self.logger.info(s)
        if not self.handler == None:
            s = s + "\n"
            self.handler(s)

    def setLoggingToHanlder(self, handler):
        self.handler = handler
