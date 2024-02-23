# 主线程调用延时队列
# 一次执行一个任务, 任务执行完毕后, 才会执行下一个任务
import time
import datetime
from script.utils.logger.logger import Logger

logger = Logger().get_logger()
class MainThreadQueue:
    def __init__(self):
        self.mainQueue = []
        self.thread = None
        self.isRun = False

    def start(self):
        self.isRun = True
        while self.isRun:
            if self.mainQueue:
                for taskEntity in self.mainQueue:
                    now = datetime.datetime.now()
                    if taskEntity.runTime <= now:
                        logger.info(f"任务：{taskEntity.taskName}，执行时间: {now.strftime('%m-%d %H:%M:%S')} 开始执行。")
                        beforeTime =  datetime.datetime.now()
                        taskEntity.task()
                        # 耗时格式化为秒
                        logger.info(f"任务：{taskEntity.taskName}，执行完毕。耗时：{round((datetime.datetime.now()-beforeTime).total_seconds(),2)}秒,延迟执行：{round((datetime.datetime.now() - taskEntity.runTime).total_seconds(),2)}秒")
                        self.mainQueue.remove(taskEntity)
                        break
                    # else:
                        # logger.info(taskEntity)
            # 休眠1s
            time.sleep(1)

    def stop(self):
        self.isRun = False
    def putTask(self,taskEntity):
        self.mainQueue.append(taskEntity)

    def queryTaskExist(self,taskName):
        for taskEntity in self.mainQueue:
            if taskEntity.taskName == taskName:
                return True
        return False


class TaskEntity:
    def __init__(self,runTime,task,taskName):
        self.thread = None
        self.isRun = False
        # 执行时间
        self.runTime = runTime
        self.task = task
        self.taskName = taskName

    # 打印
    def __str__(self):
        return f"任务：{self.taskName},执行时间： {self.runTime.strftime('%m-%d %H:%M:%S')}"
