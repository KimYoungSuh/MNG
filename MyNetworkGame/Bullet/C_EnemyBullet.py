import random

from pico2d import *

class EBullet:
    PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
    RUN_SPEED_KMPH = 1  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    image = None

    def __init__(self,Pl_x, Pl_y, PL_X, PL_Y):
        self.x = Pl_x
        self.y = Pl_y
        self.xdir = math.cos(math.atan((PL_Y - self.y) / (PL_X - self.x)))
        self.ydir = math.sin(math.atan((PL_Y - self.y) / (PL_X - self.x)))
        self.speed = 0
        self.alive =1


        if EBullet.image == None:
            EBullet.image = load_image('Bullet\Image_EBullet.png')

    def update(self,frame_time, PL_X, PL_Y):
        self.speed = EBullet.RUN_SPEED_PPS * frame_time
        self.x += self.speed * self.xdir
        self.y += self.speed * self.ydir
        if self.x >3500 :
            self.alive = 0
        if self.x < 0 :
            self.alive = 0
        if self.y >900 :
            self.alive = 0
        if self.y <0 :
            self.alive = 0
#
        if collide(self.x, self.y, self.x+10, self.y+10, PL_X, PL_Y, PL_X+10, PL_Y+10) :
            self.alive = 0

        #need collsion check

    def draw(self):
        self.image.draw(self.x, self.y)
    def draw_bb(self):
        draw_rectangle(*self.get_bb())
    def get_bb(self):
        return self.x-10 , self.y-10, self.x+10, self.y+10


def collide(left_a, bottom_a,right_a, top_a, left_b, bottom_b,right_b, top_b):

    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False

    return True
