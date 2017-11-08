import random

from pico2d import *

class BackGround:
    def __init__(self):
        self.image = load_image('KPU_GROUND.png')
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

    def draw(self):
        self.image.clip_draw_to_origin(self.window_left, self.window_bottom,
                                       self.canvas_width,self.canvas_height,
                                       0,0)

    def update(self,frame_time, pointXY):
        self.window_left = clamp(0,
                                 int(pointXY[0]) - self.canvas_width//2,
                                 self.w - self.canvas_width)
        self.window_bottom = clamp(0,
                                   int(pointXY[1]) - self.canvas_height // 2,
                                 self.h - self.canvas_height)
        print("witch x = %d witch y = %d" % (pointXY[0] , pointXY[1]))
        print("window_left= %d window_bottom = %d" % (self.window_left , self.window_bottom))


