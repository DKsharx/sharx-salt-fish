import logging
import tkinter.messagebox
from tkinter import StringVar

import ttkbootstrap as ttk
import time

from main import start_script, stop_script
from script.utils.communication import CommunicationQueueUtil
from script.utils.config import ConfigUtil, ConfigConstants


class HomeView:
    def __init__(self, root):
        self.root = root
        self.homeFrame = ttk.Frame()
        # 软件信息
        self.software_info_frame()
        # 操作面板
        self.operation_panel_frame()
        # 结果列表
        self.result_info_frame()
        # 基本信息
        self.base_info_frame()
        # 运行信息
        self.run_info_frame()

    def run_info_frame(self):
        self.runInfoFrame = ttk.Labelframe(self.homeFrame, text="运行信息")
        self.runInfoFrame.pack(side="bottom", fill="x", padx=5, pady=5)
        self.startTime = None
        self.timer_running_flag = False
        self.diff_time = 0

        self.diff_time = ConfigUtil.get_value(ConfigConstants.software_run_time_key)

        formatted_time = time.strftime('%H小时%M分钟%S秒', time.gmtime(self.diff_time))
        self.runTimeLabel = ttk.Label(self.runInfoFrame, text=f"总运行时长：{formatted_time}")
        self.runTimeLabel.pack(anchor="nw")
        self.update_timer()

    def software_info_frame(self):
        self.softwareInfoFrame = ttk.Frame(self.homeFrame)
        self.softwareInfoFrame.pack(fill="x", padx=5, pady=5)
        self.swLabel = ttk.Label(self.softwareInfoFrame, text="Sharx的咸鱼之王小助手" + ConfigUtil.get_app_version())
        self.swLabel.pack(anchor="nw")

    def operation_panel_frame(self):
        self.operationPanelFrame = ttk.Labelframe(self.homeFrame, text="操作面板")
        self.operationPanelFrame.pack(fill="x", padx=5, pady=5, ipadx=5, ipady=5)
        self.startFrame = ttk.Frame(self.operationPanelFrame)
        self.startFrame.pack(fill="x")
        self.startLabel = ttk.Label(self.startFrame, text="启动操作：")
        self.startLabel.pack(side="left")
        self.stopButton = ttk.Button(self.startFrame,
                                     command=self.stop_script,
                                     text="停止",
                                     cursor='heart',
                                     bootstyle="danger-outline",
                                     state="disabled")
        self.startButton = ttk.Button(self.startFrame, command=self.start_script, text="启动", cursor='hand2',
                                      bootstyle="success-outline")
        self.stopButton.pack(side="right", padx=5)
        self.startButton.pack(side="right")

    def result_info_frame(self):
        self.resultInfoFrame = ttk.Labelframe(self.homeFrame, text="结果信息")
        self.resultInfoFrame.pack(fill="x", padx=5, pady=5)
        self.questionPassNum = ConfigUtil.get_value(ConfigConstants.question_com_num_key)
        self.questionPassLabel = ttk.Label(self.resultInfoFrame,
                                           text=f"咸鱼大闯关-完成次数：{self.questionPassNum}")
        self.questionPassLabel.pack(anchor="nw")

    def base_info_frame(self):
        self.baseInfoFrame = ttk.Labelframe(self.homeFrame, text="基本信息")
        self.baseInfoFrame.pack(fill="x", padx=5, pady=5)
        self.powerValue = StringVar(value="当前战力：" + "0")
        self.powerLabel = ttk.Label(self.baseInfoFrame, textvariable=self.powerValue)
        self.powerLabel.pack(anchor="nw")
        self.passNumValue = StringVar(value="当前过关数：" + "0")
        self.passNumLabel = ttk.Label(self.baseInfoFrame, textvariable=self.passNumValue)
        self.passNumLabel.pack(anchor="nw")
        self.goldValue = StringVar(value="当前金币数：" + "0")
        self.goldLabel = ttk.Label(self.baseInfoFrame, textvariable=self.goldValue)
        self.goldLabel.pack(anchor="nw")
        self.brickValue = StringVar(value="当前金砖数量：" + "0")
        self.brickLabel = ttk.Label(self.baseInfoFrame, textvariable=self.brickValue)
        self.brickLabel.pack(anchor="nw")
        self.refresh_base_info()

    def refresh_base_info(self):
        base_info = CommunicationQueueUtil.get_base_info()
        if base_info:
            self.powerValue.set("当前战力：" + str(base_info['power']))
            self.passNumValue.set("当前过关数：" + str(base_info['pass_num']))
            self.goldValue.set("当前金币数：" + str(base_info['gold']))
            self.brickValue.set("当前金砖数量：" + str(base_info['brick']))
        self.baseInfoFrame.after(3000, self.refresh_base_info)

    def add(self, parent):
        parent.add(self.homeFrame, text="主页")

    def start_script(self):
        self.startButton.config(state="disabled", cursor='heart')
        self.stopButton.config(state="normal", cursor='hand2')
        self.start_cal_run_time_timer()
        try:
            start_script()
        except Exception as e:
            error_message = str(e)
            logging.error(error_message)
            tkinter.messagebox.showerror(title='错误', message=error_message)
            self.stop_script()

    def stop_script(self):
        self.stopButton.config(state="disabled", cursor='heart')
        self.startButton.config(state="normal", cursor='hand2')
        self.stop_cal_run_time_timer()
        stop_script()

    def start_cal_run_time_timer(self):
        if not self.timer_running_flag:
            self.timer_running_flag = True
            self.startTime = time.time()

    def stop_cal_run_time_timer(self):
        if self.timer_running_flag:
            self.timer_running_flag = False

    def update_timer(self):
        if self.timer_running_flag:
            now = time.time()
            self.diff_time = self.diff_time + now - self.startTime
            self.startTime = now
            formatted_time = time.strftime('%H小时%M分钟%S秒', time.gmtime(self.diff_time))
            self.runTimeLabel.config(text=f"总运行时长：{formatted_time}")
            ConfigUtil.set_value(ConfigConstants.software_run_time_key, self.diff_time)
        self.root.after(200, self.update_timer)
