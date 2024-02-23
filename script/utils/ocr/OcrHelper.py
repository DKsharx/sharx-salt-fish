import io
import os

import win32gui
from PIL import ImageGrab

from script.utils.logger.logger import Logger
from script.utils.ocr.api.PPOCR_api import GetOcrApi
from script.utils.update.FastestMirror import FastestMirror
from script.utils.update.UpdateHandler import UpdateHandler

logger = Logger().get_logger()

ocr_path = os.path.join("assets", "download", "PaddleOCR-json_v.1.3.1", "PaddleOCR-json.exe")


ocr = GetOcrApi(ocr_path)

class OcrApi():

    def __init__(self):
        # 初始化识别器对象，传入 PaddleOCR_json.exe 的路径
        self.ocr = ocr

    # 识别本地文件
    def runLocal(self, imgPath: str):
        # 识别图片，传入图片路径
        getObj = self.ocr.run(imgPath)

        return getObj['data']

    # 识别剪贴板
    def runClipboard(self):
        # 识别剪贴板图片
        getObj = self.ocr.runClipboard()
        return getObj['data']

    # 识别图片字节流
    def runBytes(self, imageBytes):
        # 识别图片字节流
        getObj = self.ocr.runBytes(imageBytes)
        return getObj['data']

    def runCurrentScreen(self):
        hwnd = win32gui.GetForegroundWindow()
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        image = ImageGrab.grab((left, top, right, bottom))
        imgByteArr = io.BytesIO()
        image.save(imgByteArr, format='PNG')
        imgByteArr = imgByteArr.getvalue()
        res = self.runBytes(imgByteArr)
        return res

    def runCurrentScreenByCut(self, x1, x2, y1, y2):
        hwnd = win32gui.GetForegroundWindow()
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        image = ImageGrab.grab((left, top, right, bottom))
        w, h = image.size
        image = image.crop((w * x1, h * y1, w * x2, h * y2))
        # 开一个python窗体来显示图片
        imgByteArr = io.BytesIO()
        image.save(imgByteArr, format='PNG')
        imgByteArr = imgByteArr.getvalue()
        res = self.runBytes(imgByteArr)
        return res

    def printResult(self, resList: list):
        """用于调试，格式化打印识别结果。\n
        `res`: OCR识别结果。"""
        # 如果resList是字符串
        if isinstance(resList, str):
            # print("OCR图片识别失败。错误信息：", resList)
            # 抛出异常
            return None
        index = 1
        # 循环
        for res in resList:
            print(f"{index}-置信度：{round(res['score'], 2)}，文本：{res['text']}")
            index += 1

    # 组合所有结果字符串
    def combineResult(self, resList: list):
        if isinstance(resList, str):
            # print("OCR图片识别失败。错误信息：", resList)
            # 抛出异常
            return None
        index = 1
        # 循环
        resultText = ""
        for res in resList:
            index += 1
            resultText += res['text']
        return resultText

    # 获取置信度最高的文本
    def getBestText(self, resList: list):
        # 如果resList是字符串
        if isinstance(resList, str):
            # print("OCR图片识别失败。错误信息：", resList)
            return None
        # 如果resList是列表
        if isinstance(resList, list):
            # 如果resList为空
            if len(resList) == 0:
                print("OCR图片识别失败。错误信息：图片中未识别出文字。")
                return None
            # 如果resList不为空
            else:
                # 获取置信度最高的文本
                bestText = resList[0]['text']
                # 循环
                for res in resList:
                    # 如果置信度更高
                    if res['score'] > resList[0]['score']:
                        # 更新置信度最高的文本
                        bestText = res['text']
                return bestText
        # 如果resList不是字符串也不是列表
        print("OCR图片识别失败。错误信息：无法识别的数据类型。")
        return None

    def recognize_multi_lines(self, imgArr):
        # 将图像保存为字节流
        image_stream = io.BytesIO()
        imgArr.save(image_stream, format='PNG')

        # 获取图像字节流
        image_bytes = image_stream.getvalue()
        # 图片数组转换成图片字节流
        r = self.runBytes(image_bytes)
        return r

    def recognize_single_line(self, imgArr, blacklist):
        pass


def install_ocr():
    url = FastestMirror.get_github_mirror(
        "https://github.com/hiroi-sora/PaddleOCR-json/releases/download/v1.3.1/PaddleOCR-json_v.1.3.1.7z")
    update_handler = UpdateHandler(url, os.path.dirname(ocr_path), "PaddleOCR-json_v.1.3.1")
    update_handler.run()


def check_path():
    if not os.path.exists(ocr_path):
        logger.warning("OCR 路径不存在: {path}".format(path=ocr_path))
        logger.info("正在下载OCR模块所需资源...")
        install_ocr()


check_path()
