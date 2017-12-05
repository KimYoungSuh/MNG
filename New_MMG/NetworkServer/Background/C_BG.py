import random

from pico2d import *
#
class BackGround:

    def __init__(self):
        global font
        BackGround.canvas_width = 1200
        BackGround.canvas_height = 900
        BackGround.w =3200
        BackGround.h =1800
        BackGround.window_left = 0
        BackGround.window_bottom = 0


    def update(self, PX , PY):
        BackGround.window_left = int(PX) - BackGround.canvas_width//2
        if BackGround.window_left <=0 :
            BackGround.window_left = 0
        elif BackGround.window_left > BackGround.w - BackGround.canvas_width:
            BackGround.window_left = BackGround.w - BackGround.canvas_width

        BackGround.window_bottom =int(PY) - BackGround.canvas_height // 2
        if BackGround.window_bottom <= 0:
            BackGround.window_bottom = 0
        elif BackGround.window_bottom > BackGround.h - BackGround.canvas_height:
            BackGround.window_bottom = BackGround.h - BackGround.canvas_height
