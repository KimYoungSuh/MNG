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
            self.recv_is_game_over()

    def recv_is_game_over(self):
        # recv is_game_over
        packed_is_game_over = self.client_socket.recv(1)
        is_game_over = data_struct.unpack_is_game_over(packed_is_game_over)
        print('i\'m recv ', is_game_over)
        time.sleep(1)


    def exit(self):
        self.client_socket.close()
        print("SOCKET closed... END")



tcp_controller = TcpContoller()
tcp_controller.tcp_client_init()
tcp_controller.loof()
tcp_controller.exit()