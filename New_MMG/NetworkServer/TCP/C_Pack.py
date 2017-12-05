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
    in_room_data_type = 'B ? ?'
    in_room_data_size = struct.calcsize(in_room_data_type)
    def pack_in_room_data(in_room_data):
        packed_data = struct.pack('B ? ?',
                                  in_room_data['character_select'],
                                  in_room_data['is_ready'],
                                  in_room_data['is_exit'])
        return packed_data

    def unpack_in_room_data(packed_data):
        unpacked_data = struct.unpack('B ? ?', packed_data)
        in_room_data = {
            'character_select': unpacked_data[0],
            'is_ready': unpacked_data[1],
            'is_exit': unpacked_data[2]
        }
        return in_room_data

    # in_room_data_server
    in_room_data_server_type = 'BBBBBBBi'
    in_room_data_server_size = struct.calcsize(in_room_data_server_type)
    def pack_in_room_data_server(in_room_data_server, gamestate):
        packed_data = struct.pack('BBBBBBBi',
                                  in_room_data_server['player_count'],
                                  in_room_data_server['player_witch_select'][0],
                                  in_room_data_server['player_witch_select'][1],
                                  in_room_data_server['player_witch_select'][2],
                                  in_room_data_server['player_ready_state'][0],
                                  in_room_data_server['player_ready_state'][1],
                                  in_room_data_server['player_ready_state'][2],
                                  gamestate)
        return packed_data
    def unpack_in_room_data_server(packed_data):
        unpacked_data = struct.unpack('BBBBBBBi', packed_data)
        in_room_data_server = {
            'player_count': unpacked_data[0],
            'player_witch_select': [unpacked_data[1], unpacked_data[2], unpacked_data[3]],
            'player1_ready_state': [unpacked_data[4], unpacked_data[5], unpacked_data[6]]
        }
        return in_room_data_server

    #room_is_full
    def pack_room_is_full(is_room_full):
        packed_data = struct.pack('?', is_room_full)
        return packed_data

    def pack_bullet_data(bullet_data):
        packed = struct.pack('=fff',
                             bullet_data.shooter,
                             bullet_data.x,
                             bullet_data.y
                             )
        #                             (bullet_data['start_pos'])['pos_x'],
        #                             (bullet_data['start_pos'])['pos_y'],
        #                             bullet_data['direction'],
        #                             bullet_data['speed'],
        #                             bullet_data['shoo,t_time'],
        #                             bullet_data['shooter'])
        return packed

    def unpack_bullet_data(packed):
        unpaked_data = struct.unpack('=fff', packed)
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
    def pack_enemy_data(enemy_data, k ):
        packed = struct.pack('=ffffi',
                             enemy_data.x,
                             enemy_data.y,
                             enemy_data.type,
                             enemy_data.state,
                             k
                             )
        return packed

    def unpack_enemy_data(packed):
        unpacked_data = struct.unpack('=ffffi', packed)
        return unpacked_data

    #player_data
    def pack_player_data(player_data):
        packed = struct.pack('=fffff',
#             player_data['player_name'].encode('utf-8'),
#             player_data['player_number'],
             player_data.x,
             player_data.y,
             player_data.sx,
             player_data.sy,
#             player_data['direction'],
             player_data.life)
#             player_data['is_damaged'],
#             player_data['player_score'])
        return packed
    def unpack_player_data(packed):
        unpacked_data = struct.unpack('=fffff', packed)
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


