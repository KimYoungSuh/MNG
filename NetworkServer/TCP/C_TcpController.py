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
SEND_TIME =0
timer =None
'''
GAME_STATE
0 = WaitingRoom
1 = Playing
2 = GAMEOVER

'''
Enemy_packed = None
_Enemy= []


class Timer():
    def __init__(self):
        self.Whattime = 0
        self.EnemyNum = 0

    def update(self, frame_time):
        self.Whattime += frame_time
        if self.Whattime >= 0.5:
            self.Whattime = 0
            return True
        else :
            return False

game_sys_main = GameSysMain()
class TcpController:
    global GAME_STATE, player_count, timer,_Bg,Enemy_packed
    GAME_STATE = 0
    player_count =0
    PORT = 19000
    timer = Timer()
    _Bg = BackGround()
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
            client_thread = threading.Thread(target=TcpController.process_client, args=(client_socket,))
            client_thread.start()



    '''
    클라이언트와 통신하는 스레드입니다.
    로직을 이안에 쓰는것은 지양합니다.
    함수를 호출하여 수정을 최소화 하세요.
    '''
    def process_client(client_socket):
        global SEND_TIME, GAME_STATE,_Bg
        player_data_size = struct.calcsize('=fff')

        game_sys_main.join_player(PlayerData)

        #접속한 플레이어를 구분짓는 넘버링
        player_number = game_sys_main.waitting_room_data['player_count']

        #플레이어넘버를 보냄
        packed_player_number =  struct.pack('i',player_number)
        print('IS PACKED_PLAYER_NUMBER SEND?')
        #client_socket.send(packed_player_number)

        if GAME_STATE == 0 :
            print('IS in recv_thread?')
            recv_thread = threading.Thread(target=TcpController.recv_thread, args=(client_socket,))
            recv_thread.start()
            while GAME_STATE ==0 :
                #todo:
                packed_data = struct.pack('BBBB???',game_sys_main.waitting_room_data['player_count'],
                        game_sys_main.waitting_room_data['player1_witch_selcet'] ,
                        game_sys_main.waitting_room_data['player2_witch_selcet'] ,
                        game_sys_main.waitting_room_data['player3_witch_selcet'] ,
                        game_sys_main.waitting_room_data['player1_ready_state'],
                        game_sys_main.waitting_room_data['player2_ready_state'],
                        game_sys_main.waitting_room_data['player3_ready_state'] )
                client_socket.send(packed_data)
        a=1
        #When I Playing send Data
        if GAME_STATE == 1 :
            current_time = time.clock()
            while 1:
                #플레이어 데이터 받기
                data = client_socket.recv(struct.calcsize('=fff'))
                _Player_Packed = data_struct.unpack_player_data(data)
                frame_time = time.clock() - current_time
                current_time += frame_time
                _Bg.update(_Player_Packed[0], _Player_Packed[1])
                #timer.update(frame_time,_Player_Packed[0], _Player_Packed[1], _Bg.window_left, _Bg.window_bottom)
                SEND_ENEMY =b'EMPTY'
                if timer.update(frame_time) == True :
                    EnemyDirNum = random.randint(0, 8)
                    if EnemyDirNum <= 3 :
                        newEnemy = Enemy1(_Player_Packed[0], _Player_Packed[1], EnemyDirNum, _Bg.window_left, _Bg.window_bottom)
                    if EnemyDirNum>= 4:
                        newEnemy = Enemy2(_Player_Packed[0], _Player_Packed[1], EnemyDirNum, _Bg.window_left, _Bg.window_bottom)

                    print('IS PACKED_ENEMY_DATA SEND?')
                    SEND_ENEMY = PACK_DATA_Enemy(newEnemy)
                client_socket.send(SEND_ENEMY)

                #에너미 만들기
                #data2 = client_socket.recv(struct.calcsize('=ffffI'))
                #_enemylist.append(data_struct.unpack_enemy_data(data2))
                #print("Enemy Packed : ", _enemylist)
                #client_socket.send(Enemy_packed)
                #print(Enemy_packed)
                #print(data_struct.unpack_enemy_data(Enemy_packed))
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
            if player_count<= numofready:
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
    Enemy_packed = data_struct.pack_enemy_data(objects)
    print(data_struct.unpack_enemy_data(Enemy_packed))
    #client_socket.sendall(Enemy_packed)
    return Enemy_packed