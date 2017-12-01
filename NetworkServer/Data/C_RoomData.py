from Data import C_StructSet

class RoomData:
    def __init__(self):
        self.room_data = C_StructSet.RoomDataStruct

    def is_room_exist(self):
        if self.room_data['full_player'] == 0: return False
        else: return True

