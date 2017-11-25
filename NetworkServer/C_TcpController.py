import socket
import threading
import time
from C_DataStruct import DataStruct

data_struct= DataStruct

class TcpController:
    PORT = 19000
    IP = ''
    MAX_BIND = 5

    def tcp_server_init(self):
        TcpController.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TcpController.server_socket.bind((self.IP, self.PORT))
        TcpController.server_socket.listen(self.MAX_BIND)
        print('TCPServer Waiting for client on port %d'% self.PORT)
        print("=" * 50)
        print("[Thread version] 서버 초기화 완료")

    '''
    클라이언트의 접속을 accept()합니다.
    accept()되면 process_client쓰레드에 client소켓을 전달해주고 client소켓을 삭제합니다.
    '''
    def accept_loof(self):
        print("[정보] 접속 대기중...")
        print("=" * 50)
        while 1:
            client_socket, address = TcpController.server_socket.accept()
            print("I got a connection from ", address)
            t1 = threading.Thread(target=TcpController.process_client, args=(client_socket,))
            t1.start()

    '''
    정보교환이 이루어 집니다.
    정보교환 로직을 이안에 쓰는것은 지양합니다.
    함수를 호출하여 수정을 최소화 하세요.
    '''
    def process_client(socket):
        while 1:
            packed_is_game_over =data_struct.pack_is_game_over(False)
            socket.send(packed_is_game_over)
            time.sleep(1)



    def exit(self):
        TcpController.server_socket.close()
        print("SOCKET closed... END")