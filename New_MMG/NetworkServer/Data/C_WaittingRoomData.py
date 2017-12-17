from Data.C_StructSet import StructSet

'''
참고하세요
WattingRoomData ={'player_count':0,
                  'player1_witch_selcet':0,
                  'player2_witch_selcet':0,
                  'player3_witch_selcet':0,
                  'player1_ready_state' : 0,
                  'player2_ready_state':0,
                  'player3_ready_state' :0
                  'GAME_STATE' : 0
                  }
'''

class WaittingRoomData:
    def __init__(self):
        self.waitting_room_data = StructSet().WaittingRoomData