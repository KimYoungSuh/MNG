import socket
import threading
import time
import random
from Enemy.C_Enemy import Enemy1
from Enemy.C_Enemy2 import Enemy2

from GameSys.C_GameSysMain import *
from Data.C_BulletData import *
from Data.C_EnemyData import *
from Data.C_PlayerData import *
from Data.C_RoomData import *
from Data.C_StructSet import *
from TCP.C_Pack import *
from Background.C_BG import BackGround

_Bg = None
data_struct = Pack
GAME_STATE =0
send_time =0
state = None
timer = None
_EnemyList = []
_Enemy= []
E_NUM = 0
player_number = 0
Enemy_packed = None
game_sys_main = None
'''
GAME_STATE
0 = WaitingRoom
1 = Playing
2 = GAMEOVER
'''
PLAYER_NUM = 0
E_NUM = 0

class Timer():
    def __init__(self):
        self.Whattime = 0
        self.EnemyNum = 0

    def update(self, frame_time):
        self.Whattime += frame_time
        if self.Whattime >= 1.5:
            self.Whattime = 0
            return True
        else :
            return False

class TcpController:
    global GAME_STATE, player_count, timer, _Bg, Enemy_packed, E_NUM, ready_state
    GAME_STATE = 0
    player_count =0
    PORT = 19000
    timer = Timer()
    ready_state = 0
    _Bg = BackGround()
    IP = ''
    E_NUM= 0
    player_number = 0
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
        global SEND_TIME, _Bg, player_number

        print("[정보] 접속 대기중...")
        print("=" * 50)
        player_number = 0

        '''
        Waitting Room
        '''

        while 1:
            client_socket, address = TcpController.server_socket.accept()

            print("I got a connection from ", address)
            client_thread = []
            client_thread.append(threading.Thread(target=TcpController.process_client, args=(client_socket,)))
            client_thread[-1].start()
             # game_sys_main.join_player(PlayerData)



    '''
    클라이언트와 통신하는 스레드입니다.
    로직을 이안에 쓰는것은 지양합니다.
    함수를 호출하여 수정을 최소화 하세요.
    '''
    def process_client(client_socket):
        global PLAYER_NUM, state, GAME_STATE, E_Data, ready_state, game_sys_main
        room_number = 0
        game_sys_main.player_count += 1
        player_number = game_sys_main.empty_player_number()

        packed_player_number = data_struct.pack_integer(player_number)
        client_socket.send(packed_player_number)

        room_number = TcpController.recv_lobby_state(client_socket, player_number) #in Lobby
        TcpController.send_in_room_data(client_socket, room_number, player_number) #in Room

        TcpController.send_in_game_data(client_socket, room_number, player_number)



    #Lobby
    '''
    selection 0 = LOBBY_DATA, selection 1 = ROOM_DATA, selection 2 = JOIN, selection 3 = CREATE
    '''
    def recv_lobby_state(client_socket, player_number):
        global game_sys_main
        in_lobby = True
        room_number = 0
        while in_lobby:
            packed_Selection = client_socket.recv(data_struct.integer_size)
            selection = data_struct.unpack_integer(packed_Selection)

            if selection == 0:
                TcpController.send_lobby_data(client_socket)
            elif selection == 2:
                room_number = TcpController.send_room_data(client_socket, player_number)
                if room_number != -1:
                    in_lobby = False
                    for i in range(3):
                        if game_sys_main.waitting_room_data[room_number]['player_number'][i] == -1:
                            game_sys_main.waitting_room_data[room_number]['player_number'][i] = player_number
                            break
            elif selection == 3:
                room_number = TcpController.recv_create_room(client_socket, player_number)
                if room_number != -1:
                    in_lobby = False
                    for i in range(3): #추후 수정
                        if game_sys_main.waitting_room_data[room_number]['player_number'][i] == -1:
                            game_sys_main.waitting_room_data[room_number]['player_number'][i] = player_number
                            break
        print(room_number)
        return room_number


    def send_room_data(client_socket, player_number):
        global game_sys_main
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
                    return game_sys_main.rooms_data[i]['room_number']
                elif(full_plyaer >= 3 and game_sys_main.rooms_data[i]['player_name3'] == 'default_name'):
                    game_sys_main.rooms_data[i]['player_name3'] = unpack_join_request_data['player_name']
                    return game_sys_main.rooms_data[i]['room_number']
                elif(full_plyaer == 4 and game_sys_main.rooms_data[i]['player_name4'] == 'default_name'):
                    game_sys_main.rooms_data[i]['player_name4'] = unpack_join_request_data['player_name']
                    return game_sys_main.rooms_data[i]['room_number']
        game_sys_main.players_data[player_number]['player_name'] = unpack_join_request_data['player_name']
        return -1

    def send_lobby_data(socket):
        global game_sys_main
        room_count = game_sys_main.exist_room_count()
        packed_room_count = data_struct.pack_integer(room_count)
        socket.send(packed_room_count)
        for i in range(room_count):
            packed_room_data = data_struct.pack_room_data(game_sys_main.rooms_data[i])
            socket.send(packed_room_data)

    def recv_create_room(client_socket, player_number):
        global game_sys_main
        packed_create_room_data = client_socket.recv(data_struct.room_data_size) #수정
        create_room_data = data_struct.unpack_room_data(packed_create_room_data)
        rooms_count = game_sys_main.exist_room_count()
        if  rooms_count < game_sys_main.maxroomcount:
            game_sys_main.rooms_data[rooms_count] = create_room_data
            game_sys_main.rooms_data[rooms_count]['room_number'] = game_sys_main.empty_room_number()
            game_sys_main.players_data[player_number]['player_name'] = create_room_data['player_name1']
            room_is_not_full = game_sys_main.rooms_data[rooms_count]['room_number']
        else:
            room_is_not_full = -1
        packed_room_is_full = data_struct.pack_integer(room_is_not_full)
        client_socket.send(packed_room_is_full)
        return room_is_not_full

    # ROOM
    '''
    state 0 = join, 1 = select, 2 = ready, 3 = out, 4 = in game
    '''
    def send_in_room_data(client_socket, room_number, player_number):
        global game_sys_main
        in_room = True
        while in_room:
            packed_in_room_data = client_socket.recv(Pack.in_room_data_size)
            print('Send')
            print(packed_in_room_data)
            in_room_data = data_struct.unpack_in_room_data(packed_in_room_data)

            if in_room_data['is_exit'] == True:
                # 소켓 해제
                pass

            player_count = 0
            ready_count = 0
            # 방내 유저 레디상태 업데이트
            # 방내 유저 캐릭터선택 정보 업데이트
            for i in range(3):#임시
                if game_sys_main.waitting_room_data[room_number]['player_number'][i] == player_number:
                    game_sys_main.waitting_room_data[room_number]['player_witch_select'][i] = in_room_data['character_select']
                    game_sys_main.waitting_room_data[room_number]['player_ready_state'][i] = in_room_data['is_ready']

            for i in range(3):#임시
                if game_sys_main.waitting_room_data[room_number]['player_number'][i] != -1:
                    player_count += 1
                if game_sys_main.waitting_room_data[room_number]['player_ready_state'][i]:
                    ready_count += 1

            game_sys_main.waitting_room_data[room_number]['player_count'] = player_count
            print(game_sys_main.waitting_room_data[room_number])
            packed_in_room_data_server = Pack.pack_in_room_data_server(game_sys_main.waitting_room_data[room_number], GAME_STATE)
            client_socket.send(packed_in_room_data_server)

            if player_count == ready_count:
                in_room = False

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

    def send_in_game_data(client_socket, room_number, player_number):
        global PLAYER_NUM, state, GAME_STATE, E_Data, ready_state, E_NUM
        current_time = time.clock()
        E_NUM = 0
        while 1:  # When Game Over
            P_Data = client_socket.recv(struct.calcsize('=fffff'))

            _Player_Packed = data_struct.unpack_player_data(P_Data)

            frame_time = time.clock() - current_time
            current_time += frame_time
            _Bg.update(_Player_Packed[0], _Player_Packed[1])
            SEND_ENEMY = b'EMPTY'
            if timer.update(frame_time) == True:
                EnemyDirNum = random.randint(0, 8)
                if EnemyDirNum <= 3:
                    newEnemy = Enemy1(_Player_Packed[2], _Player_Packed[3], EnemyDirNum, _Bg.window_left,
                                      _Bg.window_bottom)
                if EnemyDirNum >= 4:
                    newEnemy = Enemy2(_Player_Packed[2], _Player_Packed[3], EnemyDirNum, _Bg.window_left,
                                      _Bg.window_bottom)
                SEND_ENEMY = PACK_DATA_Enemy(newEnemy)
            client_socket.send(SEND_ENEMY)

    def recv_thread(client_socket):
        global GAME_STATE
        print('GAME_STATE:' , GAME_STATE)

        while GAME_STATE==0:
            print('GAME_STATE in Thread', GAME_STATE)
            recv_packed_data = client_socket.recv(struct.calcsize('=BBI'))
            recv_data = struct.unpack('=BBI', recv_packed_data)
            temp = 'player' + str(recv_data[0]) + '_witch_selcet'
            temp2 = 'player' + str(recv_data[0]) + '_ready_state'
            game_sys_main.waitting_room_data[temp] = recv_data[1]
            game_sys_main.waitting_room_data[temp2] = recv_data[2]
            print('recv data :', recv_data)
            print('game_sys_main.waitting_room_data',game_sys_main.waitting_room_data)
            numofready = game_sys_main.waitting_room_data['player1_ready_state'] +game_sys_main.waitting_room_data['player2_ready_state']+game_sys_main.waitting_room_data['player3_ready_state']
            player_count = game_sys_main.waitting_room_data['player_count']
            if player_count <= numofready:
                GAME_STATE = 1



            if(game_sys_main.waitting_room_data['ready_state'] >> (player_number-1)&0b0001==1):
                temp = ''
            else:
                temp = '해제'
            print(player_number, '번 Player가 준비를',temp,'하였습니다.')

        if(game_sys_main.waitting_room_data['ready_state'] == 0b0011):
            print(player_number, '번 Player가 게임을 시작하였습니다.')
            game_sys_main.is_start=True




    def send_is_game_over(socket):
         # 게임결과를 보냅니다
         packed_is_game_over = data_struct.pack_is_game_over(game_sys_main.is_game_over)
         socket.send(packed_is_game_over)

    def exit(self):
        TcpController.server_socket.close()
        print("SOCKET closed... END")



def PACK_DATA_Enemy(objects):
    #for objects in object :
    object_struct_packed = data_struct.pack_enemy_data(objects)
        #client_socket.sendall(Enemy_packed)
    return object_struct_packed


