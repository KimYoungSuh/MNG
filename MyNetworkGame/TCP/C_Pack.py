import sys
import struct

Point = {'pos_x': 0, 'pos_y': 0}
PlayerData = {'player_name': 'default_player',
              'player_number': 0,
              'player_pos': Point,
              'direction': 0,
              'life': 0,
              'is_damaged': True,
              'player_score': 0}

EnemyData = {'enemy_pos': 0,
             'direction': 0}

BulletData = {'start_pos': 0,
              'direction': 0,
              'speed': 0,
              'shoot_time': 0,
              'shooter': 0}

RoomData = {'room_number': 0,
            'host_number': 0,
            'room_name': 'default_name',
            'full_player': 0,
            'player_data': PlayerData,
            'is_started': False,
            'ready_player': 0b0000}


class DataStruct:
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


