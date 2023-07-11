import RPi.GPIO as GPIO

import os
import wave
from pyaudio import PyAudio,paInt16
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
import base64
import json
import time
from ARST.predict_speech_file import *

class CarVoice(object):

    def __init__(self):
        # 设置采样参数
        self.NUM_SAMPLES = 2000
        self.TIME = 2
        self.chunk = 1024

    def record(self):
        pa = PyAudio()  # 实例化 pyaudio

        # 打开输入流并设置音频采样参数 1 channel 16K framerate
        stream = pa.open(format=paInt16,
                         channels=1,
                         rate=16000,
                         input=True,
                         frames_per_buffer=self.NUM_SAMPLES)

        audioBuffer = []  # 录音缓存数组
        count = 0

        # 录制40s语音
        while count < self.TIME * 20:
            string_audio_data = stream.read(self.NUM_SAMPLES)  # 一次性录音采样字节的大小
            audioBuffer.append(string_audio_data)
            count += 1
            print('.'),  # 加逗号不换行输出

        # 保存录制的语音文件到audio.wav中并关闭流
        self.save_wave_file('audio.wav', audioBuffer)
        stream.close()

    # save wav file to filename
    def save_wave_file(self, filename, data):
        wf = wave.open(filename, 'wb')
        wf.setnchannels(1)  # set channels  1 or 2
        wf.setsampwidth(2)  # set sampwidth 1 or 2
        wf.setframerate(16000)  # set framerate 8K or 16K
        wf.writeframes(b"".join(data))  # write data
        wf.close()

    def read_wave_file(self, filename):
        fp = wave.open(filename, 'rb')
        nf = fp.getnframes()  # 获取采样点数量
        print('sampwidth:', fp.getsampwidth())
        print('framerate:', fp.getframerate())
        print('channels:', fp.getnchannels())
        f_len = nf * 2
        audio_data = fp.readframes(nf)

    def result_voice(self, res):
        x = res['Result']
        print(x)
        return x

    # 播放音频
    def sound(self, sd_path):
        path = "/home/pi/Desktop/" + sd_path
        os.system('cvlc %s' % path)


    def check_voice(self):
        from tencentcloud.asr.v20190614 import asr_client, models
        time.sleep(0.5)
        path1 = r'/home/pi/PiCar/audio.wav'
        file1 = open(path1, "rb").read()
        text = base64.b64encode(file1).decode()
        try:

            # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
            # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
            # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
            SecretId = "id"  # id
            SecretKey = "key"  # 密钥
            cred = credential.Credential(SecretId, SecretKey)
            # 实例化一个http选项，可选的，没有特殊需求可以跳过
            httpProfile = HttpProfile()
            httpProfile.endpoint = "asr.tencentcloudapi.com"

            # 实例化一个client选项，可选的，没有特殊需求可以跳过
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            # 实例化要请求产品的client对象,clientProfile是可选的
            # 实例化要请求产品的client对象
            client = asr_client.AsrClient(cred, "ap-shanghai", clientProfile)

            params = {
                "EngSerViceType": "16k_zh",
                "VoiceFormat": "wav",
                "SourceType": 1,
                "Data": text,
                "DataLen": 1
            }
            # 实例化一个请求对象,每个接口都会对应一个request对象
            req = models.SentenceRecognitionRequest()

            print("发送")
            req.from_json_string(json.dumps(params))
            # resp = client.VerifyFace(req)
            # 返回的resp是一个SentenceRecognitionResponse的实例，与请求对象对应
            resp = client.SentenceRecognition(req)
            # 输出json格式的字符串回包
            resp_str = json.loads(resp.to_json_string())

            return resp_str
        except TencentCloudSDKException as err:
            print(err)

    '''
    def check_voice(self):
        path = r'/home/pi/PiCar/audio.wav'
        return predict_speech_file(path)
    '''
    def voice_check_result(self):
        self.record()
        return self.result_voice(self.check_voice())

