import random
from pico2d import *

import State.C_Game_framework
from Background.C_BG import BackGround
from Enemy.C_Enemy import Enemy1
from Enemy.C_Enemy2 import Enemy2
from Bullet.C_EnemyBullet import EBullet
from Bullet.C_PlayerBullet import PBullet
from Life.C_Life import Life
import State.C_Gameover_state

#import C_DebugClass

from Player.C_Player import Player1
name = "collision"
wand = None
font = None
_Bg = None
_Enemys = None
_Enemy1 = []
_PBullet = []
_EBullet = []

item = []
potion = []
Time = 0.0
GameScore = 0

#
bgm = None

def enter():
    State.C_Game_framework.reset_time()
    create_world()

def exit():
    destroy_world()

class Timer():
    def __init__(self):
        self.Whattime = 0
        self.itemtime = 0
        self.potintime =0
        self.Scoretime = 0
        self.EnemyNum=0
    def update(self, frame_time):
        self.Whattime +=  frame_time
        self.itemtime += frame_time
        self.Scoretime += frame_time
        self.potintime += frame_time
        self.add()
        if(self.EnemyNum >100):
            State.C_Game_framework.change_state(State.C_Gameover_state)
    def add(self):
        if self.Whattime >= 0.5:
            self.EnemyDirNum = random.randint(0, 8)
            if self.EnemyDirNum <= 3 :
                newEnemy = Enemy1(_player.sx, _player.sy, self.EnemyDirNum)
                _Enemy1.append(newEnemy)
            elif self.EnemyDirNum >= 4 :
                newEnemy = Enemy2(_player.sx, _player.sy, self.EnemyDirNum)
                _Enemy1.append(newEnemy)


            self.Whattime = 0

def create_world():
    global _player, _Bg, _Enemy1, timer,GameScore, font, _EBullet, _PBullet, _Life
    _player = Player1()
    _Bg = BackGround()
    _Enemy1 = []
    _Life = Life(_player.life)
    timer = Timer()
    GameScore =0
    font = load_font('ENCR10B.TTF')
    _EBullet= EBullet.get_list()
    _PBullet = PBullet.get_list()

def destroy_world():
    global _player, _Bg, _Enemy1, timer,GameScore, font,_EBullet, _PBullet
    del(_player)
    del(_Bg)
    del(_EBullet)
    del(_PBullet)

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
            else:
                _player.handle_event(event)

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
    for enemy in _Enemy1:
        enemy.update(frame_time, _player.sx, _player.sy)
    for enemy in _Enemy1 :
        if collide(enemy, _player):
            _player.life -=1
            _Enemy1.remove(enemy)
    for ebullets in _EBullet:
        ebullets.update(frame_time, _player.sx, _player.sy)
    for ebullets in _EBullet :
        if collide(ebullets, _player):
            _player.life -= 1
            _EBullet.remove(ebullets)
    for pbullets in _PBullet:
        pbullets.update(frame_time,)
    for pbullets in _PBullet :
        for enemys in _Enemy1 :
            if collide(pbullets, enemys):
                _PBullet.remove(pbullets)
                _Enemy1.remove(enemys)
    for enemy in _Enemy1 :
        if enemy.alive == 0 :
            _Enemy1.remove(enemy)
    for pbullets in _PBullet :
        if pbullets.alive == 0 :
            _PBullet.remove(pbullets)
    for ebullets in _EBullet :
        if ebullets.alive == 0 :
            _EBullet.remove(ebullets)

    _player.update(frame_time)
    timer.update(frame_time)



def draw(frame_time):
    clear_canvas()
    _player.draw()
    for enemy in _Enemy1:
        enemy.draw()
    for ebullets in _EBullet:
        ebullets.draw()
    for pbullets in _PBullet:
        pbullets.draw()
 #   grass.draw_bb()
    _player.draw_bb()
    for enemy in _Enemy1 :
        enemy.draw_bb()
    for ebullets in _EBullet:
        ebullets.draw_bb()
    for pbullets in _PBullet:
        pbullets.draw_bb()
    _Life.draw()
    update_canvas()


def delete_object(objects):
    for object in objects:
        if object.alive == 0:
            objects.remove(object)
