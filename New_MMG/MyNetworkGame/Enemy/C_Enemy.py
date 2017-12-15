import random
import time
from pico2d import *
from Bullet.C_EnemyBullet import EBullet
_Bullet = []
class Enemy1:
    image =None
    def __init__(self, X, Y, State, BG_X, BG_Y):
        global font

        self.x, self.y = X , Y


        self.sx = self.x - BG_X
        self.sy = self.y - BG_Y
        self.state =State
        if Enemy1.image == None:
            Enemy1.image = load_image('..\Resource\Image_Enermy.png')
        #Enemy1._enemy.append(self)
    def returnx(self):
        return self.x
    def returny(self) :
        return self.y

    def update(self,frame_time, PL_X, PL_Y, _BG_X , _BG_Y,State):
        self.sx = self.x - _BG_X
        self.sy = self.y - _BG_Y


        #self.delete_object(_Bullet)

    #def get_list():
    #    return (Enemy1._enemy)



    def draw(self):

        self.image.draw(self.sx, self.sy)
        #font.draw(self.sx, self.sy+20 , 'X , Y : [%d, %d]' % (self.sx, self.sy))
        #font.draw(self.sx, self.sy, 'X , Y : [%d, %d]' % (self.x, self.y))

        #self.image.draw(self.sx , self.sy)
    def draw_bb(self):
        draw_rectangle(*self.get_bb())
    def get_bb(self):
        return self.sx-10 , self.sy-10, self.sx+10, self.sy+10

        #return self.sx - 10, self.sy - 10, self.sx + 10, self.sy + 10


def delete_object(objects):
    for object in objects:
        if object.alive == 0:
            objects.remove(object)




