import RPi.GPIO as GPIO
import time

class CarAlarm(object):

    def __init__(self):
        self.alarm = 8

    # 蜂鸣器报警
    def alarming(self):
        GPIO.setup(self.alarm, GPIO.OUT)  # 将BCM12号引脚设置为输出模式
        pwm = GPIO.PWM(self.alarm, 1000)  # 设置BCM12号引脚, 设置pwm频率为1000HZ
        pwm.start(50)  # 设置初始占空比（范围：0.0 <= dc <= 100.0)
        # pwm.ChangeFrequency(freq)   # freq 为设置的新频率，单位为 Hz
        # pwm.ChangeDutyCycle(dc)     # dc 为设置的新的占空比 范围：0.0-100.0
        i = 1000  # 频率
        dirs = 1  # 频率递增方向，1为正，-1为负
        try:
            count5 = 0
            while count5 < 300:  # 蜂鸣持续1.5秒
                pwm.ChangeFrequency(i)  # 为设置的新频率，单位为 Hz
                count5 += 1
                i = i + 100 * dirs  # 当前频率加上要增加的频率(10)乘以方向
                time.sleep(0.05)  # 延时0.05秒
                print('pwm当前频率为: %d ' % i)  # 控制台打印当前的频率
                if i >= 2000:  # 如果当前频率大于2000hz，方向改为负
                    dirs = -1
                elif i <= 1000:  # 如果当前频率小于1000hz，方向改为正
                    dirs = 1
            GPIO.setup(self.alarm, GPIO.OUT, initial=GPIO.HIGH)  # 初始化停止蜂鸣
        finally:
            pass
