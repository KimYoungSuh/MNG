import random
from pico2d import *

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

    def __init__(self, Enemy_dir):
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
        self.speed = Enemy2.RUN_SPEED_PPS

        self.Whattime = 0
        self.alive = 1

    def update(self, frame_time):
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
#
        self.x += self.speed * self.xdir * frame_time
        self.y += self.speed * self.ydir * frame_time

    def set_dir(self,PL_X, PL_Y):
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

    def get_distance(self,PL_X, PL_Y):
        dx = self.x - PL_X
        dy = self.y - PL_Y
        return (dx*dx)+(dy*dy)

    def ADD_Bullet(self):
        if self.Whattime >= 2.0:
            self.Whattime = 0
            return True

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

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

