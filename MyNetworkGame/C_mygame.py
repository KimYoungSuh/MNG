import os
import platform


import C_game_framework
from State import C_Start_state
import pico2d

pico2d.open_canvas(1200,900)
C_game_framework.run(C_Start_state)
pico2d.close_canvas()