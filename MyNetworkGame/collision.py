from pico2d import *

import game_framework
from BG import BackGround
from Enemy import Enemy1
from Enemy import Enemy2
from Player import Player1


name = "collision"
wand = None
_Enemy1 = []
_Enemy2 = []
_Enemy3 = []
_Bg = None
_Enemys = None
font = None
item = []
potion = []
Time = 0.0
GameScore = 0

bgm = None
class Timer:
    def __init__(self):
        self.Whattime = 0
        self.itemtime = 0
        self.potintime =0
        self.Scoretime = 0
    def update(self, frame_time):
        self.Whattime +=  frame_time
        self.itemtime += frame_time
        self.Scoretime += frame_time
        self.potintime += frame_time
        self.add()
    def add(self):
        if self.Whattime >= 1.3:
            new_fireball1 = Enemy1()
            _Enemy3.append(new_fireball1)
            new_fireball2 = Enemy2()
            _Enemy3.append(new_fireball2)

            self.Whattime = 0


def create_world():
    global witch, _Bg, _Enemy1, _Enemy2, FB3 ,wand ,FB4, Fireballnum, timer, _Enemy3,GameScore, bgm, select_witch, font
    timer = Timer()

    GameScore =0
    font = load_font('ENCR10B.TTF')
    witch = Player1()

    _Enemy1 = []
    _Enemy2 = []
    _Enemy3 = []
    _Bg = BackGround()

    witch.set_background(_Bg)

def destroy_world():
    global witch, _Bg, _Enemy3  , timer, bgm
    del(witch)
    del(_Enemy3)
    del(_Bg)
    del(bgm)



def enter():

    game_framework.reset_time()
    create_world()



def exit():
    destroy_world()


def pause():
    pass


def resume():
    pass

def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            else:
                witch.handle_event(event)




def collide(a, b):
    left_a, bottom_a,right_a, top_a = a.get_bb()
    left_b, bottom_b,right_b, top_b = b.get_bb()

    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False

    return True
def get_time(frame_time):
    global Time, Fireballnum

    Time += frame_time
    return Time

def update(frame_time):
    for enemy in _Enemy3:
        enemy.update(frame_time)

    for enemy in _Enemy3 :
        if collide(enemy, witch):
            _Enemy3.remove(enemy)

    witch.update(frame_time)
    timer.update(frame_time)




def draw(frame_time):
    clear_canvas()
    witch.draw()
    for ball in _Enemy3:
        ball.draw()

 #   grass.draw_bb()
        witch.draw_bb()
    for ball in _Enemy3 :
        ball.draw_bb()

    update_canvas()


