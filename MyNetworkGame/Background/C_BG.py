import random

from pico2d import *
#
class BackGround:
    def __init__(self):
        global font
        font = load_font('..\ENCR10B.TTF')
        self.image = load_image('..\Background\Image_BG.png')
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h
        self.window_left = 0
        self.window_bottom = 0
        #self.list = [(150,200), (200,300)]
        #self.alist = {
        #    'monster' : {'pointXY' : (200,300), 'size' : (100,100) },
        #    'bullet' : {'pointXY' : (200,300)}
        #}
        #alist['monster']['pointXY']


    def update(self,frame_time, player):
        self.window_left = int(player[0]) - self.canvas_width//2
        if self.window_left <=0 :
            self.window_left = 0
        elif self.window_left > self.image.w - self.canvas_width:
            self.window_left = self.image.w - self.canvas_width

        self.window_bottom =int(player[1]) - self.canvas_height // 2
        if self.window_bottom <= 0:
            self.window_bottom = 0
        elif self.window_bottom > self.image.h - self.canvas_height:
            self.window_bottom = self.image.h - self.canvas_height
    def draw(self):

        self.image.clip_draw_to_origin(self.window_left,self.window_bottom,
                                      self.canvas_width,self.canvas_height,
                                      0,0)
