import RPi.GPIO as GPIO


class CarOperation(object):
    def __init__(self):
        # 设置GPIO口为BCM编码方式
        GPIO.setmode(GPIO.BCM)

        # 忽略警告信息
        GPIO.setwarnings(False)
        self.IN1 = 20  # 前左电机是否开启
        self.IN2 = 21  # 后左电机是否开启
        self.IN3 = 19  # 前右电机是否开启
        self.IN4 = 26  # 后右电机是否开启
        self.ENA = 16  # 左侧电机控速
        self.ENB = 13  # 右侧电机控速
        GPIO.setup(self.ENA, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.IN1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.IN2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.ENB, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.IN3, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.IN4, GPIO.OUT, initial=GPIO.LOW)
        # 设置pwm引脚和频率为2000hz
        self.pwm_ENA = GPIO.PWM(self.ENA, 2000)
        self.pwm_ENB = GPIO.PWM(self.ENB, 2000)
        self.pwm_ENA.start(0)
        self.pwm_ENB.start(0)

    # 小车前进
    def run(self, leftSpeed, rightSpeed):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(leftSpeed)
        self.pwm_ENB.ChangeDutyCycle(rightSpeed)

    # 小车后退
    def back(self, leftSpeed, rightSpeed):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        self.pwm_ENA.ChangeDutyCycle(leftSpeed)
        self.pwm_ENB.ChangeDutyCycle(rightSpeed)

    # 小车向左倒车
    def bleft(self, leftSpeed, rightSpeed):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        self.pwm_ENA.ChangeDutyCycle(leftSpeed)
        self.pwm_ENB.ChangeDutyCycle(rightSpeed)

    # 小车向右倒车
    def bright(self, leftSpeed, rightSpeed):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(leftSpeed)
        self.pwm_ENB.ChangeDutyCycle(rightSpeed)

    # 小车左转
    def left(self, leftSpeed, rightSpeed):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(leftSpeed)
        self.pwm_ENB.ChangeDutyCycle(rightSpeed)

    # 小车右转
    def right(self, leftSpeed, rightSpeed):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(leftSpeed)
        self.pwm_ENB.ChangeDutyCycle(rightSpeed)

    # 小车原地左转
    def spin_left(self, leftSpeed, rightSpeed):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(leftSpeed)
        self.pwm_ENB.ChangeDutyCycle(rightSpeed)

    # 小车原地右转
    def spin_right(self, leftSpeed, rightSpeed):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        self.pwm_ENA.ChangeDutyCycle(leftSpeed)
        self.pwm_ENB.ChangeDutyCycle(rightSpeed)

    # 小车停止
    def brake(self):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

