import socket
import time

from TCP.C_Pack import Pack
from Data.C_BulletData import *
from Data.C_EnemyData import *
from Data.C_PlayerData import *
from Data.C_RoomData import *
from Data.C_StructSet import *
from State import C_collision
data_struct = Pack

class TcpContoller:
    SERVER_IP_ADDR ="127.0.0.1"
    SERVER_PORT = 19000


    client_socket=socket

    def tcp_client_init(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.SERVER_IP_ADDR, self.SERVER_PORT))
        return self.client_socket

    def loof(self):
        while 1:
            while 1:
                #todo: 게임중
                data = "Hello world"
                self.client_socket.sendall(C_collision.DATA_PACK_ENEMY)
                print("send data = ", data)
                self.recv_is_game_over()

            #todo: 리더보드

    def recv_is_game_over(self):
        # recv is_game_over
        packed_is_game_over = self.client_socket.recv(1)
        is_game_over = data_struct.unpack_is_game_over(packed_is_game_over)
        print('i\'m recv ', is_game_over)
        time.sleep(1)


    def exit(self):
        self.client_socket.close()
        print("SOCKET closed... END")


    #Lobby selection 0 = LOBBY_DATA, selection 1 = ROOM_DATA, selection 2 = JOIN, selection 3 = CREATE
    def send_create_room(client_socket, player_number, room_name, full_player, player_name):
        selection = 3
        packed_selection = data_struct.pack_integer(selection)
        client_socket.send(packed_selection)
        room_data = RoomData().room_data
        room_data['host_number'] = player_number
        room_data['room_name'] = room_name
        room_data['full_player'] = full_player
        room_data['player_name1'] = player_name
        create_room = data_struct.pack_room_data(room_data)
        client_socket.send(create_room)
        packed_can_make_room = client_socket.recv(data_struct.boolean_size)
        return data_struct.unpack_boolean(packed_can_make_room)


    def recv_lobby_data(client_socket):
        selection = 0
        packed_selection = data_struct.pack_integer(selection)
        client_socket.send(packed_selection)
        packed_room_count = client_socket.recv(data_struct.integer_size)
        room_count = data_struct.unpack_integer(packed_room_count)

        rooms_data = []

        for i in range(room_count):
            packed_room_data = client_socket.recv(data_struct.room_data_size)
            room_data = data_struct.unpack_room_data(packed_room_data)
            rooms_data.append(room_data)

        for room in rooms_data:
            print(room["room_name"])

        return rooms_data

    def send_join_room(client_socket, room_number, player_name, player_number):
        selection = 2
        packed_selection = data_struct.pack_integer(selection)
        client_socket.send(packed_selection)
        join_request_data = {
            'room_number': room_number,
            'player_name': player_name,
            'player_number': player_number
        }
        join_room = data_struct.pack_join_request_data(join_request_data)
        client_socket.send(join_room)

        packed_room_data = client_socket.recv(Pack.room_data_size)
        room_data = Pack.unpack_room_data(packed_room_data)

        if room_data['is_start'] == True: #3 = 시작 1 = 참가가능, 2 = 풀방
           return 3
        elif (room_data['full_player'] == 4 and room_data['player_name4'] == 'default_name') or\
            (room_data['full_player'] == 3 and room_data['player_name3'] == 'default_name') or\
            (room_data['full_player'] == 2 and room_data['player_name2'] == 'default_name'):
            return 1
        else:
            return 2

    #Wait Room
    def send_ready_state(self, is_ready):
        packed_is_ready = Pack.pack_is_game_over(is_ready)
        self.client_socket.send(packed_is_ready)



