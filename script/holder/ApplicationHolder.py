import datetime
import os

import subprocess

import win32com.client
import win32gui

from script.utils.config import ConfigUtil, ConfigConstants
from script.utils.thread import TaskEntity, GobalThreadQueueUtil
from script.utils.logger.logger import Logger

import pygetwindow as gw
import pythoncom
logger = Logger().get_logger()

class ApplicationHolder:
    def __init__(self,checkSecond,win_name):
        exe_path = self.select_exe_path()
        target_path,target_args =  self.get_target_from_lnk(exe_path)
        # 获取程序名称
        program_name = os.path.basename(target_path)
        # 替换程序名称和exe文件路径为你自己的程序和路径
        self.program_name = program_name
        self.exe_path = exe_path
        self.checkSecond = checkSecond
        self.win_name = win_name

    def check_and_start_program(self):
        logger.info(f"检测程序{self.program_name}是否在运行")
        # 检测程序是否在运行
        if not self.is_program_running():
            logger.info(f"程序{self.program_name}未运行，启动程序")
            # 启动程序
            self.start_program(self.exe_path)
            logger.info(f"程序{self.program_name}启动成功")
            # 获取窗口
            w = gw.getWindowsWithTitle(self.win_name)
            if w:
                window = w[0]
                # 初始化
                # window.moveTo(0, 0)
                # window.resizeTo(600, 1200)
                # 激活窗口
                window.activate()
        else:
            logger.info(f"程序{self.program_name}正在运行,无需启动")
        # 执行过了10分钟后再执行
        task = TaskEntity(datetime.datetime.now() + datetime.timedelta(seconds=self.checkSecond), self.check_and_start_program,
                          "检测并启动程序")
        GobalThreadQueueUtil.putTask(task)

    def select_exe_path(self):
        return ConfigUtil.get_value(ConfigConstants.app_path_key)

    # def is_program_running(self, program_name):
    #     for proc in psutil.process_iter(['name']):
    #         if proc.info['name'] == program_name:
    #             return True
    #     return False

    def is_program_running(self):
        w = gw.getWindowsWithTitle(self.win_name)
        if not w:
                return False
        if not w[0].isActive:
            logger.warning(f"{self.win_name}窗口未激活,正在激活窗口")
            w[0].activate()
        return True
    def start_program(self, exe_path):
        target_path,target_args =  self.get_target_from_lnk(exe_path)
        command = f"{target_path} {target_args}"
        logger.info(f"启动命令：{command}")
        try:
            subprocess.run(command, shell=True,timeout=10)
        except Exception as e:
            logger.error(f"启动超时,可能程序{command}已启动")

    def get_target_from_lnk(self,lnk_path):
            # 创建一个Shell对象
            pythoncom.CoInitialize()
            shell = win32com.client.Dispatch("WScript.Shell")
            # 通过Shell对象打开.lnk文件
            shortcut = shell.CreateShortCut(lnk_path)

            # 获取.lnk文件的目标路径
            target_path = shortcut.Targetpath
            target_args = shortcut.Arguments
            pythoncom.CoUninitialize()
            return target_path,target_args
    def start(self):
        logger.info("开始启动程序")
        task = TaskEntity(datetime.datetime.now(), self.check_and_start_program,
                          "检测并启动程序")
        GobalThreadQueueUtil.putTask(task)
