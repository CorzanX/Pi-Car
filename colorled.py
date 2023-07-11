import RPi.GPIO as GPIO
import time

class CarLed(object):
    def __init__(self):
        # 设置GPIO口为BCM编码方式
        GPIO.setmode(GPIO.BCM)

        # 忽略警告信息
        GPIO.setwarnings(False)


        # RGB三色灯引脚定义
        self.LED_R = 22
        self.LED_G = 27
        self.LED_B = 24

        # RGB三色灯设置为输出模式
        GPIO.setup(self.LED_R, GPIO.OUT)
        GPIO.setup(self.LED_G, GPIO.OUT)
        GPIO.setup(self.LED_B, GPIO.OUT)

    # 闪灯
    def ColorLED(self):
        # 循环显示7种不同的颜色
        i = 10
        while i > 0:
            GPIO.output(self.LED_R, GPIO.HIGH)  # 红
            GPIO.output(self.LED_G, GPIO.LOW)
            GPIO.output(self.LED_B, GPIO.LOW)
            time.sleep(0.05)
            GPIO.output(self.LED_R, GPIO.LOW)  # 绿
            GPIO.output(self.LED_G, GPIO.HIGH)
            GPIO.output(self.LED_B, GPIO.LOW)
            time.sleep(0.05)
            GPIO.output(self.LED_R, GPIO.LOW)  # 蓝
            GPIO.output(self.LED_G, GPIO.LOW)
            GPIO.output(self.LED_B, GPIO.HIGH)
            time.sleep(0.05)
            GPIO.output(self.LED_R, GPIO.HIGH)  # 红绿
            GPIO.output(self.LED_G, GPIO.HIGH)
            GPIO.output(self.LED_B, GPIO.LOW)
            time.sleep(0.05)
            GPIO.output(self.LED_R, GPIO.HIGH)  # 红蓝
            GPIO.output(self.LED_G, GPIO.LOW)
            GPIO.output(self.LED_B, GPIO.HIGH)
            time.sleep(0.05)
            GPIO.output(self.LED_R, GPIO.LOW)  # 绿蓝
            GPIO.output(self.LED_G, GPIO.HIGH)
            GPIO.output(self.LED_B, GPIO.HIGH)
            time.sleep(0.05)
            GPIO.output(self.LED_R, GPIO.LOW)  # 灭
            GPIO.output(self.LED_G, GPIO.LOW)
            GPIO.output(self.LED_B, GPIO.LOW)
            time.sleep(0.05)
            i -= 1

