from tkinter import StringVar, filedialog

import ttkbootstrap as ttk

from script.utils.config import ConfigUtil, ConfigConstants
from script.utils.update.AppUpdateHandler import AppUpdateHandler


class SettingView():

    def __init__(self, root):
        self.root = root
        self.settingFrame = ttk.Frame()
        # 基础设置
        self.baseConfigFrame = ttk.Labelframe(self.settingFrame, text="基础设置")
        self.baseConfigFrame.pack(fill="x", padx=5, pady=5)
        self.appPathFrame = ttk.Frame(self.baseConfigFrame)
        self.appPathFrame.pack(fill="x", padx=5, pady=5)
        self.appPathLabel = ttk.Label(self.appPathFrame, text="咸鱼之王启动路径：")
        self.appPathLabel.pack(side="left")
        self.appPathValue = StringVar(value=ConfigUtil.get_value(ConfigConstants.app_path_key))
        self.appPathInputEntry = ttk.Entry(self.appPathFrame,
                                           textvariable=self.appPathValue)
        self.appPathInputEntry.pack(side="left")
        self.selectAppPathButton = ttk.Button(self.appPathFrame,
                                              command=self.openFilePathSelect,
                                              cursor='hand2',
                                              text="选取路径",
                                              bootstyle="dark")
        self.selectAppPathButton.pack(side="right")

        # 功能列表
        self.functionListFrame = ttk.Labelframe(self.settingFrame, text="功能列表")
        self.functionListFrame.pack(fill="x", padx=5, pady=5)

        self.questionFunctionFrame = ttk.Frame(self.functionListFrame)
        self.questionFunctionFrame.pack(fill="x", padx=5, pady=5)
        self.questionLabel = ttk.Label(self.questionFunctionFrame, text="咸鱼大闯关功能：")
        self.questionLabel.pack(side="left")
        self.questionOpenValue = StringVar(value=ConfigUtil.get_value(ConfigConstants.question_function_key))
        self.questionOpenButton = ttk.Checkbutton(self.questionFunctionFrame,
                                                  command=self.updateConfigValue,
                                                  variable=self.questionOpenValue,
                                                  cursor='hand2',
                                                  bootstyle="success-round-toggle")
        self.questionOpenButton.pack(side="right")
        # 关于
        self.aboutFrame = ttk.Labelframe(self.settingFrame, text="关于")
        self.aboutFrame.pack(side="bottom", fill="x", padx=5, pady=5)
        self.githubLabel = ttk.Label(self.aboutFrame, text="项目主页：https://github.com/DKsharx/sharx-salt-fish")
        self.githubLabel.pack(anchor='nw')
        self.versionFrame = ttk.Frame(self.aboutFrame)
        self.versionFrame.pack(anchor='nw', fill='x')
        self.versionLabel = ttk.Label(self.versionFrame, text="当前版本：" + ConfigUtil.get_app_version())
        self.versionLabel.pack(side='left')
        self.versionUpdateButton = ttk.Button(self.versionFrame,
                                              command=self.check_update,
                                              text='检查更新',
                                              cursor='hand2',
                                              bootstyle="dark")
        self.versionUpdateButton.pack(side='left', padx=10)

    def add(self, parent):
        parent.add(self.settingFrame, text="设置")

    def updateConfigValue(self):
        ConfigUtil.set_value(ConfigConstants.question_function_key, self.questionOpenValue.get())

    def openFilePathSelect(self):
        filePath = filedialog.askopenfilename(title="选取咸鱼之王启动路径", filetypes=[('快捷方式', 'lnk')])
        if filePath:
            self.appPathValue.set(filePath)
            ConfigUtil.set_value(ConfigConstants.app_path_key, filePath)

    def check_update(self):
        AppUpdateHandler().check_update()
