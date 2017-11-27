import random
from pico2d import *
from Bullet.C_EnemyBullet import EBullet

_Bullet = []
font = None
Scean_x, Scean_y = 49, 82

class Enemy2:
    PIXEL_PER_METER = (4.0 / 0.3)  # 6 pixel 30 cm
    RUN_SPEED_KMPH = random.randint(4,10)  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    UP_RUN, RIGHT_RUN, LEFT_RUN,  DOWN_RUN, STAY = 0,1,2,3, 4

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 3
    image = None
    global font
    font = load_font('ENCR10B.TTF')
    def __init__(self, PL_X, PL_Y, Enemy_dir):
        self.rand = Enemy_dir
        self.x = 0
        self.y =0
        if self.rand == 4:
            self.x, self.y = random.randint(0, 50), random.randint(0, 900)
        elif self.rand == 5:
            self.x, self.y = random.randint(3450, 3500), random.randint(0, 900)
        elif self.rand == 6:
            self.x, self.y = random.randint(0, 3500), random.randint(0, 50)
        elif self.rand == 7:
            self.x, self.y = random.randint(0, 3500), random.randint(850, 900)
        self.x_speed = Enemy2.RUN_SPEED_PPS
        self.y_speed = Enemy2.RUN_SPEED_PPS

        self.Whattime = 0
        self.alive = 1
        self.xdir = math.cos(math.atan((PL_Y - self.y) / (PL_X - self.x)))
        self.ydir = math.sin(math.atan((PL_Y - self.y) / (PL_X - self.x)))
        if self.xdir > self.ydir  :
            if self.xdir > 0 :
                self.state = 1
            else:
                self.state = 2
        else:
            if self.ydir > 0:
                self.state = 0
            else:
                self.state = 3
        if Enemy2.image == None:
            Enemy2.image = load_image('..\Enemy\Image_Enermy2.png')

    def returnDir(self, x,y):
        pass


    def update(self,frame_time, PL_X, PL_Y):
        if self.x > 3500:
            self.x = 3500
            self.xdir *= -1
        if self.x < 0:
            self.x = 0
            self.xdir *= -1
        if self.y > 900:
            self.y = 900
            self.ydir *= -1
        if self.y < 0:
            self.y = 0
            self.ydir *= -1
        self.Whattime +=frame_time
        if self.xdir > self.ydir  :
            if self.xdir > 0 :
                self.state = 1
            else:
                self.state = 2
        else:
            if self.ydir > 0:
                self.state = 0
            else:
                self.state = 3

#
        self.x += self.x_speed * self.xdir * frame_time
        self.y += self.y_speed * self.ydir * frame_time

        self.add(PL_X,PL_Y)



        #self.delete_object(_Bullet)


    def add(self,PL_X, PL_Y):
        if self.Whattime >= 2.0:
            EBullet(self.x, self.y, PL_X,PL_Y)
            self.Whattime = 0



    def draw(self):
        self.image.clip_draw(Scean_x* self.state, 0, Scean_x, Scean_y, self.x, self.y)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())
    def get_bb(self):
        return self.x-10 , self.y-10, self.x+10, self.y+10



def delete_object(objects):
    for object in objects:
        if object.alive == 0:
            objects.remove(object)




