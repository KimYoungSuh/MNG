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
def enter():
    global image1,image2,image3, font, _BG, _WAND, select_witch, game_data
    image1 = load_image('..\Player\Image_Player.png')
    image2 = load_image('..\Player\Image_Player2.png')
    image3 = load_image('..\Player\Image_Player3.png')

    font = load_font('ENCR10B.TTF')
    _BG = C_SellectBG()
    _WAND = Wand()
    select_witch = 0
    state = 0
    game_data = C_Lobby_state.game_data

    recv_thread = threading.Thread(target=recv_data, args=(struct.calcsize('BBBB?'),))
    recv_thread.start()

def exit():
    global image1,image2,image3, font, _BG, _WAND, select_witch,state

    del(image1)
    del(image2)
    del(image3)
    del(font)
    del(_BG)
    del(_WAND)
    del(select_witch)
    del(state)

def pause():
    pass

def resume():
    pass


def handle_events(frame_time):
    global select_witch, readyState, _WAND,state

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

                point = (_WAND.x,_WAND.y)

                #CHAR SELLECT
                if ( collide_point(point, char_sellect_1_box) ):
                    select_witch= 1
                    packed_data = struct.pack('=BBB', game_data.player_number, select_witch, 0)
                    game_data.client_socket.send(packed_data)
                if ( collide_point(point, char_sellect_2_box) ):
                    select_witch =2
                    packed_data = struct.pack('=BBB', game_data.player_number, select_witch, 0)
                    game_data.client_socket.send(packed_data)
                if (collide_point(point, char_sellect_3_box)):
                    select_witch=3
                    packed_data = struct.pack('=BBB', game_data.player_number, select_witch, 0)
                    game_data.client_socket.send(packed_data)

                #READY
                if(collide_point(point, ready_button_box)):
                    if select_witch != 0:
                        packed_data = struct.pack('=BBB', game_data.player_number, select_witch, 1)
                        game_data.client_socket.send(packed_data)


                #EXIT
                if(collide_point(point, exit_button)):
                    C_Game_framework.run(C_title_state)
            else:
                _WAND.handle_event(event)





def update(frame_time):
    global _WAND
    _WAND.update(frame_time)

    if (game_data.is_start):
        packed_data = struct.pack('=BBB', game_data.player_number, select_witch, 0)
        #todo:ready버튼누른사람은 send안하게 수정해야함
        if(game_data.player_number==2):
            print('버튼누른사람')
            State.C_Game_framework.run(C_collision)
        print('버튼안누른사람')
        game_data.client_socket.send(packed_data)
        State.C_Game_framework.run(C_collision)

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

#
def recv_data(recv_size):
    while 1:
        packed_waitting_room_data = game_data.client_socket.recv(recv_size)
        recved_data = struct.unpack('BBBBB', packed_waitting_room_data)
        game_data.waitting_room_data['player_count'] = recved_data[0]
        game_data.waitting_room_data['player1_witch_selcet'] = recved_data[1]
        game_data.waitting_room_data['player2_witch_selcet'] = recved_data[2]
        game_data.waitting_room_data['player3_witch_selcet'] = recved_data[3]
        game_data.waitting_room_data['ready_state'] = recved_data[4]
        print(str(recved_data[4]))

        if (recved_data[4]==0b0011):
            game_data.ready_state=recved_data[4]
            game_data.is_start = True
            return

def draw(frame_time):
    global image1,image2,image3,_WAND
    clear_canvas()
    _BG.draw()
    image1.clip_draw(Scean_x * 3, 0, Scean_x, Scean_y, 140, 250)
    image2.clip_draw(Scean_x * 3, 0, Scean_x, Scean_y, 420, 250)
    image3.clip_draw(Scean_x * 3, 0, Scean_x, Scean_y, 700, 250)



    if select_witch == 1 :
        select_witchs()
        image1.clip_draw( Scean_x * 3, 0, Scean_x, Scean_y, 30+(170*game_data.player_number)+(230*(game_data.player_number-1)) , 600)
    if select_witch ==2 :
        select_witchs()
        image2.clip_draw(Scean_x * 3, 0, Scean_x, Scean_y, 30+(170*game_data.player_number)+(230*(game_data.player_number-1)) , 600)
    if select_witch ==3 :
        select_witchs()
        image3.clip_draw(Scean_x * 3, 0, Scean_x, Scean_y, 30+(170*game_data.player_number)+(230*(game_data.player_number-1)) , 600)

    #another player draw
    for i in range(1, game_data.waitting_room_data['player_count']+1):
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
