import random
from pico2d import *
import socket
import time
import State.C_Game_framework
from Background.C_BG import BackGround
from Enemy.C_Enemy import Enemy1
from Enemy.C_Enemy2 import Enemy2
from Bullet.C_EnemyBullet import EBullet
from Bullet.C_PlayerBullet import PBullet
from Life.C_Life import Life
from TCP.C_Pack import DataStruct

import State.C_Gameover_state
from Data.C_BulletData import *
from Data.C_EnemyData import *
from Data.C_PlayerData import *
from Data.C_RoomData import *
from Data.C_StructSet import *
from State.C_Game_data import GameData
import struct
import threading
#import C_DebugClass


from Player.C_Player import Player1

name = "collision"
wand = None
font = None
_Enemys = None
_Enemy1 = []
_PBullet = []
_EBullet = []
E_NUM=0
item = []
potion = []
Time = 0.0
GameScore = 0
SERVER_IP_ADDR ="127.0.0.1"
SERVER_PORT = 19000
SEND_TIME = 0
#
bgm = None

def enter():
    State.C_Game_framework.reset_time()
    create_world()


def exit():
    destroy_world()

#timer
'''
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
                newEnemy = Enemy1(_player.sx, _player.sy, self.EnemyDirNum ,_Bg.window_left, _Bg.window_bottom )
                _Enemy1.append(newEnemy)
                PACK_DATA_Enemy(newEnemy)

            elif self.EnemyDirNum >= 4 :
                newEnemy = Enemy2(_player.sx, _player.sy, self.EnemyDirNum,_Bg.window_left, _Bg.window_bottom)
                _Enemy1.append(newEnemy)
                PACK_DATA_Enemy(newEnemy)
            self.Whattime = 0
'''
def create_world():
    global _player, _Bg, _Enemy1, timer,GameScore, font, _EBullet, _PBullet, _Life,client_sock,tcp_controller,E_NUM, _Enemy_Data
    _Bg = BackGround()
    E_NUM =0
    _player = Player1(_Bg)
    _Enemy1 = []
    _Life = Life(_player.life)
    #timer = Timer()
    client_sock = GameData.client_socket
    #tcp_controller = TcpContoller()
    readystate = 0
    #client_sock = tcp_controller.tcp_client_init()
    t1 = threading.Thread(target=recv_thread, args=(client_sock,))
    t1.start()
    readystate = 0
    GameScore =0
    font = load_font('ENCR10B.TTF')
    _EBullet= EBullet.get_list()
    _PBullet = PBullet.get_list()


def recv_thread(client_sock):


    pass
    '''while 1:
        packed_players_data = client_sock.recv(BUFSIZE)

        temp_list = Pack.unpack_players_data(packed_players_data)
        if(GameData.player_number==1):
            _another_players[0].x = temp_list[1][0]
            _another_players[0].y = temp_list[1][1]
        elif(GameData.player_number==2):
            _another_players[0].x = temp_list[0][0]
            _another_players[0].y = temp_list[0][1]
        print(_another_players[0].x,_another_players[0].y)
'''

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
    global client_sock
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

'''
def get_time(frame_time):
    global Time, Fireballnum

    return Time
'''
def update(frame_time):
    global E_NUM ,_Enemy_Data
    #for enemy in _Enemy1:
    #    enemy.update(frame_time, _player.x, _player.y, _Bg.window_left, _Bg.window_bottom,State)
    '''
    for enemy in _Enemy1 :
        if collide(enemy, _player):
            _player.life -=1
            _Enemy1.remove(enemy)
    for ebullets in _EBullet:
        ebullets.update(frame_time, _player.x, _player.y, _Bg.window_left, _Bg.window_bottom )
        PACK_DATA_PBULLET(ebullets)

    for ebullets in _EBullet :
        if collide(ebullets, _player):
            _player.life -= 1
            _EBullet.remove(ebullets)
    for pbullets in _PBullet:
        PACK_DATA_PBULLET(pbullets)
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

#SEND_ENEMY_DATA is ENEMY _X,_Y, TYPE
    E_NUM = struct.unpack('=i', recved_E_NUM)[0]
    for enemy in range(0, E_NUM) :
        _Enemy_packed = client_sock.recv(struct.calcsize('=fffi'))
        _Enemy_Data = DataStruct.unpack_enemy_data(_Enemy_packed)
        if _Enemy_Data[2] ==1 :
            newEnemy = Enemy1(_Enemy_Data[0],_Enemy_Data[1], _Bg.window_left, _Bg.window_bottom)
        if _Enemy_Data[2] ==2 :
            newEnemy = Enemy2(_Enemy_Data[0],_Enemy_Data[1],_Bg.window_left, _Bg.window_bottom)
        _Enemy1.insert(_Enemy_Data[3], newEnemy)

        print('_Enemy1 : ', _Enemy1)

    for enemy in _Enemy1 :
        enemy.update()
'''
    _player.update(frame_time)
    Player_packed = DataStruct.pack_player_data(_player)
    client_sock.send(Player_packed)



    recved_NUM = client_sock.recv(struct.calcsize('=ii'))
    Recved_Number_Data = struct.unpack('=ii',recved_NUM )
    #SEND_ENEMY_DATA is ENEMY _X,_Y, TYPE
    E_NUM = Recved_Number_Data[0]
    EB_NUM = Recved_Number_Data[1]
    #?
    print('E_NUM ,EB_NUM : ', E_NUM,EB_NUM)
    for i in range(0, E_NUM) :
        _Enemy_packed = client_sock.recv(struct.calcsize('=ffffi'))
        _Enemy_Data = DataStruct.unpack_enemy_data(_Enemy_packed)
        if _Enemy_Data[2] ==1 :
            newEnemy = Enemy1(_Enemy_Data[0],_Enemy_Data[1],_Enemy_Data[3], _Bg.window_left, _Bg.window_bottom)
            newEnemy.update(frame_time,_player.x, _player.y, _Bg.window_left, _Bg.window_bottom,State)
        if _Enemy_Data[2] ==2 :
            newEnemy = Enemy2(_Enemy_Data[0],_Enemy_Data[1],_Enemy_Data[3],_Bg.window_left, _Bg.window_bottom)
            newEnemy.update(frame_time,_player.x, _player.y, _Bg.window_left, _Bg.window_bottom,State)
        _Enemy1.append(newEnemy)

    for i in range(0,EB_NUM) :
        _Bullet_packed = client_sock.recv(struct.calcsize('=fff'))
        _Bullet_Data = DataStruct.unpack_bullet_data(_Bullet_packed)
        if _Bullet_Data[0] == 1:     #EnemyBullet
            newEBullet = EBullet(_Bullet_Data[1],_Bullet_Data[2] )
        newEBullet.update()
        _EBullet.append(newEBullet)
        if _Bullet_Data[0] == 0:     # playerBullet
            pass





        #print("Enemy Packed : ", _enemylist)
#    timer.update(frame_time)



def draw(frame_time):
    global _Enemy1,_EBullet
    clear_canvas()
    _player.draw()
    for enemy in _Enemy1:
        enemy.draw()
    for enemy in _Enemy1:
        enemy.draw_bb()

    for ebullets in _EBullet:
        ebullets.draw()
    _Enemy1 = []
    _EBullet = []
    '''
    for enemy in _Enemy1:
        enemy.draw()
    for enemy in _Enemy1:
        enemy.draw_bb()
            _Enemy1.clear()


    for pbullets in _PBullet:
        pbullets.draw()
 #   grass.draw_bb()
    _player.draw_bb()

    for ebullets in _EBullet:
        ebullets.draw_bb()
    for pbullets in _PBullet:
        pbullets.draw_bb()
    _Life.draw(_player.life)
    '''
    update_canvas()

def PACK_DATA_Player(objects):
    Player_packed = DataStruct.pack_player_data(objects)
    client_sock.send(Player_packed)

    return Player_packed

def PACK_DATA_Enemy(objects):
    #todo: 게임중
    #for objects in object:
        #DataStruct.pack_enemy_data(objects)
        #Enemy_packed =
        #print(Enemy_packed)
        #client_socket.sendall(packed)
    Enemy_packed = DataStruct.pack_enemy_data(objects)
    #print(DataStruct.unpack_enemy_data(Enemy_packed))
    #client_sock.sendall(Enemy_packed)
    return Enemy_packed
    #

def PACK_DATA_PBULLET(objects):
    Bullet_packed = DataStruct.pack_bullet_data(objects)
    print(DataStruct.unpack_bullet_data(Bullet_packed))
    #client_sock.sendall(Bullet_packed)
    return Bullet_packed

def delete_object(objects):
    for object in objects:
        if object.alive == 0:
            objects.remove(object)



