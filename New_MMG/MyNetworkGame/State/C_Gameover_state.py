from pico2d import *


import State.C_title_state
import State.C_Game_framework
import State.C_title_state
from State.C_Game_data import GameData
import struct
from TCP.C_Pack import DataStruct


name = "Game Over"
image = None
#

def select_room1():
    pass


def select_room2():
    pass


def select_room3():
    pass


def select_room4():
    pass


def reset_lobby():
    pass


def join_room():
    pass


def create_room():
    pass


def exit_lobby():
    pass


def enter():
    global image, font, leader_board_list
    leader_board_list=[]
    image = load_image('..\State\Image_Gameover_state.jpg')
    font = load_font('..\ENCR10B.TTF')
    recv_leader_board()

def exit():
    global image
    del(image)


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
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                State.C_Game_framework.change_state(State.C_Title_state)



def update(frame_time):
    pass


def draw(frame_time):
    global image, leader_board_list, font
    clear_canvas()
    image.draw(600, 800)
    for i in range (0, len(leader_board_list)):
        font.draw(300, 500-i*40, '%d %s %s %s %s %d' % (i+1, leader_board_list[i][1],leader_board_list[i][3],leader_board_list[i][5],leader_board_list[i][7], leader_board_list[i][9]))

    update_canvas()

def recv_leader_board():
    client_sock=GameData.client_socket

    packed_leader_board_count = GameData.client_socket.recv(DataStruct.integer_size)
    leader_board_count = DataStruct.unpack_integer(packed_leader_board_count)
    for i in range(leader_board_count):
        packed_leader_bard = GameData.client_socket.recv(struct.calcsize('30s 30s 30s 30s i'))
        unpack_leader_board = struct.unpack('30s 30s 30s 30s i', packed_leader_bard)
        leader_board = (
            'p1 ', unpack_leader_board[0].decode('ascii').rstrip('\x00'),
            'p2 ', unpack_leader_board[1].decode('ascii').rstrip('\x00'),
            'p3 ', unpack_leader_board[2].decode('ascii').rstrip('\x00'),
            'time ', unpack_leader_board[3].decode('ascii').rstrip('\x00'),
            'score ', unpack_leader_board[4],
        )
        leader_board_list.append(leader_board)
    print(leader_board_list)




