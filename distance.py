import RPi.GPIO as GPIO
import time

class CarDistance(object):

    def __init__(self):
        # 设置GPIO口为BCM编码方式
        GPIO.setmode(GPIO.BCM)

        # 忽略警告信息
        GPIO.setwarnings(False)

        # 超声波引脚定义
        self.EchoPin = 0  # 回声脚
        self.TrigPin = 1  # 触发脚
        GPIO.setup(self.EchoPin, GPIO.IN)
        GPIO.setup(self.TrigPin, GPIO.OUT)

    # 超声波函数
    def Distance_test(self ):
        GPIO.output(self.TrigPin, GPIO.HIGH)
        time.sleep(0.000015)
        GPIO.output(self.TrigPin, GPIO.LOW)
        while not GPIO.input(self.EchoPin):
            pass
        t1 = time.time()
        while GPIO.input(self.EchoPin):
            pass
        t2 = time.time()
        print("distance is %d " % (((t2 - t1) * 340 / 2) * 100))
        time.sleep(0.01)
        return ((t2 - t1) * 340 / 2) * 100
