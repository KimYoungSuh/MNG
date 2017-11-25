PointStruct = {'pos_x': 0, 'pos_y': 0}

PlayerDataStruct = {'player_name': 'default_player',
              'player_number': 0,
              'player_pos': PointStruct,
              'direction': 0,
              'life': 0,
              'is_damaged': True,
              'player_score': 0}

RoomDataStruct = {'room_number':0,
            'host_number':0,
            'room_name':'default_name',
            'full_player':0,
            'player_data':PlayerDataStruct,
            'is_started':False,
            'ready_player':0b0000}

EnemyDataStruct = {'enemy_pos':0,
             'direction':0}

BulletDataStruct ={'start_pos':0,
             'direction':0,
             'speed':0,
             'shoot_time':0,
             'shooter':0}

