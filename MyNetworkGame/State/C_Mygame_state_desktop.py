import os
import platform


import State.C_Game_framework
from State import C_start_state
from State import C_title_state
from State import C_collision
import pico2d
#
pico2d.open_canvas(1200,900)
State.C_Game_framework.run(C_collision)
pico2d.close_canvas()