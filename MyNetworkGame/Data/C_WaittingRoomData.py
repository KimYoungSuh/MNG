from Data import C_StructSet

'''
참고하세요
WattingRoomData ={'player_count':0,
                  'player1_witch_selcet':0,
                  'player2_witch_selcet':0,
                  'player3_witch_selcet':0,
                  'ready_state':False
                  }
'''

class WaittingRoomData:
    def __init__(self):
        self.waitting_room_data = C_StructSet.WaittingRoomData