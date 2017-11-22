from pico2d import *

from Bullet.C_PlayerBullet import PBullet
from Enemy.C_Enemy import Enemy1

_PBullet= []
_Enemy = []

def enter():
    pass
def exit():
    pass

def create_world():
    global _player, _Bg, _Enemy1, FB3 ,wand ,FB4, Fireballnum, timer, _Enemy3,GameScore, bgm, select_witch, font , _PBullet



def destroy_world():
    global _player, _Bg, _Enemy1, FB3 ,wand ,FB4, Fireballnum, timer, _Enemy3,GameScore, bgm, select_witch, font
    del(_player)
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
    for enemy in _Enemy3:
        enemy.update(frame_time, _player.sx, _player.sy)
    for enemy in _Enemy3 :
        if collide(enemy, _player):
            _Enemy3.remove(enemy)
    for enemy in _Enemy3 :
        if enemy.alive == 0 :
            _Enemy3.remove(enemy)
    _player.update(frame_time)
    timer.update(frame_time)



def draw(frame_time):
    clear_canvas()
    _player.draw()
    for enemy in _Enemy3:
        enemy.draw()

 #   grass.draw_bb()
    _player.draw_bb()
    for enemy in _Enemy3 :
        enemy.draw_bb()

    update_canvas()


def delete_object(objects):
    for object in objects:
        if object.alive == 0:
            objects.remove(object)
