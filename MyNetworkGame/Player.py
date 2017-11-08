import random
import json
import os

from pico2d import *
import game_framework
import title_state
from BG import BackGround
#font = load_font('ENCR10B.TTF')
#font.draw(self.x - 30, self.y + 20, 'HP : %3.2f' % self.life)

world = None
_bg = None


def clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))

class Player1:
    PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
    RUN_SPEED_KMPH = 40.0  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    image = None
    UP_RUN, RIGHT_RUN, LEFT_RUN,  DOWN_RUN, STAY = 0,1,2,3, 4

    def __init__(self):
        global _Bg
        self.x, self.y = 100, 100
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.frame = 1
        _Bg = BackGround()
        self.life_time = 0.0
        self.total_frames = 0.0
        self.xdir = 0
        self.ydir =0
        self.state = self.STAY
        self.bg = 0

        if Player1.image == None:
            Player1.image = load_image('FL_ANIME.png')

    def set_background(self, bg):
        self.bg = bg

    def update(self, frame_time):
        self.life_time += frame_time
        self.total_frames += Player1.FRAMES_PER_ACTION * Player1.ACTION_PER_TIME * frame_time
        distance = Player1.RUN_SPEED_PPS * frame_time
        self.frame = (self.frame+1) %3
        self.x += (self.xdir * distance)
        self.y += (self.ydir * distance)
        _Bg.update(frame_time, (self.x, self.y))
        if(self.x < 0):
            self.x = 0
        elif(self.x > _Bg.image.w):
            self.x = _Bg.image.w
        elif(self.y<0):
            self.y = 0
        elif (self.y > _Bg.image.h):
            self.y = _Bg.image.h


    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def draw(self):                 ##Size Change
        #sx = self.x - self.bg.window_left
        #sy = self.y - self.bg.window_bottom
        _Bg.draw()
        self.image.clip_draw(self.frame * 30, self.state * 32, 30, 32, self.x, self.y)

        #debug_print('x=%d, y= %d, sx = %d, sy = %d' %(self.x, self.y,self.sx, self.sy))
        #font.draw(self.x-30,self.y+20, 'HP : %3f' %self.life)

    def get_bb(self):
        return self.x-5, self.y-5, self.x+5, self.y+5

    def handle_event(self, event):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            if self.state in (self.RIGHT_RUN, self.DOWN_RUN, self.STAY, self.UP_RUN):
                self.state = self.LEFT_RUN
                self.xdir = -1
                self.ydir = 0



        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if self.state in (self.LEFT_RUN, self.DOWN_RUN, self.STAY, self.UP_RUN):
                self.state = self.RIGHT_RUN
                self.xdir = 1
                self.ydir = 0
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            if self.state in (self.RIGHT_RUN, self.DOWN_RUN, self.STAY, self.LEFT_RUN):
                self.state = self.UP_RUN
                self.ydir = 1
                self.xdir = 0

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            if self.state in (self.RIGHT_RUN, self.UP_RUN, self.STAY, self.LEFT_RUN):
                self.state = self.DOWN_RUN
                self.ydir = -1
                self.xdir = 0
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_s):
            if self.state in (self.RIGHT_RUN, self.UP_RUN, self.STAY, self.LEFT_RUN):
                self.state = self.STAY
                self.ydir = 0
                self.xdir = 0