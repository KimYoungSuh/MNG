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
readystate= False
recv_thread_isRun=0
recv_thread2_isRun =0
PLAYER_NUM = 0
GAME_STATE = 0
delta_time = 0.3
exit_state = False

def enter():
    global GAME_STATE,image1,image2,image3, font, _BG, _WAND, select_witch, game_data, PLAYER_NUM
    global recv_thread, recv_thread_isRun, recv_thread2, recv_thread2_isRun
    image1 = load_image('..\Player\Image_Player.png')
    image2 = load_image('..\Player\Image_Player2.png')
    image3 = load_image('..\Player\Image_Player3.png')
    GAME_STATE =0
    recv_thread_isRun = 0
    font = load_font('ENCR10B.TTF')
    _BG = C_SellectBG()
    _WAND = Wand()
    select_witch = 0
    PLAYER_NUM = 0
    game_data = C_Lobby_state.game_data

    #recv_thread = threading.Thread(target=recv_data,args=(struct.calcsize('=BBBBBBBi'),))
    #recv_thread.start()

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
    global select_witch,  _WAND,state,GAME_STATE, readystate, exit_state
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
                                readystate= False

                if ( collide_point(point, char_sellect_2_box) ):
                                select_witch =2
                                readystate= False

                if (collide_point(point, char_sellect_3_box)):
                                select_witch=3
                                readystate= False

                #READY!
                if(collide_point(point, ready_button_box)):
                                if readystate == False:
                                    if select_witch != 0:
                                        readystate = True

                                elif readystate == True:
                                    readystate = False

            #EXIT
                if (collide_point(point, exit_button)):
                                # close Socket
                                exit_state = True
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

def update(frame_time):
    global _WAND, GAME_STATE, select_witch , readystate, exit_state, delta_time, game_data

    _WAND.update(frame_time)
    delta_time += frame_time
    if delta_time >= 0.3:
        TcpContoller.send_in_room_data(game_data.client_socket, select_witch, readystate, exit_state)
        room_data = TcpContoller.receive_in_room_data(game_data.client_socket)
        game_data.waitting_room_data = room_data
        delta_time = 0

    #if GAME_STATE ==1:

    ready_count = 0
    for i in range(3):
        if game_data.waitting_room_data['player_ready_state'][i]:
            ready_count += 1
    if ready_count == game_data.waitting_room_data['player_count']:
        C_Game_framework.push_state(C_collision)

def recv_data(recv_size):
    global GAME_STATE,readystate
    while GAME_STATE ==0:
        packed_waitting_room_data = game_data.client_socket.recv(recv_size)
        print('packed_waitting_room_data :' , packed_waitting_room_data)
        recved_data = struct.unpack('=BBBBBBBi', packed_waitting_room_data)
        game_data.waitting_room_data['player_count'] = recved_data[0]
        game_data.waitting_room_data['player1_witch_seledt'] = recved_data[1]
        game_data.waitting_room_data['player2_witch_seledt'] = recved_data[2]
        game_data.waitting_room_data['player3_witch_seledt'] = recved_data[3]
        game_data.waitting_room_data['player1_ready_state'] = recved_data[4]
        game_data.waitting_room_data['player2_ready_state'] = recved_data[5]
        game_data.waitting_room_data['player3_ready_state'] = recved_data[6]
        GAME_STATE = int(recved_data[7])
        print('GAME_STATE :', GAME_STATE )

def draw(frame_time):
    global image1,image2,image3,_WAND, game_data
    clear_canvas()
    _BG.draw()
    image1.clip_draw(Scean_x * 3, 0, Scean_x, Scean_y, 140, 250)
    image2.clip_draw(Scean_x * 3, 0, Scean_x, Scean_y, 420, 250)
    image3.clip_draw(Scean_x * 3, 0, Scean_x, Scean_y, 700, 250)
    #font.draw(160, 430, 'Wand_X = %d' % (_WAND.x))
    #font.draw(160, 460, 'Wand_Y = %d' % (_WAND.y))

    image_set = [image1, image2, image3]


    for i in range(3):#수정
        if game_data.waitting_room_data['player_witch_select'][i] >= 1:
            image_set[game_data.waitting_room_data['player_witch_select'][i]-1].clip_draw(
            Scean_x * 3, 0, Scean_x, Scean_y, 230 + (370 * i), 600)

    '''
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
    '''

    _WAND.draw()
    update_canvas()


def select_witchs():
    return select_witch
