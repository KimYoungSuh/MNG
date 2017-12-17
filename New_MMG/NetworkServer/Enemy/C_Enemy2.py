import random
from pico2d import *
from Bullet.C_EnemyBullet import EBullet

_Bullet = []
Scean_x, Scean_y = 49, 82

class Enemy2:
    PIXEL_PER_METER = (4.0 / 0.3)  # 6 pixel 30 cm
    RUN_SPEED_KMPH = 15  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    UP_RUN, RIGHT_RUN, LEFT_RUN,  DOWN_RUN, STAY = 0,1,2,3, 4

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 3
    image = None

    #_enemy2 = []

    def __init__(self, PL_X, PL_Y, Enemy_dir, BG_X, BG_Y):
        self.type = 2
        self.rand = Enemy_dir

        if self.rand == 4:
            self.x, self.y = random.randint(0, 50), random.randint(0, 1800)
        elif self.rand == 5:
            self.x, self.y = random.randint(3150, 3200), random.randint(0, 1800)
        elif self.rand == 6:
            self.x, self.y = random.randint(0, 3200), random.randint(0, 50)
        else :
            self.x, self.y = random.randint(0, 3200), random.randint(1750, 1800)
    #    self.sx = self.x - PL_X
    #    self.sy = self.y - PL_Y
        self.sx = self.x - BG_X
        self.sy = self.y - BG_Y
        self.speed = Enemy2.RUN_SPEED_PPS

        self.Whattime = 0
        self.alive = 1
        self.xdir = math.cos(math.atan((PL_Y - self.y) / (PL_X - self.x)))
        self.ydir = math.sin(math.atan((PL_Y - self.y) / (PL_X - self.x)))
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
        if collide(self.x, self.y, self.x+10, self.y+10, PL_X, PL_Y, PL_X+10, PL_Y+10) :
            self.alive = 0



        #self.delete_object(_Bullet)


    def ADD_Bullet(self):
        if self.Whattime >= 2.0:
            self.Whattime = 0
            return True

    def draw(self,):
        self.image.clip_draw(Scean_x* self.state, 0, Scean_x, Scean_y, self.sx, self.sy)
    #    font.draw(self.sx, self.sy, 'X , Y : [%d, %d]' % (self.sx, self.sy))
    #    self.image.clip_draw(Scean_x* self.state, 0, Scean_x, Scean_y, self.sx, self.sy)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())
    def get_bb(self):
        return self.sx - 10, self.sy - 10, self.sx + 10, self.sy + 10

        #return self.sx-10 , self.sy-10, self.sx+10, self.sy+10



def delete_object(objects):
    for object in objects:
        if object.alive == 0:
            objects.remove(object)



def collide(left_a, bottom_a,right_a, top_a, left_b, bottom_b,right_b, top_b):

    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False

    return True

