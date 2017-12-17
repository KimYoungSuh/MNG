from pico2d import *

from State import C_Game_framework
from State import C_Lobby_state
from C_Wand import Wand

name = "TitleState"
image = None
font = None
_WAND = None
bgm = None

def enter():
    global image, font, _WAND, bgm
    font = load_font('Resource\ENCR10B.TTF')
    _WAND = Wand()
    bgm = load_music('Resource\openning.mp3')
    bgm.set_volume(64)
    bgm.play(1)
    image = load_image('Resource\Image_GameTitle.png')
#
def exit():
    global image, _WAND, font, bgm
    del(image)
    del(_WAND)
    del(font)
    del(bgm)


def pause():
    pass

def resume():
    pass

def handle_events(frame_time):
    global _WAND
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            C_Game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                C_Game_framework.quit()
            elif (event.type) == (SDL_MOUSEBUTTONDOWN):
                if _WAND.x > 400 :
                    if _WAND.x < 580:
                        if _WAND.y > 270:
                            if _WAND.y < 405:
                                C_Game_framework.push_state(C_Lobby_state)

                if _WAND.x > 800:
                    if _WAND.x < 980:
                        if _WAND.y > 270:
                            if _WAND.y < 405:
                                C_Game_framework.quit()


            else:
                _WAND.handle_event(event)


def update(frame_time):
    pass

def draw(frame_time):
    global image

    clear_canvas()
    image.draw(600, 450)
    _WAND.draw()

    update_canvas()



