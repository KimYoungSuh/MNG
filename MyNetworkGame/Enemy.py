import random

from pico2d import *

_Enemy1 = []
FBnum =1
class Enemy1:
    PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
    RUN_SPEED_KMPH = random.randint(4,30)  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 3
    image = None

    def __init__(self):
        self.x, self.y = random.randint(5,30), random.randint(0, 600)
        self.frame = random.randint(0,2)
        self.speed = 0
        self.total_frames = 0.0
        self.check = True

        if Enemy1.image == None:
            Enemy1.image = load_image('squirrel.png')

    def update(self,frame_time):

        self.speed = Enemy1.RUN_SPEED_PPS * frame_time
        self.frame = (self.frame + 1) % 3
        self.total_frames += Enemy1.FRAMES_PER_ACTION * Enemy1.ACTION_PER_TIME * frame_time
        self.x += self.speed
        if self.x > 800:
            self.x = 10
            self.y = random.randint(0,600)

    def draw(self):
        self.image.draw(self.x, self.y)
    def draw_bb(self):
        draw_rectangle(*self.get_bb())
    def get_bb(self):
        return self.x-10 , self.y-10, self.x+10, self.y+10

class Enemy2:
    image = None
    PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
    RUN_SPEED_KMPH = random.randint(4, 30)  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 3
    def __init__(self):
        self.x, self.y = random.randint(0, 800) , random.randint(5,30)
        self.frame = random.randint(0,2)
        self.speed = 0
        self.total_frames = 0.0
        self.FBnum = 1

        if Enemy2.image == None:
            Enemy2.image = load_image('squirrel.png')
    def update(self,frame_time):

        self.speed = Enemy2.RUN_SPEED_PPS * frame_time
        self.frame = (self.frame + 1) % 3
        self.total_frames += Enemy2.FRAMES_PER_ACTION * Enemy2.ACTION_PER_TIME * frame_time
        self.y +=  self.speed
        self.frame = (self.frame+1) %3

        if self.y > 700:
            self.y = 10
            self.x = random.randint(0,800)
        if self.y > 350 :
            self.FBnum +=1

    def draw(self):
        self.image.draw(self.x, self.y)
    def draw_bb(self):
        draw_rectangle(*self.get_bb())
    def get_bb(self):
        return self.x-10 , self.y-10, self.x+10, self.y+10

