import socket
from Data import C_StructSet

class GameData:
    player_number=1
    client_socket = socket
    waitting_room_data= C_StructSet.WaittingRoomData
    ready_state = 0b0000
    is_start = False


    def a(self):

        return