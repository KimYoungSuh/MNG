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
state = None
SEND_TIME =0
timer =None
_EnemyList = []
E_NUM = 0
'''
GAME_STATE
0 = WaitingRoom
1 = Playing
2 = GAMEOVER
'''
PLAYER_NUM = 0
Enemy_packed = None
_Enemy= []

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

game_sys_main = GameSysMain()
class TcpController:
    global GAME_STATE, player_count, timer,_Bg,Enemy_packed,E_NUM,ready_state
    GAME_STATE = 0
    player_count =0
    PORT = 19000
    timer = Timer()
    ready_state = 0
    _Bg = BackGround()
    IP = ''
    E_NUM= 0
    PLAYER_NUM = 0
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
        global SEND_TIME, GAME_STATE, _Bg, PLAYER_NUM

        print("[정보] 접속 대기중...")
        print("=" * 50)
        PLAYER_NUM = 0

        '''
        Waitting Room
        '''

        while 1:
            client_socket, address = TcpController.server_socket.accept()

            print("I got a connection from ", address)


            client_thread = threading.Thread(target=TcpController.process_client, args=(client_socket,))
            client_thread.start()
             # game_sys_main.join_player(PlayerData)



    '''
    클라이언트와 통신하는 스레드입니다.
    로직을 이안에 쓰는것은 지양합니다.
    함수를 호출하여 수정을 최소화 하세요.
    '''
    def process_client(client_socket):
        global PLAYER_NUM, state, GAME_STATE, E_Data,ready_state

        while 1 :

            state = client_socket.recv(100)

            print('state : ', state)
            if state == b'JOIN!':  # 방 입장할때
                if PLAYER_NUM >= 3:
                    # 총 인원수가 3명이 넘으면 풀방이라고 리턴한다.
                    client_socket.send(struct.pack('is', 99, b'F'))
                else:
                    PLAYER_NUM += 1
                    print(PLAYER_NUM, "번 유저가 입장했습니다.")
                    packed_data = struct.pack('is', PLAYER_NUM, b'J')
                    client_socket.send(packed_data)
                pass
            elif state == b'Sellect':  # 캐릭터를 고를때마다 보내준다.
                # It Recv PlayerNum, SelectWitch, ReadyState
                packed_Player_Sellect = client_socket.recv(struct.calcsize('=BBi'))
                '''for check'''
                # packed_Player_Sellect = client_socket.recv(struct.calcsize('=BBi'))
                game_sys_main.waitting_room_data['player_count'] = PLAYER_NUM
                temp = 'player' + str(packed_Player_Sellect[0]) + '_witch_selcet'
                temp2 = 'player' + str(packed_Player_Sellect[0]) + '_ready_state'
                game_sys_main.waitting_room_data[temp] = packed_Player_Sellect[1]
                game_sys_main.waitting_room_data[temp2] = packed_Player_Sellect[2]
                while ready_state == 1 :
                    print('in sellect while')
                    Packed_All_Player = struct.pack('=BBBBBBBi',
                                                    game_sys_main.waitting_room_data['player_count'],
                                                    game_sys_main.waitting_room_data['player1_witch_selcet'],
                                                    game_sys_main.waitting_room_data['player2_witch_selcet'],
                                                    game_sys_main.waitting_room_data['player3_witch_selcet'],
                                                    game_sys_main.waitting_room_data['player1_ready_state'],
                                                    game_sys_main.waitting_room_data['player2_ready_state'],
                                                    game_sys_main.waitting_room_data['player3_ready_state'],
                                                    GAME_STATE)
                    client_socket.send(Packed_All_Player)
            elif state == b'Ready':
                ready_state = 1
                packed_Player_Sellect = client_socket.recv(struct.calcsize('=BBi'))
                '''for check'''
                # packed_Player_Sellect = client_socket.recv(struct.calcsize('=BBi'))
                print('packed_Player_Sellect :', struct.unpack('=BBi', packed_Player_Sellect))
                game_sys_main.waitting_room_data['player_count'] = PLAYER_NUM
                temp = 'player' + str(packed_Player_Sellect[0]) + '_witch_selcet'
                temp2 = 'player' + str(packed_Player_Sellect[0]) + '_ready_state'
                game_sys_main.waitting_room_data[temp] = packed_Player_Sellect[1]
                game_sys_main.waitting_room_data[temp2] = packed_Player_Sellect[2]
                numofready = game_sys_main.waitting_room_data['player1_ready_state'] + game_sys_main.waitting_room_data[
                    'player2_ready_state'] + game_sys_main.waitting_room_data['player3_ready_state']
                player_count = game_sys_main.waitting_room_data['player_count']
                while GAME_STATE ==0:
                    if player_count <= numofready:
                        GAME_STATE = 1
                    Packed_All_Player = struct.pack('=BBBBBBBi',
                                                game_sys_main.waitting_room_data['player_count'],
                                                game_sys_main.waitting_room_data['player1_witch_selcet'],
                                                game_sys_main.waitting_room_data['player2_witch_selcet'],
                                                game_sys_main.waitting_room_data['player3_witch_selcet'],
                                                game_sys_main.waitting_room_data['player1_ready_state'],
                                                game_sys_main.waitting_room_data['player2_ready_state'],
                                                game_sys_main.waitting_room_data['player3_ready_state'],
                                                GAME_STATE)


                    client_socket.sendall(Packed_All_Player)


                pass
            elif state == b'Out':  # 플레이어가 나갈때 불러준다
                print(PLAYER_NUM, "번 유저가 퇴장했습니다.")

                PLAYER_NUM -= 1
                # 추가구현 필요합니당! 플레이어 1,2가 있을때 플레이어1이 나가면 ?

            elif state == b'InGame':
                current_time = time.clock()
                E_NUM = 0
                while 1: # When Game Over
                    P_Data = client_socket.recv(struct.calcsize('=fffff'))

                    _Player_Packed = data_struct.unpack_player_data(P_Data)

                    frame_time = time.clock() - current_time
                    current_time += frame_time
                    _Bg.update(_Player_Packed[0], _Player_Packed[1])

                    if timer.update(frame_time) == True:
                        EnemyDirNum = random.randint(0, 8)
                        if EnemyDirNum <= 3:
                            newEnemy = Enemy1(_Player_Packed[2], _Player_Packed[3], EnemyDirNum, _Bg.window_left,
                                              _Bg.window_bottom)
                            _EnemyList.append(newEnemy)
                            E_NUM += 1
                        if EnemyDirNum >= 4:
                            newEnemy = Enemy2(_Player_Packed[2], _Player_Packed[3], EnemyDirNum, _Bg.window_left,
                                              _Bg.window_bottom)
                            _EnemyList.append(newEnemy)
                            E_NUM += 1

                    client_socket.send(struct.pack('=i', E_NUM))

                    k = 0
                    for enemy in _EnemyList:
                        enemy.update(frame_time, _Player_Packed[0], _Player_Packed[1], _Bg.window_left, _Bg.window_bottom)
                        Enemy_packed = data_struct.pack_enemy_data(enemy)
                        client_socket.send(Enemy_packed)



                # client_thread = threading.Thread(target=TcpController.process_client, args=(client_socket,))
                # client_thread.start()
                pass
            else :
                pass




    def send_room_data(socket):
        packed_request_data = socket.recv(1)
        unpack_join_request_data = data_struct.unpack_join_request_data(packed_request_data)
        #방 정보를 모두 불러들이면 구현할필요 없음 (임시)
        for i in range(game_sys_main.exist_room_count()):
            if game_sys_main.rooms_data[i]['room_number'] == unpack_join_request_data['room_number']:
                packed_room_data = data_struct.pack_room_data(game_sys_main.rooms_data[i])
                socket.send(packed_room_data)
                if (game_sys_main.rooms_data[i]['full_player'] == 4 and
                            game_sys_main.rooms_data[i]['player_name4'] == 'default_name') or\
                    (game_sys_main.rooms_data[i]['full_player'] == 3 and
                             game_sys_main.rooms_data[i]['player_name3'] == 'default_name') or\
                    (game_sys_main.rooms_data[i]['full_player'] == 2 and
                             game_sys_main.rooms_data[i]['player_name2'] == 'default_name'):
                    for i in range(2, 5):
                        if(game_sys_main.rooms_data[i]['full_player'] == 2):
                            game_sys_main.rooms_data[i]['player_name2'] = unpack_join_request_data[1]
                            #언팩시 딕셔너리 형태 유지되는지 확인필요
                        if(game_sys_main.rooms_data[i]['full_player'] == 3):
                            if(game_sys_main.rooms_data[i]['player_name2'] == 'default_name'):
                                game_sys_main.rooms_data[i]['player_name2'] = unpack_join_request_data[1]
                            else:
                                game_sys_main.rooms_data[i]['player_name3'] = unpack_join_request_data[1]
                        if(game_sys_main.rooms_data[i]['full_player'] == 4):
                            if(game_sys_main.rooms_data[i]['player_name2'] == 'default_name'):
                                game_sys_main.rooms_data[i]['player_name2'] = unpack_join_request_data[1]
                            elif(game_sys_main.rooms_data[i]['player_name3'] == 'default_name'):
                                game_sys_main.rooms_data[i]['player_name3'] = unpack_join_request_data[1]
                            else:
                                game_sys_main.rooms_data[i]['player_name4'] = unpack_join_request_data[1]
                break

    def send_lobby_data(socket):
        room_count = game_sys_main.exist_room_count()
        packed_room_count = data_struct.pack_count_data(room_count)
        socket.send(packed_room_count)
        for i in range(room_count):
            packed_room_data = data_struct.pack_room_data(game_sys_main.rooms_data[i])
            socket.send(packed_room_data)


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



    def recv_create_room(socket):
        packed_create_room_data = socket.recv(1)
        create_room_data = data_struct.unpack_room_data(packed_create_room_data)
        if game_sys_main.exist_room_count() <= game_sys_main.MAXROOMCOUNT:
            game_sys_main.rooms_data[game_sys_main.exist_room_count()] = create_room_data




    def send_is_game_over(socket):
         # 게임결과를 보냅니다
         packed_is_game_over = data_struct.pack_is_game_over(game_sys_main.is_game_over)
         socket.send(packed_is_game_over)

    def exit(self):
        TcpController.server_socket.close()
        print("SOCKET closed... END")



def PACK_DATA_Enemy(objects):
    for objects in object :
        object_struct_packed = data_struct.pack_enemy_data(objects)
        client_socket.sendall(Enemy_packed)
    return Enemy_packed


