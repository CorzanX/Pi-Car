import RPi.GPIO as GPIO

import os
import wave
from pyaudio import PyAudio,paInt16
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
        path = r'/home/pi/PiCar/audio.wav'
        return predict_speech_file(path)

    def voice_check_result(self):
        self.record()
        return self.result_voice(self.check_voice())

