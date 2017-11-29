from pico2d import *

import State.C_Game_framework
from State import C_CharSellect_State
from C_Wand import Wand
from TCP.C_TcpController import TcpContoller

name = "TitleState"
image = None
font = None
_WAND = None


def enter():
    global image, font, _WAND
    font = load_font('..\ENCR10B.TTF')
    _WAND = Wand()

    image = load_image('..\State\Image_GameTitle.png')
#
def exit():
    global image, _WAND, font
    del(image)
    del(_WAND)
    del(font)



def pause():
    pass

def resume():
    pass


def handle_events(frame_time):
    global _WAND
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            State.C_Game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                State.C_Game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                State.C_Game_framework.change_state(C_CharSellect_State)
            else :
                _WAND.handle_event(event)




def update(frame_time):
    global _WAND
    _WAND.update(frame_time)
    pass


def draw(frame_time):
    global image

    clear_canvas()
    image.draw(640, 480)
    font.draw(300, 280, 'X , Y : [%d, %d]' % (_WAND.x, _WAND.y))
    _WAND.draw()

    update_canvas()



