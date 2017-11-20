from pico2d import *

from State.C_Input import InputSys
from Background.C_SelectBG import C_SelectBG
#import char_sellect
#font = load_font('ENCR10B.TTF')
#font.draw(self.x - 30, self.y + 20, 'HP : %3.2f' % self.life)


class Wand:
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
        global _BG
        _BG = C_SelectBG()
        self.x = _BG.canvas_width/2
        self.y = _BG.canvas_height/2
        self.xdir = 0
        self.ydir = 0
        if Wand.image == None:
            Wand.image = load_image('Magic wand.png')

    def update(self, frame_time):
        distance = Wand.RUN_SPEED_PPS * frame_time
        self.x += (self.xdir * distance)
        self.y += (self.ydir * distance)
        if (self.x < 0):
            self.x = 0
        elif (self.x > _BG.canvas_width):
            self.x = _BG.canvas_width
        elif (self.y < 0):
            self.y = 0
        elif (self.y > _BG.canvas_height):
            self.y = _BG.canvas_height
    def draw(self):
        self.image.draw(self.x, self.y)

    def handle_event(self, event):
        input_move = InputSys().Get_move(event)
        input_last_vertical = InputSys().Get_last_vertical()
        input_last_horizon = InputSys().Get_last_horizon()

        # 조건판별
        is_up = (input_move & 0b1000) == 0b1000
        is_down = (input_move & 0b0100) == 0b0100
        is_left = (input_move & 0b0010) == 0b0010
        is_right = (input_move & 0b0001) == 0b0001

        self.xdir = 0
        self.ydir = 0

        if (is_up):
            if (input_last_vertical == 1):
                self.move_up()
            if (is_down & (input_last_vertical == -1)):
                self.move_down()
        if (is_down):
            if (input_last_vertical == -1):
                self.move_down()
            if (is_up & (input_last_vertical == 1)):
                self.move_up()
        if (is_left):
            if (input_last_horizon == -1):
                self.move_left()
            if (is_right & (input_last_horizon == 1)):
                self.move_right()
        if (is_right):
            if (input_last_horizon == 1):
                self.move_right()
            if (is_left & (input_last_horizon == -1)):
                self.move_left()

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
