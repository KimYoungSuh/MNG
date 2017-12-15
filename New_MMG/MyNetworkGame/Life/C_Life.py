import random
from pico2d import *
from Background.C_BG import BackGround

class Life:
#
    image = None
    def __init__(self, playerlife):
        global _Bg
        _Bg = BackGround()
        self.Now = playerlife
        if Life.image == None:
            Life.image = load_image('..\Resource\Image_Life.png')

    def update(self,frame_time, PL_X, PL_Y):
        self.Whattime += frame_time
        self.speed = Life.RUN_SPEED_PPS * frame_time
        self.x += self.speed * self.xdir
        self.y += self.speed * self.ydir
        #self.delete_object(_Bullet)

    def draw(self, pl_life):
        for i in range(0,pl_life) :
            self.image.draw(200+40 *i,200)




