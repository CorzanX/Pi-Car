# -*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time
import cv2
import collections
import sys
import numpy as np
import base64
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException

from tencentcloud.asr.v20190614 import asr_client, models
import os
import wave
from pyaudio import PyAudio,paInt16
class CarCamera(object):

    def __init__(self):
        # 设置GPIO口为BCM编码方式
        GPIO.setmode(GPIO.BCM)

        # 忽略警告信息
        GPIO.setwarnings(False)
        # 初始化上下左右角度为90度
        self.ServoUpDownPos = 90

        # 舵机引脚定义
        self.ServoUpDownPin = 9
        # 舵机
        GPIO.setup(self.ServoUpDownPin, GPIO.OUT)
        # 设置舵机的频率和起始占空比
        self.pwm_UpDownServo = GPIO.PWM(self.ServoUpDownPin, 50)
        self.pwm_UpDownServo.start(0)

    # 摄像头舵机上下旋转到指定角度
    def updownservo_appointed_detection(self, pos):
        for i in range(1):
            self.pwm_UpDownServo.ChangeDutyCycle(2.5 + 10 * pos / 180)
            time.sleep(0.02)  # 等待20ms周期结束

    # 摄像头舵机上下归位
    def servo_updown_init(self):
        self.updownservo_appointed_detection(0)

    # 舵机停止
    def servo_stop(self):
        self.pwm_UpDownServo.ChangeDutyCycle(90)  # 归零信号

    # 人脸识别
    def takePhoto(self, picpath):
        """拍照
        """
        ret, img = cv2.VideoCapture(0).read()
        cv2.imwrite('/home/pi/Desktop/' + picpath, img)
        print('Photo is token.')


    def faceDetection(self):
        """人脸检测
        """
        print("开始检测")
        faceCascade = cv2.CascadeClassifier(
            '/home/pi/Desktop/haarcascade_frontalface_default.xml')
        print("读取文件1")
        cap = cv2.VideoCapture(0)
        cap.set(3, 640)  # 宽
        cap.set(4, 480)  # 高
        print("显示照片1")
        count = 0
        wi = 0
        hi = 0
        while True:
            ret, img = cap.read()
            # img = cv2.flip(img, -1)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray,
                                                 scaleFactor=1.2,
                                                 minNeighbors=5,
                                                 minSize=(20, 20))

            for (x, y, w, h) in faces:
                # 框出人脸范围
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = img[y:y + h, x:x + w]
                wi = w
                hi = h

            cv2.imshow('video', img)

            k = cv2.waitKey(30) & 0xff
            if k == 27 or count == 30:  # 按'ESC'结束或等待时间截止
                break
            count += 1

        time.sleep(2)
        flag = False
        # 太小的不能算人脸
        if wi < 100 or hi < 100:
            flag = False
        else:
            flag = True
        # 摄像头调用完毕
        cap.release()
        cv2.destroyAllWindows()
        return flag