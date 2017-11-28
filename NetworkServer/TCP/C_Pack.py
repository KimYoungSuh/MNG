import sys
import struct
from Data import *




class Pack:
    # count_data
    def pack_count_data(count_data):
        packed_data = struct.pack('B', count_data)
        return packed_data

    # Room_data
    def pack_room_data(room_data):
        packed_data = struct.pack('BB 30s B 30s 30s 30s 30s ? B',
                           room_data['room_number'],
                           room_data['host_number'],
                           room_data['room_name'],
                           room_data['full_player'],
                           room_data['player_name1'],
                           room_data['player_name2'],
                           room_data['player_name3'],
                           room_data['player_name4'],
                           room_data['is_started'],
                           room_data['ready_player'])
        return packed_data

    def unpack_room_data(packed):
        unpacked_data = struct.unpack('BB 30s B 30s 30s 30s 30s ? B', packed)
        return unpacked_data

    #join_request_data
    def unpack_join_request_data(packed):
        unpacked_data = struct.unpack('B 30s B', packed)
        return unpacked_data

    #room_is_full
    def pack_room_is_full(is_room_full):
        packed_data = struct.pack('?', is_room_full)
        return packed_data


    # Bullet_data
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

    # enemy_data
    def pack_enemy_data(enemy_data):
        packed = struct.pack('fff', enemy_data.x, enemy_data.y, enemy_data.alive)

    def unpack_enemy_data(packed):
        unpacked_data = struct.unpack('=fff', packed)
        return unpacked_data

    #player_data
    def pack_player_data(player_data):
        packed = struct.pack('=fff',
#             player_data['player_name'].encode('utf-8'),
#             player_data['player_number'],
             (player_data.x),
             (player_data.y),
#             player_data['direction'],
             player_data.life)
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


