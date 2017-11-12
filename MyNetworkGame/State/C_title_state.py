from pico2d import *

import C_game_framework
from State import C_collision

name = "TitleState"
image = None

def enter():
    global image
    image = load_image('State\GameTitle.png')

def exit():
    global image
    del(image)


def pause():
    pass

def resume():
    pass


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            C_game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                C_game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                C_game_framework.change_state(C_collision)



def update(frame_time):
    pass


def draw(frame_time):
    global image
    clear_canvas()
    image.draw(640, 480)
    update_canvas()



