import os
import platform

if platform.architecture()[0] == '32bit':
    os.environ["PYSDL2_DLL_PATH"] = "./SDL2/x86"
else:
    os.environ["PYSDL2_DLL_PATH"] = "./SDL2/x64"


import State.C_Game_framework
import State.C_Start_state
import pico2d
#
pico2d.open_canvas(1200,900)
State.C_Game_framework.run(State.C_Start_state)
pico2d.close_canvas()