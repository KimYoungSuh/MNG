import C_game_framework
from pico2d import *

from C_Wand import Wand
from State import C_Collision
from State import C_Title_state
from Background.C_SellectBG import C_SellectBG

name = "Char_sellect"
image = None
font = None
sel = None
Scean_x, Scean_y = 82, 105
select_witch =0
def enter():
    global image, font, _BG, _WAND, select_witch
    image = load_image('Player\Image_Player.png')
    font = load_font('ENCR10B.TTF')
    _BG = C_SellectBG()
    _WAND = Wand()
    select_witch = 0

def exit():
    del(image)
    del(font)
    del(_BG)
    del(_WAND)

def pause():
    pass

def resume():
    pass


def handle_events(frame_time):
    global select_witch, readyState
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            C_game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                C_game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                if _WAND.x > 30 :
                    if _WAND.x < 275:
                        if _WAND.y > 40:
                            if _WAND.y < 350:
                                select_witch= 1
                if _WAND.x > 305:
                    if _WAND.x < 545:
                        if _WAND.y > 40:
                            if _WAND.y < 350:
                                select_witch =2
                if _WAND.x > 580:
                    if _WAND.x < 820:
                        if _WAND.y > 40:
                            if _WAND.y < 350:
                                select_witch=3
                if _WAND.x > 905 :
                    if _WAND.x < 1115:
                        if _WAND.y > 190:
                            if _WAND.y < 285:
                                readyState= 1
                                if select_witch != 0 :
                                    C_game_framework.run(C_Collision)
                if _WAND.x > 905 :
                    if _WAND.x < 1115:
                        if _WAND.y > 45:
                            if _WAND.y < 140:
                                C_game_framework.run(C_Title_state)
            else:
                _WAND.handle_event(event)





def update(frame_time):
    _WAND.update(frame_time)



def draw(frame_time):
    global image
    clear_canvas()
    _BG.draw()
    image.clip_draw(Scean_x * 1, 0, Scean_x, Scean_y, 140, 250)
    image.clip_draw(Scean_x * 2, 0, Scean_x, Scean_y, 420, 250)
    image.clip_draw(Scean_x * 3, 0, Scean_x, Scean_y, 700, 250)
    font.draw(160, 430, 'Wand_X = %d' % (_WAND.x))
    font.draw(160, 460, 'Wand_Y = %d' % (_WAND.y))

    if select_witch != 0 :
        image.clip_draw(Scean_x * select_witch, 0, Scean_x, Scean_y, 230, 600)
    _WAND.draw()
    update_canvas()



