import random
from pico2d import *


class Enemy1:

    image = None
    def __init__(self, Pl_x, Pl_y, Enemy_dir):
        self.rand = Enemy_dir

        self.speed = 0
        self.Whattime = 0
        self.alive = 1

        self.xdir =  math.cos(math.atan((Pl_x - self.x)/(Pl_y - self.y)))
        self.ydir = math.sin(math.atan((Pl_x - self.x)/(Pl_y - self.y)))

        if Enemy1.image == None:
            Enemy1.image = load_image('Enemy\Image_Enemy.png')

    def returnDir(self, x,y):
        pass


    def update(self,frame_time, PL_X, PL_Y):
        self.Whattime += frame_time
        self.speed = Enemy1.RUN_SPEED_PPS * frame_time
        self.x += self.speed * self.xdir
        self.y += self.speed * self.ydir
        for bullets in _Bullet:
            bullets.update(frame_time)
        self.add(PL_X,PL_Y)
        if self.x >3500 :
            self.alive = 0
        if self.x < 0 :
            self.alive = 0
        if self.y >900 :
            self.alive = 0
        if self.y <0:
            self.alive = 0


        delete_object(_Bullet)


        #self.delete_object(_Bullet)


    def add(self,PL_X, PL_Y):
        if self.Whattime >= 1.3:
            _Bullet.append(Bullet(self.x, self.y, PL_X,PL_Y))
            self.Whattime = 0



    def draw(self):
        self.image.draw(self.x, self.y)
        for bullets in _Bullet:
            bullets.draw()
        for bullets in _Bullet:
            bullets.draw_bb()
    def draw_bb(self):
        draw_rectangle(*self.get_bb())
    def get_bb(self):
        return self.x-10 , self.y-10, self.x+10, self.y+10


def delete_object(objects):
    for object in objects:
        if object.alive == 0:
            objects.remove(object)


