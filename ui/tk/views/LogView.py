import logging
import ttkbootstrap as ttk

from script.utils.logger.logger import Logger

loggerHelper = Logger()
logger = loggerHelper.logger


class LogView:
    def __init__(self, root):
        self.root = root
        self.listen_flag = False
        self.logFrame = ttk.Frame()
        # 日志文本框
        self.logText = ttk.Text(self.logFrame)
        self.logText.pack(fill="both", expand="yes")

    def add(self, parent):
        parent.add(self.logFrame, text="日志")
        self.start_listen_log()

    # 监听日志文件
    def start_listen_log(self):
        handler = TkHandler(self.logText)
        file_formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

        handler.setFormatter(file_formatter)
        loggerHelper.add_handler(handler)


class TkHandler(logging.Handler):
    def __init__(self, logComponent):
        super().__init__()
        self.logComponent = logComponent

    def emit(self, record):
        msg = self.format(record)
        msg = msg.encode("utf-8").decode("utf-8")
        try:
            self.logComponent.insert("end", msg + "\n")
        except Exception:
            return
