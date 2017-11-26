from pico2d import *

from Background.C_BG import BackGround
from Bullet.C_PlayerBullet import PBullet
#
from State.C_Input import InputSys

#font = load_font('ENCR10B.TTF')
#font.draw(self.x - 30, self.y + 20, 'HP : %3.2f' % self.life)

world = None
_bg = None
Scean_x, Scean_y = 82, 105

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
        self.x, self.y = 400,400
        self.life = 3
        _Bg = BackGround()
        self.xdir = 0
        self.ydir =0
        self.state = self.STAY
        self.bg = 0
        self.beforestate = 1
        self.sx = self.x - _Bg.window_left
        self.sy = self.y - _Bg.window_bottom
        self.iSpace = False
        if Player1.image == None:
            Player1.image = load_image('Player\Image_Player.png')

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

    def draw(self):                 ##Size Change
        self.sx = self.x - _Bg.window_left
        self.sy = self.y - _Bg.window_bottom
        _Bg.draw()
        if(self.state == 4):
            self.image.clip_draw(Scean_x * self.beforestate, 0, Scean_x, Scean_y, self.sx, self.sy)
        else :
            self.image.clip_draw(Scean_x * self.state, 0, Scean_x, Scean_y, self.sx, self.sy)
        #draw(self.sx, self.sy)
        #debug_print('x=%d, y= %d, sx = %d, sy = %d' %(self.x, self.y,self.sx, self.sy))
        #font.draw(self.x-30,self.y+20, 'HP : %3f' %self.life)

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
            PBullet(self.sx, self.sy, self.xdir, self.ydir)

    def move_up(self):
        self.state = self.UP_RUN
        self.beforestate = self.UP_RUN
        self.ydir = 1
    def move_down(self):
        self.state = self.DOWN_RUN
        self.beforestate = self.DOWN_RUN
        self.ydir = -1
    def move_left(self):
        self.state = self.LEFT_RUN
        self.beforestate = self.LEFT_RUN
        self.xdir = -1
    def move_right(self):
        self.state = self.RIGHT_RUN
        self.beforestate = self.RIGHT_RUN
        self.xdir = 1



        

