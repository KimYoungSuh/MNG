import platform
import os

if platform.architecture()[0] == '32bit':
    os.environ["PYSDL2_DLL_PATH"] = "./SDL2/x86"
else:
    os.environ["PYSDL2_DLL_PATH"] = "./SDL2/x64"


import C_game_framework
import C_start_state
import pico2d

pico2d.open_canvas(1200,900)
C_game_framework.run(C_start_state)
pico2d.close_canvas()