from ui.tk.views.MainWindows import MainWindows
from ui.tk.views.disclaimer.disclaimer import Disclaimer
from script.utils.logger.logger import Logger
from script.utils.ocr.OcrHelper import ocr
import atexit



logger = Logger().get_logger()


def exit_handler():
    logger.info("释放ocr资源中...")
    ocr.exit()
    logger.info("释放ocr资源成功")

if __name__ == '__main__':
    atexit.register(exit_handler)
    mainWindows = MainWindows()
    Disclaimer(mainWindows.getTk())


