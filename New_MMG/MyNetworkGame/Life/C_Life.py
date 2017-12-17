import random
from pico2d import *
from Background.C_BG import BackGround

class Life:
#
    image = None
    def __init__(self, LIFE, P_NUM):
        self.life = LIFE
        self.num = P_NUM +1
        if Life.image == None:
            Life.image = load_image('Resource\Image_Life.png')

    def update(self,frame_time, PL_X, PL_Y):
        pass
        #self.delete_object(_Bullet)

    def draw(self):
        for i in range(0,self.life) :
            self.image.draw((self.num *200)+40 *i,50)




