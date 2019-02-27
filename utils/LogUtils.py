# -*- coding:utf-8 -*-

import logging
import os
import time
import platform
import wx


class TextHandler(logging.Handler):

    def __init__(self):
        logging.Handler.__init__(self)
        self.ctrl = None

    def set_ctrl(self, ctrl):
        self.ctrl = ctrl

    def emit(self, record):
        if not self.ctrl == None:
            wx.CallAfter(self.ctrl.write, self.format(record) + "\n")


class LogUtils(object):

    log = None

    @staticmethod
    def sharedInstance(task_id):
        if LogUtils.log == None:
            LogUtils.log = LogUtils(task_id)
        return LogUtils.log

    def __init__(self, task_id):

        self.logger = logging.getLogger(task_id)
        self.level = logging.INFO
        self.fm = logging.Formatter('%(asctime)s - %(filename)s - [line:%(lineno)-d] - %(levelname)s - %(message)s')

        self.text_ctrl = None
        self.text_handler = TextHandler()

    def set_logger(self, taskid, workpath, gameName, channelId, logName=''):

        logs = os.path.join(workpath, 'Logs')  # 工作目录
        if not os.path.exists(logs):
            os.makedirs(logs)

        if logName == '':
            logName = '%s_%s_%s_%s' % (taskid, gameName, channelId, int(time.time()))

        system = platform.system()  # 区分操作系统平台
        if system == 'Windows':
            logs_path = logs + '\\' + logName + ".log"

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

        self.logger.addHandler(self.text_handler)

        self.logger.setLevel(logging.INFO)  # 设置从那个等级开始提示
        self.logger.info(u'开始写入日志...\n')

    def info(self, s):
        self.logger.info(s)

    def set_ctrl_to_logging(self, text_ctrl):
        self.text_ctrl = text_ctrl
        if not self.text_handler == None:
            self.text_handler.set_ctrl(self.text_ctrl)
