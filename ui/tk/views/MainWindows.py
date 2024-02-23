import tkinter

import ttkbootstrap as ttk

from ui.tk.views.HomeView import HomeView
from ui.tk.views.LogView import LogView
from ui.tk.views.SettingView import SettingView


class MainWindows():
    def __init__(self):
        root = ttk.Window(themename="darkly",iconphoto=None,title='sharx-salt-fish',size=(400,600))
        self.root = root
        root.wm_iconbitmap("assets/images/ui/logo.ico")
        # 选项卡
        mainNoteBook = ttk.Notebook(root)

        homeView = HomeView(root)
        homeView.add(mainNoteBook)
        logView = LogView(root)
        logView.add(mainNoteBook)
        settingView = SettingView(root)
        settingView.add(mainNoteBook)

        mainNoteBook.pack(padx=10, pady=5, fill=tkinter.BOTH, expand=True)

    def getTk(self):
        return self.root

