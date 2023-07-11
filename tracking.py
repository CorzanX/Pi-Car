import RPi.GPIO as GPIO
from operation import CarOperation
from infrared import CarInfrared
import time
import sys
class CarTracking(CarInfrared,CarOperation):

    def __init__(self, CarInfrared, CarOperation):
        CarInfrared.__init__(self)
        CarOperation.__init__(self)
        # 设置GPIO口为BCM编码方式
        GPIO.setmode(GPIO.BCM)

        # 忽略警告信息
        GPIO.setwarnings(False)
        # 红外跟随模块引脚定义
        self.FollowSensorLeft = 12
        self.FollowSensorRight = 17

        GPIO.setup(self.FollowSensorLeft, GPIO.IN)
        GPIO.setup(self.FollowSensorRight, GPIO.IN)

    #巡线
    def tracking(self, leftSpeed, rightSpeed):

        TrackSensorLeftValue1, TrackSensorLeftValue2, TrackSensorRightValue1, TrackSensorRightValue2 = CarInfrared.tracking_check(self)
        print(TrackSensorLeftValue1, TrackSensorLeftValue2, TrackSensorRightValue1, TrackSensorRightValue2)
        # 四路循迹引脚电平状态
        # 0 0 0 0
        # 黑色横线，维持上次动作
        if TrackSensorLeftValue1 == False and TrackSensorLeftValue2 == False and TrackSensorRightValue1 == False and TrackSensorRightValue2 == False:
            CarOperation.run(self,leftSpeed, rightSpeed)


        # 四路循迹引脚电平状态
        # 0 0 X 0
        # 1 0 X 0
        # 0 1 X 0
        # 以上6种电平状态时小车原地右转
        # 处理右锐角和右直角的转动
        elif (TrackSensorLeftValue1 == False or TrackSensorLeftValue2
             == False) and TrackSensorRightValue2 == False:
            CarOperation.spin_right(self,40, 40)
            time.sleep(0.08)

        # 四路循迹引脚电平状态
        # 0 X 0 0
        # 0 X 0 1
        # 0 X 1 0
        # 处理左锐角和左直角的转动
        elif TrackSensorLeftValue1 == False and (TrackSensorRightValue1 == False or
                                         TrackSensorRightValue2 == False):
            CarOperation.spin_left(self,40, 40)
            time.sleep(0.08)

        # 0 X X X
        # 最左边检测到
        elif TrackSensorLeftValue1 == False:
            CarOperation.spin_left(self,30, 30)

        # X X X 0
        # 最右边检测到
        elif TrackSensorRightValue2 == False:
            CarOperation.spin_right(self,30, 30)

        # 四路循迹引脚电平状态
        # X 0 1 X
        # 处理左小弯
        elif TrackSensorLeftValue2 == False and TrackSensorRightValue1 == True:
            CarOperation.left(self,0, 40)

        # 四路循迹引脚电平状态
        # X 1 0 X
        # 处理右小弯
        elif TrackSensorLeftValue2 == True and TrackSensorRightValue1 == False:
            CarOperation.right(self,40, 0)

        # 四路循迹引脚电平状态
        # X 0 0 X
        # 处理直线
        elif TrackSensorLeftValue2 == False and TrackSensorRightValue1 == False:
            CarOperation.run(self,leftSpeed, rightSpeed)

        # 当为1 1 1 1时小车保持上一个小车运行状态

    # 避障
    def moveaway(self):
        CarOperation.spin_left(self, 18, 18)  # 原地左转 0.6s
        time.sleep(0.6)
        CarOperation.brake(self)
        CarOperation.run(self, 10, 10)  # 前进 1s
        time.sleep(1)
        CarOperation.spin_right(self, 15, 15)  # 原地右转 0.6s
        time.sleep(0.7)
        CarOperation.run(self, 10, 10)  # 前进 1.9s
        time.sleep(1.9)
        CarOperation.spin_right(self, 20, 20)  # 原地右转 0.3s
        time.sleep(0.7)
        CarOperation.run(self, 10, 10)  # 前进1.2s
        time.sleep(1)
        CarOperation.spin_left(self, 20, 20)  # 原地左转0.3s
        time.sleep(0.6)
        print("避障完成")

    # 倒车入库
    def back_into_garage(self, leftSpeed, rightSpeed):
        TrackSensorLeftValue1, TrackSensorLeftValue2, TrackSensorRightValue1, TrackSensorRightValue2 = CarInfrared.tracking_check(self)
        print("daocheing")

        # 四路循迹引脚电平状态
        # 0 0 0 0
        # 遇到黑色横线，倒车入库
        if TrackSensorLeftValue1 == False and TrackSensorLeftValue2 == False and TrackSensorRightValue1 == False and TrackSensorRightValue2 == False:
            CarOperation.back(self, 10, 10)
            time.sleep(0.75)
            CarOperation.spin_left(self, 18, 18)
            time.sleep(0.8)
            CarOperation.back(self, 10, 10)
            time.sleep(1.2)
            sys.exit(0)

        # 四路循迹引脚电平状态
        # 0 0 X 0
        # 1 0 X 0
        # 0 1 X 0
        # 以上6种电平状态时小车原地右转
        # 处理右锐角和右直角的转动
        elif (TrackSensorLeftValue1 == False or TrackSensorLeftValue2
              == False) and TrackSensorRightValue2 == False:
            CarOperation.spin_right(self, 40, 40)
            time.sleep(0.08)

        # 四路循迹引脚电平状态
        # 0 X 0 0
        # 0 X 0 1
        # 0 X 1 0
        # 处理左锐角和左直角的转动
        elif TrackSensorLeftValue1 == False and (TrackSensorRightValue1 == False or
                                                 TrackSensorRightValue2 == False):
            CarOperation.spin_left(self, 40, 40)
            time.sleep(0.08)

        # 0 X X X
        # 最左边检测到
        elif TrackSensorLeftValue1 == False:
            CarOperation.spin_left(self, 30, 30)

        # X X X 0
        # 最右边检测到
        elif TrackSensorRightValue2 == False:
            CarOperation.spin_right(self, 30, 30)

        # 四路循迹引脚电平状态
        # X 0 1 X
        # 处理左小弯
        elif TrackSensorLeftValue2 == False and TrackSensorRightValue1 == True:
            CarOperation.left(self, 0, 40)

        # 四路循迹引脚电平状态
        # X 1 0 X
        # 处理右小弯
        elif TrackSensorLeftValue2 == True and TrackSensorRightValue1 == False:
            CarOperation.right(self, 40, 0)

        # 四路循迹引脚电平状态
        # X 0 0 X
        # 处理直线
        elif TrackSensorLeftValue2 == False and TrackSensorRightValue1 == False:
            CarOperation.run(self, leftSpeed, rightSpeed)

        # 当为1 1 1 1时小车保持上一个小车运行状态

    # 红外跟随
    def infrared_follow(self):
        # 遇到跟随物,红外跟随模块的指示灯亮,端口电平为LOW
        # 未遇到跟随物,红外跟随模块的指示灯灭,端口电平为HIGH
        LeftSensorValue = GPIO.input(self.FollowSensorLeft)
        RightSensorValue = GPIO.input(self.FollowSensorRight)

        if LeftSensorValue == False and RightSensorValue == False:
            CarOperation.run(self, 5, 5)  # 当两侧均检测到跟随物时调用前进函数
        elif LeftSensorValue == False and RightSensorValue == True:
            CarOperation.spin_left(self, 60, 60)  # 左边探测到有跟随物，有信号返回，原地向左转
            time.sleep(0.002)
        elif RightSensorValue == False and LeftSensorValue == True:
            CarOperation.spin_right(self, 60, 60)  # 右边探测到有跟随物，有信号返回，原地向右转
            time.sleep(0.002)
        elif RightSensorValue == True and LeftSensorValue == True:
            CarOperation.brake(self)  # 当两侧均未检测到跟随物时停止
            return False  # 返回是否有跟随物
        return True




