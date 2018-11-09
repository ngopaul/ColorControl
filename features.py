from app import clear_lights, return_colors, parse_multi_colors
import time
import sys
import math
import pigpio, alsaaudio, time, audioop
from struct import *
import numpy as np


card = 'sysdefault:CARD=Microphone'
inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK,device="hw:1") #'sysdefault:CARD=1')
inp.setchannels(0)
inp.setrate(8000)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
inp.setperiodsize(160)
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
    last_val = 0
    while True:
        l,data = inp.read()
        samples = np.fromstring(data, dtype=np.uint16)
        print(samples)
        new_samp = list(filter(lambda a: 700 < a < 1000, samples))
        c_samp = list(filter(lambda a: 400 < a < 700, samples))
        if l:
            a = audioop.max(data, 2)
            if a < last_val:
                a = (a + 2 * last_val)//3
            #get_lit_more('red', min(1, a/1000))
            if len(new_samp) > 0 and len(c_samp) > 0:
                b = np.mean(new_samp) - 700
                c = np.mean(c_samp) - 400
                pi.set_PWM_dutycycle(24, b/300)
                pi.set_PWM_dutycycle(25, c/300)
            last_val = a
        time.sleep(.001)

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
