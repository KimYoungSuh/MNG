import os
import platform

if platform.architecture()[0] == '32bit':
    os.environ["PYSDL2_DLL_PATH"] = "./SDL2/x86"
else:
    os.environ["PYSDL2_DLL_PATH"] = "./SDL2/x64"


import State.C_Game_framework
from State import C_start_state
from State import C_collision
import pico2d
#
pico2d.open_canvas(800,600)
State.C_Game_framework.run(C_collision)
pico2d.close_canvas()