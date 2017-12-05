import socket
from Data import C_WaittingRoomData

class GameData:
    player_number=1
    client_socket = socket
    waitting_room_data= C_WaittingRoomData.WaittingRoomData().waitting_room_data
    is_game_over =False


    def a(self):
        return GameData.client_socket