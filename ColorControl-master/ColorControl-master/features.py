from . import commands
from . import app
import time

def flash(color_dict):
    while True:
        commands.get_lit(color_dict)
        time.sleep(hi_time/1000)
        commands.clear_lights()
        time.sleep(lo_time/1000)

if __name__ == '__main__':
