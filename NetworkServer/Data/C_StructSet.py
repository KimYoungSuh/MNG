
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
            'player_name1':'default_name',
            'player_name2':'default_name',
            'player_name3':'default_name',
            'player_name4':'default_name',
            'is_start':False,
            'ready_player':0b0000}

EnemyDataStruct = {'E_x':0,
                    'E_y':0,
             'Ex_dir':0,
                   'Ey_dir': 0,
                   'TEAM' : 0}

BulletDataStruct ={'start_pos':0,
             'direction':0,
             'speed':0,
             'shoot_time':0,
             'TEAM':0}

WaittingRoomData ={'player_count':0,
                  'player1_witch_selcet':0,
                  'player2_witch_selcet':0,
                  'player3_witch_selcet':0,
                  'ready_state':0b0000
                  }

