import socket
import threading
import time

from GameSys.C_GameSysMain import *
from Data.C_BulletData import *
from Data.C_EnemyData import *
from Data.C_PlayerData import *
from Data.C_RoomData import *
from Data.C_StructSet import *
from TCP.C_Pack import *
_enemylist= []
_enemylist2= []
data_struct = Pack
GAME_STATE =0
game_sys_main = None

class TcpController:
    global GAME_STATE
    GAME_STATE = 0
    PORT = 19000
    IP = ''
    MAX_BIND = 5
    def tcp_server_init(self):
        global game_sys_main
        game_sys_main = GameSysMain()
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
            client_thread = []
            client_thread.append(threading.Thread(target=TcpController.process_client, args=(client_socket,)))
            client_thread[-1].start()



    '''
    클라이언트와 통신하는 스레드입니다.
    로직을 이안에 쓰는것은 지양합니다.
    함수를 호출하여 수정을 최소화 하세요.
    '''
    def process_client(client_socket):
        game_sys_main.player_count += 1
        player_number = game_sys_main.empty_player_number()

        packed_player_number = data_struct.pack_integer(player_number)
        client_socket.send(packed_player_number)

        TcpController.recv_lobby_state(client_socket)


        #game_sys_main.join_player(PlayerData)
        # player_data_size = struct.calcsize('=fff')
        #접속한 플레이어를 구분짓는 넘버링
        #player_number = game_sys_main.waitting_room_data['player_count']

        #플레이어넘버를 보냄
        arfter_time = time.time() + (1 / 30)

        if GAME_STATE != 1:
            recv_waiiting_room_thread = threading.Thread(target=TcpController.recv_waitting_room_thread, args=(client_socket, player_number))
            recv_waiiting_room_thread.start()



            while 1 :
                #todo:
                if (time.time() > arfter_time):
                    arfter_time = time.time() + 1 / 10
                    if(not game_sys_main.is_start):
                        TcpController.send_waitting_room_data(client_socket)
                    else:
                        TcpController.send_waitting_room_data(client_socket)
                        break

            at_first= True
            game_sys_main.players_data[0] = (400,400,3)
            game_sys_main.players_data[1] = (400,400,3)

            print('In LOCAL_AREA')

            game_data_thread = threading.Thread(target=TcpController.recv_game_data,args=(client_socket, player_number))
            game_data_thread.start()
            while 1:
                if (time.time() > arfter_time):
                    arfter_time = time.time() + 1 / 30

                    # todo :recv_player_data
                    # todo :recv_bullet_data
                    # todo :충돌체크하시오
                    # todo :if isdameged




                    #send_players_data
                    packed_players_data = data_struct.pack_players_data(game_sys_main.players_data)
                    temp=Pack.unpack_players_data(packed_players_data)
                    #print('test',temp)
                    client_socket.send(packed_players_data)

                    #print('Line3')
                    #print("Player Packed : ", _Player_Packed)

            #에너미 받기
            #data2 = client_socket.recv(struct.calcsize('=ffffI'))
            #_enemylist.append(data_struct.unpack_enemy_data(data2))
            #print("Enemy Packed : ", _enemylist)

            #총알 받기
            #data3 = client_socket.recv(struct.calcsize('=ffffff'))
            #_bullet_packed = (data_struct.unpack_bullet_data(data3))
            #print("_bullet_packed : ", _bullet_packed)

            #data = client_socket.recv(player_data_size)
            #game_sys_main.players_data[player_number-1] = data_struct.unpack_player_data(data)
            #print(game_sys_main.players_data[player_number-1])
            #print(_Player_Packed)
            #_enemylist.append(data_struct.unpack_enemy_data(data))
            #print(_enemylist)

            #TcpController.send_is_game_over(client_socket)
            # todo :gamelogic damaged
            # todo :send_player_data

            # todo :send_enemy_data

            # todo :send_bullet_data
            # todo :리더보드

    #Lobby
    '''
    selection 0 = LOBBY_DATA, selection 1 = ROOM_DATA, selection 2 = JOIN, selection 3 = CREATE
    무슨 선택인지 확인하고 선택에 따라 실행, 
    '''
    def recv_lobby_state(client_socket):
        in_lobby = True
        while(in_lobby):
            packed_Selection = client_socket.recv(data_struct.integer_size)
            selection = data_struct.unpack_integer(packed_Selection)

            if selection == 0:
                TcpController.send_lobby_data(client_socket)
            elif selection == 2:
                if TcpController.send_room_data(client_socket):
                    in_lobby = False
            elif selection == 3:
                if TcpController.recv_create_room(client_socket):
                    in_lobby = False


    def send_room_data(client_socket):
        packed_request_data = client_socket.recv(data_struct.join_request_data_size)
        unpack_join_request_data = data_struct.unpack_join_request_data(packed_request_data)

        room_count = game_sys_main.exist_room_count()
        for i in range(room_count):
            if game_sys_main.rooms_data[i]['room_number'] == unpack_join_request_data['room_number']:
                packed_room_data = data_struct.pack_room_data(game_sys_main.rooms_data[i])
                client_socket.send(packed_room_data)
                full_plyaer = game_sys_main.rooms_data[i]['full_player']
                if(full_plyaer >= 2 and game_sys_main.rooms_data[i]['player_name2'] == 'default_name'):
                    game_sys_main.rooms_data[i]['player_name2'] = unpack_join_request_data['player_name']
                    return True
                elif(full_plyaer >= 3 and game_sys_main.rooms_data[i]['player_name3'] == 'default_name'):
                    game_sys_main.rooms_data[i]['player_name3'] = unpack_join_request_data['player_name']
                    return True
                elif(full_plyaer == 4 and game_sys_main.rooms_data[i]['player_name4'] == 'default_name'):
                    game_sys_main.rooms_data[i]['player_name4'] = unpack_join_request_data['player_name']
                    return True
        return False

    def send_lobby_data(client_socket):
        room_count = game_sys_main.exist_room_count()
        packed_room_count = data_struct.pack_integer(room_count)
        client_socket.send(packed_room_count)
        for i in range(room_count):
            packed_room_data = data_struct.pack_room_data(game_sys_main.rooms_data[i])
            client_socket.send(packed_room_data)

    def recv_create_room(client_socket):
        packed_create_room_data = client_socket.recv(data_struct.room_data_size) #수정
        create_room_data = data_struct.unpack_room_data(packed_create_room_data)
        rooms_count = game_sys_main.exist_room_count()
        if  rooms_count < game_sys_main.maxroomcount:
            game_sys_main.rooms_data[rooms_count] = create_room_data
            room_is_not_full = True
        else:
            room_is_not_full = False
        packed_room_is_full = data_struct.pack_boolean(room_is_not_full)
        client_socket.send(packed_room_is_full)
        return room_is_not_full

    # ROOM
    def recv_waitting_room_thread(client_socket, player_number):
        while 1:
            if(game_sys_main.is_start):
                print(player_number,"정상적으로 recv쓰래드 종료")
                return
            else :
                try:
                    TcpController.recv_waitting_room_data(client_socket, player_number)
                except socket.error:
                    print(player_number,game_sys_main.is_start)
                    print("비정상적 종료로 recv쓰래드가 종료됨")
                    return

    def recv_waitting_room_data(client_socket, player_number):
        recv_packed_data = client_socket.recv(struct.calcsize('=BBB'))
        recv_data = struct.unpack('=BBB', recv_packed_data)

        if(not recv_data[2]==0):
            temp = 'player' + str(recv_data[0]) + '_witch_selcet'

            game_sys_main.waitting_room_data[temp] = recv_data[1]
            print(recv_data)
            print(player_number,"번 Player가 ", str(recv_data[1]), '번째 캐릭터를 선택하였습니다.')

        if (recv_data[2] == 1):
            #todo: ready state chage 함수로 만들 것
            ready_state = game_sys_main.waitting_room_data['ready_state']

            chang_ready_state = 1 << (player_number-1)
            game_sys_main.waitting_room_data['ready_state'] = ready_state ^ chang_ready_state

            if(game_sys_main.waitting_room_data['ready_state'] >> (player_number-1)&0b0001==1):
                temp = ''
            else:
                temp = '해제'
            print(player_number, '번 Player가 준비를',temp,'하였습니다.')

        if(game_sys_main.waitting_room_data['ready_state'] == 0b0011):
            print(player_number, '번 Player가 게임을 시작하였습니다.')
            game_sys_main.is_start=True

    def recv_game_data(client_socket, player_number):
        # 플레이어 데이터 받기
        while 1:
            data = client_socket.recv(struct.calcsize('=fff'))
            _Player_Data = data_struct.unpack_player_data(data)
            print(_Player_Data)
            game_sys_main.players_data[player_number - 1] = _Player_Data

    def send_waitting_room_data(client_socket):
        packed_data = struct.pack('BBBBB', game_sys_main.waitting_room_data['player_count'],
                                  game_sys_main.waitting_room_data['player1_witch_selcet'],
                                  game_sys_main.waitting_room_data['player2_witch_selcet'],
                                  game_sys_main.waitting_room_data['player3_witch_selcet'],
                                  game_sys_main.waitting_room_data['ready_state'])
        client_socket.send(packed_data)

    def send_is_game_over(socket):
         # 게임결과를 보냅니다
         packed_is_game_over = data_struct.pack_is_game_over(game_sys_main.is_game_over)
         socket.send(packed_is_game_over)

    def exit(self):
        TcpController.server_socket.close()
        print("SOCKET closed... END")
