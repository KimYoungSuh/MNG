import State.C_Game_framework
from pico2d import *
from C_Wand import Wand
from State import C_collision
from State import C_Game_framework
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

def enter():
    global image1,image2,image3, font, _BG, _WAND, select_witch, game_data
    image1 = load_image('..\Player\Image_Player.png')
    image2 = load_image('..\Player\Image_Player2.png')
    image3 = load_image('..\Player\Image_Player3.png')

    font = load_font('ENCR10B.TTF')
    _BG = C_SellectBG()
    _WAND = Wand()
    select_witch = 0
    game_data = C_Game_data.GameData()
    game_data.player_number = 1
    tcp_controller = TcpContoller()
    client_sock = tcp_controller.tcp_client_init()
    game_data.client_socket=client_sock
    packed_player_data = game_data.client_socket.recv(4)
    game_data.player_number = (struct.unpack('i',packed_player_data))[0]
    game_data.watting_room_data = WaittingRoomData().waitting_room_data
    game_data.watting_room_data['player_count']=game_data.player_number

    recv_thread = threading.Thread(target=recv_data, args=(struct.calcsize('BBBB?'),))
    recv_thread.start()

def exit():
    global image1,image2,image3, font, _BG, _WAND, select_witch
    del(image1)
    del(image2)
    del(image3)
    del(font)
    del(_BG)
    del(_WAND)

def pause():
    pass

def resume():
    pass


def handle_events(frame_time):
    global select_witch, readyState, _WAND
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            State.C_Game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                State.C_Game_framework.quit()
            elif (event.type) == (SDL_MOUSEBUTTONDOWN):
                if _WAND.x > 30 :
                    if _WAND.x < 275:
                        if _WAND.y > 40:
                            if _WAND.y < 350:
                                select_witch= 1
                if _WAND.x > 305:
                    if _WAND.x < 545:
                        if _WAND.y > 40:
                            if _WAND.y < 350:
                                select_witch =2
                if _WAND.x > 580:
                    if _WAND.x < 820:
                        if _WAND.y > 40:
                            if _WAND.y < 350:
                                select_witch=3
                packed_data = struct.pack('BB', game_data.player_number, select_witch)
                game_data.client_socket.send(packed_data)

                #READY!
                if _WAND.x > 905 :
                    if _WAND.x < 1115:
                        if _WAND.y > 230:
                            if _WAND.y < 330:
                                readyState= 1
                                if select_witch != 0 :
                                    C_Game_framework.run(C_collision)
                                    State.C_Game_framework.run(C_collision)
                #EXIT
                if _WAND.x > 905 :
                    if _WAND.x < 1115:
                        if _WAND.y > 90:
                            if _WAND.y < 190:
                                C_Game_framework.run(C_title_state)
                                State.C_Game_framework.run(C_title_state)
            else:
                _WAND.handle_event(event)





def update(frame_time):
    global _WAND
    _WAND.update(frame_time)



#
def recv_data(recv_size):
    while 1:
        packed_waitting_room_data = game_data.client_socket.recv(recv_size)
        recved_data = struct.unpack('BBBB?', packed_waitting_room_data)
        game_data.waitting_room_data['player_count'] = recved_data[0]
        game_data.waitting_room_data['player1_witch_selcet'] = recved_data[1]
        game_data.waitting_room_data['player2_witch_selcet'] = recved_data[2]
        game_data.waitting_room_data['player3_witch_selcet'] = recved_data[3]
        game_data.waitting_room_data['ready_state'] = recved_data[4]

def draw(frame_time):
    global image1,image2,image3, _WAND
    clear_canvas()
    _BG.draw()
    image1.clip_draw(Scean_x * 3, 0, Scean_x, Scean_y, 140, 250)
    image2.clip_draw(Scean_x * 3, 0, Scean_x, Scean_y, 420, 250)
    image3.clip_draw(Scean_x * 3, 0, Scean_x, Scean_y, 700, 250)
    #font.draw(160, 430, 'Wand_X = %d' % (_WAND.x))
    #font.draw(160, 460, 'Wand_Y = %d' % (_WAND.y))



    if select_witch == 1 :
        select_witchs()
        image1.clip_draw( Scean_x * 3, 0, Scean_x, Scean_y, 30+(170*game_data.player_number)+(230*(game_data.player_number-1)) , 600)
    if select_witch ==2 :
        select_witchs()
        image2.clip_draw(Scean_x * 3, 0, Scean_x, Scean_y, 30+(170*game_data.player_number)+(230*(game_data.player_number-1)) , 600)
    if select_witch ==3 :
        select_witchs()
        image3.clip_draw(Scean_x * 3, 0, Scean_x, Scean_y, 30+(170*game_data.player_number)+(230*(game_data.player_number-1)) , 600)

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
