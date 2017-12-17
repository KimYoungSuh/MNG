import random
from Background.C_BG import BackGround
from pico2d import *
class EBullet:
    PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
    RUN_SPEED_KMPH = 15  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    image = None
    _eBullet = []
    def __init__(self,_X, _Y):
        self.shooter = 1
        self._Bg = BackGround
        self.x = _X
        self.y = _Y
        self.alive =1

        if EBullet.image == None:
            EBullet.image = load_image('Resource\Image_EBullet.png')
        self.sx = self.x - self._Bg.window_left
        self.sy = self.y - self._Bg.window_bottom

    def update(self):
        self.sx = self.x - self._Bg.window_left
        self.sy = self.y - self._Bg.window_bottom

    def draw(self):
        self.image.draw(self.sx, self.sy)
    def draw_bb(self):
        draw_rectangle(*self.get_bb())
    def get_bb(self):
        return self.sx - 10, self.sy - 10, self.sx + 10, self.sy + 10

def collide(left_a, bottom_a,right_a, top_a, left_b, bottom_b,right_b, top_b):

    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False

    return True
