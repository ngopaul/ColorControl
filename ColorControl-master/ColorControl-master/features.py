from . import app
import time
import sys

def flash(color, hi_time, lo_time):
    while True:
        app.get_lit(color_dict)
        time.sleep(hi_time/1000)
        app.clear_lights()
        time.sleep(lo_time/1000)

if __name__ == '__main__':
    flash(sys.argv[1], sys.argv[2], sys.argv[3])