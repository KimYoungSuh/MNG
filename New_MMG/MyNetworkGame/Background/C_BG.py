from pico2d import *

class BackGround:

    def __init__(self):
        global font
        font = load_font('Resource\ENCR10B.TTF')
        BackGround.image = load_image('Resource\Image_BG.png')
        BackGround.canvas_width = get_canvas_width()
        BackGround.canvas_height = get_canvas_height()
        BackGround.w = BackGround.image.w
        BackGround.h = BackGround.image.h
        BackGround.window_left = 0
        BackGround.window_bottom = 0

    def update(self,frame_time, player):
        BackGround.window_left = int(player[0]) - BackGround.canvas_width//2
        if BackGround.window_left <=0 :
            BackGround.window_left = 0
        elif BackGround.window_left > BackGround.image.w - BackGround.canvas_width:
            BackGround.window_left = BackGround.image.w - BackGround.canvas_width

        BackGround.window_bottom =int(player[1]) - BackGround.canvas_height // 2
        if BackGround.window_bottom <= 0:
            BackGround.window_bottom = 0
        elif BackGround.window_bottom > BackGround.image.h - BackGround.canvas_height:
            BackGround.window_bottom = BackGround.image.h - BackGround.canvas_height
    def draw(self):
        BackGround.image.clip_draw_to_origin(BackGround.window_left,BackGround.window_bottom,
                                      BackGround.canvas_width,BackGround.canvas_height,
                                      0,0)
