# -*- coding: utf-8 -*-
# main.py
# 分析 EGG 轉換成聲音

import os
from subprocess import Popen, PIPE
from time import sleep
from random import randrange
from random import random
from player import MPG123Player

ENABLE_MPG123 = False
ENABLE_MPLAYER = False
ENABLE_MPG123PLAYER = True

files = []
p = None
doremi = None

eegArray = ['A3', 'A4', 'B3', 'B4', 'C3', 'C4', 'D3', 'D4', 'E3', 'E4', 'F3', 'F4', 'G3', 'G4']
attentionArray = ['2', '4', '8', '16']

folder = './music/lead'+str(randrange(1,4))+'/'

def mpg3player(music, frame = None):
    if frame is None:
        return Popen(['mpg123', '-q', music], shell=False, stdout=PIPE, stdin=PIPE)
        # return Popen(['mplayer', music], shell=False, stdout=PIPE, stdin=PIPE)
        return
    else:
        return Popen(['mpg123', '-q', '-n', frame, music], shell=False, stdout=PIPE, stdin=PIPE)

def playAll():
    fn = './music/loop '+str(randrange(1,21))+'.mp3'
    # p = mpg3player(fn)
    p = Popen(['mpg123', '-q', '-f', '22768', fn], shell=False, stdout=PIPE, stdin=PIPE)
    print "bg music:", fn
    print "start:", p.pid
    fn = processEGG()
    if ENABLE_MPG123:
        doremi = mpg3player(fn)
    if ENABLE_MPG123PLAYER:
        doremi = MPG123Player(fn)
    doremi.start()
    print "doremi:", fn
    # 檢查背景音是否播完
    while p.poll() is None:
        # 檢查前一個單音是否播完，播完才播下一個
        if ENABLE_MPG123:
            if doremi.poll() is not None:
                # 下一個單音
                fn = processEGG()
                # doremi = mpg3player(fn)
                doremi.play(fn)
                print "doremi:", fn

        if ENABLE_MPG123PLAYER:
            if doremi.playing is False:
                # 下一個單音
                fn = processEGG()
                # doremi = mpg3player(fn)
                doremi.play(fn)
                print "doremi:", fn

        sleep(0.1)

    if ENABLE_MPG123PLAYER:
            doremi.quitAll()
    print "done"

def processEGG():
    [attention, meditation, delta, theta, lowAlpha, heighAlpha, lowBeta, highBeta, lowGamma, highGamma] = getEGGData()
    # lead[1-3] 亂數選
    # folder = './music/lead'+str(randrange(1,4))+'/'
    # Delta, Theta, lowAlpha, heighAlpha, lowBeta, highBeta, lowGamma, highGamma
    # [A[3,4],B[3,4],C[3,4],D[3,4],E[3,4],F[3,4],G[3,4]] 14個音
    # Attention: [2,4,8,18]Bit
    # Attention/25
    bit = attentionArray[int(attention/25)]+'Bit.mp3'
    # bit = '16Bit.mp3'
    filename = folder + eegArray[int(delta/7.2)] + ' ' + bit
    return filename



def getEGGData():
    # [Attention, Meditation, Delta, Theta, lowAlpha, heighAlpha, lowBeta, highBeta, lowGamma, highGamma]
    return [int(100*random()) for i in xrange(10)]

def main():
    playAll()

if __name__ == '__main__':
    main()
