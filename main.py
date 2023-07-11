import time
import RPi.GPIO as GPIO
from tracking import CarTracking
from infrared import CarInfrared
from operation import CarOperation
from camera import CarCamera
from colorled import CarLed
from distance import CarDistance
from facecheck import CarFaceCheck
from voicecheck import CarVoice
from alarm import CarAlarm
# 设置GPIO口为BCM编码方式
GPIO.setmode(GPIO.BCM)

# 忽略警告信息
GPIO.setwarnings(False)
class Car(CarTracking, CarInfrared, CarOperation, CarDistance,  CarFaceCheck, CarCamera, CarLed, CarVoice, CarAlarm):

    def __init__(self):
        CarDistance.__init__(self)
        CarTracking.__init__(self, CarInfrared, CarOperation)

        CarFaceCheck.__init__(self, CarCamera, CarLed)
        CarVoice.__init__(self)
        CarAlarm.__init__(self)

    def AllStop(self):
        CarTracking.brake()
        GPIO.cleanup()


if __name__ == '__main__':
    car = Car()
    try:
        while True:
            distance = car.Distance_test()
            print("正在走路")
            if distance > 50:
                car.tracking(15, 15)  # 当距离障碍物较远时高速巡线前进
            elif 20 <= distance <= 50:
                car.tracking(10, 10)  # 当快靠近障碍物时低速巡线前进
            elif distance < 20: # 靠近障碍物时
                car.brake()
                time.sleep(2)
                recognition = car.checking()
                if recognition == 1:
                    time.sleep(2)
                    print("主人")
                    re = car.voice_check_result()
                    if "歌" in re:
                        car.sound("tally.mp3")
                    elif "跟" in re:
                        while car.infrared_follow():
                            pass

                    elif "回去" in re:
                        while True:
                            car.back_into_garage(5,5)

                elif recognition == 0:
                    car.sendEmail()
                    car.alarming()
                    car.sound("gege.MP3")
                    time.sleep(7)
                    
                
                elif recognition == -1:
                    car.moveaway()
    except KeyboardInterrupt:
        pass
    car.moveaway()

    car.alarming()
    time.sleep(7)
    car.pwm_ENA.stop()  # 左电机停止运行
    car.pwm_ENB.stop()  # 右电机停止运行









