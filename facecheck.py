import RPi.GPIO as GPIO
import time
from camera import CarCamera
from colorled import CarLed
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
import base64
import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
class CarFaceCheck( CarCamera, CarLed):

    def __init__(self, CarCamera, CarLed):
        CarCamera.__init__(self)
        CarLed.__init__(self)

    def checkFace(self, picpath, personid):
        from tencentcloud.iai.v20200303 import iai_client, models
        """人脸识别
        """
        # 先对拍摄到的图片进行base64编码
        with open('/home/pi/Desktop/' + picpath, 'rb') as f:
            base64_data = base64.b64encode(f.read())
        s = base64_data.decode()
        pic_b64 = 'data:image/jpg;base64,' + s  # 将图片解码

        SecretId = "id"  # id
        SecretKey = "key"  # 密钥

        try:
            # 实例化一个认证对象
            cred = credential.Credential(
                SecretId, SecretKey)  # 入参需要传入腾讯云账户secretId，secretKey

            # 实例化一个http选项
            httpProfile = HttpProfile()
            httpProfile.endpoint = "iai.tencentcloudapi.com"  # 指定接入地域域名(v默认就近接入)

            # 实例化一个client选项
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            # 实例化要请求产品的client对象
            client = iai_client.IaiClient(cred, "ap-shanghai", clientProfile)

            # 实例化一个实例信息查询请求对象req
            req = models.VerifyPersonRequest()
            params = {"Image": pic_b64, "PersonId": personid, "QualityControl": 2}
            req.from_json_string(json.dumps(params))
            # req.from_json_string(json.dumps(params))
            resp = client.VerifyFace(req)
            return True, json.loads(resp.to_json_string())

        except TencentCloudSDKException as err:
            print(err)
            return False, err

    def result(self, res):
        """判断人脸识别结果
        """
        x = res['Score']
        threshold = 85

        if x > threshold:
            return True
        return False

    def checking(self, picpath='tmp.jpg', personid='1'):
        """识别总调用
        """
        i = 0
        flag = 0
        # 摄像头纵向舵机抬至45度，方便人脸识别
        CarCamera.updownservo_appointed_detection(self, 45)
        time.sleep(1)
        CarCamera.servo_stop(self)
        # 检测是否有人脸
        havePer = CarCamera.faceDetection(self)
        if not havePer:
            # 没有人脸，返回-1
            CarCamera.servo_updown_init(self)
            return -1

        # 识别失败则再次识别，最多重复3次
        while i < 3:
            CarCamera.takePhoto(self ,picpath)
            # 调用腾讯云API得到人脸验证结果
            rflag, info = self.checkFace(picpath, personid)
            if rflag:
                # 根据验证分数得到结果
                if self.result( info):
                    # 验证通过，闪绿灯
                    GPIO.output(self.LED_R, GPIO.LOW)
                    GPIO.output(self.LED_G, GPIO.HIGH)
                    GPIO.output(self.LED_B, GPIO.LOW)
                    time.sleep(0.05)
                    GPIO.output(self.LED_R, GPIO.LOW)
                    GPIO.output(self.LED_G, GPIO.LOW)
                    GPIO.output(self.LED_B, GPIO.LOW)
                    time.sleep(0.05)
                    GPIO.output(self.LED_R, GPIO.LOW)
                    GPIO.output(self.LED_G, GPIO.HIGH)
                    GPIO.output(self.LED_B, GPIO.LOW)
                    time.sleep(0.05)
                    GPIO.output(self.LED_R, GPIO.LOW)
                    GPIO.output(self.LED_G, GPIO.LOW)
                    GPIO.output(self.LED_B, GPIO.LOW)
                    time.sleep(0.05)
                    print('好耶')
                    flag = 1
                    # 验证通过，返回1
                    CarCamera.servo_updown_init(self)
                    return flag
                else:
                    # 验证未通过，闪红灯
                    GPIO.output(self.LED_R, GPIO.HIGH)
                    GPIO.output(self.LED_G, GPIO.LOW)
                    GPIO.output(self.LED_B, GPIO.LOW)
                    time.sleep(0.05)
                    GPIO.output(self.LED_R, GPIO.LOW)
                    GPIO.output(self.LED_G, GPIO.LOW)
                    GPIO.output(self.LED_B, GPIO.LOW)
                    time.sleep(0.05)
                    GPIO.output(self.LED_R, GPIO.HIGH)
                    GPIO.output(self.LED_G, GPIO.LOW)
                    GPIO.output(self.LED_B, GPIO.LOW)
                    time.sleep(0.05)
                    GPIO.output(self.LED_R, GPIO.LOW)
                    GPIO.output(self.LED_G, GPIO.LOW)
                    GPIO.output(self.LED_B, GPIO.LOW)
                    time.sleep(0.05)
                    print('你谁啊')

            # 验证不通过，返回0
            i += 1

        CarCamera.servo_updown_init(self)
        return flag

    def sendEmail(self):
        # 设置服务器所需信息
        fromaddr = 'mail'
        password = 'key'  # 邮箱授权码
        toaddrs = ['xxxx', 'xxx']

        # 设置email信息
        content = 'Stranger！'
        textApart = MIMEText(content, 'plain', 'utf-8')

        imageFile = '/home/pi/Desktop/tmp.jpg'
        imageApart = MIMEImage(
            open(imageFile, 'rb').read(),
            imageFile.split('.')[-1])
        imageApart.add_header('Content-Disposition',
                              'attachment',
                              filename=imageFile)

        m = MIMEMultipart()
        m.attach(textApart)
        m.attach(imageApart)
        m['Subject'] = Header('来自corzan', 'utf-8')
        m['From'] = Header(f'=?utf-8?B?{base64.b64encode("来自corzan".encode()).decode()}=?= <1194082497@qq.com>')
        m['To'] = Header("来自corzan", 'utf-8')

        # 登录并发送邮件
        try:
            server = smtplib.SMTP_SSL('smtp.qq.com', 465)  # qq邮箱服务器地址
            server.login(fromaddr, password)
            server.sendmail(fromaddr, toaddrs, m.as_string())
            print('success')
            server.quit()

        except smtplib.SMTPException as e:
            print('error', e)  # 打印错误