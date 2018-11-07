from flask import Flask, render_template, request, jsonify
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

pins = [23, 24, 25]
frequency = 70
need_to_kill = False
PID = ""
last_command = ""
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
    global current_color, current_times, last_command, current_feature
    if request.method == "POST":
        info = request.values.get('info')
        times = request.values.get('times')
        array = request.values.get('array')
        print("recieved POST.", "info=", info, "times=", times, "array=", array)
        if info == 'off':
            last_command = 'off'
            clear_lights()
        elif info == 'on':
            execute_prev()
        elif info == 'flash':
            # toggle
            current_times = times.split(",")
            print(current_times)
            if current_feature == 'flash':
                last_command = 'on'
                current_feature = 'on'
                get_lit_safe(current_color)
            else:
                if current_color == "":
                    current_color = 'white'
                flash_fx(current_color, current_times[0], current_times[1])
        elif info == 'breathe':
            # toggle
            current_times = times.split(",")
            if current_feature == 'breathe':
                last_command = 'on'
                current_feature = 'on'
                get_lit_safe(current_color)
            else:
                breathe_fx(current_color, current_times[0], current_times[1])
        elif info == 'multi breathe':
            current_times = times.split(",")
            multi_fx("breathe", comma_separate(array), current_times[0], current_times[1])
        elif info == 'multi flash':
            current_times = times.split(",")
            multi_fx("flash", comma_separate(array), current_times[0], current_times[1])
        elif info == 'multi on':
            current_times = times.split(",")
            multi_fx("on", comma_separate(array), current_times[0], current_times[1])
        elif info in colors:
            if last_command == 'off' or last_command == '':
                last_command = 'on'
                current_feature = 'on'
                print("Turning the lights back on: color= " + info)
                current_color = info
                get_lit_safe(info)
            else:
                current_color = info
                execute_prev()
    return render_template('main.html')

@app.route('/status', methods = ['POST'])
def ajax_request():
    return jsonify(currentState= 'off' if last_command == 'off' else current_feature, currentColor= current_color, currentTimes= current_times)

def comma_separate(times):
    temp = repr(times).split(',')
    for i in range(len(temp)):
        temp[i] = temp[i].replace('\'', '')
        temp[i] = temp[i].replace('[', '')
        temp[i] = temp[i].replace(']', '')
    toreturn = ""
    for item in temp:
        toreturn = toreturn + item + ","
    return toreturn[:-1]

@app.route('/on/<color>', methods=['GET', 'POST'])
def on(color):
    color = color.lower()
    if color in colors:
        get_lit_safe(color)
        global current_color, current_feature, last_command
        current_color = color
        current_feature = "on"
        last_command = "on"
    return render_template('main.html')

@app.route('/off/', methods=['GET', 'POST'])
def off():
    global last_command
    last_command = "off"
    clear_lights()
    return render_template('main.html')

@app.route('/flash/<color>/<hi_time>/<lo_time>', methods=['GET', 'POST'])
def flash(color, hi_time, lo_time):
    color = color.lower()
    if not color in colors:
        return render_template('main.html')
    flash_fx(color, hi_time, lo_time)
    return render_template('main.html')

def flash_fx(color, hi_time, lo_time):
    print("Flashing lights " + color + ", times: " + hi_time, lo_time)
    color = color.lower()
    if not color in colors:
        return
    global current_color, current_times, current_feature, last_command, need_to_kill, PID
    last_command = "flash"
    current_color = color
    current_times = [str(float(hi_time)), str(float(lo_time))]
    current_feature = "flash"
    clear_lights()
    os.system("python3 features.py "+ "flash " + color + " " + hi_time + " " + lo_time + " &")
    y = subprocess.check_output(['pidof', 'python3'])
    need_to_kill = True
    PID = str(y).split(' ')[0][2:]
    print(PID)
    print(current_color)
    print(current_feature)
    print(current_times)

@app.route('/breathe/<color>/<hi_time>/<lo_time>', methods=['GET', 'POST'])
def breathe(color, hi_time, lo_time):
    color = color.lower()
    if not color in colors:
        return render_template('main.html')
    breathe_fx(color, hi_time, lo_time)
    return render_template('main.html')

def breathe_fx(color, hi_time, lo_time):
    print("Breathing lights " + color + ", times: " + hi_time, lo_time)
    color = color.lower()
    print("Color: " + color)
    if not color in colors:
        return
    global current_color, current_times, current_feature, last_command, need_to_kill, PID
    last_command = "breathe"
    current_color = color
    current_times = [str(float(hi_time)), str(float(lo_time))]
    current_feature = "breathe"
    clear_lights()
    os.system("python3 features.py "+ "breathe " + color + " " + hi_time + " " + lo_time + " &")
    y = subprocess.check_output(['pidof', 'python3'])
    need_to_kill = True
    PID = str(y).split(' ')[0][2:]
    print(PID)
    print(current_color)
    print(current_feature)
    print(current_times)

@app.route('/multi/<feature>/<colorlist>/<hi_time>')
@app.route('/multi/<feature>/<colorlist>/<hi_time>/<lo_time>')
def multi(feature, colorlist, hi_time, lo_time = ""):
    colorlist2 = parse_multi_colors(colorlist)
    for color in colorlist2:
        if not color in colors:
            return render_template('main.html')
    multi_fx(feature, colorlist, hi_time, lo_time)
    return render_template('main.html')

def multi_fx(feature, colorlist, hi_time, lo_time = ""):
    print("Multi-" + feature + "ing" + colorlist + ", times: " + hi_time, lo_time)
    colorlist2 = parse_multi_colors(colorlist)
    for color in colorlist2:
        if not color in colors:
            return
    global current_color, current_times, current_feature, last_command
    current_color = colorlist
    try:
        current_times = [str(float(hi_time)), str(float(lo_time))]
    except:
        current_times = [str(float(hi_time)), "0"]

    if feature == '23':
        feature = 'on'
    elif feature == '24':
        feature = 'flash'
    elif feature == '25':
        feature = 'breathe'

    if feature == 'on':
        lo_time = ""

    current_feature = "multi " + feature
    clear_lights()

    colorlist = colorlist.replace(' ', ',')

    last_command = "multi " + feature
    os.system("python3 features.py "+ "multi " + feature + " " + colorlist + " " + hi_time + " " + lo_time + " &")

    y = subprocess.check_output(['pidof', 'python3'])
    print(y)

    global need_to_kill, PID
    need_to_kill = True
    PID = str(y).split(' ')[0][2:]
    print(PID)
    print(current_color)
    print(current_feature)
    print(current_times)

def parse_multi_colors(colors):
    if "," in colors:
        temp = colors.split(',')
        for i in range(len(temp)):
            temp[i] = temp[i].lower()
        return temp
    else:
        temp = colors.split(' ')
        for i in range(len(temp)):
            temp[i] = temp[i].lower()
        return temp

def multi_space_to_comma(colors):
    return colors.replace(' ', ',')
    
def execute_prev():
    print("Executing previous: " + current_feature)
    if current_feature == 'on':
        get_lit_safe(current_color)
    elif current_feature == 'flash':
        flash_fx(current_color, current_times[0], current_times[1])
    elif current_feature == 'breathe':
        breathe_fx(current_color, current_times[0], current_times[1])
    elif current_feature == 'multi on':
        multi_fx('on', current_color, current_times[0], current_times[1])
    elif current_feature == 'multi flash':
        multi_fx('flash', current_color, current_times[0], current_times[1])
    elif current_feature == 'multi breathe':
        multi_fx('breathe', current_color, current_times[0], current_times[1])

@app.route('/speedup', methods=['GET', 'POST'])
def speedup():
    if current_feature == "flash":
        print("Speeding up flash.")
        if float(current_times[0])-30 > 0 and float(current_times[1])-30 > 0:
            flash_fx(current_color, str((float(current_times[0])-30)), str((float(current_times[1])-30)))
        else:
            print("Cannot speed up anymore.")
    elif current_feature == "breathe":
        print("Speeding up breathe.")
        if float(current_times[0])-30 > 0 and float(current_times[1])-30 > 0:
            breathe_fx(current_color, str((float(current_times[0])-30)), str((float(current_times[1])-30)))
        else:
            print("Cannot speed up anymore.")
    elif "multi" in current_feature:
        if "on" in current_feature:
            if float(current_times[0])-30 > 0:
                multi_fx("on", current_color, str((float(current_times[0])-30)))
        elif "flash" in current_feature:
            if float(current_times[0])-30 > 0 and float(current_times[1])-30 > 0:
                multi_fx("flash", current_color, str((float(current_times[0])-30)), str((float(current_times[1])-30)))
        else:
            if float(current_times[0])-30 > 0 and float(current_times[1])-30 > 0:
                multi_fx("breathe", current_color, str((float(current_times[0])-30)), str((float(current_times[1])-30)))
    return render_template('main.html')

@app.route('/slowdown', methods=['GET', 'POST'])
def slowdown():
    if current_feature == "flash":
        print("Slowing down flash.")
        flash_fx(current_color, str(float(current_times[0])+30), str(float(current_times[1])+30))
    elif current_feature == "breathe":
        print("Slowing down breathe.")
        breathe_fx(current_color, str(float(current_times[0])+30), str(float(current_times[1])+30))
    elif "multi" in current_feature:
        if "on" in current_feature:
            multi_fx("on", current_color, str(float(current_times[0])+30))
        elif "flash" in current_feature:
            multi_fx("flash", current_color, str(float(current_times[0])+30), str(float(current_times[1])+30))
        else:
            multi_fx("breathe", current_color, str(float(current_times[0])+30), str(float(current_times[1])+30))
    return render_template('main.html')

@app.route('/sound', methods=['GET', 'POST'])
def sound():
    sound_fx()
    return render_template('main.html')

def sound_fx():
    global current_feature, last_command, need_to_kill, PID
    current_feature = "sound"
    last_command = "sound"
    clear_lights()
    os.system("python3 features.py "+ "sound " + "&")
    y = subprocess.check_output(['pidof', 'python3'])
    need_to_kill = True
    PID = str(y).split(' ')[0][2:]
    print(PID)
    print(current_feature)

def get_lit(color):
    color_dict = colors[color]
    pi.set_PWM_dutycycle(23, color_dict['red'])
    pi.set_PWM_dutycycle(24, color_dict['green'])
    pi.set_PWM_dutycycle(25, color_dict['blue'])

def get_lit_safe(color):
    clear_lights()
    color_dict = colors[color]
    pi.set_PWM_dutycycle(23, color_dict['red'])
    pi.set_PWM_dutycycle(24, color_dict['green'])
    pi.set_PWM_dutycycle(25, color_dict['blue'])
    
def clear_lights():
    global need_to_kill
    if need_to_kill:
        os.system("kill " + PID)
        need_to_kill = False
    pi.wave_clear()
    for pin in pins:
        pi.set_mode(pin, pigpio.OUTPUT)
        pi.set_PWM_frequency(pin, frequency)
        pi.set_PWM_dutycycle(pin, 0)

if __name__ == "__main__":
   clear_lights()
   app.run(host='0.0.0.0', debug=True)
