import random

from pico2d import *
from Background.C_BG import BackGround


class PBullet:
    PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
    RUN_SPEED_KMPH = 55  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None
    _pBullet = []

    def __init__(self,Pl_x, Pl_y, Pl_Dir):
        self._Bg = BackGround
        self.shooter = 0

        self.x = Pl_x
        self.y = Pl_y
        if Pl_Dir == 0 :
            self.xdir = 0
            self.ydir = -1
        elif Pl_Dir == 1 :
            self.xdir = 0
            self.ydir = 1
        elif Pl_Dir == 2 :
            self.xdir = -1
            self.ydir = 0
        elif Pl_Dir == 3 :
            self.xdir = 1
            self.ydir = 0
        self.speed = 0
        self.alive =1
        PBullet._pBullet.append(self)
        self.sx = self.x - self._Bg.window_left
        self.sy = self.y - self._Bg.window_bottom

    def update(self,frame_time, PL_X, PL_Y):
        self.speed = PBullet.RUN_SPEED_PPS * frame_time
        self.x += self.speed * self.xdir
        self.y += self.speed * self.ydir

        if self.x >3200 :
            self.alive = 0
        if self.x < 0 :
            self.alive = 0
        if self.y >1800 :
            self.alive = 0
        if self.y <0 :
            self.alive = 0
        self.sx = self.x - self._Bg.window_left
        self.sy = self.y - self._Bg.window_bottom


    def draw(self):
        self.image.draw(self.sx, self.sy)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())
    def get_bb(self):
        return self.sx-15 , self.sy-15, self.sx+15, self.sy+15
    def get_list():
        return (PBullet._pBullet)



