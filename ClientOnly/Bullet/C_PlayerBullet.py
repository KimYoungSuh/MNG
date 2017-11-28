import random

from pico2d import *


class PBullet:
    PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
    RUN_SPEED_KMPH = 25  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None
    _pBullet = []

    def __init__(self,Pl_x, Pl_y, Pl_xdir, Pl_ydir):
        self.x = Pl_x
        self.y = Pl_y
        self.xdir = Pl_xdir
        self.ydir = Pl_ydir
        self.speed = 0
        self.alive =1
        PBullet._pBullet.append(self)


        if PBullet.image == None:
            PBullet.image = load_image('..\Bullet\Image_PBullet.png')

    def update(self,frame_time):
        self.speed = PBullet.RUN_SPEED_PPS * frame_time
        self.x += self.speed * self.xdir
        self.y += self.speed * self.ydir
        if self.x >3500 :
            self.alive = 0
        if self.x < 0 :
            self.alive = 0
        if self.y >900 :
            self.alive = 0
        if self.y <0:
            self.alive = 0



    def draw(self):
        self.image.draw(self.x, self.y)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())
    def get_bb(self):
        return self.x-10 , self.y-10, self.x+10, self.y+10
    def get_list():
        return (PBullet._pBullet)


