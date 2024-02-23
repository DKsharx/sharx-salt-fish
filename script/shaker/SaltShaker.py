# 盐罐子
import datetime
import time

from script.utils.automation.automation import Automation
from script.utils.ocr.OcrHelper import OcrApi
from script.utils.logger.logger import Logger
from script.utils.thread import GobalThreadQueueUtil, TaskEntity

logger = Logger().get_logger()
class SaltShaker:
    def __init__(self):
        self.auto = Automation("咸鱼之王")

    def start(self):
        logger.info("启动功能【盐罐自动获取】")
        task = TaskEntity(datetime.datetime.now(), self.run, "盐罐自动获取")
        GobalThreadQueueUtil.putTask(task)
    def run(self):
        self.ocr = OcrApi()
        # 点击客厅
        self.auto.click_element("./assets/images/menu/livingRoom.png", "image", 0.8, max_retries=10, offset=(10, 10))
        # 休眠2s等待进入
        time.sleep(2)
        # 领取所有罐子
        # getAllPot(self.auto)
        # 检查剩余的罐子
        goldPot = self.auto.find_element("./assets/images/livingRoom/goldPot.png","image",threshold=0.8,max_retries=3)
        if goldPot:
            logger.info("还有金罐子未领取")
        silverPot = self.auto.find_element("./assets/images/livingRoom/silverPot.png","image",threshold=0.8,max_retries=3)
        if silverPot:
            logger.info("还有银罐子未领取")
        # self.ocr.getBestText()


# 领取所有罐子
def getAllPot(auto):
    for i in range(1, 3):
        if auto.click_element("assets/images/livingRoom/getPot.png", "image", 0.8, max_retries=2,
                              offset=(10, 10)):
            time.sleep(1)
            # 随机点下半区域
            auto.random_click_half_place()
