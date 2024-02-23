import datetime
import io

import pyautogui
import win32gui

from script.utils.communication import CommunicationQueueUtil
from script.utils.ocr.OcrHelper import OcrApi
from script.utils.thread import TaskEntity, GobalThreadQueueUtil
from .pos_constants import *
from PIL import ImageGrab
import time

class BaseInfo:
    def __init__(self):
        self.ocrApi = OcrApi()
        # 当前通关数
        self.pass_num = 0
        # 当前战力
        self.power = 0
        # 当前金币数
        self.gold = 0
        # 当前金砖数量
        self.brick = 0
        # 当前离线时间(时分秒)
        self.offline_time = 0

    # 开启检测
    def startDetect(self):
        task = TaskEntity(datetime.datetime.now()+datetime.timedelta(seconds=5), self.updateInfo, "更新基础信息")
        GobalThreadQueueUtil.putTask(task)
    def updateInfo(self):
        # 更新过关数
        self.updatePassNum()
        # 更新战力
        self.updatePower()
        # 更新金币数
        self.updateGold()
        # 更新金砖数量
        self.updateBrick()
        # 更新离线时间
        self.updateOfflineTime()
        CommunicationQueueUtil.send_base_info(self.get_base_info_json())
        # 执行过了60s后再执行
        task = TaskEntity(datetime.datetime.now()+datetime.timedelta(seconds=60), self.updateInfo, "更新基础信息")
        GobalThreadQueueUtil.putTask(task)
    # 更新过关数
    def get_base_info_json(self):
        return {"pass_num":self.pass_num,"power":self.power,"gold":self.gold,"brick":self.brick,"offline_time":self.offline_time}
    def updatePassNum(self):
        res = self.getOCRResult(PASS_NUM_POS)
        if res:
            # trim
            # 结果正则匹配为第xx关才录入
            if res.startswith("第") and res.endswith("关"):
                self.pass_num = res
    # 更新战力
    def updatePower(self):
        res = self.getOCRResult(POWER_POS)
        if res:
            self.power = res
    # 更新金币数
    def updateGold(self):
        res =  self.getOCRResult(GOLD_POS)
        if res:
            # 结果正则匹配为纯数字才录入
            if res.isdigit():
                self.gold = res
    # 更新金砖数量
    def updateBrick(self):
        res =  self.getOCRResult(BRICK_POS)
        if res:
            self.brick = res
    # 更新离线时间
    def updateOfflineTime(self):
        res =  self.getOCRResult(OFFLINE_TIME_POS)
        if res:
            self.offline_time = res
    def getOCRResult(self,POS):
        try:
            # 相对于当前窗口进行截图
            # 获取当前激活窗口
            hwnd = win32gui.GetForegroundWindow()
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            # 输出坐标信息
            pos_list = list(POS)
            # 循环pos_list
            pos_list[0] = pos_list[0] * left
            pos_list[1] = pos_list[1] * top
            pos_list[2] = pos_list[2] * left
            pos_list[3] = pos_list[3] * top
            POS = tuple(pos_list)
            im = ImageGrab.grab(POS)
            # im转换图片字节流
            imgByteArr = io.BytesIO()
            im.save(imgByteArr, format='PNG')
            imgByteArr = imgByteArr.getvalue()
            res = self.ocrApi.runBytes(imgByteArr)
        except Exception as e:
            # print("OCR图片识别失败。错误信息：", e)
            return None
        result = self.ocrApi.getBestText(res)
        if result:
            return result.strip()
        return None

    def print(self):
        print("当前通关数：",self.pass_num)
        print("当前战力：",self.power)
        print("当前金币数：",self.gold)
        print("当前金砖数量：",self.brick)
        print("当前离线时间(时分秒)：",self.offline_time)




if __name__ == '__main__':
    baseInfo= BaseInfo()
    baseInfo.updatePassNum()
    print(baseInfo.pass_num)
