import ttkbootstrap as ttk

import sys
import os

from script.utils.config import ConfigUtil

path = os.path.join(os.getenv('LocalAppData'), "SharxSaltFish/disclaimer")

class Disclaimer():
    def __init__(self,window):
        self.window = window

        if not self.is_agree():

            root = ttk.Window(iconphoto=None, title='免责声明', size=(500, 200),themename='darkly')
            self.root = root
            root.wm_iconbitmap("assets/images/ui/logo.ico")
            # 设置窗口居中
            width = root.winfo_width()
            height = root.winfo_height()
            x = (root.winfo_screenwidth() // 2) - (width // 2)
            y = (root.winfo_screenheight() // 2) - (height // 2)
            root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

            label = ttk.Label(root, text='本软件开源、免费，仅供学习交流使用。开发者团队拥有本项目的最终解释权。\n'
                                         '使用本软件产生的所有问题与本项目与开发者团队无关。')
            label.pack(side='top', padx=20, pady=20)
            buttonFrame = ttk.Frame(root)
            buttonFrame.pack(side='bottom')
            noButton = ttk.Button(root, text='退出', command=self.on_closing)
            noButton.pack(side='right', padx=5, pady=5)
            yesButton = ttk.Button(root, text='我已知晓', command=self.agree)
            yesButton.pack(side='right', padx=5, pady=5)

            # 选项卡
            root.protocol("WM_DELETE_WINDOW", self.on_closing)

            window.withdraw()
            root.deiconify()
        window.mainloop()

    def on_closing(self):
        sys.exit(0)

    def is_agree(self):
        # 检查文件是否存在
        if not os.path.exists(path):
            return False
        if not ConfigUtil.get_value("agreed_to_disclaimer"):
            return False
        return True
    def agree(self):
        ConfigUtil.set_value("agreed_to_disclaimer", True)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'a').close()
        self.root.destroy()
        self.window.deiconify()
