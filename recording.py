#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import threading
import pyaudio
import wave
from pprint import pprint
import dropbox
import datetime

# マイク入力を受け付けるスレッド

class AchooDrumRecording():

    def __init__(self):
        self.CHUNK = 512
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 48000
        self.RECORD_SECONDS = 5
	self.DBX_TOKEN = "1JFyIrQfjfoAAAAAAAAGtNBvi0wrFVZ1qSrnKmdoVohO6GE92tTDYKx6m7IaXS8e"

        self.stop = False

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

        #for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
        while(True):
          if self.stop :
              print("stopping")
              break
          data = self.stream.read(self.CHUNK)
          self.frames.append(data)

        # 各種ディスクリプタをcloseしwavファイルを書き込む
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

	now = datetime.datetime.now()
	wav = ('{0:%Y%m%d%H%M%S}.wav'.format(now))

        wf = wave.open(wav, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

        # dropboxへアップロードする
        dbx = dropbox.Dropbox(self.DBX_TOKEN)
        dbx.users_get_current_account()
        f = open(wav, 'rb')
        dbx.files_upload(f.read(), '/' + wav)
        f.close()

    def set_stop(self):
        """スレッドを停止させる"""
        self.stop = True


if __name__ == '__main__':
    h = AchooDrumRecording()      #スレッドの開始
    #time.sleep(1)
    #h.stop()        #スレッドの停止
    #time.sleep(1)   #メインスレッドが終わる前に止まってる！
    print "finish"

