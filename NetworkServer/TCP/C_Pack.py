import sys
import struct
from Data import *




class Pack:
    # Boolean
    boolean_type = '?'
    boolean_size = struct.calcsize(boolean_type)
    def pack_boolean(boolean):
        return struct.pack('?', boolean)
    def unpack_boolean(packed):
        return struct.unpack('?', packed)[0]

    integer_type = 'i'
    integer_size = struct.calcsize(integer_type)
    # Inteager
    def pack_integer(integer):
        return struct.pack('i', integer)
    def unpack_integer(integer):
        return struct.unpack('i', integer)[0]

    # count_data
    def pack_count_data(count_data):
        packed_data = struct.pack('i', count_data)
        return packed_data

    def unpack_count_data(count_data):
        unpacked_data = struct.unpack('i', count_data)
        return unpacked_data

    # Room_data
    room_data_type = 'B B 30s B 30s 30s 30s 30s ? B'
    room_data_size = struct.calcsize(room_data_type)

    def pack_room_data(room_data):
            packed_data = struct.pack('BB30sB30s30s30s30s?B',
                                      room_data['room_number'],
                                      room_data['host_number'],
                                      room_data['room_name'].encode('ascii'),
                                      room_data['full_player'],
                                      room_data['player_name1'].encode('ascii'),
                                      room_data['player_name2'].encode('ascii'),
                                      room_data['player_name3'].encode('ascii'),
                                      room_data['player_name4'].encode('ascii'),
                                      room_data['is_start'],
                                      room_data['ready_player'])
            return packed_data

    def unpack_room_data(packed):
            unpacked_data = struct.unpack('B B 30s B 30s 30s 30s 30s ? B', packed)
            room_data = {
                'room_number': unpacked_data[0],
                'host_number': unpacked_data[1],
                'room_name': unpacked_data[2].decode('ascii').rstrip('\x00'),
                'full_player': unpacked_data[3],
                'player_name1': unpacked_data[4].decode('ascii').rstrip('\x00'),
                'player_name2': unpacked_data[5].decode('ascii').rstrip('\x00'),
                'player_name3': unpacked_data[6].decode('ascii').rstrip('\x00'),
                'player_name4': unpacked_data[7].decode('ascii').rstrip('\x00'),
                'is_start': unpacked_data[8],
                'ready_player': unpacked_data[9]
            }
            return room_data

    # join_request_data
    join_request_data_type = 'B 30s B'
    join_request_data_size = struct.calcsize(room_data_type)
    def pack_join_request_data(join_request_data):
        packed_data = struct.pack('B 30s B',
                                  join_request_data['room_number'],
                                  join_request_data['player_name'].encode('ascii'),
                                  join_request_data['player_number'])
        return packed_data

    def unpack_join_request_data(packed_data):
        unpacked_data = struct.unpack('B 30s B', packed_data)
        join_request_data = {
            'room_number': unpacked_data[0],
            'player_name': unpacked_data[1].decode('ascii').rstrip('\x00'),
            'player_number': unpacked_data[2]
        }
        return join_request_data

    #room_is_full
    def pack_room_is_full(is_room_full):
        packed_data = struct.pack('?', is_room_full)
        return packed_data

    def pack_bullet_data(bullet_data):
        packed = struct.pack('=ffffff',
                             bullet_data.shooter,
                             bullet_data.x,
                             bullet_data.y,
                             bullet_data.xdir,
                             bullet_data.ydir,
                             bullet_data.speed)
        #                             (bullet_data['start_pos'])['pos_x'],
        #                             (bullet_data['start_pos'])['pos_y'],
        #                             bullet_data['direction'],
        #                             bullet_data['speed'],
        #                             bullet_data['shoo,t_time'],
        #                             bullet_data['shooter'])
        return packed

    def unpack_bullet_data(packed):
        unpaked_data = struct.unpack('=ffffff', packed)
        return unpaked_data
    # Bullet_data
    '''
    def pack_bullet_data(bullet_data):
        packed = struct.pack('iiBfB',
                             (bullet_data['start_pos'])['pos_x'],
                             (bullet_data['start_pos'])['pos_y'],
                             bullet_data['direction'],
                             bullet_data['speed'],
                             bullet_data['shoot_time'],
                             bullet_data['shooter'])
    def unpack_enemy_data(packed):
        unpacked_data = struct.unpack('iiBfB', packed)
        return unpacked_data
    '''
    # enemy_data
    def pack_enemy_data(enemy_data):
        packed = struct.pack('=ffffI',
                             enemy_data.x,
                             enemy_data.y,
                             enemy_data.xdir,
                             enemy_data.ydir,
                             enemy_data.TEAM)

    def unpack_enemy_data(packed):
        unpacked_data = struct.unpack('=ffffI', packed)
        return unpacked_data

    #player_data
    def pack_player_data(player_data):
        packed = struct.pack('=fff',
#             player_data['player_name'].encode('utf-8'),
#             player_data['player_number'],
             (player_data.x),
             (player_data.y),
#             player_data['direction'],
             (player_data.life))
#             player_data['is_damaged'],
#             player_data['player_score'])
    def unpack_player_data(packed):
        unpacked_data = struct.unpack('=fff', packed)
        return unpacked_data

        '''
            def pack_player_data(player_data):
                packed = struct.pack('30s BiiBB?L',
                     player_data['player_name'].encode('utf-8'),
                     player_data['player_number'],
                     (player_data['player_pos'])['pos_x'],
                     (player_data['player_pos'])['pos_y'],
                     player_data['direction'],
                     player_data['life'],
                     player_data['is_damaged'],
                     player_data['player_score'])
                return packed
            def unpack_player_data(packed):
                unpacked_data = struct.unpack('30s BiiBB?L', packed)
                return unpacked_data
        '''
    #is_game_over
    def pack_is_game_over(is_game_over):
        return struct.pack('?', is_game_over)
    def unpack_is_game_over(packed):
        return struct.unpack('?', packed)

    #players list
    def pack_players_data(players_list):
        result = bytes()
        result += struct.pack('i',len(players_list))
        for i in range (0,len(players_list)):
            try:
                temp = struct.pack('=fff',
                                     (players_list[i][0]),
                                     (players_list[i][1]),
                                     (players_list[i][2]))
            except:
                print(i, players_list[i])
                exit(1)
            packed_player_data=temp
            result += packed_player_data
        return result

    def unpack_players_data(packed_data_list):
        temp=packed_data_list[:4]
        list_size = struct.unpack('i',temp)
        result_list=[]
        for i in range (0, list_size[0]):

            temp = packed_data_list[4+(struct.calcsize('fff'))*i:4+(struct.calcsize('fff'))*(i+1)]

            result_list.append(Pack.unpack_player_data(temp))

        return result_list


