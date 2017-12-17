import random
from pico2d import *
from Background.C_BG import BackGround

font = None


class CScore:
#
    image = None
    def __init__(self):
        global font
        font = load_font('Resource\ENCR10B.TTF')

    def update(self):
        pass
        #self.delete_object(_Bullet)

    def draw(self , Score):
        font.draw(550, 850, 'SCORE : [%d]' % (Score))



