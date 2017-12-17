from pico2d import *

font = None


class CScore:
    image = None
    def __init__(self):
        global font
        font = load_font('Resource\ENCR10B.TTF')

    def update(self):
        pass

    def draw(self , Score):
        font.draw(550, 850, 'SCORE : [%d]' % (Score))



