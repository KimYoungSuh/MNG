from pico2d import *

from State import C_Game_framework
from State import C_title_state

name = "StartState"
image = None
logo_time = 0.0

def enter():
    global image
    image = load_image('Resource\kpu_credit.png')


def exit():
    global image
    del(image)

def update(frame_time):
    global name
    global logo_time

    if (logo_time > 1):
        logo_time = 0
        C_Game_framework.change_state(C_title_state)
        #game_framework.quit()
    logo_time += frame_time
#
def draw(frame_time):
    global image
    clear_canvas()
    image.draw(640, 480)
    update_canvas()

def handle_events(frame_time):
     events = get_events()


def pause(): pass
def resume(): pass




