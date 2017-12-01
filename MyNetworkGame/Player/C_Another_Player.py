from pico2d import *

from Background.C_BG import BackGround
from Bullet.C_PlayerBullet import PBullet
#from State.C_CharSellect_State import select_witch
import State.C_CharSellect_State
from State.C_Input import InputSys

#font = load_font('ENCR10B.TTF')
#font.draw(self.x - 30, self.y + 20, 'HP : %3.2f' % self.life)

world = None
Scean_x, Scean_y = 82, 105
Select_W = None
font = None

class AnotherPlayer:
    PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
    RUN_SPEED_KMPH = 40.0  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    image = None

    UP_RUN, RIGHT_RUN, LEFT_RUN,  DOWN_RUN = 0,1,2,3,
    def __init__(self, backGround):
        global font
        font = load_font('..\ENCR10B.TTF')
        self.imagenum = State.C_CharSellect_State.select_witchs()
        global _Enemy
        global _Bg
        self.x, self.y = 400,400
        self.life = 3
        _Bg = backGround
        self.xdir = 0
        self.ydir =0
        self.state = self.DOWN_RUN
        self.bg = 0
        self.beforestate = 1
        self.sx = self.x - _Bg.window_left
        self.sy = self.y - _Bg.window_bottom
        self.iSpace = False
        if AnotherPlayer.image == None:
            if self.imagenum ==1 :
                AnotherPlayer.image = load_image('..\Player\Image_Player.png')
            elif self.imagenum == 2:
                AnotherPlayer.image = load_image('..\Player\Image_Player2.png')
            else :
                AnotherPlayer.image = load_image('..\Player\Image_Player3.png')


    def draw(self):                 ##Size Change
        #
        self.sx = self.x - _Bg.window_left
        self.sy = self.y - _Bg.window_bottom


        font.draw(800,280, 'SX , SY : [%d, %d]' % (self.sx, self.sy))

        font.draw(800,300, 'X , Y : [%d, %d]' % (self.x, self.y))
        font.draw(800,320, 'windowleft , windowbottom : [%d, %d]' % (_Bg.window_left, _Bg.window_bottom))
        font.draw(800,340, 'canvas_w , canvas_h : [%d, %d]' % (_Bg.canvas_width, _Bg.canvas_height))

        if(self.state == 4):
            self.image.clip_draw(Scean_x * self.beforestate, 0, Scean_x, Scean_y, self.sx, self.sy)
        else :
            self.image.clip_draw(Scean_x * self.state, 0, Scean_x, Scean_y, self.sx, self.sy)


    def get_bb(self):
        return self.sx-5, self.sy-5, self.sx+5, self.sy+5


        

