import RPi.GPIO as GPIO

class CarInfrared(object):

    def __init__(self):
        # 设置GPIO口为BCM编码方式
        GPIO.setmode(GPIO.BCM)

        # 忽略警告信息
        GPIO.setwarnings(False)
        self.TrackSensorLeftPin1 = 3  # 定义左边第一个循迹红外传感器引脚为3口
        self.TrackSensorLeftPin2 = 5  # 定义左边第二个循迹红外传感器引脚为5口
        self.TrackSensorRightPin1 = 4  # 定义右边第一个循迹红外传感器引脚为4口
        self.TrackSensorRightPin2 = 18  # 定义右边第二个循迹红外传感器引脚为18口
        GPIO.setup(self.TrackSensorLeftPin1, GPIO.IN)
        GPIO.setup(self.TrackSensorLeftPin2, GPIO.IN)
        GPIO.setup(self.TrackSensorRightPin1, GPIO.IN)
        GPIO.setup(self.TrackSensorRightPin2, GPIO.IN)

    def tracking_check(self):
        return [GPIO.input(self.TrackSensorLeftPin1), GPIO.input(self.TrackSensorLeftPin2),GPIO.input(self.TrackSensorRightPin1),GPIO.input(self.TrackSensorRightPin2)]

