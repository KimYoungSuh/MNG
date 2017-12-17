class StructSet:
    def __init__(self):

        self.PointStruct = {'pos_x': 0, 'pos_y': 0}

        self.PlayerDataStruct = {'player_name': 'default_player',
                      'player_number': -1,
                      'player_pos': self.PointStruct,
                      'direction': 0,
                      'life': 0,
                      'is_damaged': True,
                      'player_score': 0
                            }

        self.AllPlayerDataStruct = {'player_count':0,
                               'player_x': [0, 0, 0],
                               'player_y' : [0, 0, 0],
                               'player_sx': [0, 0, 0],
                               'player_sy' : [0, 0, 0],
                               'player_life': [0, 0, 0],
                               'player_isShoot' : [0, 0, 0],
                               'player_number': [-1, -1, -1],
                               'player_dir': [0, 0, 0]
                               }
        self.RoomDataStruct = {'room_number':-1,
                    'host_number':-1,
                    'room_name':'default_name',
                    'full_player':0,
                    'player_name1':'default_name',
                    'player_name2':'default_name',
                    'player_name3':'default_name',
                    'player_name4':'default_name',
                    'is_started':False,
                    'ready_player':0b0000}

        self.EnemyDataStruct = {'E_x':0,
                            'E_y':0,
                     'Ex_dir':0,
                           'Ey_dir': 0,
                           'TEAM' : 0}

        self.BulletDataStruct ={'start_pos':0,
                     'direction':0,
                     'speed':0,
                     'shoot_time':0,
                     'TEAM':0}

        self.WaittingRoomData ={'player_count':0,
                          'player_witch_select': [0, 0, 0],
                          'player_ready_state' : [0, 0, 0],
                           'player_number': [-1, -1, -1],
                           'emotion': [0, 0, 0]
                          }

