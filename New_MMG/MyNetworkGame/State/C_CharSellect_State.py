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
image_emotion = None
image_emotion2 = None
image_emotion3 = None
image_emotion4 = None
Scean_x, Scean_y = 82, 105
select_witch =0
select_imotion = 0
_WAND = None
state =0
readystate= False
recv_thread_isRun=0
recv_thread2_isRun =0
PLAYER_NUM = 0
GAME_STATE = 0
delta_time = 0.3
exit_state = False
image_ready = None
image_select = None
emotion_time = [0, 0, 0]
selected_box = [
    (198, 557),
    (463, 557),
    (728, 557),
    (988, 557)
]
image_box = [
    (168, 234),
    (373, 234),
    (578, 234),
    (973, 288)
]

select_box = [
    (78, 119, 258, 349),
    (283, 119, 463, 349),
    (488, 119, 668, 349),
    (689, 84, 811, 140),
    (689, 151, 811, 207),
    (689, 218, 811, 274),
    (689, 285, 811, 341),
    (827, 84, 1119, 206),
    (827, 227, 1119, 349)
]

emotion_box = [
    (269, 668),
    (534, 668),
    (799, 668),
    (1064, 668)
]

emotion_selected = [0,0,0]


def enter():
    global GAME_STATE,image1,image2,image3, font, _BG, _WAND, select_witch, game_data, PLAYER_NUM, select_imotion
    global recv_thread, recv_thread_isRun, recv_thread2, recv_thread2_isRun, image_ready, image_select
    global image_emotion, image_emotion2, image_emotion3, image_emotion4
    image1 = load_image('..\Player\Image_Player.png')
    image2 = load_image('..\Player\Image_Player2.png')
    image3 = load_image('..\Player\Image_Player3.png')
    image_ready = load_image('..\BackGround\Image_ready.png')
    image_select = load_image('..\BackGround\Image_select.png')
    image_emotion = load_image('..\BackGround\emotion_hello.png')
    image_emotion2 = load_image('..\BackGround\emotion_smile.png')
    image_emotion3 = load_image('..\BackGround\emotion_wait.png')
    image_emotion4 = load_image('..\BackGround\emotion_go.png')
    GAME_STATE =0
    recv_thread_isRun = 0
    font = load_font('ENCR10B.TTF')
    _BG = C_SellectBG()
    _WAND = Wand()
    select_witch = 0
    select_imotion = 0
    PLAYER_NUM = 0
    game_data = C_Lobby_state.game_data


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
    global select_witch,  _WAND,state,GAME_STATE, readystate, exit_state, select_imotion
    global recv_thread, recv_thread_isRun, recv_thread2, recv_thread2_isRun

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            State.C_Game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                State.C_Game_framework.quit()
            elif (event.type) == (SDL_MOUSEBUTTONDOWN):
                point = (_WAND.x, _WAND.y)
                for i in range(9):
                    if (collide_point(point, select_box[i])):
                        if i<= 2:
                            select_witch = i+1
                            readystate = False
                            break
                        elif i<= 6:
                            select_imotion = i-2
                        elif i == 8:
                                if readystate == False:
                                    if select_witch != 0:
                                        readystate = True

                                elif readystate == True:
                                    readystate = False
                        elif i == 7:
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
    global _WAND, GAME_STATE, select_witch , readystate, exit_state, delta_time, \
        game_data, emotion_selected, emotion_time, select_imotion

    _WAND.update(frame_time)
    delta_time += frame_time
    if delta_time >= 0.3:
        TcpContoller.send_in_room_data(game_data.client_socket, select_witch, readystate, exit_state, select_imotion)
        select_imotion = 0
        room_data = TcpContoller.receive_in_room_data(game_data.client_socket)
        game_data.waitting_room_data = room_data
        delta_time = 0
        print(room_data['emotion'])
    for i in range(0,3):
        if game_data.waitting_room_data['emotion'][i] != 0:
            emotion_selected[i] = game_data.waitting_room_data['emotion'][i]
            emotion_time[i] = 0

    #if GAME_STATE ==1:

    ready_count = 0
    for i in range(3):
        if game_data.waitting_room_data['player_ready_state'][i]:
            ready_count += 1
        emotion_time[i] += frame_time
    if ready_count == game_data.waitting_room_data['player_count']:
        C_Game_framework.push_state(C_collision)


def draw(frame_time):
    global image1,image2,image3,_WAND, game_data, readystate, select_box, image_box, emotion_box, emotion_selected
    global image_emotion, image_emotion2, image_emotion3, image_emotion4
    clear_canvas()
    _WAND.draw()
    _BG.draw()

    if readystate:
        image_ready.draw(image_box[3][0], image_box[3][1])

    if select_witch != 0:
        image_select.draw(image_box[select_witch-1][0], image_box[select_witch-1][1])

    image1.clip_draw(Scean_x * 3, 0, Scean_x, Scean_y, image_box[0][0], image_box[0][1])
    image2.clip_draw(Scean_x * 3, 0, Scean_x, Scean_y, image_box[1][0], image_box[1][1])
    image3.clip_draw(Scean_x * 3, 0, Scean_x, Scean_y, image_box[2][0], image_box[2][1])
    #font.draw(160, 430, 'Wand_X = %d' % (_WAND.x))
    #font.draw(160, 460, 'Wand_Y = %d' % (_WAND.y))

    image_set = [image1, image2, image3]
    image_set2 = [image_emotion4, image_emotion3, image_emotion2, image_emotion]

    for i in range(3):
        if emotion_time[i] <= 1.5 and emotion_selected[i] >= 1:
            image_set2[emotion_selected[i]-1].draw(emotion_box[i][0], emotion_box[i][1])

    for i in range(3):#수정
        if game_data.waitting_room_data['player_witch_select'][i] >= 1:
            image_set[game_data.waitting_room_data['player_witch_select'][i]-1].clip_draw(
            Scean_x * 3, 0, Scean_x, Scean_y, selected_box[i][0], selected_box[i][1])

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
