import random

from pico2d import *

from Bullet.C_EnemyBullet import Bullet
_Bullet = []

class Enemy1:
    PIXEL_PER_METER = (6.0 / 0.3)  # 10 pixel 30 cm
    RUN_SPEED_KMPH = random.randint(4,30)  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 3
    image = None

    def __init__(self, Pl_x, Pl_y):

        rand = random.randint(0, 4)
        self.x, self.y = random.randint(0, 3500), random.randint(0, 50)
        self.speed = 0
        self.Whattime = 0
        self.alive = 1
        self.xdir =  (Pl_x - self.x) /(Pl_y - self.y)
        self.ydir = (Pl_y - self.y)/ (Pl_x - self.x)
        if Enemy1.image == None:
            Enemy1.image = load_image('squirrel.png')

    def returnDir(self, x,y):
        pass


    def update(self,frame_time):
        self.Whattime += frame_time
        self.speed = Enemy1.RUN_SPEED_PPS * frame_time
        self.x += self.xdir * self.speed
        self.y += self.ydir * self.speed
        for bullets in _Bullet:
            bullets.update(frame_time)
        self.add()
        if self.x > 3500:
            self.alive =0
        if self.y > 900:
            self.alive =0

    def add(self):
        if self.Whattime >= 1.3:
            _Bullet.append(Bullet(self.x, self.y, self.xdir, self.ydir))
            self.Whattime = 0

    def delete_object(objects):
        for object in objects :
            if object.alive == 0:
                object.remove(object)



    def draw(self):
        self.image.draw(self.x, self.y)
        for bullets in _Bullet:
            bullets.draw()
    def draw_bb(self):
        draw_rectangle(*self.get_bb())
    def get_bb(self):
        return self.x-10 , self.y-10, self.x+10, self.y+10
