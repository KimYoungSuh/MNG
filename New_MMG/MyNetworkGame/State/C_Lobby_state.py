from pico2d import *


from State import C_Game_framework
from State import C_Game_data
from State import C_CharSellect_State
from Background.C_LobbyBG import C_LobbyBG
from C_Wand import Wand
from TCP.C_TcpController import TcpContoller
from TCP.C_Pack import DataStruct

name = "Lobby"
image = None
_BG = None
_WAND = None
font = None
game_data = None
selection_image = None
selection = -1
rooms_data = []
delta_time = 2

COLLISION_BOX = [
    (79, 614, 1123, 719),
    (79, 507, 1123, 614),
    (79, 401, 1123, 507),
    (79, 296, 1123, 401),
    (79, 83, 372, 303),
    (453, 83, 747, 303),
    (828, 83, 1123, 303),
    (1005, 719, 1123, 823)
]


def select_room1(): #방 누를 시 정보 출력
    global selection
    selection = 1

def select_room2():
    global selection
    selection = 2


def select_room3():
    global selection
    selection = 3


def select_room4():
    global selection
    selection = 4


def reset_lobby(): #로비 정보 요청
    global rooms_data, delta_time
    print('r')
    if delta_time >= 2:
        delta_time = 0
        print("OK")
        rooms_data = TcpContoller.recv_lobby_data(game_data.client_socket)
        for room in rooms_data:
            print(room['room_name'])
        print(rooms_data)


def join_room(): # 참가 요청
    if selection > len(rooms_data) or selection < 0 :
        return
    result = TcpContoller.send_join_room(game_data.client_socket, rooms_data[selection-1]['room_number'], "Witch2")

    if result == 1:
        C_Game_framework.push_state(C_CharSellect_State)
    elif result == 2:
        print('is full')
    elif result == 3:
        print('is started')


def create_room(): # 생성 요청
    global game_data
    room_number = TcpContoller.send_create_room(game_data.client_socket, game_data.player_number, "TEST_ROOM", 3, "Witch")
    if room_number != -1:
        C_Game_framework.push_state(C_CharSellect_State)
    else:
        pass
        #방 생성 실패시

def exit_lobby():
    C_Game_framework.pop_state()


handle_function = [
    select_room1,
    select_room2,
    select_room3,
    select_room4,
    join_room,
    create_room,
    exit_lobby,
    reset_lobby
]

def collide_point(point, box):
    x_point, y_point = point
    left_b, bottom_b, right_b, top_b = box

    if x_point < left_b:
        return False
    if x_point > right_b:
        return False
    if y_point > top_b:
        return False
    if y_point < bottom_b:
        return False

    return True

def enter():
    global _BG, _WAND, font, game_data, selection_image
    font = load_font('..\Resource\ENCR10B.TTF')
    _BG = C_LobbyBG()
    _WAND = Wand()
    selection_image = load_image('..\Resource\Image_Lobby_Select.png')

    game_data = C_Game_data.GameData
    tcp_controller = TcpContoller()
    client_sock = tcp_controller.tcp_client_init()
    game_data.client_socket = client_sock

    packed_player_number = client_sock.recv(DataStruct.integer_size)
    player_number = DataStruct.unpack_integer(packed_player_number)

    game_data.player_number = player_number

    reset_lobby()

def exit():
    global _BG, _WAND, font
    del(font)
    del(_BG)
    del(_WAND)

def pause():
    pass

def resume():
    pass

def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            C_Game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                C_Game_framework.quit()
            elif event.type == SDL_MOUSEBUTTONDOWN:
                for i in range(0, 8):
                    if collide_point((_WAND.x, _WAND.y), COLLISION_BOX[i]):
                        handle_function[i]()
                        break;
            else:
                _WAND.handle_event(event)


def update(frame_time):
    global delta_time
    delta_time += frame_time

def draw(frame_time):
    global rooms_data
    clear_canvas()
    _BG.draw()
    if selection >= 1:
        selection_image.draw(600, (775 - (107 * selection)))
    for i in range(len(rooms_data)):
        font.draw(100, (668 - (107 * i)), 'Room name : %s' % (rooms_data[i]['room_name']))

    _WAND.draw()
    update_canvas()



