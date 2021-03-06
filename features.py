from app import clear_lights, return_colors, parse_multi_colors
import time
import sys
import math
import pigpio, time
#import alsaaudio, audioop
from struct import *
import numpy as np
from math import *

card = 'sysdefault:CARD=Microphone'
#inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK,device="hw:1") #'sysdefault:CARD=1')
#inp.setchannels(0)
#inp.setrate(8000)
#inp.setrate(16000)
#inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
#inp.setperiodsize(160)
max_value = 0

pi = pigpio.pi()

def convert(color):
    color['green'] *= 200/255
    color['blue'] *= 150/255
    return color

colors = return_colors()

def get_lit(color):
    color_dict = colors[color]
    pi.set_PWM_dutycycle(23, color_dict['red'])
    pi.set_PWM_dutycycle(24, color_dict['green'])
    pi.set_PWM_dutycycle(25, color_dict['blue'])

def get_lit_more(color, percent):
    color_dict = colors[color]
    pi.set_PWM_dutycycle(23, color_dict['red']*percent)
    pi.set_PWM_dutycycle(24, color_dict['green']*percent)
    pi.set_PWM_dutycycle(25, color_dict['blue']*percent)

def flash(color, hi_time, lo_time):
    hi_time = float(hi_time)
    lo_time = float(lo_time)
    while True:
        get_lit(color)
        time.sleep(hi_time/1000)
        clear_lights()
        time.sleep(lo_time/1000)

def breathe(color, length, lo_time):
    length = float(length)
    lo_time = float(lo_time)
    while True:
        counter = 0
        while counter < 100:
            counter += 1
            get_lit_more(color, math.sin(math.pi*counter/100))
            time.sleep(length/100000)
        time.sleep(lo_time/1000)

# Colors is a LIST of color
def multi_on(colors, length):
    i = 0
    n = len(colors)
    while True:
        get_lit(colors[i])
        i = (i + 1) % n
        time.sleep(float(length)/1000)

def multi_flash(colors, hi_time, lo_time):
    hi_time = float(hi_time)
    lo_time = float(lo_time)
    i = 0
    n = len(colors)
    while True:
        get_lit(colors[i])
        time.sleep(hi_time/1000)
        clear_lights()
        time.sleep(lo_time/1000)
        i = (i + 1) % n

def multi_breathe(colors, length, lo_time):
    length = float(length)
    lo_time = float(lo_time)
    n = len(colors)
    i = 0
    while True:
        counter = 0
        while counter < 100:
            counter += 1
            get_lit_more(colors[i], math.sin(math.pi*counter/100))
            time.sleep(length/100000)
        i = (i + 1) % n
        time.sleep(lo_time/1000)

def sound():
    return
    t = 0.001
    tau = 0.0005
    last_val = [0, 0, 0]
    while True:
        l,data = inp.read()
        samples = np.absolute(np.fromstring(data, dtype=np.int16))
        # print(samples)
        # b_samp = list(filter(lambda a: 100 < a < 200, samples))
        # c_samp = list(filter(lambda a: 50 < a < 100, samples))
        if l:
            a = audioop.max(data, 2) # - 100
            # a = exp_fn(last_val[0], a, t, tau)
            # last_val[0] = a
            # print(a)
            if a == 0 and last_val[0] == 0 or a > 0:
                get_lit_more('white', min(1, a/10000))
            last_val[0] = a
            #if len(b_samp) > 0 and len(c_samp) > 0:
            #    b = np.mean(b_samp) - 100
            #    b = exp_fn(last_val[1], a, t, tau)
            #    last_val[1] = b
            #    c = np.mean(c_samp) - 50
            #    c = exp_fn(last_val[2], a, t, tau)
            #    last_val[2] = c
            #    print(b, c)
            #    pi.set_PWM_dutycycle(24, min(255, b * 255/50))
            #    pi.set_PWM_dutycycle(25, min(255, c * 255/50))
        time.sleep(t)

def exp_fn(prev, curr, t, tau):
    return curr + (prev - curr)*exp(-t/tau)

if __name__ == '__main__':
    func = sys.argv[1]
    if func == 'flash':
        flash(sys.argv[2], sys.argv[3], sys.argv[4])
    elif func == 'breathe':
        breathe(sys.argv[2], sys.argv[3], sys.argv[4])
    elif func == 'multi':
        multi_type = sys.argv[2]
        if multi_type == 'breathe':
            multi_breathe(parse_multi_colors(sys.argv[3]), sys.argv[4], sys.argv[5])
        elif multi_type == 'on':
            multi_on(parse_multi_colors(sys.argv[3]), sys.argv[4])
        elif multi_type == 'flash':
            multi_flash(parse_multi_colors(sys.argv[3]), sys.argv[4], sys.argv[5])
    elif func == 'sound':
        sound()
