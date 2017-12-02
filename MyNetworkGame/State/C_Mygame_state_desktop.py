import os
import platform


from State import C_Game_framework
from State import C_start_state
import pico2d
#
pico2d.open_canvas(1200,900)
State.C_Game_framework.run(C_start_state)
pico2d.close_canvas()