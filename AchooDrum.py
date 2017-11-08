#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os
import time
import drumhat
import pygame

import signal

from pprint import pprint
from recording import AchooDrumRecording

import sys

class AchooDrum:
    #DUM_FOLDER = ""
    #files = None
    #samples = None

    def __init__(self, source):
        DRUM_FOLDER = source
    
        BANK = os.path.join(os.path.dirname(__file__), DRUM_FOLDER)
        pygame.mixer.init(44100, -16, 1, 512)
        pygame.mixer.set_num_channels(16)

        self.files = glob.glob(os.path.join(BANK, "*.wav"))
        self.files.sort()
        self.samples = [pygame.mixer.Sound(f) for f in self.files]

    def start_record(self):
        for i in [0, 1, 2, 3, 4, 5, 6, 7]:
            drumhat.led_on(i + 1)
            pygame.time.wait(100);
            drumhat.led_off(i + 1)

ad = AchooDrum("drums")
ad.start_record()

def handle_hit(event):
    ad.samples[event.channel].play(loops = 0)
    print("You hit pad {}, playing: {}".format(event.pad, ad.files[event.channel]))
    ad.hit_time = time.time()

def handle_release():
    pass

drumhat.on_hit(drumhat.PADS, handle_hit)
drumhat.on_release(drumhat.PADS, handle_release)

r = AchooDrumRecording()

# シグナルハンドラ
def handler(signal, frame):
    r.set_stop()
    sys.exit(0)

signal.signal(signal.SIGINT, handler)

while(True):
    time.sleep(1)

