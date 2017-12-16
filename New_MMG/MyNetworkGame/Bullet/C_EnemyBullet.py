import random
from Background.C_BG import BackGround
from pico2d import *
class EBullet:
    PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
    RUN_SPEED_KMPH = 15  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    image = None
    _eBullet = []
    def __init__(self,_X, _Y):
        self.shooter = 1
        self._Bg = BackGround
        self.x = _X
        self.y = _Y
    #    self.sx = self.x - PL_X
    #    self.sy = self.y - PL_Y
        self.alive =1
        EBullet._eBullet.append(self)

        if EBullet.image == None:
            EBullet.image = load_image('Resource\Image_EBullet.png')
        self.sx = self.x - self._Bg.window_left
        self.sy = self.y - self._Bg.window_bottom

    def update(self):
        self.sx = self.x - self._Bg.window_left
        self.sy = self.y - self._Bg.window_bottom
    #    self.sx = self.x - PL_X
    #    self.sy = self.y - PL_Y
#
    #    if collide(self.x, self.y, self.x+10, self.y+10, PL_X, PL_Y, PL_X+10, PL_Y+10) :
    #        self.alive = 0

        #need collsion check

    def draw(self):
        self.image.draw(self.sx, self.sy)
#        self.image.draw(self.sx, self.sy)
    def draw_bb(self):
        draw_rectangle(*self.get_bb())
    def get_bb(self):
        return self.sx - 10, self.sy - 10, self.sx + 10, self.sy + 10
        #return self.sx-10 , self.sy-10, self.sx+10, self.sy+10
    def get_list():
        return (EBullet._eBullet)

def collide(left_a, bottom_a,right_a, top_a, left_b, bottom_b,right_b, top_b):

    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False

    return True
