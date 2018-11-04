from flask import Flask, render_template, request
import time
import RPi.GPIO as GPIO
import pigpio
import os
import subprocess
import re

pi = pigpio.pi()

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

frequency = 70
need_to_kill = False
PID = ""
current_color = ""
current_feature = ""
current_times = [0, 0]

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

    # Light Blue
    'lightblue': {'red': 0.0, 'green': 0.0, 'blue': 255.0},
}

def return_colors():
    return colors

@app.route("/", methods=['GET', 'POST'])
def main():
   if request.method == "POST":
       color = request.values.get('color')
       off = request.values.get('off')
       if color:
           get_lit(color)
       if off:
           clear_lights()
   return render_template('main.html')

@app.route('/on/<color>', methods=['GET', 'POST'])
def on(color):
    clear_lights()
    color = color.lower()
    if color in colors:
        get_lit(color)
        global current_color, current_feature
        current_color = color
        current_feature = "on"
    return render_template('main.html')

@app.route('/off/', methods=['GET', 'POST'])
def off():
    clear_lights()
    return render_template('main.html')

@app.route('/flash/<color>/<hi_time>/<lo_time>', methods=['GET', 'POST'])
def flash(color, hi_time, lo_time):
    if not color in colors:
        return render_template('main.html')
    flash_fx(color, hi_time, lo_time)
    return render_template('main.html')

def flash_fx(color, hi_time, lo_time):
    if not color in colors:
        return
    global current_color, current_times, current_feature
    current_color = color
    current_times = [hi_time, lo_time]
    current_feature = "flash"
    clear_lights()

    os.system("python3 features.py "+ "flash " + color + " " + hi_time + " " + lo_time + " &")

    y = subprocess.check_output(['pidof', 'python3'])
    print(y)

    global need_to_kill, PID
    need_to_kill = True
    print(PID)
    print(current_color)
    print(current_feature)
    print(current_times)
    PID = str(y).split(' ')[0][2:]

@app.route('/breathe/<color>/<length>/<lo_time>', methods=['GET', 'POST'])
def breathe(color, length, lo_time):
    if not color in colors:
        return render_template('main.html')
    breathe_fx(color, length, lo_time)
    return render_template('main.html')

def breathe_fx(color, length, lo_time):
    print("Color: " + color)
    if not color in colors:
        return
    global current_color, current_times, current_feature
    current_color = color
    current_times = [length, lo_time]
    current_feature = "breathe"
    clear_lights()

    os.system("python3 features.py "+ "breathe " + color + " " + length + " " + lo_time + " &")

    y = subprocess.check_output(['pidof', 'python3'])
    print(y)

    global need_to_kill, PID
    need_to_kill = True
    print(PID)
    print(current_color)
    print(current_feature)
    print(current_times)
    PID = str(y).split(' ')[0][2:]

@app.route('/speedup', methods=['GET', 'POST'])
def speedup():
    if current_feature == "flash":
        print("Speeding up flash.")
        flash_fx(current_color, str((int(current_times[0])*3/4)//1), str((int(current_times[1])*3/4)//1))
    elif current_feature == "breathe":
        print("Speeding up breathe.")
        breathe_fx(current_color, str((int(current_times[0])*3/4)//1), str((int(current_times[1])*3/4)//1))
    return render_template('main.html')

@app.route('/slowdown', methods=['GET', 'POST'])
def slowdown():
    if current_feature == "flash":
        print("Slowing down flash.")
        flash_fx(current_color, str((int(current_times[0])*4/3)//1), str((int(current_times[1])*4/3)//1))
    elif current_feature == "breathe":
        print("Slowing down breathe.")
        breathe_fx(current_color, str((int(current_times[0])*4/3)//1), str((int(current_times[1])*4/3)//1))
    return render_template('main.html')
    

def get_lit(color):
    color_dict = colors[color]
    pi.set_PWM_dutycycle(23, color_dict['red'])
    pi.set_PWM_dutycycle(24, color_dict['green'])
    pi.set_PWM_dutycycle(25, color_dict['blue'])
    
def clear_lights():
    global need_to_kill, current_color
    
    if need_to_kill:
        os.system("kill " + PID)
        need_to_kill = False
        
    current_color = ""
    
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
    
def custom_pwm(pin, duty, length):
    print(length - 2650)
    pulses = [pigpio.pulse(1<<pin, 0, duty*10), pigpio.pulse(0, 1<<pin, 2560 - duty*10)] * max(length - 2560, 1)
    return pulses

if __name__ == "__main__":
   clear_lights()
   app.run(host='0.0.0.0', debug=True)
