import sys
import struct
from Data import *

class Pack:

    def pack_player_data(player_data):
        packed = struct.pack('30s BBBBB?L',
             player_data.player_data['player_name'].encode('utf-8'),
             player_data.player_data['player_number'],
             (player_data.player_data['player_pos'])['pos_x'],
             (player_data.player_data['player_pos'])['pos_y'],
             player_data.player_data['direction'],
             player_data.player_data['life'],
             player_data.player_data['is_damaged'],
             player_data.player_data['player_score'])
        return packed

    def unpack_player_data(packed):
        unpacked_data = struct.unpack('30s BBBBB?L', packed)
        return unpacked_data

    def pack_is_game_over(is_game_over):
        return struct.pack('?', is_game_over)
    def unpack_is_game_over(packed):
        return struct.unpack('?', packed)


