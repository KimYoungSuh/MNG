import socket
import threading
import time
import random
from Enemy.C_Enemy import Enemy1
from Enemy.C_Enemy2 import Enemy2
from Bullet.C_EnemyBullet import EBullet
from Bullet.C_PlayerBullet import PBullet
from GameSys.C_GameSysMain import *
from TCP.C_Pack import *
from Background.C_BG import BackGround
import gc

_Bg = None
data_struct = DataStruct
GAME_STATE =0
send_time =0
state = None
timer = None
_Bullet = []
_PBullet = []
_EnemyList = []
_Enemy= []
E_NUM = 0
game_sys_main = None

to_all_event=list(range(16))
to_one_event=list(range(16))
for i in range(16):
    to_all_event[i] = threading.Event()
    to_one_event[i] = threading.Event()
player_number = 0
Enemy_packed = None
'''
GAME_STATE
0 = WaitingRoom
1 = Playing
2 = GAMEOVER
'''
LOBBY_DATA=0
ROOM_DATA=1
JOIN=2
CREATE=3
EXIT=4
SOCKET_CLOSE = -2





class TcpController:
    global GAME_STATE, player_count, _Bg, Enemy_packed, E_NUM, ready_state,game_sys_main, Image_size,Canvas_size
    GAME_STATE = 0
    Image_size=[0,3500,0,1800]
    Canvas_size=[0,1200,0,900]

    player_count =0
    PORT = 19000
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
        global PLAYER_NUM, state, GAME_STATE, E_Data, ready_state
        room_exit_ack = True
        room_number = 0
        game_sys_main.player_count += 1
        player_number = game_sys_main.empty_player_number()

        packed_player_number = data_struct.pack_integer(player_number)
        client_socket.send(packed_player_number)
        istime = time.clock()

        while room_exit_ack:
            print('room_number : ', room_number)
            room_number = TcpController.recv_lobby_state(client_socket, player_number) #in Lobby
            if room_number == SOCKET_CLOSE:
                return
            print('player_number : ', player_number)
            room_exit_ack = TcpController.send_in_room_data(client_socket, room_number, player_number)  # in Room
        TcpController.send_in_game_data(client_socket, room_number, player_number)

    #Lobby
    def recv_lobby_state(client_socket, player_number):
        global game_sys_main
        in_lobby = True
        state = 0

        while in_lobby:
            packed_Selection = client_socket.recv(data_struct.integer_size)
            selection = data_struct.unpack_integer(packed_Selection)

            if selection == LOBBY_DATA:
                TcpController.send_lobby_data(client_socket)
            elif selection == JOIN:
                state = TcpController.send_room_data(client_socket, player_number)
                is_none_room =(state == -1)
                if not is_none_room:
                    in_lobby = False
                    for i in range(3):
                        if game_sys_main.waitting_room_data[state-1]['player_number'][i] == -1:
                            game_sys_main.waitting_room_data[state-1]['player_number'][i] = player_number
                            break
            elif selection == CREATE:
                state = TcpController.recv_create_room(client_socket, player_number)
                if state != -1:
                    in_lobby = False
                    for i in range(3):  # 추후 수정
                        if game_sys_main.waitting_room_data[state-1]['player_number'][i] == -1:
                            game_sys_main.waitting_room_data[state-1]['player_number'][i] = player_number
                            break
            elif selection == EXIT:
                state = TcpController.recv_exit_server(client_socket, player_number)
                break;

        return state

    def recv_create_room(client_socket, player_number):
        global game_sys_main

        packed_create_room_data = client_socket.recv(data_struct.room_data_size) #수정
        create_room_data = data_struct.unpack_room_data(packed_create_room_data)
        rooms_count = game_sys_main.exist_room_count()
        if  rooms_count < game_sys_main.maxroomcount:
            game_sys_main.rooms_data[rooms_count] = create_room_data
            game_sys_main.rooms_data[rooms_count]['room_number'] = game_sys_main.empty_room_number()
            game_sys_main.players_data[player_number]['player_name1'] = create_room_data['player_name1']
            room_is_not_full = game_sys_main.rooms_data[rooms_count]['room_number']
        else:
            room_is_not_full = -1
        packed_room_is_full = data_struct.pack_integer(room_is_not_full)
        client_socket.send(packed_room_is_full)
        return room_is_not_full


    def send_room_data(client_socket, player_number):
        global game_sys_main
        packed_request_data = client_socket.recv(data_struct.join_request_data_size)
        unpack_join_request_data = data_struct.unpack_join_request_data(packed_request_data)

        room_count = game_sys_main.exist_room_count()
        for i in range(room_count):
            if game_sys_main.rooms_data[i]['room_number'] == unpack_join_request_data['room_number']:
                packed_room_data = data_struct.pack_room_data(game_sys_main.rooms_data[i])
                client_socket.send(packed_room_data)
                if game_sys_main.rooms_data[i]['is_started']:
                    break
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
        game_sys_main.players_data[player_number]['player_name1'] = unpack_join_request_data['player_name']
        return -1

    def send_lobby_data(socket):
        global game_sys_main

        room_count = game_sys_main.exist_room_count()
        print('room_count', room_count)
        packed_room_count = data_struct.pack_integer(room_count)
        socket.send(packed_room_count)
        for i in range(room_count):
            print(game_sys_main.rooms_data[i])
            packed_room_data = data_struct.pack_room_data(game_sys_main.rooms_data[i])
            socket.send(packed_room_data)

    def recv_exit_server(socket, player_number):
        global game_sys_main

        game_sys_main.player_exit(player_number)

        socket.send(data_struct.pack_boolean(True))
        socket.close()
        return -2

    # ROOM
    '''
    state 0 = join, 1 = select, 2 = ready, 3 = out, 4 = in game
    '''

    def send_in_room_data(client_socket, room_number, player_number):
        global game_sys_main
        player_name = ['player_name1', 'player_name2', 'player_name3', 'player_name4']
        in_room = True
        data_reset = False

        #state
        join = 0
        select = 1
        ready = 2
        out = 3
        in_game = 4

        while in_room:
            packed_in_room_data = client_socket.recv(data_struct.in_room_data_size)
            in_room_data = data_struct.unpack_in_room_data(packed_in_room_data)

            if in_room_data['is_exit'] == True:
                # 소켓 해제
                for i in range(3):
                    if data_reset and game_sys_main.waitting_room_data[room_number-1]['player_number'][i] != -1:
                        if game_sys_main.rooms_data[room_number-1]['host_number'] == -1:
                            game_sys_main.rooms_data[room_number-1]['host_number'] = game_sys_main.waitting_room_data[room_number-1]['player_number'][i]
                        game_sys_main.waitting_room_data[room_number-1]['player_number'][i - 1] = game_sys_main.waitting_room_data[room_number-1]['player_number'][i]
                        game_sys_main.waitting_room_data[room_number-1]['player_witch_select'][i - 1] = game_sys_main.waitting_room_data[room_number-1]['player_witch_select'][i]
                        game_sys_main.rooms_data[room_number-1][player_name[i-1]] = game_sys_main.rooms_data[room_number-1][player_name[i]]
                        game_sys_main.waitting_room_data[room_number-1]['player_number'][i] = -1
                        game_sys_main.waitting_room_data[room_number-1]['player_witch_select'][i] = 0
                        game_sys_main.waitting_room_data[room_number-1]['player_ready_state'][i] = False
                        game_sys_main.rooms_data[room_number-1][player_name[i - 1]] = game_sys_main.rooms_data[room_number-1][player_name[i]]
                    elif game_sys_main.waitting_room_data[room_number-1]['player_number'][i] == player_number:
                        game_sys_main.waitting_room_data[room_number - 1]['player_number'][i] = -1
                        if game_sys_main.rooms_data[room_number-1]['host_number'] == player_number:
                            game_sys_main.rooms_data[room_number-1]['host_number'] = -1
                        game_sys_main.waitting_room_data[room_number-1]['player_witch_select'][i] = 0
                        game_sys_main.waitting_room_data[room_number-1]['player_ready_state'][i] = False
                        game_sys_main.rooms_data[room_number-1][player_name[i]] = 'default_name'
                        data_reset = True

            in_room_player_count = 0
            ready_count = 0
            # 방내 유저 레디상태 업데이트
            # 방내 유저 캐릭터선택 정보 업데이트
            for i in range(3):  # 임시
                if game_sys_main.waitting_room_data[room_number-1]['player_number'][i] == player_number:
                    game_sys_main.waitting_room_data[room_number-1]['player_witch_select'][i] = in_room_data[
                        'character_select']
                    game_sys_main.waitting_room_data[room_number-1]['player_ready_state'][i] = in_room_data['is_ready']
                    game_sys_main.waitting_room_data[room_number-1]['emotion'][i] = in_room_data['emotion']

            for i in range(3):  # 임시
                #print(game_sys_main.waitting_room_data[room_number - 1]['player_number'][i])
                if game_sys_main.waitting_room_data[room_number-1]['player_number'][i] != -1:
                    in_room_player_count += 1
                if game_sys_main.waitting_room_data[room_number-1]['player_ready_state'][i]:
                    ready_count += 1

            game_sys_main.waitting_room_data[room_number-1]['player_count'] = in_room_player_count

            if in_room_player_count <= 0:
                game_sys_main.rooms_data[room_number-1]['room_number'] = -1
                game_sys_main.rooms_data[room_number-1]['room_name'] = 'default_name'
                game_sys_main.rooms_data[room_number-1]['full_player'] = 0

            if data_reset:
                packed_exit_ack = data_struct.pack_boolean(True)
                client_socket.send(packed_exit_ack)
                return True
            else:
                #print('in room count : ', game_sys_main.waitting_room_data[room_number-1]['player_count'])
                #print('count : ', in_room_player_count)
                packed_in_room_data_server = data_struct.pack_in_room_data_server(game_sys_main.waitting_room_data[room_number-1],
                                                                           GAME_STATE)
                client_socket.send(packed_in_room_data_server)

            if in_room_player_count == ready_count:
                in_room = False
                game_sys_main.rooms_data[room_number-1]['is_started'] = True
        return False

    def game_thread(client_socket, room_number):
        global main_time
        room_player = game_sys_main.waitting_room_data[room_number-1]['player_number']
        room_player_data = game_sys_main.all_player_data[room_number]
        while 1:
            for i in range (3):
                if(room_player[i]==-1):
                    break
                to_all_event[room_player[i]].wait()
                to_all_event[room_player[i]].clear()
            frame_time = time.clock() - main_time
            main_time += frame_time
            if timer.update(frame_time) == True:  # 적 만드는 부분
                EnemyDirNum = random.randint(0, 8)
                if EnemyDirNum <= 3:
                    newEnemy = Enemy1( EnemyDirNum)
                    dis=[]
                    for i in range(3):
                        if (room_player[i] == -1):
                            break
                        dis.append(newEnemy.get_distance(room_player_data['player_x'][i], room_player_data['player_y'][i]))
                    near=dis.index(min(dis))
                    newEnemy.set_dir(room_player_data['player_x'][near],room_player_data['player_y'][near])
                    _EnemyList.append(newEnemy)

                if EnemyDirNum >= 4:
                    newEnemy = Enemy2(EnemyDirNum)
                    dis = []
                    for i in range(3):
                        if (room_player[i] == -1):
                            break
                        dis.append(
                            newEnemy.get_distance(room_player_data['player_x'][i], room_player_data['player_y'][i]))
                    near = dis.index(min(dis))
                    newEnemy.set_dir(room_player_data['player_x'][near], room_player_data['player_y'][near])
                    _EnemyList.append(newEnemy)
            for i in range(3):
                if (room_player[i] == -1):
                    break
                if room_player_data['player_isShoot'][i]==True:
                    newBullet = PBullet(room_player_data['player_x'][i], room_player_data['player_y'][i], room_player_data['player_dir'][i])
                    _Bullet.append(newBullet)

            for pbullets in _Bullet:
                if pbullets.shooter == 0:
                    for enemys in _EnemyList:
                        if collide(pbullets, enemys):
                            pbullets.alive = 0
                            enemys.alive = 0

            for enemy in _EnemyList:
                if enemy.ADD_Bullet() == True:
                    newBullet = EBullet(enemy.x, enemy.y)
                    dis = []
                    for i in range(3):
                        if (room_player[i] == -1):
                            break
                        dis.append(newBullet.get_distance(room_player_data['player_x'][i], room_player_data['player_y'][i]))
                    near = dis.index(min(dis))
                    newBullet.set_dir(room_player_data['player_x'][near], room_player_data['player_y'][near])
                    _Bullet.append(newBullet)

            for enemy in _EnemyList:
                enemy.update(frame_time)

            for bullets in _Bullet:
                bullets.update(frame_time)

            for enemy in _EnemyList:
                if enemy.alive == 0:
                    _EnemyList.remove(enemy)
            for pbullets in _Bullet:
                if pbullets.alive == 0:
                    _Bullet.remove(pbullets)
            for ebullets in _Bullet:
                if ebullets.alive == 0:
                    _Bullet.remove(ebullets)






            for i in range (3):
                if(room_player[i]==-1):
                    break
                to_one_event[room_player[i]].set()
            gc.collect()




    def send_in_game_data(client_socket, room_number, player_number):
        global main_time,PLAYER_NUM, state, GAME_STATE,timer, E_Data, ready_state, E_NUM
        global player_count,Image_size  ,Canvas_size
        room_player = game_sys_main.waitting_room_data[room_number - 1]['player_number']
        game_sys_main.all_player_data[room_number]['player_number'][player_number] = player_number
        in_player=(-1,-1,-1)
        current_time = time.clock()
        E_NUM = 0
        timer = Timer()
        main_time = time.clock()


        if player_number==game_sys_main.rooms_data[room_number-1]['host_number']:
            t1 = threading.Thread(target=TcpController.game_thread, args=(client_socket, room_number))
            t1.start()
        gc.disable()

        while 1:  # When Game Over
            if current_time+0.033  < time.clock():
                current_time = time.clock()
                P_Data = client_socket.recv(struct.calcsize('=ffffiBf'))
                _Player_Packed = data_struct.unpack_player_data(P_Data)
                for i in range(3):  # 임시
                    if game_sys_main.all_player_data[room_number]['player_number'][i] == player_number:
                        game_sys_main.all_player_data[room_number]['player_count'] = game_sys_main.waitting_room_data[room_number-1]['player_count']
                        game_sys_main.all_player_data[room_number]['player_x'][i] =_Player_Packed[0]
                        game_sys_main.all_player_data[room_number]['player_y'][i] = _Player_Packed[1]
                        game_sys_main.all_player_data[room_number]['player_sx'][i] = _Player_Packed[2]
                        game_sys_main.all_player_data[room_number]['player_sy'][i] = _Player_Packed[3]
                        game_sys_main.all_player_data[room_number]['player_life'][i] = _Player_Packed[4]
                        game_sys_main.all_player_data[room_number]['player_isShoot'][i] = _Player_Packed[5]
                        game_sys_main.all_player_data[room_number]['player_dir'][i] = _Player_Packed[6]
                packed_all_player_data = data_struct.pack_all_player_data(game_sys_main.all_player_data[room_number])

                to_all_event[player_number].set()
                to_one_event[player_number].wait()
                to_one_event[player_number].clear()
                client_socket.send(packed_all_player_data)

                # Gameover의 위치는 recv와 send 사이

                client_socket.send(struct.pack('?', game_sys_main.is_game_over))
                if (game_sys_main.is_game_over):
                    break
                client_socket.send(struct.pack('=ii', len(_EnemyList), len(_Bullet)))
                Enemys_IN_Window = []
                Bullets_IN_Window =[]
                for enemy in _EnemyList:
                    #플레이어 x로 계산
                    if _Player_Packed[0]<600 :
                        if Canvas_size[1] > enemy.x: #캔버스 사이즈보다 작고
                            if Image_size[0] < enemy.x: # 0보다 크다
                                if _Player_Packed[1] + 600 > enemy.y:
                                    if _Player_Packed[1] - 600 < enemy.y:
                                        Enemy_packed = data_struct.pack_enemy_data(enemy, k)
                                        Enemys_IN_Window.append(Enemy_packed)
                    elif _Player_Packed[0]>2900 :
                        if Image_size[1] > enemy.x:
                            if Image_size[1] - Canvas_size[1] +200 < enemy.x:
                                if _Player_Packed[1] + 600 > enemy.y:
                                    if _Player_Packed[1] - 600 < enemy.y:
                                        Enemy_packed = data_struct.pack_enemy_data(enemy, k)
                                        Enemys_IN_Window.append(Enemy_packed)
                    #플레이어 y로 계산
                    if _Player_Packed[1] <450 :
                        if _Player_Packed[0] + 800 > enemy.x:
                            if _Player_Packed[0] - 800 < enemy.x:
                                if Canvas_size[2] < enemy.y:
                                    if Canvas_size[3] > enemy.y:
                                        Enemy_packed = data_struct.pack_enemy_data(enemy, k)
                                        Enemys_IN_Window.append(Enemy_packed)

                    elif _Player_Packed[1] > 1350 :
                        if _Player_Packed[0] + 800 > enemy.x:
                            if _Player_Packed[0] - 800 < enemy.x:
                                if Image_size[3] - Canvas_size[3] < enemy.y:
                                    if Image_size[3]  > enemy.y:
                                        Enemy_packed = data_struct.pack_enemy_data(enemy, k)
                                        Enemys_IN_Window.append(Enemy_packed)

                    else :
                        if _Player_Packed[0] +800 > enemy.x :
                            if _Player_Packed[0] -800 < enemy.x :
                                if _Player_Packed[1] + 600 > enemy.y:
                                    if _Player_Packed[1] - 600 < enemy.y:
                                        Enemy_packed = data_struct.pack_enemy_data(enemy, k)
                                        Enemys_IN_Window.append(Enemy_packed)


                for bullets in _Bullet:
                    if _Player_Packed[0] < 600:
                        if Canvas_size[1] > bullets.x:  # 캔버스 사이즈보다 작고
                            if Image_size[0] < bullets.x:  # 0보다 크다
                                if _Player_Packed[1] + 600 > bullets.y:
                                    if _Player_Packed[1] - 600 < bullets.y:
                                        bullet_packed = data_struct.pack_bullet_data(bullets)
                                        Bullets_IN_Window.append(bullet_packed)
                    elif _Player_Packed[0] > 2900:
                        if Image_size[1] > bullets.x:
                            if Image_size[1] - Canvas_size[1] < bullets.x:
                                if _Player_Packed[1] + 600 > bullets.y:
                                    if _Player_Packed[1] - 600 < bullets.y:
                                        bullet_packed = data_struct.pack_bullet_data(bullets)
                                        Bullets_IN_Window.append(bullet_packed)
                    # 플레이어 y로 계산
                    if _Player_Packed[1] < 450:
                        if _Player_Packed[0] + 800 > bullets.x:
                            if _Player_Packed[0] - 800 < bullets.x:
                                if Canvas_size[2] < bullets.y:
                                    if Canvas_size[3] > bullets.y:
                                        bullet_packed = data_struct.pack_bullet_data(bullets)
                                        Bullets_IN_Window.append(bullet_packed)

                    elif _Player_Packed[1] > 1350:
                        if _Player_Packed[0] + 800 > bullets.x:
                            if _Player_Packed[0] - 800 < bullets.x:
                                if Image_size[3] - Canvas_size[3] < bullets.y:
                                    if Image_size[3] > bullets.y:
                                        bullet_packed = data_struct.pack_bullet_data(bullets)
                                        Bullets_IN_Window.append(bullet_packed)

                    else:
                        if _Player_Packed[0] + 800 > bullets.x:
                            if _Player_Packed[0] - 800 < bullets.x:
                                if _Player_Packed[1] + 600 > bullets.y:
                                    if _Player_Packed[1] - 600 < bullets.y:
                                        bullet_packed = data_struct.pack_bullet_data(bullets)
                                        Bullets_IN_Window.append(bullet_packed)

                client_socket.send(struct.pack('=ii', len(Enemys_IN_Window), len(Bullets_IN_Window)))

                for Enemy_packed in Enemys_IN_Window:
                    client_socket.send(Enemy_packed)

                for bullet_packed in Bullets_IN_Window:
                    client_socket.send(bullet_packed)

                gc.collect()
        gc.enable()





        leader_board = open('LeaderBoard.txt', 'a+t')
        new_score = ('p1', 'd', 'p2', 'd', 'p3', 'd', 'time', '00.00.00', 'score', '9')

        for temp in new_score:
            leader_board.write(temp)
        leader_board.write('\n')
        leader_board.seek(0)
        before_leader_board = leader_board.readlines()
        leader_list = []
        for temp in before_leader_board:
            temp_tuple = ()
            p1_pos = temp.find('p1')
            p2_pos = temp.find('p2')
            p3_pos = temp.find('p3')
            time_pos = temp.find('time')
            score_pos = temp.find('score')
            temp_tuple = ('p1', temp[p1_pos + 2:p2_pos],
                          'p2', temp[p2_pos + 2:p3_pos],
                          'p3', temp[p3_pos + 2:time_pos],
                          'time', temp[time_pos + 4:score_pos],
                          'score', temp[score_pos + 5: len(temp) - 1])

            leader_list.append(temp_tuple)
        after_leader_board = sorted(leader_list, key=lambda score: score[9], reverse=True)
        if(len(after_leader_board)>10):
            after_leader_board.pop()
        leader_board.close()
        leader_board = open('LeaderBoard.txt', 'wt')
        count = 0

        for leader_list_temp in after_leader_board:
            count += 1
            if count > 10: break
            for leader_tuple_temp in leader_list_temp:
                leader_board.write(leader_tuple_temp)
            leader_board.write('\n')


        packed_leader_board_count = data_struct.pack_integer(len(after_leader_board))
        client_socket.send(packed_leader_board_count)

        for i in range(0, len(after_leader_board)):
            print(after_leader_board[i])
            print(i)
            packed_leader_board= struct.pack('30s 30s 30s 30s i',
                                             after_leader_board[i][1].encode('ascii'),
                                             after_leader_board[i][3].encode('ascii'),
                                             after_leader_board[i][5].encode('ascii'),
                                             after_leader_board[i][7].encode('ascii'),
                                             int(after_leader_board[i][9]))

            client_socket.send(packed_leader_board)
        leader_board.close()
        del (leader_board)





def send_is_game_over(socket):
         # 게임결과를 보냅니다
         packed_is_game_over = data_struct.pack_is_game_over(game_sys_main.is_game_over)
         socket.send(packed_is_game_over)

def exit(self):
    TcpController.server_socket.close()
    print("SOCKET closed... END")



def collide(a, b):
    left_a, bottom_a,right_a, top_a = a.get_bb()
    left_b, bottom_b,right_b, top_b = b.get_bb()
    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False

    return True

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