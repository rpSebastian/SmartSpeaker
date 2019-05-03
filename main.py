from snowboy import snowboydecoder
import sys
import signal
from robot.player import Player
from robot.robot import Robot
from time import sleep

class SmartSpeaker():
    def __init__(self):
        self.interrupted = False
        self.model = "snowboy.pmdl"
        signal.signal(signal.SIGINT, self.signal_handler)
        self.detector = snowboydecoder.HotwordDetector(self.model, sensitivity=0.42)
        print('Listening... Press Ctrl+C to exit')
        self.robot = Robot()
        self.music_player = self.robot.get_music_player()
        self.player = Player()
        
    def signal_handler(self, signal, frame):
        self.interrupted = True

    def interrupt_callback(self):
        return self.interrupted

    def detected_callback(self):
        self.music_player.pause()
        self.player.play_ding()

    def speeched_callback(self, fname):
        self.player.play_dong()
        self.robot.process(fname)
        sleep(1)
        self.music_player.cont()


    def run(self):
        self.detector.start(detected_callback=self.detected_callback, speeched_callback=self.speeched_callback,
               interrupt_check=self.interrupt_callback,
               sleep_time=0.03)

SmartSpeaker().run()
