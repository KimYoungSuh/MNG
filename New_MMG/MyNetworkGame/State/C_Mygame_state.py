import os
import platform


import State.C_Game_framework
from State import C_title_state
import pico2d

if platform.architecture()[0] == '32bit':
    os.environ["PYSDL2_DLL_PATH"] = "./SDL2/x86"
else:
    os.environ["PYSDL2_DLL_PATH"] = "./SDL2/x64"

pico2d.open_canvas(1200,900)
State.C_Game_framework.run(C_title_state)
pico2d.close_canvas()