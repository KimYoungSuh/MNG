import sys
import struct
from Data import *

class Pack:
    # Room_data
    def pack_room_data(room_data):
        pack = struct.pack('BB 30s B 30s 30s 30s 30s ? B',
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
        packed = struct.pack('iiB',
                             (enemy_data['enemy_pos'])['pox_x'],
                             (enemy_data['enemy_pos'])['pox_y'],
                             enemy_data['direction'])
    def unpack_enemy_data(packed):
        unpacked_data = struct.unpack('iiB', packed)
        return unpacked_data

    #player_data
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

    #is_game_over
    def pack_is_game_over(is_game_over):
        return struct.pack('?', is_game_over)
    def unpack_is_game_over(packed):
        return struct.unpack('?', packed)


