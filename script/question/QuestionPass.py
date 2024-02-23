import datetime

from script.utils.logger.logger import Logger
from script.utils.ocr.OcrHelper import OcrApi
from fuzzywuzzy import process

# 读取本地文本txt
import json

from script.utils.thread import GobalThreadQueueUtil, TaskEntity

question_path = "assets/question/question_bank.txt"

logger = Logger().get_logger()
class QuestionPasser:
    def __init__(self):
        # 读取本地文本文件
        with open(question_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        json_string = '[' + ','.join([line.strip().replace("\n", "") for line in lines]) + ']'
        # 转换每一行文本为JSON对象
        questions = json.loads(json_string)
        # 循环json，用标题作为key 组装一个map
        self.questions = {q['q']: q for q in questions}
        # 将所有的key组装成一个list
        self.questions_list = list(self.questions.keys())
    def start(self):
        logger.info("启动功能【咸鱼大闯关】")
        task = TaskEntity(datetime.datetime.now(), self.run, "咸鱼大闯关")
        GobalThreadQueueUtil.putTask(task)
    def run(self):
        for i in range(10):
            ocr = OcrApi()
            y_offset_1 = 0.095
            y_offset_2 = 0.268
            x_offset_2 = 0.8
            res = ocr.runCurrentScreenByCut(0, x_offset_2, y_offset_1, y_offset_2)
            # 模糊字符串匹配算法
            questionStr = ocr.combineResult(res)
            if questionStr:
                matchResult = process.extractOne(questionStr, self.questions_list)
                ans = self.questions.get(matchResult[0])['ans'] == 'A'
                logger.info(f"【咸鱼大闯关】匹配答案：{ans},题目：{questionStr},匹配结果：{matchResult}")
        task = TaskEntity(datetime.datetime.now()+datetime.timedelta(days=3), self.run, "咸鱼大闯关")
        GobalThreadQueueUtil.putTask(task)
