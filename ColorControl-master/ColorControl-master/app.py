from flask import Flask, render_template, request
from . import commands
import RPi.GPIO as GPIO
import pigpio
import subprocess
import sys

pi = pigpio.pi()

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

pins = {
   23 : {'name' : 'Red', 'state' : GPIO.LOW}, 
   24 : {'name' : 'Green', 'state' : GPIO.LOW},
   25 : {'name' : 'Blue', 'state' : GPIO.LOW}
}

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

frequency = 70

clear_lights()

def convert(color):
    color['green'] *= 200/255
    color['blue'] *= 150/255
    return color

colors = {
    # White (255. 200, 150)
    'white': {'red': 255.0, 'green': 200.0, 'blue': 150.0},

    # Red (255, 0, 0)
    'red' : convert({'red': 255.0, 'green': 0.0, 'blue': 0.0}), 

    # Yellow (255, 255, 0)
    'yellow' : convert({'red': 255.0, 'green': 255.0, 'blue': 0.0}), 

    # Orange (255. 87, 51)
    'orange' : convert({'red': 255.0, 'green': 87.0, 'blue': 51.0}),

    # Green (0, 255, 0)
    'green' : convert({'red': 0.0, 'green': 255.0, 'blue': 0.0}),

    # Aqua (0, 255, 255)
    'aqua' : convert({'red': 0.0, 'green': 255.0, 'blue': 255.0}),

    # Blue (0, 0, 255)
    'blue' : convert({'red': 0.0, 'green': 0.0, 'blue': 255.0}),

    # Pink (255, 0, 255)
    'pink' : convert({'red': 255.0, 'green': 0.0, 'blue': 255.0}),

    # Purple/Violet (128, 0, 128)
    'purple' : convert({'red': 128.0, 'green': 0.0, 'blue': 128.0}),

    # Navy (0, 0, 128)
    'navy' : convert({'red': 0.0, 'green': 0.0, 'blue': 128.0}),
}

# Goal: Web Requests will initiate GPIO methods
@app.route("/", methods=['GET', 'POST'])
def main():
   return render_template('main.html')

@app.route('/on/<color>', methods=['GET', 'POST'])
def on(color):
    clear_lights()
    print(color)
    color = color.lower()
    pi.set_PWM_dutycycle(23, 0)
    pi.set_PWM_dutycycle(24, 0)
    pi.set_PWM_dutycycle(25, 0)
    if color in colors:
        get_lit(colors[color])
    return render_template('main.html')

@app.route('/flash/<color>/<hi_time>/<lo_time>', methods=['GET', 'POST'])
def flash(color, hi_time, lo_time):
    if not color in colors:
        return
    hi_time = int(hi_time)
    lo_time = int(lo_time)
    clear_lights()
    return render_template('main.html')

@app.route('/off/', methods=['GET', 'POST'])
def off():
    print('Turning off the lights')
    clear_lights()
    pi.set_PWM_dutycycle(23, 0)
    pi.set_PWM_dutycycle(24, 0)
    pi.set_PWM_dutycycle(25, 0)
    return render_template('main.html')

def clear_lights():
    pi.wave_clear()
    pi.set_mode(23, pigpio.OUTPUT)
    pi.set_mode(24, pigpio.OUTPUT)
    pi.set_mode(25, pigpio.OUTPUT)

    pi.set_PWM_frequency(23, frequency)
    pi.set_PWM_frequency(24, frequency)
    pi.set_PWM_frequency(25, frequency)

    pi.set_PWM_dutycycle(23, 0)
    pi.set_PWM_dutycycle(24, 0)
    pi.set_PWM_dutycycle(25, 0)

def get_lit(color_dict):
    pi.set_PWM_dutycycle(23, color_dict['red'])
    pi.set_PWM_dutycycle(24, color_dict['green'])
    pi.set_PWM_dutycycle(25, color_dict['blue'])

def custom_pwm(pin, duty, length):
    print(length-2650)
    toReturn = [pigpio.pulse(1<<pin, 0, duty*10), pigpio.pulse(0, 1<<pin, 2560 - duty*10)] * max(length - 2560, 1)
    return toReturn

if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True)

   
