import random
from pico2d import *
from Bullet.C_EnemyBullet import EBullet
_Bullet = []
font = None
class Enemy1:
    PIXEL_PER_METER = (4.0 / 0.3)  # 6 pixel 30 cm
    RUN_SPEED_KMPH = random.randint(4,10)  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 3
    image = None
    #_enemy = []

    def __init__(self, PL_X, PL_Y, Enemy_dir, BG_X, BG_Y):
        self.rand = Enemy_dir
        global font

        font = load_font('..\ENCR10B.TTF')


        if self.rand == 0:
            self.x, self.y = random.randint(0, 50), random.randint(0, 1800)
        elif self.rand == 1:
            self.x, self.y = random.randint(3150, 3200), random.randint(0, 1800)
        elif self.rand == 2:
            self.x, self.y = random.randint(0, 3200), random.randint(0, 50)
        elif self.rand == 3:
            self.x, self.y = random.randint(0, 3200), random.randint(1750, 1800)
        #self.sx = self.x - PL_X
        #self.sy = self.y - PL_Y
        self.x_speed = Enemy1.RUN_SPEED_PPS
        self.y_speed = Enemy1.RUN_SPEED_PPS

        self.sx = self.x - BG_X
        self.sy = self.y - BG_Y

        self.Whattime = 0
        self.alive = 1
        self.xdir = math.cos(math.atan((PL_Y - self.y) / (PL_X - self.x)))
        self.ydir = math.sin(math.atan((PL_Y - self.y) / (PL_X - self.x)))
        if Enemy1.image == None:
            Enemy1.image = load_image('..\Enemy\Image_Enermy.png')
        #Enemy1._enemy.append(self)
    def returnx(self):
        return self.x
    def returny(self) :
        return self.y

    def update(self,frame_time, PL_X, PL_Y, _BG_X , _BG_Y):
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

#
        self.x += self.x_speed * self.xdir * frame_time
        self.y += self.y_speed * self.ydir * frame_time
        self.sx = self.x - _BG_X
        self.sy = self.y - _BG_Y
        self.ADD_Bullet(PL_X,PL_Y)



        #self.delete_object(_Bullet)

    #def get_list():
    #    return (Enemy1._enemy)
    def ADD_Bullet(self,PL_X, PL_Y):
        if self.Whattime >= 2.0:
            EBullet(self.x, self.y, PL_X,PL_Y)
            self.Whattime = 0



    def draw(self):
        font.draw(self.sx, self.sy, 'sX , sY : [%d, %d]' % (self.sx, self.sy))
    #    font.draw(self.x, self.y+20, 'SX , SY : [%d, %d]' % (self.sx, self.sy))

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




