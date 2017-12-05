from pico2d import *


import State.C_title_state
import State.C_Game_framework
import State.C_title_state

name = "Game Over"
image = None
#

def select_room1():
    pass


def select_room2():
    pass


def select_room3():
    pass


def select_room4():
    pass


def reset_lobby():
    pass


def join_room():
    pass


def create_room():
    pass


def exit_lobby():
    pass


def enter():
    global image
    image = load_image('State\Image_Gameover_state.jpg')

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
            State.C_Game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                State.C_Game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                State.C_Game_framework.change_state(State.C_Title_state)



def update(frame_time):
    pass


def draw(frame_time):
    global image
    clear_canvas()
    update_canvas()




