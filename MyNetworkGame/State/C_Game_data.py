import socket
from Data import C_StructSet

class GameData:
    player_number=1
    client_socket = socket
    waitting_room_data= C_StructSet.WaittingRoomData


    def a(self):
        return GameData.client_socket