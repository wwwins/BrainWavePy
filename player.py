# -*- coding: utf-8 -*-
# player.py
# mpg123Player
# Ref: https://groups.google.com/forum/#!topic/web2py/aUHqZe15VPA
'''
p = MPG123Player('/root/BrainWavePython/music/car_v8.mp3')
p.start()
cnt = 0
while True:
        print 'playing:', p.playing, 'cur_seconds:', p.cur_seconds, p.total_seconds
        if cnt > 100:
                break
        if p.playing is False:
                p.play('/root/BrainWavePython/music/lead1/D4 16Bit.mp3')
        cnt += 1
        sleep(0.1)
p.quitAll()
'''
import threading
from subprocess import Popen, PIPE
from threading import Thread

class MPG123Player(Thread):

    def __init__(self, music=''):
        self.music = music
        Thread.__init__(self)
        self._kill_me = False
        self.playing = None
        self.cur_seconds = 0
        self.total_seconds = 0
        self.player = self.init_player()

    def finish_it(self):
        self._kill_me = True
        self.playing = False

    def init_player(self):
        return Popen(['mpg123', '-R', self.music], shell=False, stdout=PIPE, stdin=PIPE)

    def run(self):
        '''Thread method that is called when a Thread is started,
        this is the "main loop" of it'''
        try:
            print("loop")
            self.player_loop()
        finally:
            self.quit()

    def play(self, music=''):
        music = music or self.music
        if music:
            cmd = 'LOAD ' + music
            self.player_cmd(cmd)
            self.playing = True

    def stop(self):
        self.player_cmd('STOP')

    def pause(self):
        self.player_cmd('PAUSE')

    def player_cmd(self, cmd):
        self.player.stdin.write(cmd + '\n')

    def quitAll(self):
        self.player_cmd('QUIT')
        self.finish_it()
        self.player.terminate()

    def quit(self):
        self.player.terminate()

    def player_loop(self):
        player = self.player

        self.play()

        while not self._kill_me:
            status = player.stdout.readline()
            '''here we have to keep reading the stdout, because if we don't
            read from it this buffer get full and the mpg123 stops working.
            '''
            #print status
            if status.startswith('@F'):
                cmd_name, cur_frame,  frames_left, cur_seconds, seconds_left = status.split()
                if cmd_name == '@F' and cur_seconds == '0.00':
                    self.total_seconds = float(seconds_left)
                cur_seconds = float(cur_seconds)
                self.cur_seconds = cur_seconds
            if status.startswith('@P 0'):
                self.playing = False
