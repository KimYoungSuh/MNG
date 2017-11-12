from pico2d import *

from Background.C_BG import BackGround
from Bullet.C_PlayerBullet import Bullet

#font = load_font('ENCR10B.TTF')
#font.draw(self.x - 30, self.y + 20, 'HP : %3.2f' % self.life)

world = None
_bg = None
_Bullet = []

def clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))

class Player1:
    PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
    RUN_SPEED_KMPH = 40.0  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    image = None
    UP_RUN, RIGHT_RUN, LEFT_RUN,  DOWN_RUN, STAY = 0,1,2,3, 4

    def __init__(self):
        global _Bg
        global _Enemy
        self.x, self.y = 0, 0
        _Bg = BackGround()
        self.xdir = 0
        self.ydir =0
        self.state = self.STAY
        self.bg = 0
        if Player1.image == None:
            Player1.image = load_image('Player\Image_PlayerUP.png')

    def update(self, frame_time):
        distance = Player1.RUN_SPEED_PPS * frame_time
        self.x += (self.xdir * distance)
        self.y += (self.ydir * distance)
        _Bg.update(frame_time, (self.x, self.y))
        if(self.x < 0):
            self.x = 0
        elif(self.x > _Bg.w):
            self.x = _Bg.w
        elif(self.y<0):
            self.y = 0
        elif (self.y > _Bg.h):
            self.y = _Bg.h
        for bullets in _Bullet:
            bullets.update(frame_time)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def draw(self):                 ##Size Change
        self.sx = self.x - _Bg.window_left
        self.sy = self.y - _Bg.window_bottom
        _Bg.draw()
        for bullets in _Bullet:
            bullets.draw()
        if(self.state ==self.LEFT_RUN):
            Player1.image = load_image('Player\Image_PlayerLEFT.png')
            self.image.draw(self.sx, self.sy)
        if (self.state == self.RIGHT_RUN):
            Player1.image = load_image('Player\Image_PlayerRIGHT.png')
            self.image.draw(self.sx, self.sy)
        if (self.state == self.DOWN_RUN):
            Player1.image = load_image('Player\Image_PlayerDOWN.png')
            self.image.draw(self.sx, self.sy)
        if (self.state == self.UP_RUN):
            Player1.image = load_image('Player\Image_PlayerUP.png')
            self.image.draw(self.sx, self.sy)
        #debug_print('x=%d, y= %d, sx = %d, sy = %d' %(self.x, self.y,self.sx, self.sy))
        #font.draw(self.x-30,self.y+20, 'HP : %3f' %self.life)

    def get_bb(self):
        return self.sx-5, self.sy-5, self.sx+5, self.sy+5

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
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                _Bullet.append(Bullet(self.sx, self.sy, self.xdir, self.ydir))

