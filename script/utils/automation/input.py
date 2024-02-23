import random

import pyautogui
import time

from script.utils.logger.logger import Logger

logger = Logger().get_logger()

class Input:
    pyautogui.FAILSAFE = False

    @staticmethod
    def mouse_click(x, y):
        try:
            pyautogui.click(x, y)
            logger.debug("鼠标点击 ({x}, {y})".format(x=x, y=y))
        except Exception as e:
            logger.error("鼠标点击出错：{e}".format(e=e))

    # 范围内随机点击
    @staticmethod
    def mouse_click_random(x1,y1, x2, y2):
        # x1,y1为范围左上角坐标，x2,y2为范围右下角坐标
        # 随机一个整数,最小值为x1，最大值为x2
        x = random.randint(x1,x2)
        y = random.randint(y1,y2)
        try:
            pyautogui.click(x, y)
            logger.debug("鼠标点击 ({x}, {y})".format(x=x, y=y))
        except Exception as e:
            logger.error(("鼠标点击出错：{e}").format(e=e))

    @staticmethod
    def mouse_down(x, y):
        try:
            pyautogui.mouseDown(x, y)
            logger.debug(("鼠标按下 ({x}, {y})").format(x=x, y=y))
        except Exception as e:
            logger.error(("鼠标按下出错：{e}").format(e=e))

    @staticmethod
    def mouse_up():
        try:
            pyautogui.mouseUp()
            logger.debug(("鼠标释放"))
        except Exception as e:
            logger.error(("鼠标释放出错：{e}").format(e=e))

    @staticmethod
    def mouse_move(x, y):
        try:
            pyautogui.moveTo(x, y)
            logger.debug(("鼠标移动 ({x}, {y})").format(x=x, y=y))
        except Exception as e:
            logger.error(("鼠标移动出错：{e}").format(e=e))

    @staticmethod
    def mouse_scroll(count, direction=-1):
        for i in range(count):
            pyautogui.scroll(direction)
        logger.debug(("滚轮滚动 {x} 次").format(x=count * direction))

    @staticmethod
    def press_key(key, wait_time=0.2):
        try:
            pyautogui.keyDown(key)
            time.sleep(wait_time)
            pyautogui.keyUp(key)
            logger.debug(("键盘按下 {key}").format(key=key))
        except Exception as e:
            logger.debug(("键盘按下 {key} 出错：{e}").format(key=key, e=e))

    @staticmethod
    def press_mouse(wait_time=0.2):
        try:
            pyautogui.mouseDown()
            time.sleep(wait_time)
            pyautogui.mouseUp()
            logger.debug(("按下鼠标左键"))
        except Exception as e:
            logger.debug(("按下鼠标左键出错：{e}").format(e=e))
