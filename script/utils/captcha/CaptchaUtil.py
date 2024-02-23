from script.utils.captcha.RotateCaptcha import RotateCaptcha
from script.utils.logger.logger import Logger

logger = Logger().get_logger()
rotateCaptcha = RotateCaptcha()
class CaptchaUtil:
    @staticmethod
    def getRotateCaptchaRValue(imgPath):
        rotated_image = rotateCaptcha.getImgFromDisk(imgPath)
        predicted_angle = rotateCaptcha.predictAngle(rotated_image)  # 预测还原角度
        logger.info("需旋转角度：{}".format(predicted_angle))

        corrected_image = rotateCaptcha.rotate(rotated_image, -predicted_angle)  # 矫正后图像
        rotateCaptcha.showImg(corrected_image)  # 展示图像

if __name__ == '__main__':
    CaptchaUtil.getRotateCaptchaRValue("D:\\sharx-salt-fish\\assets\\images\\captcha\\1.png")
