import random

from pico2d import *

import C_game_framework
from Background.C_BG import BackGround
from Enemy.C_Enemy import Enemy1
from Player.C_Player import Player1

name = "collision"
wand = None
_Enemy1 = []
_Enemy3 = []
_Bg = None
_Enemys = None
font = None
item = []
potion = []
Time = 0.0
GameScore = 0

bgm = None

def enter():

    C_game_framework.reset_time()
    create_world()



def exit():
    destroy_world()

class Timer():
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
        if self.Whattime >= 2.0:
            self.EnemyDirNum = random.randint(0, 3)
            if self.EnemyDirNum ==0 :
                newEnemy = Enemy1(witch.sx, witch.sy)
                _Enemy3.append(newEnemy)
                self.Whattime = 0
            elif self.EnemyDirNum ==1 :
                newEnemy = Enemy1(witch.sx, witch.sy)
                _Enemy3.append(newEnemy)
                self.Whattime = 0
            elif self.EnemyDirNum ==2 :
                newEnemy = Enemy1(witch.sx, witch.sy)
                _Enemy3.append(newEnemy)
                self.Whattime = 0
            elif self.EnemyDirNum ==3 :
                newEnemy = Enemy1(witch.sx, witch.sy)
                _Enemy3.append(newEnemy)
                self.Whattime = 0

def create_world():
    global witch, _Bg, _Enemy1, FB3 ,wand ,FB4, Fireballnum, timer, _Enemy3,GameScore, bgm, select_witch, font
    timer = Timer()

    GameScore =0
    font = load_font('ENCR10B.TTF')
    witch = Player1()

    _Enemy1 = []
    _Enemy3 = []
    _Bg = BackGround()


def destroy_world():
    global witch, _Bg, _Enemy3  , timer, bgm
    del(witch)
    del(_Enemy3)
    del(_Bg)
    del(bgm)




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
    for enemy in _Enemy3 :
        if enemy.alive == 0 :
            _Enemy3.remove(enemy)
    witch.update(frame_time)

    timer.update(frame_time)



def draw(frame_time):
    clear_canvas()
    witch.draw()
    for enemy in _Enemy3:
        enemy.draw()

 #   grass.draw_bb()
    witch.draw_bb()
    for enemy in _Enemy3 :
        enemy.draw_bb()

    update_canvas()


def delete_object(objects):
    for object in objects:
        if object.alive == 0:
            object.remove(object)
