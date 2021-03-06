import socket
import time

from TCP.C_Pack import DataStruct
from Data.C_BulletData import *
from Data.C_EnemyData import *
from Data.C_PlayerData import *
from Data.C_RoomData import *
from Data.C_StructSet import *

data_struct = DataStruct

class TcpContoller:
    SERVER_IP_ADDR ="127.0.0.1"
    SERVER_PORT = 19000


    client_socket=socket

    def tcp_client_init(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.SERVER_IP_ADDR, self.SERVER_PORT))

    def loof(self):
        while 1:
            while 1:
                #todo: 게임중
                data = "Hello world"
                self.client_socket.sendall(data_struct.pack_enemy_data())
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


    #Lobby
    def send_create_room(self, host_number, room_name, full_player, player_name):
        #방 정보를 모두 불러들이면 서버 내 최대 방 개수 확인할필요없음
        room_data = {
            'room_number': 0,
            'host_number': host_number,
            'room_name': room_name,
            'full_player': full_player,
            'player_name1': player_name,
            'player_name2': 0,
            'player_name3': 0,
            'player_name4': 0,
            'is_started': False,
            'ready_player': 0
        }
        create_room = data_struct.pack_room_data(room_data)
        self.client_socket.send(create_room)

    def send_join_room(self, room_number, player_data):
        join_request_data = {
            'room_number': room_number,
            'player_name': player_data['player_name'],
            'player_number': player_data['player_number']
        }
        join_room = data_struct.pack_room_data(join_request_data)
        self.client_socket.send(join_room)
        #방 정보를 모두 불러들이면 구현할필요 없음 (임시)
        packed_room_is_full = self.client_socket.recv(1)
        room_is_full = DataStruct.unpack_room_is_full(packed_room_is_full)
        if(room_is_full):
            #disconnect room
            print("room is full")
        else:
            #connect room
            print("connecting")
            pass

    #Wait Room
    def send_ready_state(self, is_ready):
        packed_is_ready = DataStruct.pack_is_game_over(is_ready)
        self.client_socket.send(packed_is_ready)




tcp_controller = TcpContoller()
tcp_controller.tcp_client_init()
tcp_controller.loof()
tcp_controller.exit()