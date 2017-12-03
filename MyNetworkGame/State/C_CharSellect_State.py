import State.C_Game_framework
from pico2d import *
from C_Wand import Wand
from State import C_collision
from State import C_Game_framework
from State import C_Lobby_state
from State import C_title_state
from Background.C_SellectBG import C_SellectBG
from TCP.C_TcpController import TcpContoller
from State import C_Game_data
from Data.C_WaittingRoomData import WaittingRoomData
import struct
import threading
import socket
name = "Char_sellect"
image1 = None
image2= None
image3 = None
font = None
sel = None
Scean_x, Scean_y = 82, 105
select_witch =0
_WAND = None
state =0
readystate= 0
recv_thread_isRun=0
recv_thread2_isRun =0
PLAYER_NUM = 0
GAME_STATE = 0

def enter():
    global GAME_STATE,image1,image2,image3, font, _BG, _WAND, select_witch, game_data, PLAYER_NUM
    global recv_thread, recv_thread_isRun, recv_thread2, recv_thread2_isRun
    image1 = load_image('..\Player\Image_Player.png')
    image2 = load_image('..\Player\Image_Player2.png')
    image3 = load_image('..\Player\Image_Player3.png')
    GAME_STATE =0
    recv_thread_isRun = 0
    recv_thread2_isRun =0
    font = load_font('ENCR10B.TTF')
    _BG = C_SellectBG()
    _WAND = Wand()
    select_witch = 0
    PLAYER_NUM = 0
    game_data = C_Lobby_state.game_data
    game_data.client_socket.send(b'JOIN!')

    packed_player_data = game_data.client_socket.recv(100)
    print('packed_player_data  :' , struct.unpack('is',packed_player_data) )
    game_data.player_number = struct.unpack('is',packed_player_data)[0]
    R_TEXT = struct.unpack('is',packed_player_data)[1]

    recv_thread = threading.Thread(target=recv_data,args=(struct.calcsize('=BBBBBBBi'),))
    recv_thread2 = threading.Thread(target=recv_data2,args=(struct.calcsize('=BBBBBBB'),))

    #game_data.player_number = (struct.unpack('i',packed_player_data))
    #game_data.watting_room_data = WaittingRoomData().waitting_room_data
    #game_data.watting_room_data['player_count']=game_data.player_number


def exit():
    global image1,image2,image3, font, _BG, _WAND, select_witch,state
    game_data.client_socket.send(b'Out')
    del(image1)
    del(image2)
    del(image3)
    del(font)
    del(_BG)
    del(_WAND)

    del(select_witch)

def pause():
    pass

def resume():
    pass


def handle_events(frame_time):
    global select_witch,  _WAND,state,GAME_STATE,readystate

    global recv_thread, recv_thread_isRun, recv_thread2, recv_thread2_isRun

    char_sellect_1_box = (30, 40, 275, 350)
    char_sellect_2_box = (305, 40, 545, 350)
    char_sellect_3_box = (580, 40, 820, 350)
    ready_button_box = (905, 230, 1115, 330)
    exit_button = (905, 90, 115, 190)
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            State.C_Game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                State.C_Game_framework.quit()
            elif (event.type) == (SDL_MOUSEBUTTONDOWN):
                point = (_WAND.x, _WAND.y)
                if (collide_point(point, char_sellect_1_box)):
                                select_witch= 1
                                readystate= 0
                                game_data.client_socket.sendall(b'Sellect')
                                packed_data = struct.pack('=BBi', game_data.player_number, select_witch, readystate)
                                game_data.client_socket.send(packed_data)
                                if recv_thread2_isRun == 0:
                                    recv_thread2_isRun = 1
                                    recv_thread2.run()

                if ( collide_point(point, char_sellect_2_box) ):

                                select_witch =2
                                readystate= 0
                                game_data.client_socket.sendall(b'Sellect')
                                packed_data = struct.pack('=BBi', game_data.player_number, select_witch, readystate)
                                game_data.client_socket.send(packed_data)
                                if recv_thread2_isRun == 0:
                                    recv_thread2_isRun = 1
                                    recv_thread2.run()
                if (collide_point(point, char_sellect_3_box)):
                                select_witch=3
                                readystate= 0
                                game_data.client_socket.sendall(b'Sellect')
                                packed_data = struct.pack('=BBi', game_data.player_number, select_witch, readystate)
                                game_data.client_socket.send(packed_data)
                                if recv_thread2_isRun == 0:
                                    recv_thread2_isRun = 1
                                    recv_thread2.run()
                #READY!
                if(collide_point(point, ready_button_box)):
                                if readystate == 0 :
                                    if select_witch != 0 :
                                        readystate = 1

                                        game_data.client_socket.sendall(b'Ready')
                                        packed_data = struct.pack('=BBi', game_data.player_number, select_witch,readystate)
                                        game_data.client_socket.send(packed_data)
                                        if recv_thread_isRun == 0:
                                            recv_thread_isRun = 1
                                            recv_thread.start()
                                elif readystate ==1 :
                                    if select_witch != 0 :
                                        game_data.client_socket.sendall(b'Ready')
                                        readystate = 0
                                        packed_data = struct.pack('=BBi', game_data.player_number, select_witch,readystate)
                                        game_data.client_socket.send(packed_data)


            #EXIT
                if (collide_point(point, exit_button)):
                                game_data.client_socket.sendall(b'Out')
                                packed_data = struct.pack('=BBi', game_data.player_number, 0, 0)
                                game_data.client_socket.send(packed_data)
                                # close Socket
                                C_Game_framework.change_state(C_title_state)

            else:
                _WAND.handle_event(event)

def collide_point(point, box):
    x_point, y_point = point
    left_b, bottom_b, right_b, top_b = box

    if(left_b>x_point):
        return False
    if(right_b<x_point):
        return False
    if(top_b<y_point):
        return False
    if(bottom_b>y_point):
        return False
    return True


def send_packed_Player_Sellect2(Packed) :
    global PLAYER_NUM, GAME_STATE
    print('Packed :', Packed)
    game_data.client_socket.send(Packed)
    print('LineEndofSendPackedPlayerSellect2')
    #recv_thread = threading.Thread(target=recv_data, args=(struct.calcsize('BBBBBBBi'),))
    #recv_thread.start()




def update(frame_time):
    global _WAND, GAME_STATE
    _WAND.update(frame_time)
    if GAME_STATE ==1:
        game_data.client_socket.sendall(b'InGame')
        C_Game_framework.run(C_collision)


#
def recv_data(recv_size):
    global GAME_STATE,readystate

    while GAME_STATE ==0:

        packed_waitting_room_data = game_data.client_socket.recv(recv_size)
        print('packed_waitting_room_data :' , packed_waitting_room_data)
        recved_data = struct.unpack('=BBBBBBBi', packed_waitting_room_data)
        game_data.waitting_room_data['player_count'] = recved_data[0]
        game_data.waitting_room_data['player1_witch_selcet'] = recved_data[1]
        game_data.waitting_room_data['player2_witch_selcet'] = recved_data[2]
        game_data.waitting_room_data['player3_witch_selcet'] = recved_data[3]
        game_data.waitting_room_data['player1_ready_state'] = recved_data[4]
        game_data.waitting_room_data['player2_ready_state'] = recved_data[5]
        game_data.waitting_room_data['player3_ready_state'] = recved_data[6]
        GAME_STATE = int(recved_data[7])
        print('GAME_STATE :', GAME_STATE )

def recv_data2(recv_size):
    global readystate, GAME_STATE

    while readystate ==1:
        print('Hi im recv2 Thread')
        packed_waitting_room_data = game_data.client_socket.recv(recv_size)
        print('packed_waitting_room_data :', packed_waitting_room_data)
        recved_data = struct.unpack('=BBBBBBBi', packed_waitting_room_data)
        game_data.waitting_room_data['player_count'] = recved_data[0]
        game_data.waitting_room_data['player1_witch_selcet'] = recved_data[1]
        game_data.waitting_room_data['player2_witch_selcet'] = recved_data[2]
        game_data.waitting_room_data['player3_witch_selcet'] = recved_data[3]
        game_data.waitting_room_data['player1_ready_state'] = recved_data[4]
        game_data.waitting_room_data['player2_ready_state'] = recved_data[5]
        game_data.waitting_room_data['player3_ready_state'] = recved_data[6]
        GAME_STATE = int(recved_data[7])



def draw(frame_time):
    global image1,image2,image3,_WAND
    clear_canvas()
    _BG.draw()
    image1.clip_draw(Scean_x * 3, 0, Scean_x, Scean_y, 140, 250)
    image2.clip_draw(Scean_x * 3, 0, Scean_x, Scean_y, 420, 250)
    image3.clip_draw(Scean_x * 3, 0, Scean_x, Scean_y, 700, 250)
    #font.draw(160, 430, 'Wand_X = %d' % (_WAND.x))
    #font.draw(160, 460, 'Wand_Y = %d' % (_WAND.y))


    #My
    if select_witch == 1 :
        select_witchs()
        image1.clip_draw( Scean_x * 3, 0, Scean_x, Scean_y, 30+(170*game_data.player_number)+(230*(game_data.player_number-1)) , 600)
    if select_witch ==2 :
        select_witchs()
        image2.clip_draw(Scean_x * 3, 0, Scean_x, Scean_y, 30+(170*game_data.player_number)+(230*(game_data.player_number-1)) , 600)
    if select_witch ==3 :
        select_witchs()
        image3.clip_draw(Scean_x * 3, 0, Scean_x, Scean_y, 30+(170*game_data.player_number)+(230*(game_data.player_number-1)) , 600)




    for i in range(1, PLAYER_NUM+1):
        if(i != game_data.player_number):
            temp = 'player' + str(i) + '_witch_selcet'
            temp_select_witch = game_data.waitting_room_data[temp]
            if temp_select_witch == 1:
                select_witchs()
                image1.clip_draw(Scean_x * 3, 0, Scean_x, Scean_y,
                                 30 + (170 * i) + (230 * (i - 1)), 600)
            if temp_select_witch == 2:
                select_witchs()
                image2.clip_draw(Scean_x * 3, 0, Scean_x, Scean_y,
                                 30 + (170 * i) + (230 * (i - 1)), 600)
            if temp_select_witch == 3:
                select_witchs()
                image3.clip_draw(Scean_x * 3, 0, Scean_x, Scean_y,
                                 30 + (170 * i) + (230 * (i - 1)), 600)


    _WAND.draw()
    update_canvas()


def select_witchs():
    return select_witch
