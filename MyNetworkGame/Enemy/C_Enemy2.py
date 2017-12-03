import random
from pico2d import *
from Bullet.C_EnemyBullet import EBullet

_Bullet = []

class Enemy2:

    image = None

    #_enemy2 = []

    def __init__(self, X, Y,BG_X, BG_Y):
        global font

        self.x, self.y = X , Y


        self.sx = self.x - BG_X
        self.sy = self.y - BG_Y

        '''
            if self.xdir > self.ydir:
            if self.xdir > 0:
                self.state = 1
            else:
                self.state = 2
        else:
            if self.ydir > 0:
                self.state = 0
            else:
                self.state = 3
        '''
        if Enemy2.image == None:
            Enemy2.image = load_image('..\Enemy\Image_Enermy2.png')
       # Enemy2._enemy2.append(self)
   # def get_list():
   #     return (Enemy2._enemy2)
    def returnDir(self, x,y):
        pass

    def update(self, frame_time, PL_X, PL_Y, _BG_X, _BG_Y):
        if self.x > 3200:
            self.x = 3200
            self.xdir *= -1
        if self.x < 0:
            self.x = 0
            self.xdir *= -1
        if self.y > 1800:
            self.y = 1800
            self.ydir *= -1
        if self.y < 0:
            self.y = 0
            self.ydir *= -1
        self.Whattime +=frame_time
        if self.xdir > self.ydir:
            if self.xdir > 0:
                self.state = 1
            else:
                self.state = 2
        else:
            if self.ydir > 0:
                self.state = 0
            else:
                self.state = 3
        self.sx = self.x - _BG_X
        self.sy = self.y - _BG_Y
    #    self.sx = self.x - PL_X
    #    self.sy = self.y - PL_Y
#
        self.x += self.speed * self.xdir * frame_time
        self.y += self.speed * self.ydir * frame_time

        self.add(PL_X,PL_Y)



        #self.delete_object(_Bullet)


    def add(self,PL_X, PL_Y):
        if self.Whattime >= 2.0:
            EBullet(self.x, self.y, PL_X,PL_Y)
            self.Whattime = 0

    def draw(self,sx,sy):
        Scean_x, Scean_y = 49, 82
        self.image.clip_draw(Scean_x* self.state, 0, Scean_x, Scean_y, sx, sy)
    #    font.draw(self.sx, self.sy, 'X , Y : [%d, %d]' % (self.sx, self.sy))
    #    self.image.clip_draw(Scean_x* self.state, 0, Scean_x, Scean_y, self.sx, self.sy)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())
    def get_bb(self):
        return self.sx-10 , self.sy-10, self.sx+10, self.sy+10

        #return self.sx-10 , self.sy-10, self.sx+10, self.sy+10



def delete_object(objects):
    for object in objects:
        if object.alive == 0:
            objects.remove(object)




