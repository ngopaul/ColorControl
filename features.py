from app import clear_lights, return_colors, get_lit
import time
import sys
import math
import pigpio

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
            time.sleep(length/10000)
        time.sleep(lo_time/100)

# Colors is a LIST of color
def multi_on(colors, length):
    i = 0
    n = len(colors)
    while True:
        get_lit(colors[i])
        i = (i + 1) % n

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
    while True:
        counter = 0
        i = 0
        while counter < 100:
            counter += 1
            get_lit_more(colors[i], math.sin(math.pi*counter/100))
            time.sleep(length/10000)
            i = (i + 1) % n
        time.sleep(lo_time/100)
        

if __name__ == '__main__':
    func = sys.argv[1]
    if func == 'flash':
        flash(sys.argv[2], sys.argv[3], sys.argv[4])
    elif func == 'breathe':
        breathe(sys.argv[2], sys.argv[3], sys.argv[4])
