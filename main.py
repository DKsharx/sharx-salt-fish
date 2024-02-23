from script.baseInfo.BaseInfo import BaseInfo
from script.holder.ApplicationHolder import ApplicationHolder
from script.question.QuestionPass import QuestionPasser
from script.utils.config import ConfigUtil, ConfigConstants
from script.utils.logger.logger import Logger
from script.utils.thread import GobalThreadQueueUtil
logger = Logger().get_logger()




def start_script():
    logger.info("开始执行脚本")
    ConfigUtil.check_config()
    GobalThreadQueueUtil.start()
    # 基础信息定时OCR获取
    # BaseInfo().startDetect()
    ApplicationHolder(checkSecond=600, win_name="咸鱼之王").start()
    # SaltShaker().start()
    if ConfigUtil.get_value(ConfigConstants.question_function_key) == '1':
        QuestionPasser().start()

def stop_script():
    logger.info("停止脚本")
    GobalThreadQueueUtil.stop()

if __name__ == '__main__':
    start_script()
