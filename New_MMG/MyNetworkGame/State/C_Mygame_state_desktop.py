import os
import platform


from State import C_Game_framework
from State import C_title_state
import pico2d

def start():
    pico2d.open_canvas(1200,900,True)
    C_Game_framework.run(C_title_state)
    pico2d.close_canvas()