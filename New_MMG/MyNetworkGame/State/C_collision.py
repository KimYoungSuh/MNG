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
from State import C_Lobby_state
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
from Player.C_Player import Player2

name = "collision"
wand = None
font = None
_Enemys = None
_Enemy1 = []
_PBullet = []
_EBullet = []
AnotherPlayer = []
E_NUM=0
item = []
potion = []
Time = 0.0
GameScore = 0
#SERVER_IP_ADDR ="127.0.0.1"
#SERVER_PORT = 19000
#SEND_TIME = 0

#
bgm = None

def enter():
    State.C_Game_framework.reset_time()
    create_world()


def exit():
    destroy_world()

#timer
def create_world():
    global _player, _Bg, _Enemy1, timer,GameScore, font, _EBullet, _PBullet, _Life,client_sock,tcp_controller,E_NUM, _Enemy_Data
    global MyNumber,AnotherPlayer,unpacked_all_player_data,game_data,P_NUM
    _Bg = BackGround()
    E_NUM =0
    _player = Player1(_Bg)
    AnotherPlayer =[]
    _Enemy1 = []
    _Life = Life(_player.life)
    #timer = Timer()
    client_sock = GameData.client_socket
    MyNumber = GameData.player_number
    #tcp_controller = TcpContoller()
    readystate = 0
    #client_sock = tcp_controller.tcp_client_init()
    t1 = threading.Thread(target=recv_thread, args=(client_sock,))
    t1.start()
    readystate = 0
    GameScore =0
    font = load_font('Resource\ENCR10B.TTF')

    Enemy1(0,0,0,0,0)
    Enemy2(0,0,0,0,0)
    EBullet(0,0)
    PBullet(0,0)

def recv_thread(client_sock):
    global AnotherPlayer, _Enemy1, _EBullet, _Bg

    _ETEMP = []
    _BTEMP = []
    _PTEMP = []
    current_time = time.clock()

    while 1:
        if current_time + 0.01 < time.clock():
            current_time = time.clock()

            Player_packed = DataStruct.pack_player_data(_player)
            client_sock.send(Player_packed)
            _player.isshoot = False

            #AllPlayerRECVED START
            all_player_packed = client_sock.recv(struct.calcsize('=iffffffffffffiiiBBBfff'))
            unpacked_all_player_data = DataStruct.unpack_all_player_data(all_player_packed)
            for i in range(unpacked_all_player_data['player_count']):
                if i != MyNumber:
                    newPlayer = Player2(unpacked_all_player_data['player_x'][i],
                                        unpacked_all_player_data['player_y'][i],
                                        unpacked_all_player_data['player_dir'][i],
                                        _Bg.window_left, _Bg.window_bottom,
                                        GameData.waitting_room_data['player_witch_select'][i])
                    _PTEMP.append(newPlayer)
            AnotherPlayer = _PTEMP
            if len(_PTEMP) > 0:
                _PTEMP = []
            #ALLPlayerRECVED END

            #GAMEOVER RECVED START
            packed_is_game_over = client_sock.recv(struct.calcsize('?'))
            GameData.is_game_over = (struct.unpack('?', packed_is_game_over))[0]
            if (GameData.is_game_over):
                print('game_over')
                State.C_Game_framework.change_state(State.C_Gameover_state)
                return
            #GAMEOVER RECVED END


            recved_NUM = client_sock.recv(struct.calcsize('=ii'))
            Recved_Number_Data = struct.unpack('=ii', recved_NUM)

            recved_IN_Window_NUM = client_sock.recv(struct.calcsize('=ii'))
            Recved_IN_Window_Number_Data = struct.unpack('=ii', recved_IN_Window_NUM)
            # SEND_ENEMY_DATA is ENEMY _X,_Y, TYPEUM = 0
            E_NUM = Recved_IN_Window_Number_Data[0]
            EB_NUM = Recved_IN_Window_Number_Data[1]
            # ?

            for i in range(0, E_NUM):
                _Enemy_packed = client_sock.recv(struct.calcsize('=fffi'))
                _Enemy_Data = DataStruct.unpack_enemy_data(_Enemy_packed)
                if _Enemy_Data[2] == 1:
                    newEnemy = Enemy1(_Enemy_Data[0], _Enemy_Data[1], _Enemy_Data[3], _Bg.window_left, _Bg.window_bottom)
                    #newEnemy.update(_player.x, _player.y, _Bg.window_left, _Bg.window_bottom, State)
                if _Enemy_Data[2] == 2:
                    newEnemy = Enemy2(_Enemy_Data[0], _Enemy_Data[1], _Enemy_Data[3], _Bg.window_left, _Bg.window_bottom)
                    #newEnemy.update(_player.x, _player.y, _Bg.window_left, _Bg.window_bottom, State)
                _ETEMP.append(newEnemy)
            _Enemy1 = _ETEMP
            if len(_ETEMP) > 0:
                _ETEMP = []




            for i in range(0, EB_NUM):
                _Bullet_packed = client_sock.recv(struct.calcsize('=fff'))
                _Bullet_Data = DataStruct.unpack_bullet_data(_Bullet_packed)
                if _Bullet_Data[0] == 1:  # EnemyBullet
                    newBullet = EBullet(_Bullet_Data[1], _Bullet_Data[2])

                elif _Bullet_Data[0] == 0:  # playerBullet
                    newBullet = PBullet(_Bullet_Data[1], _Bullet_Data[2])
                #newBullet.update()
                _BTEMP.append(newBullet)
            _EBullet = _BTEMP
            if len(_BTEMP) > 0:
                _BTEMP = []



pass



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

        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_g:
                GameData.is_game_over=True

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
    global E_NUM ,_Enemy_Data,unpacked_all_player_data

    _player.update(frame_time)

        #print("Enemy Packed : ", _enemylist)
#    timer.update(frame_time)



def draw(frame_time):
    global _Enemy1,_EBullet , AnotherPlayer,unpacked_all_player_data,MyNumber,_player
    clear_canvas()

    _player.draw(_player.x , _player.y)
    for enemy in _Enemy1:
        enemy.draw()
    for Another in AnotherPlayer:
        if Another != MyNumber :
            Another.draw()

    for ebullets in _EBullet:
        ebullets.draw()

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

def delete_object(objects):
    for object in objects:
        if object.alive == 0:
            objects.remove(object)



