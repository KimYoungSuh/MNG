from pico2d import *

import State.C_CharSellect_State
from State.C_Input import InputSys
import random

world = None
Scean_x, Scean_y = 82, 105
Select_W = None
font = None
def clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))

'''
playerdir
 0 down
 1 up
 2 left
 3 right
 4 down left
 5 down right
 6 up left
 7 up right
'''
class Player1:
    PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
    RUN_SPEED_KMPH = 40.0  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    image = None

    UP_RUN, RIGHT_RUN, LEFT_RUN,  DOWN_RUN = 0,1,2,3,
    def __init__(self, backGround ,
                 _X =random.randint(300, 2900), _Y = random.randint(300, 1500)):
        self.imagenum = State.C_CharSellect_State.select_witchs()
        global _Enemy
        global _Bg
        self.x, self.y = _X, _Y
        self.life = 3
        _Bg = backGround
        self.xdir = 0
        self.ydir =0
        self.state = self.DOWN_RUN
        self.beforestate = 1
        self.sx = self.x - _Bg.window_left
        self.sy = self.y - _Bg.window_bottom
        self.isshoot = False
        self.playerdir = 0
        if Player1.image == None:
            if self.imagenum ==1 :
                Player1.image = load_image('..\Resource\Image_Player.png')
            elif self.imagenum == 2:
                Player1.image = load_image('..\Resource\Image_Player2.png')
            else :
                Player1.image = load_image('..\Resource\Image_Player3.png')

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

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def draw(self, _X , _Y):                 ##Size Change
        #
        self.sx = _X - _Bg.window_left
        self.sy = _Y - _Bg.window_bottom


        _Bg.draw()

        if(self.state == 4):
            self.image.clip_draw(Scean_x * self.beforestate, 0, Scean_x, Scean_y, self.sx, self.sy)
        else :
            self.image.clip_draw(Scean_x * self.state, 0, Scean_x, Scean_y, self.sx, self.sy)

    def get_bb(self):
        return self.sx-5, self.sy-5, self.sx+5, self.sy+5

    def handle_event(self, event):
        #C_input 으로 부터 InputSys 가져옴
        input_move = InputSys().Get_move(event)
        input_shoot = InputSys().Get_shoot_key(event)
        input_last_vertical = InputSys().Get_last_vertical()
        input_last_horizon = InputSys().Get_last_horizon()

        #조건판별
        is_up = (input_move & 0b1000) == 0b1000
        is_down = (input_move & 0b0100) == 0b0100
        is_left = (input_move & 0b0010) == 0b0010
        is_right = (input_move & 0b0001) == 0b0001

        self.xdir = 0
        self.ydir = 0


        if(is_up):
            if(input_last_vertical==1):
                self.move_up()
            if(is_down & (input_last_vertical==-1)):
                self.move_down()
        if(is_down):
            if (input_last_vertical == -1):
                self.move_down()
            if(is_up & (input_last_vertical == 1)):
                self.move_up()
        if(is_left):
            if (input_last_horizon== -1):
                self.move_left()
            if (is_right & (input_last_horizon == 1)):
                self.move_right()
        if(is_right):
            if (input_last_horizon == 1):
                self.move_right()
            if (is_left & (input_last_horizon == -1)):
                self.move_left()


        if(input_shoot):
            self.isshoot = True
            bullet_dir = (0,0)
            if(self.state ==self.UP_RUN):
                bullet_dir = (0, 1)
            if (self.state == self.DOWN_RUN):
                bullet_dir = (0, -1)
            if (self.state == self.LEFT_RUN):
                bullet_dir = (-1, 0)
            if (self.state == self.RIGHT_RUN):
                bullet_dir = (1, 0)
            #Bullet(self.x, self.y, bullet_dir[0], bullet_dir[1])

    def move_up(self):
        self.state = self.UP_RUN
        self.beforestate = self.UP_RUN
        self.ydir = 1
        self.playerdir = 1
    def move_down(self):
        self.state = self.DOWN_RUN
        self.beforestate = self.DOWN_RUN
        self.ydir = -1
        self.playerdir = 0
    def move_left(self):
        self.state = self.LEFT_RUN
        self.beforestate = self.LEFT_RUN
        self.xdir = -1
        self.playerdir = 2
    def move_right(self):
        self.state = self.RIGHT_RUN
        self.beforestate = self.RIGHT_RUN
        self.xdir = 1
        self.playerdir = 3



        

