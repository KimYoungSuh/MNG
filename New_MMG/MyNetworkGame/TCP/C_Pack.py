import sys
import struct
from Data import *

class DataStruct:
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

    # Room_data
    room_data_type = 'i i 30s i 30s 30s 30s 30s ? i'
    room_data_size = struct.calcsize(room_data_type)
    def pack_room_data(room_data):
        packed_data = struct.pack(DataStruct.room_data_type,
                                  room_data['room_number'],
                                  room_data['host_number'],
                                  room_data['room_name'].encode('ascii'),
                                  room_data['full_player'],
                                  room_data['player_name1'].encode('ascii'),
                                  room_data['player_name2'].encode('ascii'),
                                  room_data['player_name3'].encode('ascii'),
                                  room_data['player_name4'].encode('ascii'),
                                  room_data['is_started'],
                                  room_data['ready_player'])
        return packed_data

    def unpack_room_data(packed):
        unpacked_data = struct.unpack(DataStruct.room_data_type, packed)
        room_data = {
            'room_number': unpacked_data[0],
            'host_number': unpacked_data[1],
            'room_name': unpacked_data[2].decode('ascii').rstrip('\x00'),
            'full_player': unpacked_data[3],
            'player_name1': unpacked_data[4].decode('ascii').rstrip('\x00'),
            'player_name2': unpacked_data[5].decode('ascii').rstrip('\x00'),
            'player_name3': unpacked_data[6].decode('ascii').rstrip('\x00'),
            'player_name4': unpacked_data[7].decode('ascii').rstrip('\x00'),
            'is_started': unpacked_data[8],
            'ready_player': unpacked_data[9]
        }
        return room_data

    # join_request_data
    join_request_data_type = 'B 30s'
    join_request_data_size = struct.calcsize(room_data_type)
    def pack_join_request_data(join_request_data):
        packed_data = struct.pack('B 30s',
                                  join_request_data['room_number'],
                                  join_request_data['player_name'].encode('ascii'))
        return packed_data
    def unpack_join_request_data(packed_data):
        unpacked_data = struct.unpack('B 30s', packed_data)
        join_request_data = {
            'room_number': unpacked_data[0],
            'player_name': unpacked_data[1].decode('ascii').rstrip('\x00')
        }
        return join_request_data

    # in_room_data
    in_room_data_type = 'B ? ? B'
    in_room_data_size = struct.calcsize(in_room_data_type)
    def pack_in_room_data(in_room_data):
        packed_data = struct.pack('B ? ? B',
                                      in_room_data['character_select'],
                                      in_room_data['is_ready'],
                                      in_room_data['is_exit'],
                                      in_room_data['emotion'])
        return packed_data
    def unpack_in_room_data(packed_data):
        unpacked_data = struct.unpack('B ? ? B', packed_data)
        in_room_data = {
                'character_select': unpacked_data[0],
                'is_ready': unpacked_data[1],
                'is_exit': unpacked_data[2],
                'emotion': unpacked_data[3]}
        return in_room_data

    # in_room_data_server
    in_room_data_server_type = 'BBBBBBBiBBB'
    in_room_data_server_size = struct.calcsize(in_room_data_server_type)
    def pack_in_room_data_server(in_room_data_server, gamestate):
            packed_data = struct.pack('BBBBBBBiBBB',
                                      in_room_data_server['player_count'],
                                      in_room_data_server['player_witch_select'][0],
                                      in_room_data_server['player_witch_select'][1],
                                      in_room_data_server['player_witch_select'][2],
                                      in_room_data_server['player_ready_state'][0],
                                      in_room_data_server['player_ready_state'][1],
                                      in_room_data_server['player_ready_state'][2],
                                      gamestate,
                                      in_room_data_server['emotion'][0],
                                      in_room_data_server['emotion'][1],
                                      in_room_data_server['emotion'][2])
            return packed_data

    def unpack_in_room_data_server(packed_data):
        unpacked_data = struct.unpack('BBBBBBBiBBB', packed_data)
        in_room_data_server = {
            'player_count': unpacked_data[0],
            'player_witch_select': [unpacked_data[1], unpacked_data[2], unpacked_data[3]],
            'player_ready_state': [unpacked_data[4], unpacked_data[5], unpacked_data[6]],
            'emotion': [unpacked_data[8], unpacked_data[9], unpacked_data[10]]
        }
        return in_room_data_server

    #room_is_full
    def unpack_room_is_full(packed_data):
        unpacked_data = struct.unpack('?', packed_data)
        return unpacked_data

    # Bullet_data
    bullet_data_type = '=fff'
    bullet_data_size = struct.calcsize(bullet_data_type)
    def pack_bullet_data(bullet_data):
        packed = struct.pack('=fff',
                             bullet_data.shooter,
                             bullet_data.x,
                             bullet_data.y)
#                             (bullet_data['start_pos'])['pos_x'],
#                             (bullet_data['start_pos'])['pos_y'],
#                             bullet_data['direction'],
#                             bullet_data['speed'],
#                             bullet_data['shoo,t_time'],
#                             bullet_data['shooter'])
        return packed
    def unpack_bullet_data(packed):
        unpaked_data = struct.unpack('=fff',packed)
        return unpaked_data
    #def unpack_enemy_data(packed):
    #    unpacked_data = struct.unpack('iiBfB', packed)
    #    return unpacked_data

    # enemy_data
    '''
    def pack_enemy_data(enemy_data):
        packed = struct.pack('=fffffI',
                             enemy_data.x,
                             enemy_data.y,
                             enemy_data.xdir,
                             enemy_data.ydir,
                             enemy_data.speed,
                             enemy_data.type
                             )
        return packed

    def unpack_enemy_data(packed):
        unpacked_data = struct.unpack('=fffffI', packed)
        return unpacked_data
    '''

    def pack_all_player_data(all_player_data):
        packed_data = struct.pack('=i fff fff fff fff iii BBB fff',
                                  all_player_data['player_count'],

                                  all_player_data['player_x'][0],
                                  all_player_data['player_x'][1],
                                  all_player_data['player_x'][2],

                                  all_player_data['player_y'][0],
                                  all_player_data['player_y'][1],
                                  all_player_data['player_y'][2],

                                  all_player_data['player_sx'][0],
                                  all_player_data['player_sx'][1],
                                  all_player_data['player_sx'][2],

                                  all_player_data['player_sy'][0],
                                  all_player_data['player_sy'][1],
                                  all_player_data['player_sy'][2],

                                  all_player_data['player_life'][0],
                                  all_player_data['player_life'][1],
                                  all_player_data['player_life'][2],

                                  all_player_data['player_isShoot'][0],
                                  all_player_data['player_isShoot'][1],
                                  all_player_data['player_isShoot'][2],

                                  all_player_data['player_dir'][0],
                                  all_player_data['player_dir'][1],
                                  all_player_data['player_dir'][2]
                                  )
        return packed_data

    def unpack_all_player_data(packed_data):
        unpacked_data = struct.unpack('=i fff fff fff fff iii BBB fff', packed_data)
        all_player_data = {
            'player_count': unpacked_data[0],
            'player_x': [unpacked_data[1], unpacked_data[2], unpacked_data[3]],
            'player_y': [unpacked_data[4], unpacked_data[5], unpacked_data[6]],
            'player_sx': [unpacked_data[7], unpacked_data[8], unpacked_data[9]],
            'player_sy': [unpacked_data[10], unpacked_data[11], unpacked_data[12]],
            'player_life': [unpacked_data[13], unpacked_data[14], unpacked_data[15]],
            'player_isShoot': [unpacked_data[16], unpacked_data[17], unpacked_data[18]],
            'player_dir': [unpacked_data[19], unpacked_data[20], unpacked_data[21]]
        }
        return all_player_data

    enemy_data_type = '=fff'
    enemy_data_size = struct.calcsize(enemy_data_type)

    def pack_enemy_data(enemy_data, k):
        packed = struct.pack('=fffi',
                             enemy_data.x,
                             enemy_data.y,
                             enemy_data.type,
                             k
                             )
        return packed

    def unpack_enemy_data(packed):
        unpacked_data = struct.unpack('=fffi', packed)
        return unpacked_data

    #player_data

    player_data_type = '=fffff'
    player_data_size = struct.calcsize(player_data_type)
    def pack_player_data(p_data):
        packed = struct.pack('=ffffiBf',
#           player_data['player_name'].encode('utf-8'),
#           player_data['player_number'],
                             p_data.x,
                             p_data.y,
                             p_data.sx,
                             p_data.sy,
#             player_data['direction'],
                             p_data.life,
                             p_data.isshoot,
                             p_data.playerdir
                             )
#             player_data['is_damaged'],
#             player_data['player_score'])
        return packed
    def unpack_player_data(packed):
        unpacked_data = struct.unpack('=ffffiBf', packed)
        return unpacked_data
    #def unpack_player_data(packed):
    ##    unpacked_data = struct.unpack('30s BiiBB?L', packed)
    #    return unpacked_data

    #is_game_over
    def pack_is_game_over(is_game_over):
        return struct.pack('?', is_game_over)
    def unpack_is_game_over(packed):
        return struct.unpack('?', packed)


