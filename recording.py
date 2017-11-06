#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import threading
import pyaudio
import wave
from pprint import pprint

# マイク入力を受け付けるスレッド

class AchooDrumRecording():

    def __init__(self):
        self.CHUNK = 512
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 48000
        self.RECORD_SECONDS = 5
        self.WAVE_OUTPUT_FILENAME = "output.wav"

        self.stop_event = threading.Event() # 停止させるかのフラグ

        self.p = pyaudio.PyAudio()

        self.stream = self.p.open(format = self.FORMAT,
                channels = self.CHANNELS,
                rate = self.RATE,
                input = True,
                frames_per_buffer = self.CHUNK)
        self.frames = []

        # スレッドの作成と開始
        self.thread = threading.Thread(target = self.target)
        self.thread.start()

    def target(self):
        # データを取得し配列にどんどん追加する
        print("* recording")

        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
          data = self.stream.read(self.CHUNK)
          self.frames.append(data)

        print("* done recording")

    def stop(self):
        """スレッドを停止させる"""
        self.stop_event.set()
        self.thread.join()    #スレッドが停止するのを待つ

    def __del__(self):
	print("decontructor")
        # 各種ディスクリプタをcloseしwavファイルを書き込む
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

if __name__ == '__main__':
    h = AchooDrumRecording()      #スレッドの開始
    time.sleep(1)
    h.stop()        #スレッドの停止
    time.sleep(1)   #メインスレッドが終わる前に止まってる！
    print "finish"

