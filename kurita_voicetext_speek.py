# -*- coding: utf-8 -*#
import socket
import sys
import subprocess
import requests
import time
import pandas as pd

#復唱のため
import re
import urllib2
import json
#ソーシャルコメントのため
import datetime
import s1_quick, s2
import random

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import threading
import multiprocessing
import os
from multiprocessing import Value

# voiceTEXT webAPIによるオンライン音声合成 ---------------------++
def voicetext(t,s,p,v):
    url = 'https://api.voicetext.jp/v1/tts'
    key = "6kap37zg1w8coh60:"
    payload={'text':t,
            'speaker':'takeru',     # show, haruka、hikari、takeru、santa、bear
             'speed':s,           # 50から400(%)まで defaultで100
             'pitch':p,           # 50から200(%)まで defaultで100
             'volume':v,          # 50から200(%)まで defaultで100
            #  感情カテゴリは話者 haruka, hikari, takeru, santa, bear にのみ使用可
            #  'emotion':e,         # happiness, anger, sadnessいずれか
            #  'emotion_level':el,  # 1〜4 で強度指定
            # 'format':'mp3',       # defaultでwav
    }
    r = requests.post(url, params=payload, auth=(key, ''))

    # f = open("./wav2hz/voicetext_wav/tmp.wav", 'wb')
    fd
    f.write(r.content)
    f.close()

    # afplay = ['afplay', './wav2hz/voicetext_wav/tmp.wav']
    aplay = ['aplay', './tmp.wav']
    wr = subprocess.Popen(aplay)

# 四朗くん初期値をグローバル変数として宣言
speed = 100
pitch = 100
volume = 150

# もりあがりデモの際はこのコメントアウトを外してサーバ化->クライアント接続と同時に発話を開始

# メインプログラム: ただ喋らせるだけ 
def main():
    speechText = sys.argv[1]
    voicetext(speechText,speed,pitch,volume)

# 実行
main()
