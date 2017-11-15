import os
import platform


import C_game_framework
from State import C_start_state
import pico2d

pico2d.open_canvas(1200,900)
C_game_framework.run(C_start_state)
pico2d.close_canvas()